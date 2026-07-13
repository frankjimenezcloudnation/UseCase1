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


def test_compare_demo_mode(client: TestClient) -> None:
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
    assert isinstance(first["sources"], list)
