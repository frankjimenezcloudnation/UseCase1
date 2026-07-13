from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.schemas.comparison import AnalysisRequest, AnalysisResponse
from app.services.claude_analysis import analyse
from app.services.documents import scan_documents

router = APIRouter()


class DocumentInfo(BaseModel):
    id: str
    filename: str
    role: str
    doc_type: str


class DocumentsResponse(BaseModel):
    ai_configured: bool
    model: str
    fund: list[DocumentInfo]
    benchmark: list[DocumentInfo]


@router.get("/documents", response_model=DocumentsResponse)
def list_documents() -> DocumentsResponse:
    """List the fund corpus and benchmark references the prototype can analyse."""
    docs = scan_documents()
    fund = [DocumentInfo(id=d.id, filename=d.filename, role=d.role, doc_type=d.doc_type)
            for d in docs if d.role == "fund"]
    benchmark = [DocumentInfo(id=d.id, filename=d.filename, role=d.role, doc_type=d.doc_type)
                 for d in docs if d.role == "benchmark"]
    return DocumentsResponse(
        ai_configured=settings.has_ai_credentials,
        model=settings.CLAUDE_MODEL,
        fund=fund,
        benchmark=benchmark,
    )


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
