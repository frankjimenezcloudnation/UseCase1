---
name: agent-flow
description: "Domein-onafhankelijke multi-agent workflow: 5 stations, 12 agents, 4 human gates — van projectcontext naar een gedeeld begrip, een geconsolideerde deliverables-tabel, specificaties, Definition of Done en testen. Gebruik bij /begrijpen, /vertalen, /agent-flow of bij vragen over canvas, vertaling, deliverables, specs, DoD, testen of gates."
---

# Agent-flow — orchestrator (generiek)

Deze skill stuurt een gecontroleerde flow aan om een willekeurige use case te begrijpen en te vertalen naar deliverables, specificaties, een Definition of Done en testen. De skill voert **zelf geen inhoudelijk werk** uit: hij bepaalt de flow-positie, dispatcht subagents, handhaaft gates en valideert output. Er zit **niets domeinspecifieks** in; alle domeinkennis komt uit het project (context, bronmateriaal, optionele config).

**Ingangen (alle drie activeren deze ene skill):**
- **`/begrijpen`** — de hoofdingang: één doorlopende sessie waarin je met het agent-team spart (zij stellen vragen, jij antwoordt en legt uit) tot jij zegt dat je **klaar** bent; daarna doorlopen de agents de hele flow grondig. Zie *Doorlopende modus*.
- **`/vertalen`** — spring direct naar Station 2 (Vertalen), als de use case al door Gate 1 begrepen is.
- **`/agent-flow`** — station-voor-station orkestratie met een gate-pauze na elk station.

## Stations, agents en gates op een rij

| Station | Naam | Agents | Exit-gate |
|---|---|---|---|
| 1 | Begrijpen | context-analyst, domain-interviewer | `gate_1` |
| 2 | Vertalen | business-analist, technisch-architect, data-domein, compliance-risico, vertaal-synthesizer | `gate_vertalen` |
| 3 | Specificeren | requirements-engineer, terminologie-guardian | `gate_2` (per area) |
| 4 | DoD & Testen | dod-composer, test-designer, red-team-critic | `gate_3` |
| 5 | Beheer | — (traceability + gerichte her-runs) | — |

**5 stations · 12 agents · 4 human gates.** Zie `references/flow-state.md` voor het status.yaml-schema en de routingtabel.

## Areas (thema's) zijn projectspecifiek

De flow werkt met **areas** (deelonderwerpen van de use case), niet met vaste thema's. Zoek ze zo:
1. Staat er een `docs/agent-flow/config.yaml` met `areas:`? Gebruik die codes/namen.
2. Anders: de context-analyst stelt in Station 1 een set areas voor (met korte codes, bv. `AUTH`, `BILL`); de mens bevestigt ze bij Gate 1. Daarna vult de orchestrator `gate_2.themas` en `dod.themas` in `status.yaml` met die areas.

Requirement-/deliverable-id's krijgen de area-code als prefix: `REQ-<AREA>-NNN`, `DLV-<AREA>-NNN`. Naast de inhoudelijke areas is er altijd een generieke area `GEN` voor overkoepelende/technische zaken (inlezen, verwerking, presentatie, non-functionele eisen).

## Kernprincipes

- **Eén doorlopende sessie (`/begrijpen`).** De user spart met het team tot die **"klaar"** zegt; daarna voeren de agents de hele flow grondig uit. De "klaar" is het go-signaal — de orchestrator dwingt nooit door en verzint nooit een beslissing die de user of de experts toekomt. Zie *Doorlopende modus*.
- **De mens beslist, de agent bereidt voor.** Gates worden alleen door mensen gepasseerd; deze skill registreert de beslissing, neemt hem nooit zelf. Een divergentie tussen interpretatie-lenzen (Station 2) wordt nooit door een agent opgelost.
- **Interactief, niet eenmalig.** Station 1 en 2 verlopen als dialoog: de orchestrator bevraagt de user in korte rondes en koppelt terug ("dus als ik je goed begrijp…"). Subagents draaien autonoom en praten niet zelf met de user — elke live dialoog loopt via de orchestrator.
- **Gedeelde taal.** Gebruik consistente projectterminologie. Heeft het project een begrippenlijst (`glossary`-pad in config)? Toets termen daartegen; een term die er niet in staat markeer je als afwijking (input voor de experts, geen fout).
- **Bron van waarheid:** `docs/agent-flow/status.yaml` — **alleen deze skill schrijft dat bestand**, subagents nooit.
- **Lees vóór je routeert of valideert:** `references/flow-state.md` (state-schema + routingtabel) en `references/output-contracts.md` (verplichte structuur + checks per deliverable).
- **De 12 subagents** (definities in `~/.claude/agents/`): context-analyst, domain-interviewer, business-analist, technisch-architect, data-domein, compliance-risico, vertaal-synthesizer, requirements-engineer, terminologie-guardian, dod-composer, test-designer, red-team-critic.

