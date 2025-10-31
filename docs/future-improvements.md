# Future Improvements

Once the core workflow is solid, here’s where we can keep leveling up the project. Think of this as a backlog of “nice to have” tasks that move the app from prototype to production-ready.

---

## Backend ideas

- **Account-aware lists**  
  Add JWT auth so each household sees only their own groceries. That unlocks features like shared lists and reminders.

- **Schema migrations + Postgres**  
  Bring in Alembic and support a Postgres connection string. SQLite has been great for dev, but migrations keep us safe as models evolve.

- **Better querying**  
  `/groceries` already caps page size; next up is richer filters (date ranges, purchased status, household) and cursor-based pagination so large tenants stay fast.

- **Background jobs**  
  Use FastAPI background tasks (or Celery if things grow) to send reminder emails, schedule recurring lists, or clean up old data.

- **Validation polish**  
  Expand domain rules (no duplicate items per list, maximum quantity thresholds) and surface friendly problem details when business rules fail.

---

## Frontend ideas

- **Real routing**  
  Wire up Angular Router so planner and history views get their own URLs. It’s easier to share links and add future screens.

- **Lightweight caching**  
  Introduce NgRx or signals-based state to keep grocery data in memory, reducing repeat API calls after edits and paving the way for optimistic UI updates.

- **UI/UX polish**  
  Add confirmations before destructive actions, tighten up responsive layouts, and maybe sprinkle in quick metrics (counts, last updated).

- **Accessibility pass**  
  Audit keyboard interactions, aria labels, and color contrast to make the app friendly for everyone; pair this with automated tooling (axe, Lighthouse) to catch regressions.

- **Testing story**  
  Expand Karma/Jasmine coverage and add an end-to-end suite (Playwright or Cypress) to cover the submit-and-verify flow.

- **Shared domain package**  
  Extract the TypeScript interfaces into a workspace library or publishable package so generated backend typings can stay in sync with the Angular models without manual edits.

---

## Shared & DevOps ideas

- **CI/CD pipeline**  
  Automate linting, tests, and Docker builds with GitHub Actions so every change ships with confidence.

- **Deployment scripts**  
  Add Docker Compose profiles (dev/staging/prod) or lightweight Kubernetes manifests to document how we expect to run the services, including seeded demo data for QA environments.

- **Observability**  
  Layer in structured logging and basic metrics (Prometheus/Grafana stack works fine) so we can troubleshoot and watch usage trends.

- **Secrets management**  
  Hook up environment variables to a secrets manager (GitHub Actions secrets, Doppler, etc.) to keep credentials out of source control and make rotation painless.

- **Eventing & real-time**  
  As shared lists arrive, consider server-sent events or WebSocket gateways so clients stay in sync without polling.

- **Data lifecycle**  
  Document and automate retention policies (archiving old groceries, anonymizing PII) to ease compliance conversations later.

- **Consolidated task runner**  
  Introduce a Makefile (or npm/pipenv equivalent) to bundle common workflows—install, lint, build, test—behind a single command for contributors.

These ideas aren’t required to keep the app running today, but knocking them out will make the system more trustworthy, easier to maintain, and ready for real users.
