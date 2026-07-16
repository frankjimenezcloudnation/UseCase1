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

## Agent-flow (voor het verfijnen van de tool)

Een Claude Code multi-agent workflow die de use case gecontroleerd vertaalt naar
specificaties, een Definition of Done en acceptatietesten — met de pensioendeskundigen
als beslissers op elke inhoudelijke stap. **4 stations, 7 agents, 3 human gates.**

**Ingangen (slash-commands):**

- **`/begrijpen`** — start Station 1 (Begrijpen): de brainstorm-/begripsfase. Bouwt het
  Use Case Canvas en zet onduidelijkheden om in geprioriteerde expertvragen. Gebruik dit
  om de agents scherp te krijgen wat we met UC1 bedoelen, vóór er iets gespecificeerd wordt.
- **`/agent-flow`** — de volledige orkestratie over alle stations (begrijpen → specificeren
  → DoD & testen → beheer), met gate-handhaving en outputvalidatie.

**Structuur:**

- `.claude/skills/agent-flow/` — de orchestrator-skill (`SKILL.md`) + `references/`
  (`flow-state.md` = state-schema & routing, `output-contracts.md` = validatiecontracten).
- `.claude/agents/` — de 7 agent-definities (context-analyst, domain-interviewer,
  requirements-engineer, ontology-guardian, dod-composer, test-designer, red-team-critic).
- `.claude/commands/begrijpen.md` — de `/begrijpen`-ingang.
- `docs/agent-flow/` — deliverables (canvas, vragen, specs, DoD, tests, red-team),
  `status.yaml` (gate-/flow-state, bron van waarheid) en `traceability.yaml`.
- `scripts/doc_tools.py` — teksttoegang tot binaire bronnen (ontologie-zoeken, DOCX/XLSX),
  draait op `backend/.venv/bin/python` (geen extra dependencies).
- `context/` — lokale broncontext (projectcontext + spec), **gitignored**; niet gepusht.

Principes: de mens beslist en de agent bereidt voor; elke bevinding is traceerbaar naar een
bron; `OntologySnapshot.xlsx` is de gedeelde taal; en recente stakeholderinput wint van het
contextdocument. `.md`/`.yaml` uit deze flow worden nooit door de analyse-pipeline ingelezen
(die scant alleen `.pdf/.docx/.xlsx` in de repo-root en `uploads/`).
