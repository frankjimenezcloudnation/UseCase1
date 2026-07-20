# Output-contracten per deliverable (generiek)

De orchestrator valideert elk agent-deliverable tegen dit contract voordat het aan mensen wordt getoond. Niet-conforme output gaat terug naar de agent met de concrete fouten (max. 2 retries), daarna aan de user voorgelegd. In de checks is `<AREA>` een projectspecifieke code van 2–4 hoofdletters (bv. `AUTH`, `BILL`, `GEN`); gebruik het patroon `[A-Z]{2,4}`.

**Universele regels (alle Markdown-deliverables):**
- Elk deliverable eindigt met de sectie `## Open vragen en aannames` — check (láátste H2 moet exact dit zijn): `[ "$(grep -E '^## ' <bestand> | tail -n1)" = '## Open vragen en aannames' ]`.
- Elk cijfer zonder geverifieerde bron draagt het label `(illustratief)`.
- YAML-deliverables (golden-dataset, traceability) zijn uitgezonderd van de staartregel.

---

## 1. Use Case Canvas (`docs/agent-flow/01-canvas/use-case-canvas.md`)

**Structuur:** kop `Status: concept|klaar_voor_review`. H2's in volgorde: `## Doel`, `## Actoren`, `## Scope`, `## Huidige situatie (IST)`, `## Gewenste situatie (SOLL)`, `## Behoeften en gap`, `## Expliciete aannames`, `## Bekende cijfers`, `## Onduidelijkheden en ambiguïteiten`, `## Signaleringen`, `## Open vragen en aannames`. `Scope` bevat een tabel met de voorgestelde **areas** (code + naam + in/uit scope + motivatie). IST en SOLL bevatten elk een `Zakelijk:`- en een `Technisch:`-invalshoek.

**Checks:** `grep -q "^## Doel" <bestand>` per kop; `grep -Eq "Status: (concept|klaar_voor_review)" <bestand>`; `grep -Eq "Zakelijk:" <bestand> && grep -Eq "Technisch:" <bestand>`; Scope-tabel bevat ≥1 area-rij.

---

## 2. Vragenlijst (`docs/agent-flow/02-vragen/vragen-<datum>.md`)

**Structuur:** per area een H2; per vraag velden `**Prioriteit:**` (hoog/middel/laag), `**Dimensie:**` (IST/SOLL × zakelijk/technisch), `**Canvas-referentie:**`, `**Waarom ertoe doet:**`, en waar mogelijk gesloten antwoordopties.

**Checks:** `grep -Eq "Prioriteit:.*\b(hoog|middel|laag)\b" <bestand>`; `[ "$(grep -c '\*\*Prioriteit:\*\*' <bestand>)" = "$(grep -c '\*\*Canvas-referentie:\*\*' <bestand>)" ]`.

---

## 3. Specs per area (`docs/agent-flow/03-specs/specs-<area>.md`)

