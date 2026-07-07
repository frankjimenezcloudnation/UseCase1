from fastapi.testclient import TestClient


def test_item_crud(client: TestClient) -> None:
    # Create
    resp = client.post("/api/v1/items", json={"name": "Widget", "description": "A thing"})
    assert resp.status_code == 201
    created = resp.json()
    item_id = created["id"]
    assert created["name"] == "Widget"

    # Read
    resp = client.get(f"/api/v1/items/{item_id}")
    assert resp.status_code == 200

    # Update
    resp = client.put(f"/api/v1/items/{item_id}", json={"name": "Gadget"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Gadget"

    # List
    resp = client.get("/api/v1/items")
    assert resp.status_code == 200
    assert any(i["id"] == item_id for i in resp.json())

    # Delete
    resp = client.delete(f"/api/v1/items/{item_id}")
    assert resp.status_code == 204

    # Confirm gone
    resp = client.get(f"/api/v1/items/{item_id}")
    assert resp.status_code == 404