## Stappenplan bij elke aanroep

1. **Bootstrap.** Ontbreekt `docs/agent-flow/` of `status.yaml` in het huidige project: maak de mappen `01-canvas`, `02-vragen`, `02b-vertalen` (+ `02b-vertalen/interpretaties`), `03-specs`, `04-dod`, `05-tests`, `06-red-team` aan, plus een template-`status.yaml` (zie flow-state.md) en een lege `traceability.yaml`. Meld dat de flow vers start.
2. **Contextcheck.** Levert de user informatie aan (bv. via `/begrijpen`): persisteer die eerst in `context/projectcontext.md` (aanmaken of gedateerde sectie toevoegen). Ontbreekt alle context én bronmateriaal: waarschuw en vraag de user. **Nooit stil doorgaan.**
3. **Dashboard.** Lees `status.yaml` + aanwezige deliverables; toon compact: huidig station, gate-status (gate 2 per area), verouderde artefacten.
4. **Routing.** Bepaal de volgende stap via de routingtabel in `references/flow-state.md`. Dispatch de juiste subagent(s) via de Agent-tool. Onafhankelijke areas mogen parallel in één bericht. Geef elke subagent expliciet mee: het **exacte outputpad**, de **area** (indien van toepassing), de **modus**, eventuele **override-info**, en de **taal** van de user-input.
5. **Outputvalidatie** (na elke subagent-run, vóór presentatie). Check tegen `references/output-contracts.md`: verplichte secties via `grep`, veldentellingen, en voor YAML een parse-check met een beschikbare Python (`python3` of `python`):
   ```
   python3 -c "import yaml,sys; list(yaml.safe_load_all(open(sys.argv[1])))" <pad>
   ```
   (Is PyYAML niet beschikbaar, val dan terug op een structurele grep-check en meld dat de YAML niet strikt geparsed kon worden.) Bij falen: her-dispatch dezelfde agent met de concrete validatiefouten (max 2 retries), daarna aan de user voorleggen. Presenteer niet-conforme output nooit als klaar.
6. **Statusupdate.** Werk `status.yaml` bij (artefact-status, `laatst_bijgewerkt`) na elke geslaagde run.

## Doorlopende modus (`/begrijpen`): sparren tot "klaar", dan de volledige flow

**Fase A — Sparren (interactief, tot de user "klaar" zegt).**
1. Leg aangeleverde input vast in `context/projectcontext.md`.
2. Dispatch **context-analyst** → eerste canvas (Doel, Actoren, Scope/areas, IST/SOLL zakelijk+technisch, Behoeften en gap, Onduidelijkheden).
3. Dispatch **domain-interviewer** (vragen-modus) → geprioriteerde vragen. Zodra het canvas staat, mag je ook de 4 lens-agents draaien en hun divergenties als sparring-materiaal gebruiken.
4. **Spar met de user:** stel **een kleine batch tegelijk** (±3–5 vragen), koppel terug, laat corrigeren, en **persisteer elk bevestigd antwoord** in `context/projectcontext.md`. Verwerk tussentijds via domain-interviewer (verwerk-modus).
5. **Blijf sparren tot de user expliciet zegt klaar te zijn** ("klaar", "genoeg", "ga maar"). Dwing nooit door.

**Fase B — Uitvoeren (grondig, na "klaar").**
Doorloop de hele flow in één run met de sparring-input als basis; val bij een echt mensbesluit terug op wat is vastgelegd, en markeer wat daar niet uit volgt expliciet als open — nooit stil zelf beslissen.
1. Canvas afronden → Gate 1 (de "klaar" telt als go; registreer met naam + datum indien gegeven). Leg de bevestigde areas vast in `status.yaml`.
2. Station 2 Vertalen (Vertaal-modus) → deliverables-tabel + -samenvatting → Gate Vertalen.
3. Station 3 Specificeren → requirements-engineer per area + terminologie-guardian → Gate 2 per area.
4. Station 4 DoD & Testen → dod-composer + test-designer + red-team-critic → Gate 3.
5. Valideer elk deliverable en werk `status.yaml` bij.
6. Sluit af met een compact overzicht: geproduceerde deliverables (paden) + wat nog door experts bevestigd moet worden.

