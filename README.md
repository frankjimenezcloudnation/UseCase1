# UseCase1

Full-stack monorepo:

- **`backend/`** — Python API built with FastAPI (Pydantic v2, pytest).
- **`frontend/`** — React + TypeScript SPA built with Vite and Chakra UI v3.

## Quick start

Run the two apps in separate terminals.

**Backend** (Python 3.11–3.13):

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://localhost:8000/docs
```

**Frontend** (Node 18+):

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

The frontend proxies `/api/*` to the backend during development, so both must
be running. See each subdirectory's `README.md` for details.
