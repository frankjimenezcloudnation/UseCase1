# Projectcontext — WTP agent-flow (Use Case 1)

> **Let op (bij levering in het documentatiepakket):** paden naar `backend/`, `frontend/`, `.xlsx`-bronnen, `.json`-outputs en `docs/bronnen_geanonimiseerd/` verwijzen naar de **bron-repository** en zitten niet in dit pakket. In het pakket meegeleverd zijn de Markdown-documenten (human-readable set + voor-ai set).

## Aanvullende input — 2026-07-20

**Modus:** corpus-only. De gebruiker heeft (nog) geen aparte projectbeschrijving of implementatieplan aangeleverd; de agents werken op de brondocumenten die in `UseCase1/` aanwezig zijn. Deze sectie is het ankerdocument; nieuwe input wordt hieronder gedateerd toegevoegd (nooit overschrijven, recente input wint).

**Aanroep:** `/begrijpen` vanuit de `cloudnation`-map (wrapper-command dat `UseCase1/` als projectbasis gebruikt).

### Beschikbaar corpus in `UseCase1/`
- `2023-12-07 DPD – Transitieplan versie 1.0.pdf`
- `2025 Implementatieplan WTP SPF v1.0.pdf`
- `2025.09.15 Transitieplan Wtp DPF V1.3.pdf`
- `2025.12.18 Abtn 2026 SPF DEF.pdf`
- `AnalyseQwik_FPR_202508.docx`
- `Bijlage g- FPR Operating Manual APS-AIM v1.0 SPF.pdf`
- `OntologySnapshot.xlsx`
- `Overzicht_PDC_Beroepse_202600611.xlsx`
- `PRESENTATIE.md`
- `SPF Flexibele Premieregeling 2026.1_def.pdf`
- `Specificatie Flexibele premieovereenkomst 0.08.docx`
- Codebase: `backend/` (FastAPI) en `frontend/` (Vite/React), o.a. `backend/app/services/ontology.py` en `extraction.py`.

### Nog te bevestigen door de gebruiker/deskundigen
- Of één specifiek document leidend is (bijv. de Specificatie Flexibele premieovereenkomst of het Implementatieplan WTP).
- De concrete scope/behoefte van de WTP-tool die verfijnd wordt (IST/SOLL) — dit moet in de sparring scherp worden.

## EINDDOEL (verduidelijkt door user — 2026-07-20, leidend)

De kern-use-case is een **vergelijking tussen het fonds en de IG&H-standaard**, per ontologie-onderwerp:
1. **Fondskant:** bepaal per ontologie-onderwerp de waarde van het fonds, UITSLUITEND uit de fondsspecifieke bestanden (FPR, ABTN, implementatieplan, operating manual).
2. **IG&H-standaardkant:** bepaal per onderwerp wat de IG&H-standaard aanbiedt, uit `Specificatie Flexibele premieovereenkomst` + `AnalyseQwik` (geanonimiseerd).
3. **Vergelijk** beide (beide op de ontologie gemapt) en benoem de **verschillen** tussen fonds en standaard.

**Cruciale nuance — multipliciteit (beide kanten):** de IG&H-standaard is een "menu" met per onderwerp vaak **meerdere** mogelijke waarden (breder gespecialiseerd). Maar **ook een fonds kan meerdere waarden** per onderwerp hebben — bv. `basis premievrijstelling` kan op meerdere manieren bepaald zijn (zie PDC). Beide kanten zijn dus **sets van waarden**. Voorbeeld waar de standaard breder is: `type regeling` → IG&H = {basisregeling, excedentregeling, …}, fonds = doorgaans één daarvan.

**Bronnen + prioriteit (leidend bij tegenspraak; hoger wint):**
- **Fondskant (alleen fondsspecifiek):** 1. reglement (FPR) · 2. ABTN · 3. FPR Operating Manual · 4. implementatieplan · 5. transitieplan. Bij extra aangeleverde documenten: laat de **gebruiker** de prioriteit bepalen. NB: voor SPF zijn de aanwezige transitieplannen van andere fondsen (DPF/DPD) → niet gebruiken.
- **IG&H-standaardkant:** 1. **PDC Beroepse** — kolom D `IG&H Standaard Horizon` (meest recent/correct) · 2. `Specificatie Flexibele premieovereenkomst` · 3. `AnalyseQwik`. De **PDC mag uitsluitend voor de standaardkant** worden gebruikt, NOOIT voor de fondskant.

