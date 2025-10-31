from datetime import date, timedelta
import uuid

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


def test_duplicate_item_type_returns_conflict(client: TestClient) -> None:
    name = f"Frozen-{uuid.uuid4()}"
    first = client.post("/api/v1/item_types", json={"name": name})
    assert first.status_code == 200

    duplicate = client.post("/api/v1/item_types", json={"name": name})
    assert duplicate.status_code == 409
    assert "exists" in duplicate.json()["detail"]


def test_create_item_with_unknown_type_fails(client: TestClient) -> None:
    response = client.post(
        "/api/v1/items",
        json={"name": f"UnknownType-{uuid.uuid4()}", "item_type_id": 999_999},
    )

    assert response.status_code == 400
    assert "Unknown item type" in response.json()["detail"]


def test_create_grocery_item_with_invalid_reference(client: TestClient) -> None:
    grocery = client.post(
        "/api/v1/groceries",
        json={
            "family_id": 1,
            "grocery_date": date.today().isoformat(),
            "grocery_items": [],
        },
    ).json()

    response = client.post(
        f"/api/v1/groceries/{grocery['id']}/items",
        json={"item_id": 999_999, "quantity": 1, "purchased": False},
    )

    assert response.status_code == 400
    assert "Invalid grocery or item reference." in response.json()["detail"]


def test_patch_grocery_item_toggle_purchased(client: TestClient) -> None:
    item_id = client.get("/api/v1/items").json()[0]["id"]
    grocery = client.post(
        "/api/v1/groceries",
        json={
            "family_id": 1,
            "grocery_date": date.today().isoformat(),
            "grocery_items": [{"item_id": item_id, "quantity": 1, "purchased": False}],
        },
    ).json()

    grocery_item_id = grocery["grocery_items"][0]["id"]
    patch_response = client.patch(
        f"/api/v1/grocery_items/{grocery_item_id}",
        json={"purchased": True},
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["purchased"] is True


def test_delete_grocery_with_items_cascades(client: TestClient) -> None:
    item_id = client.get("/api/v1/items").json()[0]["id"]
    grocery = client.post(
        "/api/v1/groceries",
        json={
            "family_id": 1,
            "grocery_date": date.today().isoformat(),
            "grocery_items": [{"item_id": item_id, "quantity": 1, "purchased": False}],
        },
    ).json()

    delete_response = client.delete(f"/api/v1/groceries/{grocery['id']}")
    assert delete_response.status_code == 200

    follow_up = client.get(f"/api/v1/groceries/{grocery['id']}")
    assert follow_up.status_code == 404


def test_items_endpoint_respects_limit(client: TestClient) -> None:
    response = client.get("/api/v1/items", params={"limit": 1})
    assert response.status_code == 200
    assert len(response.json()) <= 1
