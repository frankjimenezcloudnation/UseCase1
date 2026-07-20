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

Een Claude Code multi-agent workflow die de use case gecontroleerd vertaalt naar een
geconsolideerde deliverables-tabel, specificaties, een Definition of Done en
acceptatietesten — met de pensioendeskundigen als beslissers op elke inhoudelijke stap.
**5 stations, 12 agents, 4 human gates.**

**Ingangen (slash-commands):**

- **`/begrijpen`** — **de hoofdingang**: één doorlopende sessie. Je levert je informatie,
  spart met het agent-team (zij stellen vragen, jij antwoordt en legt uit) tot je zegt dat
  je **klaar** bent, en daarna doorlopen de agents de hele flow grondig (begrijpen →
  vertalen → specificeren → DoD & testen) en leveren alle deliverables op — met wat nog
  door deskundigen bevestigd moet worden expliciet gemarkeerd.
- **`/vertalen`** — spring direct naar Station 2 (Vertalen), als het canvas al door Gate 1
  is: een team van 4 interpretatie-agents (business, techniek, data/ontologie,
  compliance/risico) leest het canvas elk vanuit hun eigen invalshoek; de
  vertaal-synthesizer voegt dat samen tot één geconsolideerde deliverables-tabel en
  markeert waar de lenzen botsen als divergentie. Die divergenties worden via een
  vertaalchat opgelost — nooit door een agent zelf. Resultaat: een volledige technische
  tabel voor de dev-agents én een korte samenvatting voor de business-mensen.
- **`/agent-flow`** — dezelfde flow, maar station-voor-station met een gate-pauze na elk
  station, voor wie stap voor stap meer controle wil.

**Structuur:**

- `.claude/skills/agent-flow/` — de orchestrator-skill (`SKILL.md`) + `references/`
  (`flow-state.md` = state-schema & routing, `output-contracts.md` = validatiecontracten).
- `.claude/agents/` — de 12 agent-definities: context-analyst, domain-interviewer
  (Station 1); business-analist, technisch-architect, data-ontologie, compliance-risico,
  vertaal-synthesizer (Station 2); requirements-engineer, ontology-guardian (Station 3);
  dod-composer, test-designer, red-team-critic (Station 4).
- `.claude/commands/` — de `/begrijpen`- en `/vertalen`-ingangen.
- `docs/agent-flow/` — deliverables (canvas, vragen, vertaling/deliverables-tabel, specs,
  DoD, tests, red-team), `status.yaml` (gate-/flow-state, bron van waarheid) en
  `traceability.yaml`.
- `scripts/doc_tools.py` — teksttoegang tot binaire bronnen (ontologie-zoeken, DOCX/XLSX),
  draait op `backend/.venv/bin/python` (geen extra dependencies).
- `context/` — lokale broncontext (projectcontext + spec), **gitignored**; niet gepusht.

Principes: de mens beslist en de agent bereidt voor; elke bevinding is traceerbaar naar een
bron; `OntologySnapshot.xlsx` is de gedeelde taal; recente stakeholderinput wint van het
contextdocument; en een divergentie tussen interpretatie-lenzen wordt nooit stilzwijgend
opgelost — alleen de gebruiker beslist. `.md`/`.yaml` uit deze flow worden nooit door de
analyse-pipeline ingelezen (die scant alleen `.pdf/.docx/.xlsx` in de repo-root en `uploads/`).
