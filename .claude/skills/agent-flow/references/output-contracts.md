# Output-contracten per deliverable

De orchestrator valideert elk agent-deliverable tegen dit contract voordat het aan mensen wordt getoond. Niet-conforme output gaat terug naar de agent met de concrete validatiefouten (max. 2 retries), daarna wordt het aan de user voorgelegd.

**Universele regels (alle Markdown-deliverables):**
- Elk deliverable eindigt met de sectie `## Open vragen en aannames` — check (de láátste H2-kop moet exact deze zijn, niet alleen ergens aanwezig): `[ "$(grep -E '^## ' <bestand> | tail -n1)" = '## Open vragen en aannames' ]`.
- Elk cijfer zonder geverifieerde bron draagt het label `(illustratief)`.
- YAML-deliverables (golden-dataset, traceability) zijn uitgezonderd van de staartregel; hun open punten landen in het begeleidende Markdown-deliverable.

---

## 1. Use Case Canvas (`docs/agent-flow/01-canvas/use-case-canvas.md`)

**Verplichte structuur:**
- Kop bevat `Status: concept` of `Status: klaar_voor_review`.
- H2's in volgorde: `## Doel`, `## Actoren`, `## Scope`, `## Huidige situatie (IST)`, `## Gewenste situatie (SOLL)`, `## Behoeften en gap`, `## Expliciete aannames`, `## Bekende cijfers`, `## Onduidelijkheden en ambiguïteiten`, `## Signaleringen`, `## Open vragen en aannames`.
- `Scope`-sectie bevat een tabel waarin alle 5 thema's voorkomen (opbouwsystematiek, partnerpensioen, indexatie, compensatie, beleggingsrisico).
- `Huidige situatie (IST)` en `Gewenste situatie (SOLL)` bevatten elk zowel een `Zakelijk:`- als een `Technisch:`-invalshoek.

