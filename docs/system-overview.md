# System Overview

This project is a small two-piece setup: a FastAPI backend that keeps track of grocery lists and an Angular frontend that lets people build and review those lists. The goal was to keep the stack lightweight, quick to spin up, and easy to hack on for weekend improvements.

- **Backend (`backend/`)** — FastAPI service that exposes `/api/v1` routes, stores data in SQLite, and seeds a handful of starter groceries on boot.
- **Frontend (`grocery-frontend/`)** — Angular single-page app that drives the “plan a grocery trip / check what’s already on the list” experience.

Everything runs happily on a laptop. Boot both services, hit `http://localhost:4200`, and you’re ready to start adding groceries.

---

## How the pieces talk to each other

1. The frontend loads at `localhost:4200` and immediately asks the backend for available items and saved grocery lists.
2. When you build a new list, the Angular app posts JSON to the backend’s `/api/v1/groceries` endpoint.
3. FastAPI validates the payload with Pydantic, writes it through SQLAlchemy into SQLite, and sends the updated list back.
4. Any follow-up edits or inline item changes go through RESTful routes such as `/api/v1/grocery_items/{id}` (PATCH/DELETE) so the UI and database stay in sync without manual refreshes.

Because everything leans on HTTP + JSON, swapping the frontend or backend would be straightforward if requirements change later.

---

## Running the stack

### Backend quickstart

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

By default the API lives at `http://localhost:8000`. If you need different settings, create a `.env` file in this folder with overrides (e.g., database path or allowed CORS origins). The SQLite file sits in `backend/data/grocery.db`, and the startup script seeds a few sample items so the UI isn’t empty on first launch.

**Prefer containers?** From the repo root, run:

```bash
docker compose up --build backend
```

The compose file mounts `./backend` for live code reloads and keeps the SQLite data under `./data`, so you don’t lose anything between runs.

### Frontend quickstart

```bash
cd grocery-frontend
npm install
npm start
```

Angular CLI serves the client at `http://localhost:4200` with hot reload. The API base URL lives in `src/app/services/grocery.service.ts`; update `apiUrl` if you move the backend. For a production bundle, run `npm run build`—the static files land in `dist/`.

---

## Under the hood

**Backend**
- FastAPI for routing, dependency injection, and auto-generated docs.
- Pydantic v2 schemas define request/response contracts.
- SQLAlchemy ORM + SQLite handle persistence with minimal setup; cascade deletes keep grocery items tidy when a list disappears.
- `start.sh` is the production entrypoint used by the Docker image.
- Tests live in `backend/tests/` and use `pytest` with FastAPI’s `TestClient`.

**Frontend**
- Angular 19 with standalone components keeps the project compact.
- RxJS and `HttpClient` manage API calls and async flows.
- `grocery-form` is a reactive form that builds the payload sent to the backend.
- `grocery-list` now supports add/edit/delete flows and purchased toggles on top of the previously saved lists view.
- Styling is plain CSS—no dependency on Material or other UI kits.

---

## What to remember

- Start the backend first so the frontend has something to talk to.
- The backend ships with Docker support; the frontend typically runs via `ng serve`, with a Dockerfile available if you need a static bundle later.
- Configuration is intentionally simple: `.env` for FastAPI, Angular constants for the client.
- Tests (`python3 -m pytest` and `npm test`) run fast enough to be part of your regular workflow.
- For discussion/next steps, see `docs/future-improvements.md` for scaling ideas and feature backlog notes.

That’s the whole system—lean, predictable, and ready for new features without a ton of ceremony.
