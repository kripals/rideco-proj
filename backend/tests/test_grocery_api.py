from datetime import date, timedelta

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Grocery API is running"}


def test_list_items_seeded(client: TestClient) -> None:
    response = client.get("/api/v1/items")

    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert {"id", "name", "item_type_id"}.issubset(items[0].keys())


def test_create_and_fetch_grocery(client: TestClient) -> None:
    items_response = client.get("/api/v1/items")
    item_ids = [item["id"] for item in items_response.json()[:2]]

    payload = {
        "family_id": 1,
        "grocery_date": date.today().isoformat(),
        "grocery_items": [
            {"item_id": item_ids[0], "quantity": 2, "purchased": False},
            {"item_id": item_ids[1], "quantity": 1, "purchased": True},
        ],
    }

    create_response = client.post("/api/v1/groceries", json=payload)
    assert create_response.status_code == 200
    created = create_response.json()

    assert created["family_id"] == payload["family_id"]
    assert created["grocery_date"] == payload["grocery_date"]
    assert len(created["grocery_items"]) == 2

    grocery_id = created["id"]
    fetch_response = client.get(f"/api/v1/groceries/{grocery_id}")
    assert fetch_response.status_code == 200
    fetched = fetch_response.json()
    assert fetched["id"] == grocery_id
    assert fetched["grocery_items"][0]["item"]["id"] == payload["grocery_items"][0]["item_id"]


def test_update_grocery_metadata(client: TestClient) -> None:
    item_id = client.get("/api/v1/items").json()[0]["id"]
    create_payload = {
        "family_id": 1,
        "grocery_date": date.today().isoformat(),
        "grocery_items": [{"item_id": item_id, "quantity": 1, "purchased": False}],
    }
    grocery = client.post("/api/v1/groceries", json=create_payload).json()

    new_date = (date.today() + timedelta(days=1)).isoformat()
    update_response = client.put(
        f"/api/v1/groceries/{grocery['id']}",
        json={"grocery_date": new_date},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["grocery_date"] == new_date
    assert updated["family_id"] == create_payload["family_id"]


def test_update_nonexistent_grocery_returns_not_found(client: TestClient) -> None:
    response = client.put(
        "/api/v1/groceries/99999",
        json={"family_id": 2},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Grocery not found"
