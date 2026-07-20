---
name: agent-flow
description: "Orchestreert de WTP agent-flow voor Use Case 1: 5 stations, 12 agents, 4 human gates — van projectcontext naar Use Case Canvas, een geconsolideerde deliverables-tabel, specificaties, Definition of Done en acceptatietesten. Gebruik bij /agent-flow of bij vragen over canvas, vertaling, deliverables, specs, DoD, testen, golden dataset of gates."
---

# Agent-flow — orchestrator (Use Case 1)

Deze skill stuurt de agent-flow aan tijdens het verfijnen van de WTP-tool. De skill voert **zelf geen inhoudelijk werk** uit: hij bepaalt de flow-positie, dispatcht subagents, handhaaft gates en valideert output.

**Ingangen (alle drie activeren deze ene skill):**
- **`/begrijpen`** — de hoofdingang: één doorlopende sessie waarin je met het agent-team spart (zij stellen vragen, jij antwoordt en legt uit) tot jij zegt dat je **klaar** bent; daarna doorlopen de agents de hele flow grondig. Zie *Doorlopende modus*.
- **`/vertalen`** — spring direct naar Station 2 (Vertalen), als het canvas al door Gate 1 is.
- **`/agent-flow`** — station-voor-station orkestratie met een gate-pauze na elk station, voor wie stap voor stap meer controle wil.

## Stations, agents en gates op een rij

| Station | Naam | Agents | Exit-gate |
|---|---|---|---|
| 1 | Begrijpen | context-analyst, domain-interviewer | `gate_1` |
| 2 | Vertalen | business-analist, technisch-architect, data-ontologie, compliance-risico, vertaal-synthesizer | `gate_vertalen` |
| 3 | Specificeren | requirements-engineer, ontology-guardian | `gate_2` (per thema) |
| 4 | DoD & Testen | dod-composer, test-designer, red-team-critic | `gate_3` |
| 5 | Beheer | — (traceability + gerichte her-runs) | — |

**5 stations · 12 agents · 4 human gates.** Zie `references/flow-state.md` voor het volledige status.yaml-schema en de routingtabel.

## Kernprincipes

- **Eén doorlopende sessie (`/begrijpen`).** De user spart met het team tot die **"klaar"** zegt; daarna voeren de agents de hele flow grondig uit (Begrijpen → Vertalen → Specificeren → DoD & Testen). De "klaar" van de user is het go-signaal — de orchestrator dwingt nooit door, en verzint nooit een beslissing die de user of de deskundigen toekomt. Zie *Doorlopende modus*.
- **Doel van Station 1: gedeeld begrip.** Zowel de agents als de user moeten de behoefte scherp krijgen: de **huidige situatie (IST)** en de **gewenste situatie (SOLL)**, telkens in **technische én zakelijke** termen. Het canvas legt dat vast; de interviewdialoog zorgt dat óók de user het scherp krijgt.
- **Doel van Station 2: business ↔ techniek vertalen.** Een team van 4 lens-agents interpreteert het canvas onafhankelijk (business, techniek, data/ontologie, compliance/risico); de vertaal-synthesizer voegt dat samen tot één deliverables-tabel en maakt conflicten tussen lenzen expliciet zichtbaar als divergenties — nooit stilzwijgend opgelost.
- **Interviewend/vertalend, niet eenmalig.** Station 1 én Station 2 verlopen als een interactieve dialoog: de orchestrator bevraagt de user in korte, gerichte rondes en koppelt steeds terug ("dus als ik je goed begrijp…"). Subagents draaien autonoom en praten niet zelf met de user — elke live dialoog loopt dus via de orchestrator (zie *Interview-modus* en *Vertaal-modus*).
- **De mens beslist, de agent bereidt voor.** Gates worden alleen door mensen gepasseerd; deze skill registreert de beslissing, neemt hem nooit zelf. Bij Station 2 geldt dit het sterkst: een divergentie tussen lenzen wordt **nooit** door een agent opgelost.
- **Bron van waarheid:** `docs/agent-flow/status.yaml` — **alleen deze skill schrijft dat bestand**, subagents nooit.
- **Lees vóór je routeert of valideert:** `references/flow-state.md` (state-schema + routingtabel) en `references/output-contracts.md` (verplichte structuur + checks per deliverable).
- **De 12 subagents** (definities in `.claude/agents/`): context-analyst, domain-interviewer, business-analist, technisch-architect, data-ontologie, compliance-risico, vertaal-synthesizer, requirements-engineer, ontology-guardian, dod-composer, test-designer, red-team-critic.