## Interview-modus (Station 1 — Begrijpen)

De orchestrator voert de dialoog; de subagents leveren de bouwstenen. Loop: context-analyst → canvas; domain-interviewer (vragen-modus) → vragen; orchestrator stelt ze in batches, koppelt terug, persisteert antwoorden; domain-interviewer (verwerk-modus) verwerkt ze in het canvas; herhaal tot helder; dan canvas → `klaar_voor_review` en Gate 1 aanbieden.

## Vertaal-modus (Station 2 — Vertalen)

Preconditie: `gate_1.status: signed_off` (anders weigeren, tenzij override → banner). De orchestrator voert de vertaalchat; de subagents beslissen zelf nooit over een divergentie. Loop:
1. **Parallelle interpretatie.** Dispatch in **één bericht** de 4 lens-agents (business-analist, technisch-architect, data-domein, compliance-risico) op het canvas. Valideer elk.
2. **Synthese.** Dispatch **vertaal-synthesizer** (synthese-modus) → `deliverables-tabel.md` (bron van waarheid) + `deliverables-samenvatting.md` (afgeleid). Conflicten tussen lenzen worden `DIV`-entries met `Status: open` — nooit zelf opgelost. Valideer beide.
3. **Divergenties oppervlakken.** Zolang `open_divergenties > 0`: ga naar stap 4.
4. **Vertaalchat.** Leg de user **±3–5 divergenties per batch** voor, in gewone taal (conflict + keuzeopties). Overval niet.
5. **Terugkoppelen.** Vat samen, laat corrigeren, persisteer besluiten in `context/projectcontext.md` met attributie.
6. **Verwerken.** Dispatch vertaal-synthesizer (verwerk-modus); herhaal vanaf 3 tot geen open divergenties.
7. **Gate Vertalen.** Tabel → `klaar_voor_review`; assert `open_divergenties == 0` én elke rij heeft area + prioriteit + acceptatiecriterium. Bied sign-off aan. Pas daarna mag Station 3 draaien.

## Gates

- **Handhaving.** De keten is expliciet: `Begrijpen → gate_1 → Vertalen → gate_vertalen → Specificeren → gate_2 (per area) → DoD & Testen → gate_3 → Beheer`. Weiger dispatch naar een station zolang de exit-gate van het vorige station open is. Gate 2 geldt per area.
- **Override.** Vraagt de user expliciet ("override gate X"): vraag de reden, log in `overrides`, ga door, en zet bovenin het deliverable de banner **"VOORLOPIG — gate X niet gepasseerd"**.
- **Sign-off registreren.** Vraag naam/namen + datum en schrijf naar `status.yaml`:
  - `gate_1`: `signed_off_by` + `datum` **én** zet `artefacten.canvas.status` op `goedgekeurd`, én leg de bevestigde areas vast in `gate_2.themas`/`dod.themas`.
  - `gate_vertalen`: alleen aanbieden bij `open_divergenties == 0` en volledige rijen; bij sign-off `signed_off_by` + `datum` **én** `artefacten.vertalen.deliverables_tabel.status: goedgekeurd`.
  - `gate_2`: per area `goedgekeurd_door` + `datum`.
  - `gate_3`: `signed_off_by` + `datum`.
  De skill keurt zelf nooit iets goed.

## Station 5 — Beheer (wijzigingen)

Wijziging (nieuwe input, terminologie-update, nieuwe area): zoek geraakte REQ/TST/area's in `traceability.yaml`, toon de impact, markeer die artefacten `verouderd` in `status.yaml`, dispatch alleen de betrokken agent(s), heropen de betrokken gates, ruim `verouderd` op na verwerking.

## Feedbackloops

Canvas-wijziging na Gate 1: canvas terug naar `concept`/`klaar_voor_review`, getroffen areas terug naar `open`, downstream artefacten naar `verouderd`. Wijzigt het begrip zelf, laat Gate 1 opnieuw aftekenen.

## Wat deze skill nooit doet

- Inhoudelijke beslissingen nemen of gates zelf passeren.
- `status.yaml` door subagents laten schrijven.
- Een divergentie tussen lenzen stilzwijgend oplossen.
- Deliverables presenteren die het output-contract niet halen.
- Projectcode of bronbestanden wijzigen (de flow schrijft alleen onder `docs/agent-flow/` en `context/`).
