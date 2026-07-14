"""Sentence embeddings with a swappable backend and a persistent on-disk cache.

Backends (settings.EMBED_BACKEND):
  • "azure" (default) — Azure OpenAI `text-embedding-3-large` via the Azure AI Foundry gateway
    (same endpoint/key as the foundry-eu MCP). High quality, EU-hosted. No query/passage prefixes.
  • "local" — sentence-transformers `multilingual-e5-base`, offline. Uses "query:"/"passage:"
    prefixes as that model expects.

Both return L2-normalised float32 vectors (cosine == dot, matching Qdrant COSINE). Reproducible.

Embedding cache: every vector is cached on disk keyed by (model, role, text-hash). The expensive
one-time cost is embedding the ~2885 ontology concepts; with the cache they are embedded ONCE ever
and reused on every later index rebuild (e.g. when only the fund documents change), so rebuilds
drop from minutes to seconds. `model_id()` is part of the key, so switching backend/model is safe.
"""

from __future__ import annotations

import hashlib
import pickle
import re
import threading

import numpy as np

from app.core.config import settings

_lock = threading.Lock()
_local_model = None
_azure_client = None
_dim: int | None = None

# Persistent embedding cache (loaded once per process).
_cache: dict[str, np.ndarray] | None = None
_AZURE_BATCH = 128
_AZURE_WORKERS = 12


# --- backend identity -------------------------------------------------------

def model_id() -> str:
    if settings.EMBED_BACKEND == "azure":
        return f"azure:{settings.AZURE_EMBED_DEPLOYMENT}"
    return f"local:{settings.EMBED_MODEL}"


# --- embedding cache --------------------------------------------------------

def _cache_path():
    slug = re.sub(r"[^0-9A-Za-z]+", "_", model_id())
    return settings.uploads_path / f"_embed_cache_{slug}.pkl"


def _load_cache() -> dict[str, np.ndarray]:
    global _cache
    if _cache is None:
        with _lock:
            if _cache is None:
                p = _cache_path()
                try:
                    _cache = pickle.loads(p.read_bytes()) if p.exists() else {}
                except (OSError, pickle.PickleError, EOFError):
                    _cache = {}
    return _cache


def _persist_cache() -> None:
    p = _cache_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(_cache, protocol=pickle.HIGHEST_PROTOCOL))
    tmp.replace(p)  # atomic


def _key(text: str, role: str) -> str:
    h = hashlib.sha256()
    h.update(model_id().encode())
    h.update(b"\0")
    h.update(role.encode())
    h.update(b"\0")
    h.update(text.encode("utf-8", errors="ignore"))
    return h.hexdigest()


# --- local (sentence-transformers) ------------------------------------------

def _get_local():
    global _local_model
    if _local_model is None:
        with _lock:
            if _local_model is None:
                from sentence_transformers import SentenceTransformer

                m = SentenceTransformer(settings.EMBED_MODEL)
                m.eval()
                _local_model = m
    return _local_model


# --- azure (Azure OpenAI via Foundry gateway) -------------------------------

def _foundry_endpoint() -> str:
    ep = (settings.FOUNDRY_ENDPOINT or "").rstrip("/")
    if not ep:
        raise RuntimeError(
            "EMBED_BACKEND=azure but FOUNDRY_ENDPOINT is not set (add it to backend/.env)."
        )
    return ep if ep.endswith("/models") else ep + "/models"


def _get_azure():
    global _azure_client
    if _azure_client is None:
        with _lock:
            if _azure_client is None:
                from azure.ai.inference import EmbeddingsClient
                from azure.core.credentials import AzureKeyCredential

                if not settings.FOUNDRY_API_KEY:
                    raise RuntimeError(
                        "EMBED_BACKEND=azure but FOUNDRY_API_KEY is not set (add it to backend/.env)."
                    )
                _azure_client = EmbeddingsClient(
                    endpoint=_foundry_endpoint(),
                    credential=AzureKeyCredential(settings.FOUNDRY_API_KEY),
                )
    return _azure_client


def _azure_embed_batch(batch: list[str]) -> list[list[float]]:
    resp = _get_azure().embed(model=settings.AZURE_EMBED_DEPLOYMENT, input=batch)
    return [item.embedding for item in sorted(resp.data, key=lambda d: d.index)]


# --- raw backend embedding (uncached) ---------------------------------------

def _backend_embed(texts: list[str], role: str) -> np.ndarray:
    """Embed texts with the active backend and L2-normalise. `role` only affects the local e5
    model (query:/passage: prefix); Azure ignores it."""
    if settings.EMBED_BACKEND == "azure":
        batches = [texts[i : i + _AZURE_BATCH] for i in range(0, len(texts), _AZURE_BATCH)]
        if len(batches) <= 1:
            out = _azure_embed_batch(batches[0]) if batches else []
        else:
            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=_AZURE_WORKERS) as ex:
                out = [v for part in ex.map(_azure_embed_batch, batches) for v in part]
        arr = np.asarray(out, dtype=np.float32)
    else:
        prefix = "query: " if role == "query" else "passage: "
        arr = _get_local().encode(
            [f"{prefix}{t}" for t in texts],
            normalize_embeddings=True, batch_size=64, convert_to_numpy=True,
            show_progress_bar=False,
        ).astype(np.float32)
        return arr  # already normalised by sentence-transformers
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return arr / norms


# --- cached embedding -------------------------------------------------------

def _embed_cached(texts: list[str], role: str) -> np.ndarray:
    if not texts:
        return np.zeros((0, dim()), dtype=np.float32)
    cache = _load_cache()
    keys = [_key(t, role) for t in texts]
    missing = [i for i, k in enumerate(keys) if k not in cache]
    if missing:
        fresh = _backend_embed([texts[i] for i in missing], role)
        for j, i in enumerate(missing):
            cache[keys[i]] = fresh[j]
        _persist_cache()
    return np.stack([cache[k] for k in keys])


# --- public API -------------------------------------------------------------

def warm_up() -> None:
    dim()


def dim() -> int:
    global _dim
    if _dim is None:
        _dim = int(_backend_embed(["dimensieprobe"], "query").shape[1])
    return _dim


def embed_passages(texts: list[str]) -> np.ndarray:
    return _embed_cached(texts, role="passage")


def embed_query(text: str) -> np.ndarray:
    return _embed_cached([text], role="query")[0]


def embed_queries(texts: list[str]) -> np.ndarray:
    """Embed several queries in one cached, batched call (used to embed all theme queries at once)."""
    return _embed_cached(texts, role="query")