## Stappenplan bij elke aanroep

1. **Bootstrap.** Ontbreekt `docs/agent-flow/` of `status.yaml`: maak de mappen `01-canvas`, `02-vragen`, `02b-vertalen` (+ `02b-vertalen/interpretaties`), `03-specs`, `04-dod`, `05-tests`, `06-red-team` aan, een template-`status.yaml` en een lege `traceability.yaml`, en meld dat de flow vers start.
2. **Contextcheck.** Levert de user informatie aan (bv. via `/begrijpen`, in de prompt of als bijlage): persisteer die eerst in `context/projectcontext.md` (aanmaken, of een gedateerde sectie toevoegen) vóór je agents dispatcht — dat is het ankerdocument dat alle agents lezen. Ontbreken daarna nog steeds `context/projectcontext.md` én `context/implementatieplan-agent-flow.md`: waarschuw expliciet en vraag de user — doorgaan op corpus-only, of eerst het document plaatsen? Geef de keuze mee in de dispatch-prompt. **Nooit stil doorgaan.**
3. **Dashboard.** Lees `status.yaml` + de aanwezige deliverables; toon compact: huidig station, gate-status (gate 2 per thema), verouderde artefacten.
4. **Routing.** Bepaal de volgende stap via de routingtabel in `references/flow-state.md`. Leg de user in één zin voor wat er gaat gebeuren en dispatch dan de juiste subagent(s) via de Agent-tool. Onafhankelijke thema's (Station 2/3) mogen parallel in één bericht. Geef elke subagent in de dispatch-prompt expliciet mee: het **exacte outputpad**, het **thema** (indien van toepassing), de **modus** (domain-interviewer), eventuele **override-informatie**, en de **taal** van de user-input.
5. **Outputvalidatie** (na elke subagent-run, vóór presentatie aan de user). Check het geschreven deliverable tegen `references/output-contracts.md`: verplichte secties via `grep`, veldentellingen, en voor YAML een parse-check:
   ```
   backend/.venv/bin/python -c "import yaml,sys; list(yaml.safe_load_all(open(sys.argv[1])))" <pad>
   ```
   Bij falen: her-dispatch dezelfde agent met de concrete validatiefouten (max 2 retries), daarna aan de user voorleggen. Presenteer niet-conforme output nooit als klaar.
6. **Statusupdate.** Werk `status.yaml` bij (artefact-status, `laatst_bijgewerkt`) na elke geslaagde run.

## Doorlopende modus (`/begrijpen`): sparren tot "klaar", dan de volledige flow

Dit is de hoofdmanier om de flow te draaien: één doorlopende sessie. De orchestrator voert het gesprek; de subagents leveren de vragen en bouwstenen (zij praten nooit zelf met de user).

**Fase A — Sparren (interactief, tot de user "klaar" zegt).**
1. Leg de aangeleverde input vast in `context/projectcontext.md` (aanmaken of gedateerde sectie toevoegen).
2. Dispatch **context-analyst** → eerste canvas (Doel, Actoren, Scope, IST/SOLL zakelijk+technisch, Behoeften en gap, Onduidelijkheden).
3. Dispatch **domain-interviewer** (vragen-modus) → geprioriteerde vragen (Dimensie IST/SOLL × zakelijk/technisch). Zodra het canvas staat, mag je ook de 4 lens-agents draaien en hun divergenties als extra sparring-materiaal gebruiken.
4. **Spar met de user:** stel **een kleine batch tegelijk** (±3–5 vragen), in gewone taal; koppel na elke batch terug ("dus als ik je goed begrijp…"), laat corrigeren, en **persisteer elk bevestigd antwoord** in `context/projectcontext.md` met attributie. Verwerk tussentijds via domain-interviewer (verwerk-modus).
5. **Blijf sparren tot de user expliciet zegt klaar te zijn** ("klaar", "genoeg", "ga maar"). Overval de user niet en dwing nooit door; als de vragen op lijken, vraag: "Heb je nog aanvullingen, of gaan de agents aan de slag?"

