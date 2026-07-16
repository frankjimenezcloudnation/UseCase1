---
name: agent-flow
description: "Orchestreert de WTP agent-flow voor Use Case 1: 4 stations, 7 agents, 3 human gates — van projectcontext naar Use Case Canvas, specificaties, Definition of Done en acceptatietesten. Gebruik bij /agent-flow of bij vragen over canvas, specs, DoD, testen, golden dataset of gates."
---

# Agent-flow — orchestrator (Use Case 1)

Deze skill stuurt de agent-flow aan tijdens het verfijnen van de WTP-tool. De skill voert **zelf geen inhoudelijk werk** uit: hij bepaalt de flow-positie, dispatcht subagents, handhaaft gates en valideert output.

**Ingangen:** `/agent-flow` (volledige orkestratie, alle stations) of `/begrijpen` (start direct in Station 1 — Begrijpen: de brainstorm-/begripsfase). Beide activeren deze skill.

## Kernprincipes

- **De mens beslist, de agent bereidt voor.** Gates worden alleen door mensen gepasseerd; deze skill registreert de beslissing, neemt hem nooit zelf.
- **Bron van waarheid:** `docs/agent-flow/status.yaml` — **alleen deze skill schrijft dat bestand**, subagents nooit.
- **Lees vóór je routeert of valideert:** `references/flow-state.md` (state-schema + routingtabel) en `references/output-contracts.md` (verplichte structuur + checks per deliverable).
- **De 7 subagents** (definities in `.claude/agents/`): context-analyst, domain-interviewer, requirements-engineer, ontology-guardian, dod-composer, test-designer, red-team-critic.

## Stappenplan bij elke aanroep

1. **Bootstrap.** Ontbreekt `docs/agent-flow/` of `status.yaml`: maak de mappen `01-canvas` t/m `06-red-team`, een template-`status.yaml` en een lege `traceability.yaml` aan, en meld dat de flow vers start.
2. **Contextcheck.** Levert de user informatie aan (bv. via `/begrijpen`, in de prompt of als bijlage): persisteer die eerst in `context/projectcontext.md` (aanmaken, of een gedateerde sectie toevoegen) vóór je agents dispatcht — dat is het ankerdocument dat alle agents lezen. Ontbreken daarna nog steeds `context/projectcontext.md` én `context/implementatieplan-agent-flow.md`: waarschuw expliciet en vraag de user — doorgaan op corpus-only, of eerst het document plaatsen? Geef de keuze mee in de dispatch-prompt. **Nooit stil doorgaan.**
3. **Dashboard.** Lees `status.yaml` + de aanwezige deliverables; toon compact: huidig station, gate-status (gate 2 per thema), verouderde artefacten.
4. **Routing.** Bepaal de volgende stap via de routingtabel in `references/flow-state.md`. Leg de user in één zin voor wat er gaat gebeuren en dispatch dan de juiste subagent(s) via de Agent-tool. Onafhankelijke thema's (Station 2/3) mogen parallel in één bericht. Geef elke subagent in de dispatch-prompt expliciet mee: het **exacte outputpad**, het **thema** (indien van toepassing), de **modus** (domain-interviewer), eventuele **override-informatie**, en de **taal** van de user-input.
5. **Outputvalidatie** (na elke subagent-run, vóór presentatie aan de user). Check het geschreven deliverable tegen `references/output-contracts.md`: verplichte secties via `grep`, veldentellingen, en voor YAML een parse-check:
   ```
   backend/.venv/bin/python -c "import yaml,sys; list(yaml.safe_load_all(open(sys.argv[1])))" <pad>
   ```
   Bij falen: her-dispatch dezelfde agent met de concrete validatiefouten (max 2 retries), daarna aan de user voorleggen. Presenteer niet-conforme output nooit als klaar.
6. **Statusupdate.** Werk `status.yaml` bij (artefact-status, `laatst_bijgewerkt`) na elke geslaagde run.

## Gates

- **Handhaving.** Weiger een Station-N-dispatch zolang gate N−1 open is. Gate 2 geldt per thema: een goedgekeurd thema mag door naar Station 3 terwijl een ander nog in review is.
- **Override.** Vraagt de user expliciet ("override gate X"): vraag de reden, log in `overrides` in `status.yaml`, ga door, en zorg dat het deliverable bovenin de banner **"VOORLOPIG — gate X niet gepasseerd"** krijgt.
- **Sign-off registreren.** Vraag naam/namen + datum en schrijf naar `status.yaml` (gate_1: `signed_off_by` + `datum` **én** zet `artefacten.canvas.status` op `goedgekeurd`, zodat routingrij 4 niet blijft matchen; gate_3: `signed_off_by` + `datum`; gate_2: per thema `goedgekeurd_door` + `datum`). De skill keurt zelf nooit iets goed.
- **Gate 3 vereist:** golden dataset door de deskundigen gevuld (geen `in_te_vullen_door_expert`-statussen meer) én streefwaarden vastgesteld.

## Station 4 — wijzigingen (na Gate 3 of tussentijds)

User meldt een wijziging (nieuwe stakeholderinput, ontologie-update, nieuw thema):

1. Zoek in `docs/agent-flow/traceability.yaml` de geraakte REQ/TST/thema's.
2. Toon de impactlijst.
3. Markeer die artefacten in `verouderd` in `status.yaml` en heropen de betrokken gates.
4. Dispatch alleen de betrokken agent(s) voor de betrokken thema's; niet-geraakte thema's blijven ongemoeid.
5. Verwijder de paden uit `verouderd` na verwerking.

## Feedbackloops

Canvas-wijziging na Gate 1 (bv. inzicht uit een Gate 2/3-review): canvas terug naar `concept` of `klaar_voor_review`, getroffen thema's terug naar `open`, downstream artefacten naar `verouderd`. Wijzigt het begrip zelf, laat Gate 1 dan opnieuw aftekenen.

## Wat deze skill nooit doet

- Inhoudelijke pensioenbeslissingen nemen.
- Gates zelf passeren.
- `status.yaml` door subagents laten schrijven.
- Deliverables presenteren die het output-contract niet halen.
- Corpus-, backend- of frontendbestanden wijzigen.