**Structuur:** per requirement een H3 `### REQ-<AREA>-[0-9]{3}` met velden `**Beschrijving:**`, `**Bron:**` (incl. DLV-id waar van toepassing), `**Acceptatiecriteria:**` (Given/When/Then), `**Prioriteit:**` (Must/Should/Could/Won't), `**Open vragen:**`.

**Checks:** `grep -Ec "^### REQ-[A-Z]{2,4}-[0-9]{3}"` == `grep -c "\*\*Bron:\*\*"` == `grep -c "\*\*Prioriteit:\*\*"`; `grep -q "Given" && grep -q "When" && grep -q "Then"`; teller > 0.

---

## 4. Terminologie-afwijkingen (`docs/agent-flow/03-specs/terminologie-afwijkingen.md`)

**Structuur per afwijking:** `**Term:**` / `**Getroffen requirements:**` / `**Classificatie:**` (exact / synoniem-verdacht / niet gevonden) / `**Voorstel:**` (`vervang door <term>` of `uitbreiden begrippenlijst — expertbesluit`) / `**Status:**` (open/opgelost).

**Checks:** aantal `**Term:**` == `**Voorstel:**` == `**Status:**`; bij ≥1 afwijking elke Classificatie geldig: `[ "$(grep -c '\*\*Term:\*\*' <bestand>)" -eq 0 ] || grep -Eq "Classificatie:.*\b(exact|synoniem-verdacht|niet gevonden)\b" <bestand>`. (Heeft het project geen begrippenlijst, dan mag dit deliverable "n.v.t. — geen glossary" bevatten met alleen de staartsectie.)

---

## 5. Definition of Done (`docs/agent-flow/04-dod/dod-<area>.md`)

**Structuur:** 4 H2-lagen `## Functioneel`, `## Traceerbaarheid`, `## Kwaliteit`, `## Demonstreerbaar`; elk criterium refereert ≥1 REQ-id.

**Checks:** alle 4 koppen aanwezig; `grep -c "REQ-" <bestand>` > 0.

---

## 6. Validatietesten (`docs/agent-flow/05-tests/validatietesten.md`)

**Structuur:** IDs `TST-VAL-[0-9]{3}`, elk met gekoppelde REQ-ids; dekking van de technische kernrisico's van het project (input/verwerking/output/regressie).

**Checks:** `grep -Eq "TST-VAL-[0-9]{3}"` en `grep -q "REQ-"`; ≥4 unieke ID's: `[ "$(grep -Eo "TST-VAL-[0-9]{3}" <bestand> | sort -u | wc -l)" -ge 4 ]`.

---

## 7. Acceptatietesten (`docs/agent-flow/05-tests/acceptatietesten.md`)

**Structuur:** IDs `TST-ACC-[0-9]{3}`; een set kwaliteitsmetrics als tabel met richtwaarden gelabeld "voorstel — experts stellen vast"; waar relevant een subsectie over het **asymmetrisch principe** (welke fout zwaarder weegt dan een andere in dit domein).

**Checks:** `grep -Eq "TST-ACC-[0-9]{3}"`; tabel met ≥1 metric aanwezig.

---

## 8. Golden/evaluatie-dataset (`docs/agent-flow/05-tests/golden-dataset.yaml`)

**Structuur:** parsebare YAML; per entry een testgeval met verwachte uitkomst, relevantie/impact, bron, en `status: in_te_vullen_door_expert`. Voldoende spreiding over de areas.

**Checks:** `python3 -c "import yaml,sys; list(yaml.safe_load_all(open(sys.argv[1])))" <bestand>` slaagt (of grep-fallback bij ontbrekende PyYAML); `grep -q "verwachte_uitkomst:" <bestand>`.

---

## 9. Red-team bevindingen (`docs/agent-flow/06-red-team/bevindingen-<datum>.md`)

**Structuur:** per bevinding H3 `### RTC-[0-9]{3} — <titel>` met `**Categorie:**`, `**Getroffen artefacten:**`, `**Scenario:**`, `**Ernst:**` (kritisch/hoog/middel/laag), `**Aanbeveling:**`.

**Checks:** `grep -Eq "^### RTC-[0-9]{3}"`; aantal `RTC-`-koppen == `**Ernst:**` == `**Aanbeveling:**`; `grep -Eq "Ernst:.*\b(kritisch|hoog|middel|laag)\b"`.

---

## 10. Lens-interpretaties (`docs/agent-flow/02b-vertalen/interpretaties/interpretatie-<lens>.md`)

**Structuur:** kop `# Interpretatie — <lens>`; `## Interpretaties`-tabel gekeyd op canvas-referentie, ≥1 datarij; staartregel.

**Checks:** `grep -q "^# Interpretatie" && grep -q "^## Interpretaties"`; `[ "$(grep -c '^|' <bestand>)" -ge 2 ]`.

---

## 11. Deliverables-tabel (`docs/agent-flow/02b-vertalen/deliverables-tabel.md`) — bron van waarheid

**Structuur:** kop `Status: concept|klaar_voor_review|goedgekeurd`. H2's: `## Deliverables`, `## Divergenties en openstaande vertaalkeuzes`, `## Signaleringen`, `## Open vragen en aannames`. Tabel met exact 10 kolommen: `business-req | afgestemde interpretatie | deliverable | technische vertaling | area | prioriteit | owner | afhankelijkheden | acceptatiecriterium | status`. `deliverable`-cel bevat `DLV-<AREA>-[0-9]{3}` (gevolgd door `— `); `prioriteit` ∈ MoSCoW; rij-`status` ∈ divergent/afgestemd/definitief. Elke `### DIV-NNN` heeft `**Betrokken deliverable(s):**`, `**Lenzen in conflict:**`, `**Type:**`, `**Standpunt per lens:**`, `**Vertaalkeuze voor de mens:**`, `**Status:**` (open/besloten), + bij besloten `**Besluit:**` met attributie.

**Checks:**
- Header: `grep -Eq '^\| *business-req *\|.*\| *status *\|' <bestand>`; kolomtelling 11 pipes: `[ "$(grep -m1 '^| *business-req' <bestand> | grep -o '|' | wc -l)" -eq 11 ]`.
- `prioriteit` ∈ MoSCoW: `grep -Eq "Must|Should|Could|Won't" <bestand>`.
- `DLV-`-ids uniek als **definiërend** voorkomen (id gevolgd door `— `): `[ "$(grep -Eo 'DLV-[A-Z]{2,4}-[0-9]{3} —' <bestand> | sort -u | wc -l)" = "$(grep -Eo 'DLV-[A-Z]{2,4}-[0-9]{3} —' <bestand> | wc -l)" ]` (bare id-verwijzingen in de afhankelijkheden-kolom tellen niet mee).
- DIV-veldgelijkheid: aantal `### DIV-` == aantal `**Status:**` binnen de divergentie-sectie.
- **Open-divergentietelling:** `open_divergenties` in `status.yaml` == `grep -c '\*\*Status:\*\* open'` binnen de divergentie-sectie (orchestrator berekent dit).
- Staartregel + `(illustratief)`-regel.

---

## 12. Deliverables-samenvatting (`docs/agent-flow/02b-vertalen/deliverables-samenvatting.md`) — mensen, afgeleid

**Structuur:** H2's `## In één oogopslag`, `## Per area`, `## Nog te besluiten`, `## Open vragen en aannames`. Citeert `deliverables-tabel.md` als bron. Kort & krachtig.

**Checks:** alle 4 H2's aanwezig; `grep -q "deliverables-tabel.md" <bestand>`; "Nog te besluiten" is leeg wanneer `open_divergenties == 0`; staartregel.
