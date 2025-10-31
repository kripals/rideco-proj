# Grocery Frontend

This is the Angular client for the Grocery Planner app. It lets you build grocery lists and browse everything you’ve already saved. The UI talks to the FastAPI backend that lives in `./backend`.

## What you need

- Node.js 18 (or newer)
- npm 9+

## Getting started

Install dependencies once:

```bash
npm install
```

Start the dev server:

```bash
npm start
```

Angular CLI serves the app at `http://localhost:4200` with live reload. The code expects the backend at `http://localhost:8000/api/v1`; change the `apiUrl` in `src/app/services/grocery.service.ts` if your backend runs elsewhere.

## Useful scripts

- `npm start` – run the dev server
- `npm run build` – create a production build in `dist/`
- `npm test` – execute unit tests with Karma

## Project notes

- The planner page creates new grocery lists; the saved lists page lets you mark items as purchased, adjust quantities, add catalog items to an existing list, or delete items/lists outright.
- Components live in `src/app`. `grocery-form` handles creating a list and `grocery-list` shows what’s already stored.
- Styles are plain CSS. Global rules are in `src/styles.css`, and each component keeps its own styles next to the TypeScript file.
- The expected workflow is to run the Angular CLI dev server (`npm start`). A Dockerfile lives here for future production builds, but it isn’t wired into any scripts yet; feel free to build it manually if you want a static bundle served via nginx.
