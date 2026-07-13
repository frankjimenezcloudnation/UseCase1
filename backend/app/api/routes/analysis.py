from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import settings
from app.schemas.comparison import AnalysisRequest, AnalysisResponse, DocumentPatch
from app.services.claude_analysis import analyse
from app.services.documents import (
    clear_override,
    find_document,
    scan_documents,
    set_override,
)

router = APIRouter()

_SUPPORTED = {".pdf", ".docx", ".xlsx", ".xls"}


class DocumentInfo(BaseModel):
    id: str
    filename: str
    role: str
    doc_type: str
    source: str  # "builtin" | "upload"


class DocumentsResponse(BaseModel):
    ai_configured: bool
    model: str
    fund: list[DocumentInfo]
    benchmark: list[DocumentInfo]


def _to_info(d) -> DocumentInfo:
    return DocumentInfo(id=d.id, filename=d.filename, role=d.role, doc_type=d.doc_type, source=d.source)


def _documents_response() -> DocumentsResponse:
    docs = scan_documents()
    return DocumentsResponse(
        ai_configured=settings.has_ai_credentials,
        model=settings.CLAUDE_MODEL,
        fund=[_to_info(d) for d in docs if d.role == "fund"],
        benchmark=[_to_info(d) for d in docs if d.role == "benchmark"],
    )


@router.get("/documents", response_model=DocumentsResponse)
def list_documents() -> DocumentsResponse:
    """List the fund corpus and benchmark references the prototype can analyse."""
    return _documents_response()


@router.post("/documents", response_model=DocumentsResponse)
async def upload_document(
    file: UploadFile = File(...),
    role: str | None = Form(default=None),
    doc_type: str | None = Form(default=None),
) -> DocumentsResponse:
    """Upload a new fund/benchmark document. Stored on disk in the uploads directory."""
    name = Path(file.filename or "").name
    if not name:
        raise HTTPException(status_code=400, detail="Geen bestandsnaam ontvangen.")
    if Path(name).suffix.lower() not in _SUPPORTED:
        raise HTTPException(
            status_code=400,
            detail="Niet-ondersteund bestandstype. Toegestaan: PDF, DOCX, XLSX.",
        )
    if role is not None and role not in ("fund", "benchmark"):
        raise HTTPException(status_code=400, detail="role moet 'fund' of 'benchmark' zijn.")

    settings.uploads_path.mkdir(parents=True, exist_ok=True)
    target = settings.uploads_path / name
    # Avoid clobbering an existing upload with the same name.
    counter = 1
    while target.exists():
        target = settings.uploads_path / f"{Path(name).stem} ({counter}){Path(name).suffix}"
        counter += 1

    content = await file.read()
    target.write_bytes(content)

    # Apply optional role/type override, keyed on the freshly written filename's id.
    if role or doc_type:
        from app.services.documents import _make_id  # local import: internal id helper

        set_override(_make_id(target.name), role=role, doc_type=doc_type)

    return _documents_response()


@router.patch("/documents/{doc_id}", response_model=DocumentsResponse)
def patch_document(doc_id: str, patch: DocumentPatch) -> DocumentsResponse:
    """Change a document's role (fund/benchmark) and/or its human label."""
    if find_document(doc_id) is None:
        raise HTTPException(status_code=404, detail="Document niet gevonden.")
    if patch.role is None and patch.doc_type is None:
        raise HTTPException(status_code=400, detail="Niets om te wijzigen.")
    set_override(doc_id, role=patch.role, doc_type=patch.doc_type)
    return _documents_response()


@router.delete("/documents/{doc_id}", response_model=DocumentsResponse)
def delete_document(doc_id: str) -> DocumentsResponse:
    """Remove a document. Uploaded files are deleted from disk; built-in reference
    documents are hidden (never physically deleted) so the shipped corpus stays intact."""
    doc = find_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document niet gevonden.")
    if doc.source == "upload":
        try:
            doc.path.unlink(missing_ok=True)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Verwijderen mislukt: {e}")
        clear_override(doc_id)
    else:
        # Built-in: hide via override rather than delete the shipped source file.
        set_override(doc_id, hidden=True)
    return _documents_response()


@router.post("/compare", response_model=AnalysisResponse)
def compare(req: AnalysisRequest) -> AnalysisResponse:
    """Run Use Case 1: compare the selected fund documents against the standard product."""
    docs = scan_documents()
    if not docs:
        raise HTTPException(
            status_code=404,
            detail=f"No source documents found in {settings.DOCUMENTS_DIR}",
        )
    by_id = {d.id: d for d in docs}

    def resolve(ids: list[str], role: str):
        if ids:
            selected = [by_id[i] for i in ids if i in by_id and by_id[i].role == role]
            if selected:
                return selected
        # Default: all documents of this role.
        return [d for d in docs if d.role == role]

    fund_docs = resolve(req.fund_document_ids, "fund")
    benchmark_docs = resolve(req.benchmark_document_ids, "benchmark")

    if not fund_docs:
        raise HTTPException(status_code=400, detail="No fund documents available to analyse.")

    return analyse(fund_docs, benchmark_docs)
