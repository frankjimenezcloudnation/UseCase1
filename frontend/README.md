# UseCase1 — Frontend (React + TypeScript + Chakra UI)

Built with Vite, React 19, TypeScript, and Chakra UI v3.

## Setup

```bash
cd frontend
npm install
cp .env.example .env   # optional — defaults use the dev proxy
```

## Run

```bash
npm run dev
```

Opens http://localhost:5173. API calls to `/api/*` are proxied to the FastAPI
backend at http://localhost:8000 (see `vite.config.ts`). Start the backend too.

## Build

```bash
npm run build     # type-check + production bundle into dist/
npm run preview   # serve the production build locally
```

## Structure

```
src/
  main.tsx                    # Entry point; wraps app in <Provider>
  App.tsx                     # Layout shell (header + color-mode toggle)
  api/
    client.ts                 # Typed fetch wrapper (base URL + /api/v1 prefix)
    items.ts                  # Items endpoint bindings + types
  components/ui/
    provider.tsx              # Chakra + color-mode (next-themes) provider
    color-mode.tsx            # Light/dark toggle button
  pages/
    ItemsPage.tsx             # Demo CRUD page against the backend
```

Path alias `@/` maps to `src/`. Configure the API base URL via
`VITE_API_BASE_URL` (leave empty to use the Vite dev proxy).
