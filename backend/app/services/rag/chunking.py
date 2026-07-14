"""Split the corpus into retrieval chunks with citation metadata.

Documents are split page-aware (the extractor tags text with '--- page N ---'), so every chunk
carries the page it came from and the model can cite it. Ontology concepts are one chunk each
(name + definition + clarification), which is their natural unit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.core.config import settings
from app.services.documents import Document

_PAGE_RE = re.compile(r"---\s*page\s+(\d+)\s*---")


@dataclass
class Chunk:
    text: str
    filename: str
    role: str            # "fund" | "benchmark"
    kind: str            # "document" | "ontology"
    doc_type: str = ""
    page: int = 0
    name: str = ""       # ontology concept name
    external_id: str = ""
    definition: str = ""
    clarification: str = ""
    payload: dict = field(default_factory=dict)


def _window(text: str, size: int, overlap: int) -> list[str]:
    text = text.strip()
    if len(text) <= size:
        return [text] if text else []
    out: list[str] = []
    step = max(1, size - overlap)
    for i in range(0, len(text), step):
        piece = text[i : i + size].strip()
        if piece:
            out.append(piece)
        if i + size >= len(text):
            break
    return out


def chunk_document(doc: Document, text: str) -> list[Chunk]:
    size, overlap = settings.CHUNK_SIZE, settings.CHUNK_OVERLAP
    segments: list[tuple[int, str]] = []
    matches = list(_PAGE_RE.finditer(text))
    if matches:
        for i, m in enumerate(matches):
            page = int(m.group(1))
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            seg = text[start:end].strip()
            if seg:
                segments.append((page, seg))
    else:
        segments.append((0, text))

    chunks: list[Chunk] = []
    for page, seg in segments:
        for piece in _window(seg, size, overlap):
            chunks.append(
                Chunk(text=piece, filename=doc.filename, role=doc.role, kind="document",
                      doc_type=doc.doc_type, page=page)
            )
    return chunks


def chunk_ontology(concepts: list, filename: str) -> list[Chunk]:
    """One chunk per ontology concept. The searchable text combines all fields; the individual
    fields are kept so they can be shown verbatim as proof."""
    chunks: list[Chunk] = []
    for c in concepts:
        body = c.name.replace("_", " ")
        if c.definition:
            body += f": {c.definition}"
        if c.clarification:
            body += f" — toelichting: {c.clarification}"
        chunks.append(
            Chunk(text=body, filename=filename, role="benchmark", kind="ontology",
                  doc_type="Ontology", page=1, name=c.name.replace("_", " "),
                  external_id=c.external_id, definition=c.definition, clarification=c.clarification)
        )
    return chunks
