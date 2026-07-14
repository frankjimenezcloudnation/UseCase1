"""Tests for the RAG chunking + corpus keying (no embedding model needed — fast)."""

from pathlib import Path

from app.services.documents import Document
from app.services.rag import chunking, index


def _doc(role: str = "fund") -> Document:
    return Document(id="d1", filename="Test.pdf", role=role, doc_type="Transitieplan",
                    source="builtin", path=Path("Test.pdf"))


def test_chunk_document_is_page_aware() -> None:
    text = "\n--- page 3 ---\nEerste alinea over premie.\n--- page 4 ---\nTweede alinea over toeslag."
    chunks = chunking.chunk_document(_doc(), text)
    assert len(chunks) == 2
    assert {c.page for c in chunks} == {3, 4}
    assert all(c.role == "fund" and c.kind == "document" for c in chunks)
    assert "premie" in chunks[0].text.lower()


def test_chunk_document_windows_long_pages() -> None:
    long_text = "\n--- page 1 ---\n" + ("woord " * 400)  # ~2400 chars on one page
    chunks = chunking.chunk_document(_doc(), long_text)
    assert len(chunks) >= 2  # split into overlapping windows
    assert all(c.page == 1 for c in chunks)


def test_chunk_ontology_one_per_concept() -> None:
    class C:
        def __init__(self, name, definition, clar, ext):
            self.name, self.definition, self.clarification, self.external_id = name, definition, clar, ext

    concepts = [C("Risicodelingsreserve", "Een reserve.", "Toelichting.", "25_01"),
                C("Toeslag", "Een verhoging.", "", "25_02")]
    chunks = chunking.chunk_ontology(concepts, "OntologySnapshot.xlsx")
    assert len(chunks) == 2
    assert chunks[0].kind == "ontology" and chunks[0].role == "benchmark"
    assert chunks[0].external_id == "25_01"
    assert "Risicodelingsreserve" in chunks[0].text


def test_corpus_id_is_deterministic_and_content_sensitive() -> None:
    d, txt = _doc(), "wat tekst over de regeling"
    id1 = index.corpus_id([(d, txt)], [])
    id2 = index.corpus_id([(d, txt)], [])
    id3 = index.corpus_id([(d, txt + " extra")], [])
    assert id1 == id2  # same content -> same collection
    assert id1 != id3  # changed content -> new collection (rebuild)
