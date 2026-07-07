# UseCase1 — Backend (FastAPI)

## Requirements

- Python **3.11–3.13** (3.14 is not yet supported by the pinned pydantic/Rust toolchain)

## Setup

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1
- Interactive docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

## Test

```bash
pytest
```

## Structure

```
app/
  main.py            # App factory, CORS, router wiring
  core/config.py     # Settings (env-driven, pydantic-settings)
  api/
    router.py        # Aggregates all route modules under /api/v1
    routes/          # Endpoint modules (health, items, ...)
  schemas/           # Pydantic request/response models
  services/          # Business logic (item_service is in-memory; swap for a DB)
tests/               # pytest + FastAPI TestClient
```

To add a resource: create a schema in `schemas/`, a service in `services/`, a
route module in `api/routes/`, then register it in `api/router.py`.
