# Backend — WTP Pension Prototyping Engine (Use Case 1)

FastAPI service that implements **Use Case 1: Fondsreglement vs. Standaardproduct**.
It ingests a pension fund's unstructured corpus (FPR, ABTN, Operating Manual,
Transitieplan, Implementatieplan) and compares it against the standard Wtp product
(IG&H AllVida / Feniqs Qwik + the ontology snapshot), using **Anthropic Claude**
structured outputs to emit a typed `FundComparisonReport` with source provenance.

## Requirements

- Python **3.11–3.13** (3.14 not yet supported by the pinned pydantic/Rust toolchain)

## Setup

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # add your Anthropic key (ANTHROPIC_API_KEY or ATP)
```

## Run

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- `GET  /api/v1/analysis/documents` — list the classified fund + benchmark corpus
- `POST /api/v1/analysis/compare`   — run the entitlement audit (Claude)

Without an Anthropic key the compare endpoint returns a **grounded demo report**
so the UI is fully demonstrable; the `mode` field reports `live` vs `demo`.

## Test

```bash
pytest
```

## How it works

```
app/
  services/
    documents.py        # scans DOCUMENTS_DIR, classifies files (fund | benchmark)
    extraction.py       # PDF (page-tagged) / DOCX / XLSX -> text
    claude_analysis.py  # builds the prompt, calls messages.parse(FundComparisonReport)
  schemas/comparison.py # the structured-output schema (per the WTP tech spec)
  api/routes/analysis.py
```

`DOCUMENTS_DIR` defaults to the `UseCase1/` project root, where the sample
SPF/DPF documents live. Point it elsewhere to analyse a different corpus.