**Vergelijkingslogica (set-vs-set):** fonds ⊆ standaard → *past binnen standaard* (geen afwijking); fonds bevat waarde(n) buiten standaard → *echte afwijking* (maatwerk/niet ondersteund); standaard heeft extra opties → *standaard biedt meer* (informatief). Plus dekking-signalen (niet in fonds / niet in standaard gevonden).

**Status t.o.v. dit einddoel:** de fondskant-engine bestaat (`onderdeel_analysis.py`, single-value). NOG TE DOEN: (a) fondskant meervoudige waarden + docprioriteit laten teruggeven; (b) **standaardkant-analyse** (PDC-kolom D + Specificatie + AnalyseQwik, meervoudig); (c) **vergelijkingsstap** fonds↔standaard als einddeliverable.

## Aanvullende input — 2026-07-20 (herijking scope; recente input wint)

De gebruiker herijkt de opzet. De kern-use-case is **niet** een generieke documentvergelijking, maar een **volledige, geautomatiseerde analyse van alle onderwerpen in `OntologySnapshot.xlsx`, tabblad `PROPERTY`** (~2611 rijen = ~2600 onderwerpen), toegepast op fondsdocumenten.

**Geverifieerde datastructuur — PROPERTY-tab (2611 × 28), kolomkoppen in rij 1:**
- `G = Name` — naam van het onderwerp (bv. `Aanlevering_premies`, `Leidende_premie`, `Aansluiting_pensioenfonds`).
- `H = Definition`, `I = Clarification`, `J = Goal`, `K = Source`, `L = Type` (bv. `enumeration`) — toelichtende info per onderwerp.
- `M = Multiplicity` (bv. `0..n`).
- `N = Question` — de letterlijk te beantwoorden vraag per onderwerp (bv. "Welke premies worden aangeleverd?").
- `O = Category` — categorie; samen met `C = ClassExternalId` / `D = SubClassExternalId` bruikbaar om onderwerpen te groeperen en batchgewijs sneller te beantwoorden.
- `P = DomainValue` — verwachte antwoordwaarden, comma-gescheiden (bv. `Reguliere_premie,Bijspaarpremie,Anders`).

**Gewenste output per onderwerp:** het antwoord op de vraag (`N`), bij voorkeur gemapt op één van de toegestane waarden uit `P`. Lukt mapping op `P` niet, dan alsnog het vrije antwoord op de vraag/waarde teruggeven. Categorieën gebruiken om efficiënter (batchgewijs) tot antwoorden te komen.

**Handmatige referentie-uitwerking:** `Overzicht_PDC_Beroepse_202600611.xlsx`, tab `Product inrichting` (312 rijen). Rij 1: kolommen `D t/m I` = fondsen (`IG&H Standaard Horizon`, `SPH&P`, `SPF`, `SPD`, `SPV`, `SPOA`). Per rij: `B = onderwerp`, `C = kandidaatwaarde`, per fonds (D–I) een markering of die waarde van toepassing is; `J` = productcode-referentie. Dit is met de hand gedaan voor een deel van de onderwerpen en een aantal fondsen — de tool moet dit schalen naar alle ~2600 onderwerpen.

### Nog te bevestigen (herijking)
- Voor welk(e) **fonds(en)** moet de tool eerst draaien? Corpus in de repo lijkt vooral **SPF** (FPR SPF, ABTN SPF, Transitieplan). Welke documenten horen bij welk fonds?
- Gewenste **outputvorm** (per fonds × onderwerp: DomainValue + fallback vrije tekst; met **bronverwijzing/provenance** en **confidence** voor verificatie door deskundigen?).
- Categorisering: primair via `O = Category` of via de klasse-hiërarchie (`C`/`D`)?

