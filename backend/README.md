# Grocery API Backend

FastAPI service that powers the grocery management application. It provides versioned REST endpoints (`/api/v1/...`) for item catalog lookup, grocery list creation, and list maintenance. The backend uses SQLAlchemy with an SQLite database and automatically seeds sample data on startup.

## Prerequisites
- Python 3.11+
- (Recommended) Virtual environment such as `python -m venv venv`

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Environment Configuration
Runtime settings are read from `.env`:

```env
DATABASE_URL=sqlite:///data/grocery.db
ALLOWED_ORIGINS=http://localhost:4200
```

- `DATABASE_URL` – SQLAlchemy connection string (defaults to a local SQLite file).
- `ALLOWED_ORIGINS` – comma-separated list of origins allowed by CORS middleware.

`python-dotenv` loads `.env` automatically when `main.py` starts.

## Running the Server
```bash
uvicorn main:app --reload
```

The `start.sh` script provides the production command used in Docker:
```bash
./start.sh
```

When the API boots, the lifespan handler creates database tables and seeds sample item types/items.

## Formatting & Static Analysis
Run these commands from the `backend/` directory after making changes:

```bash
isort .
black .
flake8
mypy .
```

- `isort` and `black` keep imports and code style consistent.
- `flake8` highlights lint issues.
- `mypy` enforces static typing across the project.

## Testing
Pytest exercises the public endpoints with an isolated SQLite database. Execute:

```bash
python3 -m pytest
```

Tests live in `tests/` and reuse the FastAPI `TestClient`.

## API Reference (v1)

| Method | Path                               | Description                              |
| ------ | ---------------------------------- | ---------------------------------------- |
| `GET`  | `/api/v1/item_types`               | List item categories.                    |
| `POST` | `/api/v1/item_types`               | Create a new item category.              |
| `GET`  | `/api/v1/items`                    | List inventory items with types.         |
| `POST` | `/api/v1/items`                    | Create a new inventory item.             |
| `GET`  | `/api/v1/groceries`                | List grocery lists (with items).         |
| `POST` | `/api/v1/groceries`                | Create a grocery list (optionally nested items). |
| `GET`  | `/api/v1/groceries/{grocery_id}`   | Retrieve a grocery list by ID.           |
| `PUT`  | `/api/v1/groceries/{grocery_id}`   | Update grocery metadata (date/family).   |
| `DELETE` | `/api/v1/groceries/{grocery_id}` | Delete a grocery list.                   |
| `GET`  | `/api/v1/grocery_items`            | List all grocery items across lists.     |
| `GET`  | `/api/v1/groceries/{id}/items`     | List items for a specific grocery.       |
| `POST` | `/api/v1/groceries/{id}/items`     | Add an item to a grocery list.           |
| `PUT`  | `/api/v1/grocery_items/{item_id}`  | Update an existing grocery item.         |
| `DELETE` | `/api/v1/grocery_items/{item_id}`| Remove a grocery item.                   |

### Sample: Create Grocery
```http
POST /api/v1/groceries
Content-Type: application/json

{
  "family_id": 1,
  "grocery_date": "2024-06-20",
  "grocery_items": [
    {"item_id": 1, "quantity": 2, "purchased": false},
    {"item_id": 3, "quantity": 1, "purchased": true}
  ]
}
```

Response:
```json
{
  "id": 42,
  "family_id": 1,
  "grocery_date": "2024-06-20",
  "created_at": "2024-06-18T12:34:56.123456",
  "grocery_items": [
    {
      "id": 101,
      "grocery_id": 42,
      "item_id": 1,
      "quantity": 2,
      "purchased": false,
      "created_at": "2024-06-18T12:34:56.123456",
      "item": {...}
    },
    ...
  ]
}
```

## Project Structure
```
backend/
├── grocery_api/
│   ├── crud.py          # Database interaction logic
│   ├── database.py      # SQLAlchemy engine/session setup
│   ├── models.py        # ORM models
│   ├── schemas.py       # Pydantic schemas
│   └── seed.py          # Startup data seeding
├── main.py              # FastAPI application entry point
├── requirements.txt     # Backend dependencies
├── start.sh             # Production launch script
└── tests/               # Pytest suite for API endpoints
```

## Notes
- The database auto-creates and seeds at startup; delete `data/grocery.db` to reset.
- To change seeding, edit `grocery_api/seed.py`.
- All endpoints are CORS-enabled for origins specified in `.env`.

Feel free to expand this README with additional deployment or CI/CD instructions as the project grows.
