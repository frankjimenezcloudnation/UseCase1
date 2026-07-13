"""Registry of the fund + benchmark source documents.

Scans the configured documents directory and classifies each file by filename into:
  - role: "fund"       -> the specific fund's legal/actuarial corpus (FPR, ABTN, ...)
  - role: "benchmark"  -> the standard product / ontology it is compared against
Each document gets a stable id (the file stem) the frontend selects by.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from app.core.config import settings

_SUPPORTED = {".pdf", ".docx", ".xlsx", ".xls"}


@dataclass
class Document:
    id: str
    filename: str
    role: str  # "fund" | "benchmark"
    doc_type: str  # short human label, e.g. "ABTN", "Operating Manual"
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


def scan_documents() -> list[Document]:
    base = settings.documents_path
    docs: list[Document] = []
    if not base.exists():
        return docs
    for path in sorted(base.iterdir()):
        if not path.is_file() or path.suffix.lower() not in _SUPPORTED:
            continue
        classified = _classify(path.name)
        if classified is None:
            continue
        role, doc_type = classified
        docs.append(
            Document(
                id=_make_id(path.name),
                filename=path.name,
                role=role,
                doc_type=doc_type,
                path=path,
            )
        )
    return docs


def documents_by_id() -> dict[str, Document]:
    return {d.id: d for d in scan_documents()}
