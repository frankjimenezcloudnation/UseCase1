"""Vector index over the whole corpus, backed by Qdrant (embedded local mode).

Scalability: Qdrant is a production vector database. We run it here in embedded/on-disk mode
(no server needed), and switching to a hosted/Docker Qdrant for production scale is a one-line
change to the client constructor — the rest of this module is unchanged.

Reproducibility: embeddings are deterministic (local e5), each corpus is a collection keyed by a
content hash, and retrieval is deterministic for a fixed index. A collection is built once and
reused; it is only rebuilt when the documents (or the embedding model / RAG version) change.
"""

from __future__ import annotations

import hashlib
import threading

from app.core.config import settings
from app.services.rag import chunking, embeddings

# Bump to invalidate all existing collections when chunking/retrieval logic changes.
RAG_VERSION = "1"

_client = None
_lock = threading.Lock()


def _get_client():
    global _client
    if _client is None:
        with _lock:
            if _client is None:
                from qdrant_client import QdrantClient

                settings.qdrant_path.mkdir(parents=True, exist_ok=True)
                _client = QdrantClient(path=str(settings.qdrant_path))
    return _client


def corpus_id(docs_with_text: list[tuple], ont_concepts: list) -> str:
    h = hashlib.sha256()
    h.update(f"{RAG_VERSION}|{embeddings.model_id()}|{settings.CHUNK_SIZE}|{settings.CHUNK_OVERLAP}".encode())
    for doc, text in sorted(docs_with_text, key=lambda t: t[0].filename):
        h.update(doc.filename.encode("utf-8"))
        h.update(b"\0")
        h.update(text.encode("utf-8", errors="ignore"))
        h.update(b"\0")
    h.update(f"ontology:{len(ont_concepts)}".encode())
    for c in ont_concepts[:50]:  # sample is enough to detect a changed snapshot
        h.update((c.external_id + c.name).encode("utf-8", errors="ignore"))
    return h.hexdigest()[:16]


def ensure_corpus(docs_with_text: list[tuple], ont_concepts: list, ont_filename: str) -> str:
    """Build the collection if it does not yet exist; return its name."""
    from qdrant_client.models import Distance, PointStruct, VectorParams

    client = _get_client()
    name = f"corpus_{corpus_id(docs_with_text, ont_concepts)}"
    if client.collection_exists(name):
        return name

    # Chunk everything.
    chunks: list[chunking.Chunk] = []
    for doc, text in docs_with_text:
        chunks.extend(chunking.chunk_document(doc, text))
    if ont_concepts:
        chunks.extend(chunking.chunk_ontology(ont_concepts, ont_filename))
    if not chunks:
        # Empty corpus — create an empty collection so callers don't crash.
        client.create_collection(name, vectors_config=VectorParams(size=embeddings.dim(), distance=Distance.COSINE))
        return name

    vectors = embeddings.embed_passages([c.text for c in chunks])
    client.create_collection(
        name, vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE)
    )
    points = [
        PointStruct(
            id=i,
            vector=vectors[i].tolist(),
            payload={
                "text": c.text, "filename": c.filename, "role": c.role, "kind": c.kind,
                "doc_type": c.doc_type, "page": c.page, "name": c.name,
                "external_id": c.external_id, "definition": c.definition,
                "clarification": c.clarification,
            },
        )
        for i, c in enumerate(chunks)
    ]
    # Upsert in batches to keep memory bounded.
    for start in range(0, len(points), 256):
        client.upsert(name, points[start : start + 256])
    return name


def retrieve(collection: str, query: str, k: int, role: str | None = None,
             kind: str | None = None, query_vector=None) -> list[dict]:
    """Hybrid retrieval: vector nearest-neighbours, re-ranked with a keyword-overlap boost so
    exact term matches (percentages, named concepts) are not missed. Deterministic.

    `query_vector` may be a pre-computed embedding (so callers can embed many queries in one
    batched call); otherwise the query text is embedded here."""
    from qdrant_client.models import FieldCondition, Filter, MatchValue

    client = _get_client()
    conditions = []
    if role:
        conditions.append(FieldCondition(key="role", match=MatchValue(value=role)))
    if kind:
        conditions.append(FieldCondition(key="kind", match=MatchValue(value=kind)))
    qfilter = Filter(must=conditions) if conditions else None

    qvec = embeddings.embed_query(query) if query_vector is None else query_vector
    hits = client.query_points(
        collection, query=qvec.tolist(), limit=max(k * 4, k), query_filter=qfilter, with_payload=True
    ).points
    if not hits:
        return []

    terms = {t for t in _tokens(query) if len(t) >= 4}

    def rescore(hit) -> float:
        text_tokens = set(_tokens(hit.payload.get("text", "")))
        kw = len(terms & text_tokens) / len(terms) if terms else 0.0
        return float(hit.score) + 0.15 * kw

    ranked = sorted(hits, key=lambda h: (-rescore(h), h.id))
    return [h.payload for h in ranked[:k]]


def _tokens(text: str) -> list[str]:
    import re

    return re.sub(r"[^0-9a-zà-ÿ%]+", " ", text.lower()).split()