**Automatische checks:**
- Elke H2-kop: `grep -q "^## Doel" <bestand>` (herhaal per kop, incl. `## Huidige situatie (IST)`, `## Gewenste situatie (SOLL)`, `## Behoeften en gap`).
- Statusregel: `grep -Eq "Status: (concept|klaar_voor_review)" <bestand>`.
- Thema-dekking: `grep -qi "opbouwsystematiek" <bestand>` (herhaal voor alle 5 thema's).
- IST/SOLL-invalshoeken: `grep -Eq "Zakelijk:" <bestand> && grep -Eq "Technisch:" <bestand>`.

---

## 2. Vragenlijst (`docs/agent-flow/02-vragen/vragen-<datum>.md`)

**Verplichte structuur:**
- Per thema met open punten een H2; elke vraag een eigen kop of genummerd item.
- Velden per vraag: `**Prioriteit:**` (hoog/middel/laag), `**Canvas-referentie:**`, `**Waarom ertoe doet:**`, en waar mogelijk gesloten antwoordopties.

**Automatische checks:**
- `grep -Eq "Prioriteit:.*\b(hoog|middel|laag)\b" <bestand>`
- Elke vraag heeft precies één `**Prioriteit:**`- en één `**Canvas-referentie:**`-veld, dus die tellingen moeten gelijk zijn: `[ "$(grep -c '\*\*Prioriteit:\*\*' <bestand>)" = "$(grep -c '\*\*Canvas-referentie:\*\*' <bestand>)" ]` (houd elk veld op een eigen regel).

---

## 3. Specs per thema (`docs/agent-flow/03-specs/specs-<thema>.md`)

**Verplichte structuur:**
- Per requirement een H3 met ID-patroon `### REQ-(OPB|PP|IDX|COMP|BEL|GEN)-[0-9]{3}`.
- Velden per requirement: `**Beschrijving:**`, `**Bron:**`, `**Acceptatiecriteria:**` (Given/When/Then), `**Prioriteit:**` (Must/Should/Could/Won't), `**Open vragen:**`.

**Automatische checks:**
- `grep -Ec "^### REQ-(OPB|PP|IDX|COMP|BEL|GEN)-[0-9]{3}"` == `grep -c "\*\*Bron:\*\*"` == `grep -c "\*\*Prioriteit:\*\*"`.
- Given/When/Then aanwezig: `grep -q "Given" <bestand> && grep -q "When" <bestand> && grep -q "Then" <bestand>`.
- Minimaal 1 requirement: teller > 0.

---

## 4. Ontologie-afwijkingen (`docs/agent-flow/03-specs/ontologie-afwijkingen.md`)

**Verplichte structuur per afwijking:**
- `**Term:**` / `**Getroffen requirements:**` (REQ-ids) / `**Classificatie:**` (exact / synoniem-verdacht / niet gevonden) / `**Voorstel:**` (`vervang door <ontologieterm>` of `uitbreiden ontologie — expertbesluit`) / `**Status:**` (open / opgelost).

**Automatische checks:**
- Aantal `**Term:**` == aantal `**Voorstel:**` == aantal `**Status:**`.
- Als er ≥1 afwijkingsentry is, moet elke Classificatie een geldige waarde hebben (bij nul afwijkingen — alle termen exact — is dit n.v.t. en slaagt de check): `[ "$(grep -c '\*\*Term:\*\*' <bestand>)" -eq 0 ] || grep -Eq "Classificatie:.*\b(exact|synoniem-verdacht|niet gevonden)\b" <bestand>`.

---

## 5. Definition of Done (`docs/agent-flow/04-dod/dod-<thema>.md`)

**Verplichte structuur:**
- 4 verplichte lagen als H2: `## Functioneel`, `## Traceerbaarheid`, `## Kwaliteit`, `## Demonstreerbaar`.
- Elk criterium refereert minimaal één REQ-id.

**Automatische checks:**
- Alle 4 koppen: `grep -q "^## Functioneel" <bestand>` (herhaal per laag).
- `grep -c "REQ-" <bestand>` > 0.

---

## 6. Validatietesten (`docs/agent-flow/05-tests/validatietesten.md`)

**Verplichte structuur:**
- IDs `TST-VAL-[0-9]{3}`, elk met gekoppelde REQ-ids.
- Dekking van minimaal: extractie-paginanummers, classificatie fonds-vs-benchmark, JSON-contract, regressie demo-modus.

**Automatische checks:**
- `grep -Eq "TST-VAL-[0-9]{3}" <bestand>` en `grep -q "REQ-" <bestand>`.
- Minimaal 4 unieke testgevallen: `[ "$(grep -Eo "TST-VAL-[0-9]{3}" <bestand> | sort -u | wc -l)" -ge 4 ]` (telt distinct ID's; `grep -Ec` zou regels tellen i.p.v. ID's).

---

## 7. Acceptatietesten (`docs/agent-flow/05-tests/acceptatietesten.md`)

**Verplichte structuur:**
- IDs `TST-ACC-[0-9]{3}`.
- De 4 metrics als tabel: recall materiële afwijkingen, precisie, citaat-juistheid, impact-overeenstemming — richtwaarden gelabeld "voorstel — deskundigen stellen vast".
- Eigen subsectie voor het asymmetrisch principe (gemiste hoog-impact afwijking weegt zwaarder dan vals alarm).

**Automatische checks:**
- `grep -Eq "TST-ACC-[0-9]{3}" <bestand>`.
- `grep -qi "asymmetri" <bestand>`.
- `grep -qi "recall" <bestand> && grep -qi "precisie" <bestand> && grep -qi "citaat" <bestand>`.

---

## 8. Golden dataset (`docs/agent-flow/05-tests/golden-dataset.yaml`)

**Verplichte structuur:**
- Parsebare YAML; per entry: `fonds`, `thema`, `verwachte_afwijking`, `impact` (Hoog/Middel/Laag/Geen), `bron`, `status: in_te_vullen_door_expert`.
- Minimaal 2–3 fondsen en alle vijf thema's vertegenwoordigd.

**Automatische checks:**
- `backend/.venv/bin/python -c "import yaml,sys; list(yaml.safe_load_all(open(sys.argv[1])))" <bestand>` slaagt (`safe_load_all` accepteert ook een multi-document YAML met `---`-scheidingen).
- `grep -q "fonds:" <bestand> && grep -q "verwachte_afwijking:" <bestand>` (deze grep-check borgt dat het niet leeg/alleen-commentaar is).

---

## 9. Red-team bevindingen (`docs/agent-flow/06-red-team/bevindingen-<datum>.md`)

**Verplichte structuur:**
- Per bevinding een H3 `### RTC-[0-9]{3} — <titel>` met velden: `**Categorie:**` (edge case / hallucinatierisico / tegenstrijdige bronnen / waar-staat-dat), `**Getroffen artefacten:**` (REQ/TST-ids of artefactpad), `**Scenario:**`, `**Ernst:**` (kritisch/hoog/middel/laag), `**Aanbeveling:**`.

**Automatische checks:**
- `grep -Eq "^### RTC-[0-9]{3}" <bestand>`.
- Aantal `RTC-`-koppen == aantal `**Ernst:**` == aantal `**Aanbeveling:**`.
- `grep -Eq "Ernst:.*\b(kritisch|hoog|middel|laag)\b" <bestand>`.
