# WTP Pension Prototyping Engine — Use Case 1

Prototype for the Dutch **Wet toekomst pensioenen (Wtp)** transition: automatically
compare a pension fund's unstructured corpus (FPR, ABTN, Transitieplan, Operating
Manual, Implementatieplan) against the standard Wtp product (IG&H AllVida / Feniqs
Qwik + the ontology snapshot), and surface entitlement gaps, actuarial impact,
proposed Qwik rule-engine configuration, and full source provenance.

- **`backend/`** — FastAPI + Anthropic Claude (`messages.parse` → `FundComparisonReport`)
- **`frontend/`** — React + TypeScript + Chakra UI v3, CloudNation brand system
- Sample fund/benchmark documents live in this directory (`*.pdf`, `*.docx`, `*.xlsx`)

## Quick start

**Backend** (Python 3.11–3.13):

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your Anthropic key (ANTHROPIC_API_KEY or ATP)
uvicorn app.main:app --reload    # http://localhost:8000/docs
```

**Frontend** (Node 18+):

```bash
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

Open http://localhost:5173, keep the default document selection, and click
**"Vergelijking uitvoeren"**. With an Anthropic key configured, Claude analyses
the corpus live; without one, a grounded demo report is returned so the flow is
always demonstrable (the UI shows which mode ran).

## What's implemented (Use Case 1)

1. **Ingestion & classification** — `documents.py` scans the corpus and labels each
   file as fund vs. benchmark; `extraction.py` reads PDF (page-tagged) / DOCX / XLSX.
2. **Schema-enforced extraction** — Claude is forced to emit the exact
   `FundComparisonReport` schema from the technical specification (structured outputs).
3. **Auditable output** — every comparison cites its source document, article, page
   number and a verbatim quote, per the provenance requirement (DNB/AFM).
4. **Qwik-ready** — each deviation includes proposed Qwik rule-engine configuration
   parameters as JSON.
