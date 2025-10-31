import uuid
from datetime import date, timedelta
from typing import Any, Dict

from fastapi.testclient import TestClient


def test_root_endpoint_returns_service_health(client: TestClient) -> None:
    """User hits '/' to verify the service is alive and gets the health message."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Grocery API is running"}


def test_list_items_seeded_should_return_a_list_of_seeded_items(
    client: TestClient,
) -> None:
    """User requests catalog items and receives pre-seeded inventory."""
    response = client.get("/api/v1/items")

    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert {"id", "name", "item_type_id"}.issubset(items[0].keys())


def test_create_and_fetch_grocery_should_successfully_create_and_retrieve_a_grocery_list(
    client: TestClient,
) -> None:
    """User creates a grocery list then fetches it back to confirm persistence."""
    items_response = client.get("/api/v1/items")
    item_ids = [item["id"] for item in items_response.json()[:2]]

    payload: Dict[str, Any] = {
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
    assert (
        fetched["grocery_items"][0]["item"]["id"]
        == payload["grocery_items"][0]["item_id"]
    )


def test_update_grocery_metadata_should_allow_updating_a_grocery_lists_metadata(
    client: TestClient,
) -> None:
    """User moves a grocery trip to a new date and sees the change reflected."""
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


def test_update_nonexistent_grocery_should_return_not_found_when_updating_a_nonexistent_grocery(
    client: TestClient,
) -> None:
    """User attempts to edit a missing grocery list and receives a 404."""
    response = client.put(
        "/api/v1/groceries/99999",
        json={"family_id": 2},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Grocery not found"


def test_duplicate_item_type_should_return_conflict_when_creating_an_item_type_with_a_duplicate_name(
    client: TestClient,
) -> None:
    """User attempts to create a duplicate item type and is warned with 409."""
    name = f"Frozen-{uuid.uuid4()}"
    first = client.post("/api/v1/item_types", json={"name": name})
    assert first.status_code == 200

    duplicate = client.post("/api/v1/item_types", json={"name": name})
    assert duplicate.status_code == 409
    assert "exists" in duplicate.json()["detail"]


def test_create_item_with_unknown_type_should_return_bad_request_when_creating_an_item_with_an_unknown_type(
    client: TestClient,
) -> None:
    """User tries to add an item with an invalid type and gets a 400."""
    response = client.post(
        "/api/v1/items",
        json={"name": f"UnknownType-{uuid.uuid4()}", "item_type_id": 999_999},
    )

    assert response.status_code == 400
    assert "Unknown item type" in response.json()["detail"]


def test_create_grocery_item_with_invalid_reference_should_return_bad_request_when_adding_a_nonexistent_item_to_a_grocery_list(
    client: TestClient,
) -> None:
    """User adds an item with a bad reference and receives a helpful error."""
    grocery: Dict[str, Any] = client.post(
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


def test_patch_grocery_item_toggle_purchased_should_allow_toggling_a_grocery_items_purchased_status(
    client: TestClient,
) -> None:
    """User marks an item as purchased via PATCH and sees the status flip."""
    item_id = client.get("/api/v1/items").json()[0]["id"]
    grocery: Dict[str, Any] = client.post(
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


def test_delete_grocery_with_items_should_remove_items(client: TestClient) -> None:
    """User deletes a grocery list and expects its items to disappear as well."""
    item_id = client.get("/api/v1/items").json()[0]["id"]
    grocery: Dict[str, Any] = client.post(
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


def test_items_endpoint_should_respect_limit(client: TestClient) -> None:
    """User requests a single item and the API honors the page size limit."""
    response = client.get("/api/v1/items", params={"limit": 1})
    assert response.status_code == 200
    assert len(response.json()) <= 1