**Fase B — Uitvoeren (grondig, na "klaar").**
Zodra de user klaar is, doorloop je de hele flow in één run met de sparring-input als basis. Val bij een echt mensbesluit terug op wat in Fase A is vastgelegd; kun je iets daar niet uit oplossen, leg het dan kort voor of markeer het expliciet als open — nooit stil zelf beslissen.
1. **Station 1 afronden** → canvas `klaar_voor_review`; Gate 1 (de "klaar" van de user telt als go-signaal; registreer met naam + datum als die gegeven zijn, anders noteer "akkoord user, <datum>").
2. **Station 2 Vertalen** → volg *Vertaal-modus*: 4 lenzen parallel → vertaal-synthesizer → deliverables-tabel + -samenvatting. Los divergenties op uit de vastgelegde sparring-context; een divergentie die daar niet uit volgt, leg je kort voor of laat je als open DIV staan. → Gate Vertalen.
3. **Station 3 Specificeren** → requirements-engineer per thema (parallel) + ontology-guardian → Gate 2 per thema.
4. **Station 4 DoD & Testen** → dod-composer + test-designer + red-team-critic → Gate 3. De golden-dataset-grondwaarheden kunnen alleen deskundigen vaststellen: lever het skelet + voorstellen en markeer die expliciet als "nog te bevestigen door deskundigen" — presenteer ze nooit als vastgesteld.
5. **Valideer** elk deliverable tegen `references/output-contracts.md` (max 2 retries) en werk `status.yaml` bij.
6. **Sluit af** met een compact overzicht: alle geproduceerde deliverables (paden) + een expliciete lijst van wat nog door deskundigen bevestigd moet worden.

De *Interview-modus* en *Vertaal-modus* hieronder zijn de sub-procedures die deze doorlopende modus gebruikt; `/vertalen` en `/agent-flow` geven toegang tot dezelfde stappen station-voor-station.

## Interview-modus (Station 1 — Begrijpen)

De orchestrator voert de interview-dialoog; de subagents leveren de bouwstenen. Loop:

1. **Startbegrip.** Dispatch de **context-analyst** → eerste canvas-concept met o.a. `Huidige situatie (IST)`, `Gewenste situatie (SOLL)` (elk zakelijk + technisch) en `Behoeften en gap`. Wat nog onbekend is, staat in `Onduidelijkheden en ambiguïteiten`.
2. **Vragen voorbereiden.** Dispatch de **domain-interviewer** (vragen-modus) → een geprioriteerde vragenlijst, geordend langs IST vs. SOLL en zakelijk vs. technisch.
3. **Interviewen (orchestrator ↔ user).** Stel de user **een kleine batch tegelijk** (±3–5 vragen), in gewone taal, en maak expliciet of het over de huidige of de gewenste situatie gaat en of het zakelijk of technisch is. Overval de user niet met de hele lijst.
4. **Terugkoppelen.** Vat na elke batch kort samen wat je begrepen hebt en laat de user corrigeren — zo groeit óók het begrip van de user. Persisteer bevestigde antwoorden in `context/projectcontext.md`.
5. **Verwerken.** Dispatch de **domain-interviewer** (verwerk-modus) om de antwoorden met attributie in het canvas te verwerken; herhaal vanaf stap 3 tot IST/SOLL helder zijn en alleen nog echte expertvragen open staan.
6. **Gate 1.** Zet de canvas op `klaar_voor_review` en bied Gate 1 aan (sign-off door de deskundigen).

## Vertaal-modus (Station 2 — Vertalen)

