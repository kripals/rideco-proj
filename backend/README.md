# Grocery API Backend

This is the backend service for the Grocery Management app. It’s built with FastAPI and provides versioned REST APIs (`/api/v1/...`) for managing grocery lists, items, and categories. The backend uses SQLAlchemy for ORM and stores data in an SQLite database. When it starts up, it automatically creates the database tables and seeds a few sample records.

---

## Getting Started

### Requirements

- Python 3.11 or newer
- (Recommended) Create a virtual environment to keep dependencies isolated:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Installation

Set things up the way that fits your workflow—either directly on your machine or inside Docker.

**Local Python environment**

Once inside your virtual environment:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

**Docker image**

If you prefer to stay containerized, simply run the following command from the root folder:

```bash
docker-compose up -d --build
```

This will build the image and start the container using the configurations already set up in the `docker-compose.yml` file. No additional setup is required.

---

## Configuration

The app reads environment variables from a `.env` file at startup. A typical setup looks like this:

```env
DATABASE_URL=sqlite:///data/grocery.db
ALLOWED_ORIGINS=http://localhost:4200
```

- `DATABASE_URL` — the SQLAlchemy database connection string.
- `ALLOWED_ORIGINS` — a comma-separated list of frontend origins allowed by CORS.

When running with Docker, pass the same `.env` file using `--env-file .env`. Mounting `./data` into `/app/data` keeps your SQLite database on the host so it survives container restarts.

---

## Running the Server

To run locally with auto-reload:

```bash
uvicorn main:app --reload
```

In production (or Docker), use the included start script:

```bash
./start.sh
```

You don't need to run this command if you've already used `docker-compose up`, as it handles building the image, starting the container, and setting up the database. However, if you want to run the container manually (e.g., for debugging or custom setups), you can use the following command:

```bash
docker run --env-file .env -v $(pwd)/data:/app/data -p 8000:8000 grocery-api-backend
```

When the app starts, it creates the database (if missing) and seeds sample item types and items.

---

## Interactive API Documentation

With the server running (locally or via Docker), open the automatically generated Swagger UI:

- [http://localhost:8000/docs](http://localhost:8000/docs) — interactive Swagger documentation where you can explore every endpoint, inspect schemas, and fire sample requests.
- [http://localhost:8000/redoc](http://localhost:8000/redoc) — read-only ReDoc documentation for a concise reference of request/response models.

Both views reflect the live application state, so any changes to the API will show up immediately.

---

## Code Quality Tools

From the `backend/` directory, you can format, lint, and type-check your code:

```bash
isort .
black .
flake8
mypy .
```

- `isort` and `black` keep the code consistent and readable.
- `flake8` checks for style and logic issues.
- `mypy` enforces type hints.

---

## Running Tests

The project uses `pytest` with an in-memory SQLite database for tests:

```bash
python3 -m pytest
```

All tests live in the `tests/` folder and use FastAPI’s `TestClient` for endpoint testing.

---

## API Overview

**Base URL:** `/api/v1`

| Method | Endpoint                 | Description                       |
|--------|--------------------------|---------------------------------|
| GET    | /item_types              | List all item categories         |
| POST   | /item_types              | Add a new item category          |
| GET    | /items                   | List all items and their types   |
| POST   | /items                   | Create a new item                |
| GET    | /groceries               | List grocery lists (with items)  |
| POST   | /groceries               | Create a new grocery list        |
| GET    | /groceries/{id}          | Get a grocery list by ID         |
| PUT    | /groceries/{id}          | Update grocery list details      |
| DELETE | /groceries/{id}          | Delete a grocery list            |
| GET    | /grocery_items           | List all grocery items           |
| GET    | /groceries/{id}/items    | List items for a specific grocery list |
| POST   | /groceries/{id}/items    | Add an item to a grocery list    |
| PUT    | /grocery_items/{id}      | Update a grocery item            |
| PATCH  | /grocery_items/{id}      | Partially update (e.g., toggle `purchased`) |
| DELETE | /grocery_items/{id}      | Delete a grocery item            |

All list endpoints accept optional `skip` and `limit` query parameters (with `limit` clamped to 1–100) for lightweight pagination.

### Example: Create Grocery List

**Request:**

```
POST /api/v1/groceries
Content-Type: application/json
```

```json
{
  "family_id": 1,
  "grocery_date": "2024-06-20",
  "grocery_items": [
    {"item_id": 1, "quantity": 2, "purchased": false},
    {"item_id": 3, "quantity": 1, "purchased": true}
  ]
}
```

**Response:**

```json
{
  "id": 42,
  "family_id": 1,
  "grocery_date": "2024-06-20",
  "created_at": "2024-06-18T12:34:56.123456",
  "grocery_items": [
    {"id": 101, "grocery_id": 42, "item_id": 1, "quantity": 2, "purchased": false},
    {"id": 102, "grocery_id": 42, "item_id": 3, "quantity": 1, "purchased": true}
  ]
}
```

---

## Project Structure

```
backend/
├── grocery_api/
│   ├── crud.py          # Database queries and API logic
│   ├── database.py      # SQLAlchemy engine and session
│   ├── models.py        # ORM models
│   ├── schemas.py       # Pydantic validation models
│   └── seed.py          # Data seeding at startup
├── main.py              # FastAPI app entry point
├── requirements.txt     # Dependencies
├── start.sh             # Docker/production entry script
└── tests/               # Unit tests
```

---

## Notes

- The database auto-creates and seeds on startup. Delete `data/grocery.db` if you want a clean reset.
- You can edit `grocery_api/seed.py` to change the sample data.
- CORS is enabled for the origins defined in `.env`.
- Create/update endpoints translate database conflicts (e.g., duplicate names or invalid foreign keys) into clean `409` or `400` responses, so client errors never surface as 500s.

---

## Author

Created and maintained by Kripal Shrestha  
📧 kripalshrestha@hotmail.com  
🌐 [https://www.kripal.dev](https://www.kripal.dev)