### Bevestigde beslissingen — 2026-07-20 (door user)
- **Testscope:** alleen fonds **SPF**; een steekproef van **~200 onderwerpen** uit de PROPERTY-tab (kleiner = makkelijker controleerbaar).
- **Vaste selectie:** de ~200 onderwerpen worden **één keer** gekozen en daarna **elke testronde hergebruikt** (reproduceerbaar; vaste seed / vastgelegde lijst).
- **PDC Beroepse is GEEN informatiebron** voor de analyse. Het model mag `Overzicht_PDC_Beroepse` niet als input gebruiken; het dient alleen als referentie/validatie (en eventueel om de testselectie te kiezen).
- **Anonimiseren:** `AnalyseQwik_FPR_202508.docx` én `Specificatie Flexibele premieovereenkomst 0.08.docx` moeten worden **geanonimiseerd** — die bevatten al fondsspecifiek ingevulde informatie. Doel: de tool moet bruikbaar zijn voor **nieuwe fondsen** die hun reglement tegen "onze standaard" willen laten analyseren. (Nog te detailleren: wat telt precies als fondsspecifiek en moet worden weggehaald.)
- **Outputvorm per onderwerp (testfase):**
  1. één gekozen **DomainValue uit `P`** (bij enumeration),
  2. een **bronverwijzing** (document + vindplaats),
  3. een **confidence**,
  4. tijdens het testen óók een **vrij-tekst antwoord** dat laat zien hóé de tool het onderwerp analyseert.
- **Niet-enumeration onderwerpen:** beantwoord volgens het aangegeven **`Type` (kolom L)** / format (vrije tekst, getal, datum, enz.). **Markeer expliciet** wanneer het antwoord niet binnen de enumeration of het aangegeven format past — dat is signaal om het ontologiemodel eventueel aan te passen.
- **"Klaar" = de beschreven steekproef** volledig doorlopen (SPF, ~200 onderwerpen).

### Koppelingsanalyse PDC ↔ ontologie (geverifieerd 2026-07-20)
- PDC `Product inrichting`: **152 unieke onderwerpen** (kolom B), 12 categorieën.
- Direct 1:1 op PROPERTY-naam koppelbaar: **16**. Gedeeltelijke/fuzzy overlap: ~69. Geen match: 67.
- Kolom `J` (productcode/notitie) mapt **niet** op PROPERTY-`ExternalId` (0 exacte matches; deels vrije tekst).
- Oorzaak: PDC gebruikt business-/CLASS-namen; PROPERTY gebruikt specifieke propertynamen (bv. PDC `Lumpsum_uitkering` ↔ PROPERTY `Indicatie_lumpsum`; PDC `Vervroeging`/`Deeltijdpensioen` zijn CLASSes, geen properties). Schone 1:1-koppeling is daardoor beperkt.

### Ontwerpeisen tool — 2026-07-20 (door user)
- **R1 — Klasse-groepering (één onderwerp → meerdere vragen).** Een business-/PDC-onderwerp komt vaak overeen met een hele ontologie-**CLASS**; de tool behandelt dan **alle PROPERTY-vragen binnen die class** samen. Voorbeeld: PDC "Voorportaal / indicatie voorportaal" = CLASS `Voorportaal` (`25_01.03.42.000`) met ~13 PROPERTY-vragen (o.a. `Indicatie_voorportaal_toestaan`, `Soort_voorportaal`, `Voorportaal_ivm_wachttijd/_drempelperiode/_jonger_dan_toetredingsleeftijd`, `Dekking_voorportaal`, `Risicodekking_gedurende_voorportaal`). Groeperen via **kolom C (ClassExternalId) → CLASS.Name** (en `D`/SubClass). Dit realiseert tevens het eerder genoemde "categorieën gebruiken om efficiënter te antwoorden".
- **R2 — Contextverrijking van generieke/contextafhankelijke vragen.** Sommige PROPERTY-vragen verwijzen impliciet naar het onderwerp waar ze onder vallen (bv. `Afrondingsmethode_datum` → "Hoe wordt de datum afgerond?"). De tool moet het **bovenliggende onderwerp uit de hiërarchie (kolom C/D → CLASS/SUBCLASS.Name)** aan de vraag toevoegen, zodat gericht wordt gezocht (bv. afronding van *toetredingsdatum* vs *standaard pensioendatum*). Ontbreekt de door de PDC verwachte granulariteit in de ontologie, **markeer dat expliciet** als granulariteitsgat (input voor aanpassing van het ontologiemodel).