Preconditie: `gate_1.status: signed_off`. Weiger anders — tenzij expliciete override (banner "VOORLOPIG — gate 1 niet gepasseerd"). De orchestrator voert de vertaalchat; de subagents leveren de bouwstenen en beslissen zelf nooit over een divergentie. Loop:

1. **Parallelle interpretatie.** Dispatch in **één bericht** de 4 lens-agents — business-analist, technisch-architect, data-ontologie, compliance-risico — elk op het canvas + projectcontext. Valideer elk deliverable tegen `references/output-contracts.md` vóór je verdergaat.
2. **Synthese.** Dispatch de **vertaal-synthesizer** (synthese-modus) → leest de 4 interpretaties + canvas, schrijft in één run `deliverables-tabel.md` (bron van waarheid) én `deliverables-samenvatting.md` (afgeleid). Elk conflict tussen lenzen wordt een `DIV`-entry met `Status: open` — de synthesizer beslist nooit zelf. Valideer beide documenten.
3. **Divergenties oppervlakken.** Lees `open_divergenties` (afgeleid uit de sectie "Divergenties en openstaande vertaalkeuzes"). Zolang dit > 0: ga naar stap 4.
4. **Vertaalchat (orchestrator ↔ user).** Leg de user **een kleine batch tegelijk** (±3–5 divergenties) voor, in gewone zakelijke taal: benoem het conflict tussen de lenzen en de concrete keuzeopties. Overval niet met de hele lijst.
5. **Terugkoppelen.** Vat na elke batch samen ("dus als ik je goed begrijp, kiezen we voor…") en laat corrigeren. Recente input wint. Persisteer bevestigde besluiten in `context/projectcontext.md` met attributie (`besloten door <naam>, <datum>`).
6. **Verwerken.** Dispatch de **vertaal-synthesizer** (verwerk-modus) om de besluiten te verwerken: DIV `open → besloten` (+ Besluit + attributie), rijstatus `divergent → afgestemd`. Valideer. Herhaal vanaf stap 3 tot er **geen** open divergenties meer zijn.
7. **Gate Vertalen.** Zet de tabel op `klaar_voor_review`; assert `open_divergenties == 0` én elke rij heeft thema + prioriteit + acceptatiecriterium. Bied sign-off aan (naam + datum). Pas daarna mag Station 3 (Specificeren) draaien.

## Gates

- **Handhaving.** De keten is expliciet, niet een rekenregel op stationnummers: `Begrijpen → gate_1 → Vertalen → gate_vertalen → Specificeren → gate_2 (per thema) → DoD & Testen → gate_3 → Beheer`. Weiger dispatch naar een station zolang de exit-gate van het vorige station open is. Gate 2 geldt per thema: een goedgekeurd thema mag door naar Station 4 terwijl een ander nog in review is.
- **Override.** Vraagt de user expliciet ("override gate X"): vraag de reden, log in `overrides` in `status.yaml`, ga door, en zorg dat het deliverable bovenin de banner **"VOORLOPIG — gate X niet gepasseerd"** krijgt.
- **Sign-off registreren.** Vraag naam/namen + datum en schrijf naar `status.yaml`:
  - `gate_1`: `signed_off_by` + `datum` **én** zet `artefacten.canvas.status` op `goedgekeurd` (zodat de canvas-routingrij niet blijft matchen).
  - `gate_vertalen`: alleen aanbieden als `open_divergenties == 0` en elke rij thema+prioriteit+acceptatiecriterium heeft; bij sign-off `signed_off_by` + `datum` **én** zet `artefacten.vertalen.deliverables_tabel.status` op `goedgekeurd` (elke rijstatus mag dan naar `definitief`).
  - `gate_2`: per thema `goedgekeurd_door` + `datum`.
  - `gate_3`: `signed_off_by` + `datum`.
  De skill keurt zelf nooit iets goed.
- **Gate 3 vereist:** golden dataset door de deskundigen gevuld (geen `in_te_vullen_door_expert`-statussen meer) én streefwaarden vastgesteld.

## Station 5 — Beheer (wijzigingen, na Gate 3 of tussentijds)

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
