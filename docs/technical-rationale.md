# Technical Rationale

Here’s the thinking behind the stack. The project needed to come together fast, stay easy to reason about, and be friendly for future contributors. Everything below reflects those goals.

---

## Backend decisions

**FastAPI over Flask/Django**  
We wanted typed routes, request validation, and OpenAPI docs without bolting on extra libraries. FastAPI gives that out of the box, runs async when we need it, and stays lightweight. Django REST Framework was more weight than the project needed, and Flask would have required stitching together validation and schema tooling ourselves.

**Pydantic schemas**  
FastAPI pairs naturally with Pydantic, so we lean on v2 models for both request validation and response serialization. Having the types in place catches data mistakes early and keeps the docs honest. Alternatives like Marshmallow would add extra plumbing for not much gain.

**SQLAlchemy + SQLite**  
SQLAlchemy’s ORM keeps the models declarative and makes relationship handling (items, item types, groceries) straightforward. SQLite is plenty for local dev and small deployments, and the connection string can move to Postgres later with zero code changes. SQLModel was tempting, but sticking with SQLAlchemy gives us finer control over queries.

**Defensive CRUD layer**  
Routes stay thin; all the database work happens in `grocery_api/crud.py`. We wrapped writes in `IntegrityError` handling so user mistakes (duplicate names, bad FK references) come back as 4xx responses instead of 500s, and we added cascade deletes + pagination helpers to keep responses predictable as data grows.

**Dedicated seed + migrations later**  
Starting the API shouldn’t leave the UI blank. Seeding a few default categories and items means designers/QA can see something immediately. This lives alongside migration-ready models, so swapping to Alembic later is painless.

**Observability & docs baked in**  
FastAPI’s Swagger UI (`/docs`) and ReDoc (`/redoc`) stay enabled in every environment. Combined with typed responses and error envelopes, reviewers get a live contract without needing Postman collections.

**Supporting tooling**  
- `python-dotenv` lets us manage environment overrides quietly—handy when you want to point the app at a different database locally.  
- `pytest` + FastAPI’s `TestClient` give us fast API checks and form the foundation for regression tests.  
- The Dockerfile mirrors the production entrypoint (`start.sh`) so local Docker runs behave like actual deployments.

---

## Frontend decisions

**Angular 19 instead of React/Vue**  
The brief already pushed us toward Angular, and we leaned into it. Standalone components keep the boilerplate low, the CLI handles bundling/testing, and reactive forms are a nice fit for building grocery payloads. React would have needed extra choices around routing/forms; Angular gives a single opinionated path.

**Plain CSS**  
Adding Angular Material would have ballooned the bundle and pushed a design look we didn’t need. Rolling our own CSS gives full control and keeps the app tiny. Styles live next to components so it’s obvious where to tweak layout.

**Component breakdown**  
- `GroceryFormComponent` owns the form: date picker, item list, validation messaging, and the call to the backend.  
- `GroceryListComponent` now handles item-level actions (toggle purchased, quantity adjustments, deletions) and hosts an inline “add item” workflow, demonstrating how the UI exercises the richer backend API.

**Centralized data access (`GroceryService`)**  
Angular’s `HttpClient` sits behind a small service that describes the payload types. That way every component uses the same API surface, and changing the backend URL happens in one place.

**Simple navigation**  
Instead of wiring up Angular routing, the app keeps a lightweight tab switcher. For an app this size it’s faster to understand, and we can always add real routes if requirements grow.

---

## Takeaways

- Every choice favors fast feedback loops: hot reload on both sides, quick tests, and minimal ceremony.  
- The path to “deploy this somewhere” is already there—backend Docker support, Angular build output, and env overrides are part of the repo.  
- Swapping out pieces later (e.g., Postgres, different UI framework) is possible because the boundaries are clean: HTTP APIs with typed contracts on one side, a service layer on the other.  
- Longer-term ideas (multi-family sharing, auth, hosted DB) live in `docs/future-improvements.md`, giving reviewers a window into how the system scales to more demanding scenarios.

In short, the stack is intentionally boring in the best way—easy to maintain now and flexible enough for the next round of features.
