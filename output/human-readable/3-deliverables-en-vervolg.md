# 3 — Deliverables en vervolg

## Wat is er opgeleverd?

| # | Opgeleverd | Wat het is | Status |
|---|---|---|---|
| 1 | Vaste testset (102 onderwerpen) | De set onderwerpen; 71 met een handmatig SPF-antwoord als ijkpunt | Klaar |
| 2 | Geanonimiseerde standaardbronnen | Standaarddocumenten zonder fondsspecifieke informatie | Klaar |
| 3 | PDC ↔ ontologie-koppeling | Welke ontologie-vraag hoort bij welk PDC-onderwerp (met betrouwbaarheid) | Klaar |
| 4 | Analyse-tool (fondskant) | Beantwoordt per onderwerp met bron + betrouwbaarheid | Klaar |
| 5 | Validatierapport | Vergelijkt de tool-antwoorden met het handwerk | Klaar |
| 6 | Lijst van 23 model-gaten | Waar het ontologiemodel het PDC-onderscheid niet vat | Klaar (voor review) |
| 7 | Slimmere "betekenis"-zoekmethode | Verhoogt de dekking | Nog te doen |
| 8 | Inbouw in de applicatie | Onderdeel-analyse via de webapplicatie | Nog te doen |
| 9 | Standaardkant-analyse (IG&H) | Bepaalt per onderwerp wat IG&H aanbiedt, uit PDC + standaardspecificatie + Qwik (meervoudige waarden) | Nog te doen |
| 10 | Vergelijking fonds ↔ IG&H-standaard | Zet per onderwerp de fondswaarde tegen de standaard-set af en benoemt de verschillen — de einddoelstelling | Nog te doen |

## Testscenario's per deliverable

Elke deliverable heeft een test die controleert of het werkt — hier in gewone taal (de technische Given/When/Then-versie staat in de bijgeleverde **voor-ai** map, bestand `deliverables-en-testscenarios.md`):

1. **Testset compleet & herbruikbaar** (bij deliverable 1). De vastgelegde testset bevat 102 onderwerpen (106 unieke vragen), elk met een ontologie-vraag; 71 hebben een SPF-ijkpunt. Opnieuw inladen van de bevroren testset geeft exact dezelfde lijst. → **Geslaagd**.
2. **Anonimisering lekt geen fondsnamen** (2). In de geanonimiseerde documenten staan geen fondsnamen meer; de originelen zijn ongewijzigd. → **Geslaagd** (0 fondsnamen).
3. **Koppeling verwijst alleen naar bestaande onderwerpen** (3). Elke gekoppelde ontologie-property bestaat echt en heeft een betrouwbaarheidsscore. → **Geslaagd** (102 gekoppeld, 0 verzonnen).
4. **De tool onderbouwt en verzint niet** (4). Bij een onderwerp dat in het reglement staat geeft de tool het juiste antwoord met een gecontroleerd citaat; bij een onderwerp dat er niet staat zegt ze eerlijk "niet gevonden". → **Geslaagd** (0 mislukkingen · 49 gecontroleerde citaten).
5. **De validatie telt eerlijk** (5). "Ja"-varianten tellen als "ja"; eenheid-hints als "jaren" worden niet als fout geteld. → **Geslaagd** (~64% op de 22 beantwoorde, toetsbare instanties).
6. **Model-gaten zijn onderbouwd** (6). Elk van de 23 gaten heeft een uitleg (bijvoorbeeld: "afkoopmoment" mist de keuze *emigratie*). → **Geslaagd** (23 gaten).
7. **Betekenis-zoekmethode verhoogt de dekking** (7). Met de slimmere zoekmethode worden meer onderwerpen beantwoord dan de huidige 40 van 133, zonder verlies van betrouwbaarheid. → **Nog te draaien**.
8. **Onderdeel-analyse via de applicatie** (8). Via de webapplicatie levert een analyse hetzelfde resultaat als de losse tool en toont het in de interface. → **Nog te draaien**.
9. **Standaardkant klopt en is meervoudig** (9). Voor een onderwerp waar IG&H meerdere opties toestaat (bv. type regeling) levert de standaardkant alle toegestane waarden, uit de juiste bron (PDC vóór specificatie vóór Qwik). → **Nog te draaien**.
10. **Vergelijking benoemt de juiste verschillen** (10). Voor een onderwerp waar de fondswaarde binnen de standaard valt → "past binnen standaard"; valt ze erbuiten → "echte afwijking". → **Nog te draaien**.

Kort: de opgeleverde onderdelen (1 t/m 6) zijn **geslaagd**; 7 t/m 10 staan nog open omdat die onderdelen nog gebouwd worden.

## Wat vragen we van de deskundigen?

De tool bereidt voor; deze punten vragen een menselijk oordeel. De volledige, concrete lijsten staan in [4 — Reviewlijst voor deskundigen](4-reviewlijst.md):

1. **De 8 afwijkende antwoorden.** Klopt het handwerk, of heeft de tool een goed punt? Voorbeeld: is er bij SPF nu wel of geen minimum pensioengevend inkomen ("ten minste nihil")?
2. **De 7 gevallen "buiten format".** Hier past het gevonden antwoord niet netjes in de voorgeschreven keuzelijst — mogelijk moet het ontologiemodel worden aangepast.
3. **De 23 model-gaten.** Per gat: moet het ontologiemodel worden uitgebreid, of is het onderscheid overbodig?
4. **De streefwaarden.** Welke accuraatheid en dekking vinden we "goed genoeg"? (Nu: ~64% op de beantwoorde, toetsbare instanties.)

## Vervolgstappen (voorstel)

1. **Dekking verhogen** — de slimmere zoekmethode (betekenis i.p.v. trefwoorden) aanzetten; die staat al in de codebase klaar.
2. **Meer bronnen** — ook inrichtings-/implementatiedocumenten meenemen voor onderwerpen die niet in het reglement staan.
3. **Standaardkant + vergelijking bouwen** — de IG&H-standaard per onderwerp bepalen en fonds vs. standaard vergelijken (de einddoelstelling).
4. **Expertreview** van de punten hierboven verwerken.
5. **Ontologiemodel bijwerken** met de bevindingen.
6. **Opschalen** van 102 naar meer onderwerpen, en **inbouwen** in de applicatie voor dagelijks gebruik.

Verder lezen: [samenvatting en resultaten](1-samenvatting-en-resultaten.md) · [aanpak en bouw](2-aanpak-en-bouw.md) · [reviewlijst](4-reviewlijst.md).
