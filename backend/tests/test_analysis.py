from fastapi.testclient import TestClient


def test_list_documents(client: TestClient) -> None:
    resp = client.get("/api/v1/analysis/documents")
    assert resp.status_code == 200
    body = resp.json()
    assert "fund" in body and "benchmark" in body
    assert isinstance(body["ai_configured"], bool)
    # The bundled SPF/DPF corpus should classify into both buckets.
    assert len(body["fund"]) >= 1
    assert len(body["benchmark"]) >= 1
    # Every document reports its source (builtin vs upload).
    assert all(d["source"] in ("builtin", "upload") for d in body["fund"] + body["benchmark"])


def test_compare_shape(client: TestClient) -> None:
    resp = client.post("/api/v1/analysis/compare", json={})
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] in ("live", "demo")
    report = body["report"]
    assert report["fund_name"]
    assert len(report["entitlements"]) >= 1
    first = report["entitlements"][0]
    assert first["area"]
    assert first["deviation_severity"] in ("High", "Medium", "Low", "None")
    # New split-source schema: fund side and standard side are separate lists.
    assert isinstance(first["current_points"], list)
    assert isinstance(first["standard_points"], list)
    assert isinstance(first["current_sources"], list)
    assert isinstance(first["standard_sources"], list)
    assert isinstance(first["evidence_verified"], bool)
    # No LaTeX / math markers should leak into member-facing text.
    assert "\\sum" not in first["impact_explanation"]
    assert "$" not in first["impact_explanation"]
