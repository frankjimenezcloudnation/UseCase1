"""Registry of the fund + benchmark source documents.

Scans two locations and classifies each file by filename into:
  - role: "fund"       -> the specific fund's legal/actuarial corpus (FPR, ABTN, ...)
  - role: "benchmark"  -> the standard product / ontology it is compared against

Sources:
  - "builtin"  -> shipped reference documents in DOCUMENTS_DIR (never deleted from disk)
  - "upload"   -> user-uploaded documents in UPLOADS_DIR (deletable)

A small JSON override store (UPLOADS_DIR/_overrides.json) lets the user re-classify a
document (role / doc_type) or hide a built-in one — without touching the original file.
Each document gets a stable id (slug + filename hash) the frontend selects by.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from app.core.config import settings

_SUPPORTED = {".pdf", ".docx", ".xlsx", ".xls"}
_OVERRIDES_FILE = "_overrides.json"


@dataclass
class Document:
    id: str
    filename: str
    role: str  # "fund" | "benchmark"
    doc_type: str  # short human label, e.g. "ABTN", "Operating Manual"
    source: str  # "builtin" | "upload"
    path: Path = field(repr=False)


def _classify(name: str) -> tuple[str, str] | None:
    """Return (role, doc_type) for a filename, or None to skip."""
    low = name.lower()

    # --- Benchmark / standard references ---
    if "specificatie" in low and "premieovereenkomst" in low:
        return "benchmark", "IG&H AllVida — standaard specificatie"
    if "analyseqwik" in low or "qwik" in low:
        return "benchmark", "Feniqs Qwik — analyse & inrichting"
    if "ontology" in low:
        return "benchmark", "Ontology Snapshot (single source of truth)"
    if "overzicht_pdc" in low or "pdc" in low:
        return "benchmark", "PDC-overzicht (productdefinities)"

    # --- Fund corpus ---
    if "abtn" in low:
        return "fund", "ABTN (actuariële bedrijfstechnische nota)"
    if "operating manual" in low or "fpr operating" in low:
        return "fund", "FPR Operating Manual"
    if "premieregeling" in low or "pensioenreglement" in low or "fpr" in low:
        return "fund", "Fonds Pensioenreglement (FPR)"
    if "transitieplan" in low:
        return "fund", "Transitieplan"
    if "implementatieplan" in low:
        return "fund", "Implementatieplan WTP"
    if "compensatieplan" in low:
        return "fund", "Compensatieplan"
    return None


def _make_id(filename: str) -> str:
    stem = Path(filename).stem
    slug = "".join(c if c.isalnum() else "-" for c in stem.lower()).strip("-")
    slug = "-".join(filter(None, slug.split("-")))[:48]
    digest = hashlib.sha1(filename.encode()).hexdigest()[:6]
    return f"{slug}-{digest}"


# --- Override store -------------------------------------------------------

def _overrides_path() -> Path:
    return settings.uploads_path / _OVERRIDES_FILE


def load_overrides() -> dict[str, dict]:
    p = _overrides_path()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_overrides(overrides: dict[str, dict]) -> None:
    settings.uploads_path.mkdir(parents=True, exist_ok=True)
    _overrides_path().write_text(json.dumps(overrides, ensure_ascii=False, indent=2), encoding="utf-8")


def set_override(doc_id: str, **fields) -> None:
    overrides = load_overrides()
    entry = overrides.get(doc_id, {})
    entry.update({k: v for k, v in fields.items() if v is not None})
    overrides[doc_id] = entry
    save_overrides(overrides)


def clear_override(doc_id: str) -> None:
    overrides = load_overrides()
    if doc_id in overrides:
        del overrides[doc_id]
        save_overrides(overrides)


# --- Scanning -------------------------------------------------------------

def _scan_dir(base: Path, source: str, classify_unknown: bool) -> list[Document]:
    """Scan one directory. When classify_unknown is True, files the classifier does
    not recognise are still included (default role/type) so uploads always appear."""
    docs: list[Document] = []
    if not base.exists():
        return docs
    for path in sorted(base.iterdir()):
        if not path.is_file() or path.suffix.lower() not in _SUPPORTED:
            continue
        classified = _classify(path.name)
        if classified is None:
            if not classify_unknown:
                continue
            role, doc_type = "fund", "Nieuw document (nog te classificeren)"
        else:
            role, doc_type = classified
        docs.append(
            Document(
                id=_make_id(path.name),
                filename=path.name,
                role=role,
                doc_type=doc_type,
                source=source,
                path=path,
            )
        )
    return docs


def scan_documents() -> list[Document]:
    """All visible documents (built-in + uploads) with overrides applied."""
    overrides = load_overrides()
    builtin = _scan_dir(settings.documents_path, "builtin", classify_unknown=False)
    uploaded = _scan_dir(settings.uploads_path, "upload", classify_unknown=True)

    docs: list[Document] = []
    for d in builtin + uploaded:
        ov = overrides.get(d.id, {})
        if ov.get("hidden"):
            continue
        if ov.get("role") in ("fund", "benchmark"):
            d.role = ov["role"]
        if ov.get("doc_type"):
            d.doc_type = ov["doc_type"]
        docs.append(d)
    return docs


def documents_by_id() -> dict[str, Document]:
    return {d.id: d for d in scan_documents()}


def find_document(doc_id: str) -> Document | None:
    return documents_by_id().get(doc_id)
