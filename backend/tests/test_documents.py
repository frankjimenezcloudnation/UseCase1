"""Tests for document management: upload, re-classify (role), delete."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.fixture(autouse=True)
def _isolated_uploads(tmp_path, monkeypatch):
    """Point the uploads dir at a temp folder so tests never touch the real repo."""
    monkeypatch.setattr(settings, "UPLOADS_DIR", str(tmp_path / "uploads"))
    yield


def _upload(client: TestClient, name: str, role: str | None = None):
    data = {"role": role} if role else {}
    return client.post(
        "/api/v1/analysis/documents",
        files={"file": (name, b"%PDF-1.4 dummy content", "application/pdf")},
        data=data,
    )


def test_upload_reclassify_and_delete(client: TestClient) -> None:
    # Upload as a fund document.
    resp = _upload(client, "MijnFonds Transitieplan.pdf", role="fund")
    assert resp.status_code == 200
    body = resp.json()
    uploaded = [d for d in body["fund"] if d["source"] == "upload"]
    assert len(uploaded) == 1
    doc_id = uploaded[0]["id"]

    # Re-classify it to benchmark with a custom label.
    resp = client.patch(
        f"/api/v1/analysis/documents/{doc_id}",
        json={"role": "benchmark", "doc_type": "Eigen standaard"},
    )
    assert resp.status_code == 200
    body = resp.json()
    moved = [d for d in body["benchmark"] if d["id"] == doc_id]
    assert len(moved) == 1 and moved[0]["doc_type"] == "Eigen standaard"
    assert all(d["id"] != doc_id for d in body["fund"])

    # Delete it — an uploaded file is removed entirely.
    resp = client.delete(f"/api/v1/analysis/documents/{doc_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert all(d["id"] != doc_id for d in body["fund"] + body["benchmark"])


def test_reject_unsupported_filetype(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/analysis/documents",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert resp.status_code == 400


def test_delete_missing_document_404(client: TestClient) -> None:
    resp = client.delete("/api/v1/analysis/documents/does-not-exist")
    assert resp.status_code == 404