### Standaard-testset vastgelegd — 2026-07-20 (door user goedgekeurd)
De semantische mapping (PDC Beroepse `Product inrichting` ↔ OntologySnapshot `PROPERTY`, via de klasse-hiërarchie) is de **vaste standaard-testset**. Vastgelegd in `docs/testset/golden-testset.json` (machine-leesbaar) en `docs/testset/golden-testset.md` (overzicht).
- **102 PDC-onderwerpen** gemapt → **106 unieke ontologie-PROPERTY-vragen** (in een analyse-run 133 vraag-instanties). Confidence: high 40, medium 45, low 17.
- **23** onderwerpen dragen een **`granularity_gap`-markering** binnen de 102-testset (gekoppeld, maar ontologie vat het PDC-onderscheid niet volledig; over alle 152 PDC-onderwerpen waren het er 36) → ontologie-verbeterlijst voor deskundigen.
- Van de 152 PDC-onderwerpen: **102 gemapt, 48 `no_match`, 2 zonder duidelijke uitkomst** (102 + 48 + 2 = 152). No_match is deels echte lacune, deels kandidaat-scope-fout — later met gerichte her-run te verbeteren.
- **Scope/DoD bijgesteld (recente input wint):** de eerder genoemde "~200 onderwerpen"-testscope (regels hierboven) is bijgesteld naar deze **102 PDC-koppelbare onderwerpen** (goedgekeurd door user), omdat slechts 102 van de 152 PDC-onderwerpen koppelbaar bleken. De "~200" leest dus niet meer als openstaande eis.
- De mapping is gemaakt door 4 parallelle LLM-agents over pre-geëxtraheerde JSON (naam + vraag + type + DomainValue per kandidaat).

### Voortgang
- ✅ **Stap 1 — SPF-grondwaarheid** toegevoegd. Kolom F (SPF) in `Product inrichting` is ingevuld (Wingdings-vinkje `ü`=✓, 121 markeringen). 71 van de 102 testset-onderwerpen hebben een SPF-antwoord; opgenomen als `spf_ground_truth` in `docs/testset/golden-testset.json`.
- ✅ **Stap 2 — Anonimiseren** klaar. `AnalyseQwik` en `Specificatie Flexibele premieovereenkomst` geanonimiseerd (maskeren met `[FONDS]`; rode fondsblokken + "Fondsen"-secties verwijderd; 0 resterende fondsnamen). Kopieën in `docs/bronnen_geanonimiseerd/`; originelen ongemoeid.
- ⏳ **Stap 3 — Tool gebouwd (standalone runner), volledige run loopt.**
  - Servicemodule `backend/app/services/onderdeel_analysis.py`: beantwoordt per ontologie-vraag uit de golden-testset o.b.v. de SPF-fondsdocumenten via Claude structured output (`claude-opus-4-8`) → gekozen DomainValue + vrije tekst + confidence + `buiten_format` + verbatim bronverwijzing (server-side geverifieerd via `verification.py`). **Deterministische keyword-retrieval over pagina-chunks** (geen embeddings/Qdrant — die deps zijn niet geïnstalleerd; sluit aan bij de filosofie van `ontology.py`).
  - Runner `backend/scripts/run_onderdeel_analyse.py` (draaien vanuit `backend/`, `--limit N` voor een deelrun). Fondscorpus = SPF FPR/ABTN/Implementatieplan/Operating Manual; standaard = geanonimiseerde Specificatie/AnalyseQwik.
  - Output: `docs/testset/analyse-resultaat.json` + validatiesamenvatting (vergelijkt met `spf_ground_truth`; ja/nee-varianten en eenheid-hints als 'jaren' worden correct behandeld).
  - Testrun (6 onderwerpen) gevalideerd: pipeline werkt, bronnen geverifieerd; tool inhoudelijk sterk. Volledige run over 102 onderwerpen loopt.

### Nog te doen na de run
- Resultaten + accuraatheid tegen de PDC beoordelen; echte fouten vs. meetartefacten scheiden.
- Later: full API/frontend-integratie van de onderdeel-modus; gerichte her-run van de `no_match`-koppelingen; ontologie-verbeterlijst (23 `granularity_gap` in de testset); **standaardkant-analyse + vergelijking fonds↔IG&H-standaard (einddoel, zie sectie EINDDOEL).**
