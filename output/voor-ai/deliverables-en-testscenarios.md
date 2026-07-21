# Deliverables & testscenario's — WTP onderdeel-analyse (Use Case 1, fonds SPF)

Status: klaar_voor_review
Datum: 2026-07-20

Deze tabel volgt het skill-contract voor de Deliverables-tabel (10 kolommen). Elk deliverable heeft hieronder een gekoppeld testscenario (Given/When/Then) met een verifieerbaar acceptatiecriterium. Thema is meestal `generiek`: deze use case volgde de per-onderwerp-route i.p.v. de 5 pensioenthema's. Testset-omvang: 102 onderwerpen → 106 unieke ontologie-vragen; een run doorloopt 133 vraag-instanties.

## Deliverables

| business-req | afgestemde interpretatie | deliverable | technische vertaling | thema | prioriteit | owner/dev-agent | afhankelijkheden | acceptatiecriterium | status |
|---|---|---|---|---|---|---|---|---|---|
| Alle ~2600 PROPERTY-onderwerpen per fonds automatisch beantwoorden | Start met een vaste, valideerbare steekproef (SPF) | DLV-GEN-001 — Vaste golden-testset (102 onderwerpen) | `golden-testset.json`/`.md`, afgeleid uit PDC↔PROPERTY-mapping | generiek | Must | data-ontologie / orchestrator | OntologySnapshot, PDC Beroepse | 102 onderwerpen met ontologie-vraag; 71 met `spf_ground_truth`; herbruikbaar | definitief |
| Tool moet werken voor nieuwe fondsen, zonder fondsspecifieke lek | Standaardbronnen anonimiseren (maskeren) | DLV-GEN-002 — Geanonimiseerde standaardbronnen | docx-anonimiseerder: `[FONDS]`-masking + rode blokken/"Fondsen"-secties verwijderd | generiek | Must | compliance-risico | Specificatie, AnalyseQwik | 0 resterende fondsnamen in output | definitief |
| PDC-onderwerpen koppelen aan de juiste ontologie-vragen | Semantische koppeling via klasse-hiërarchie (R1) | DLV-GEN-003 — Semantische PDC↔ontologie-mapping | 4 parallelle LLM-agents over class-scoped kandidaten | generiek | Must | data-ontologie | DLV-GEN-001 | 102/152 gemapt; per onderwerp minimale set + confidence | definitief |
| Per onderwerp het fondsantwoord bepalen, herleidbaar | DomainValue + vrije tekst + bron + confidence (R2) | DLV-GEN-004 — Onderdeel-analyse-engine (fondskant) | `extraction` + keyword-retrieval + Claude structured output + `verification` (repository: backend) | generiek | Must | technisch-architect | DLV-GEN-001, DLV-GEN-002 | per vraag: waarde/vrije tekst + geverifieerde bron + confidence + `buiten_format` | definitief |
| Antwoorden toetsen aan grondwaarheid | Validatie tegen PDC-SPF-antwoorden | DLV-GEN-005 — Validatierapport | vergelijking met `spf_ground_truth` (ja/nee-varianten, eenheid-hints) | generiek | Must | test-designer | DLV-GEN-004 | accuraatheid + dekking + #geverifieerde citaten gerapporteerd | definitief |
| Ontologie verbeteren waar ze het PDC-onderscheid niet vat | Model-gaten expliciet markeren, mens beslist | DLV-GEN-006 — Ontologie-model-gaten (23 in de testset) | `granularity_gap` + toelichting per onderwerp | generiek | Should | ontology-guardian | DLV-GEN-003 | elk gat met onderbouwing; klaar voor expertreview | afgestemd |
| Hogere dekking dan de 40/133 baseline | Semantische i.p.v. keyword-retrieval | DLV-GEN-007 — RAG-embeddings retrieval | bestaande `rag/`-stack (embeddings + Qdrant) aansluiten | generiek | Should | technisch-architect | DLV-GEN-004 | embeddings actief; dekking > keyword-baseline | divergent |
| Bruikbaar in de productflow | Onderdeel-modus in de app | DLV-GEN-008 — API/frontend-integratie | route + schema + UI voor onderdeel-analyse | generiek | Could | technisch-architect | DLV-GEN-004 | endpoint + zichtbare resultaten in frontend | divergent |
| Bepalen wat de IG&H-standaard aanbiedt per onderwerp | Zelfde per-onderwerp-aanpak, meervoudige waarden | DLV-GEN-009 — Standaardkant-analyse (IG&H) | bron in prioriteit: PDC (kolom D `IG&H Standaard Horizon`) → Specificatie → AnalyseQwik; meervoudige DomainValues | generiek | Must | technisch-architect | DLV-GEN-001, DLV-GEN-002 | per onderwerp de door IG&H toegestane waarde(n) met bron | divergent |
| Verschil fonds ↔ IG&H-standaard benoemen (einddoel) | Set-vs-set vergelijking | DLV-GEN-010 — Vergelijking fonds↔standaard | per onderwerp: past-binnen / echte-afwijking / standaard-biedt-meer / dekking-gat | generiek | Must | technisch-architect | DLV-GEN-004, DLV-GEN-009 | per onderwerp verschiltype + bronnen van beide kanten | divergent |

## Testscenario's

### TST-001 — Golden-testset compleet & herbruikbaar (DLV-GEN-001)
- **Given** de bevroren `golden-testset.json` (in de repository; `golden-testset.md` in dit pakket).
- **When** de bevroren testset opnieuw wordt ingeladen.
- **Then** het bevat 102 onderwerpen (106 unieke ontologie-vragen), elk met ≥1 `ontology_questions`-entry; 71 hebben een `spf_ground_truth`. Herladen levert een inhoud-identieke lijst (reproduceerbaarheid = herladen van het vastgelegde bestand, niet het opnieuw draaien van de niet-deterministische LLM-mapping).
- **Verwacht:** 102 onderwerpen · 106 unieke vragen · 133 vraag-instanties · 71 met SPF-ijkpunt.
- **Status:** geslaagd.

### TST-002 — Anonimisering lekt geen fondsnamen (DLV-GEN-002)
- **Given** de geanonimiseerde bestanden (repository: `docs/bronnen_geanonimiseerd/`).
- **When** gescand op fondsnamen (`SPF|SPD|SPH&P|SPV|SPOA|AKZO|ADP|BerPF`).
- **Then** 0 treffers; de originele bronbestanden zijn ongewijzigd.
- **Verwacht:** Specificatie 0 hits, AnalyseQwik 0 hits.
- **Status:** geslaagd.

### TST-003 — Mapping verwijst alleen naar bestaande properties (DLV-GEN-003)
- **Given** de geconsolideerde mapping / golden-testset.
- **When** elke geselecteerde `property_name` wordt opgezocht in de PROPERTY-tab.
- **Then** elke property bestaat (geen verzonnen namen) en elk onderwerp heeft een confidence.
- **Verwacht:** 102 gemapte onderwerpen; 0 properties zonder details.
- **Status:** geslaagd.

### TST-004 — Engine antwoordt gegrond en hallucineert niet (DLV-GEN-004)
- **Given** een onderwerp waarvan het antwoord expliciet in het reglement staat (bv. `Type_pensioenovereenkomst`) én een onderwerp dat niet in de bron staat.
- **When** de engine beide analyseert.
- **Then** het eerste levert het juiste antwoord (`Flexibele_Premieovereenkomst`) met een server-geverifieerd verbatim citaat (paginabron) en confidence `high`; het tweede levert `niet_gevonden=true` zonder verzonnen bron.
- **Verwacht:** alle getoonde bronnen `verified=true`; geen antwoord zonder citaat.
- **Status:** geslaagd (0 mislukte calls, 49 geverifieerde citaten in de volledige run).

### TST-005 — Validatie telt correct (ja/nee-varianten & eenheid-hints) (DLV-GEN-005)
- **Given** de analyse-resultaten met `spf_ground_truth`.
- **When** de validatie draait.
- **Then** `komt_overeen_met_pdc` ∈ {ja, nee, n.v.t.}; een enum-variant als `ja_vrij_te_kiezen_maximum` telt als 'ja' t.o.v. grondwaarheid 'ja'; een eenheid-hint als `jaren` wordt `n.v.t.`.
- **Verwacht:** ~64% op de 22 beantwoorde, toetsbare vraag-instanties.
- **Status:** geslaagd.

### TST-006 — Model-gaten zijn onderbouwd (DLV-GEN-006)
- **Given** de mapping/testset met `granularity_gap`-markeringen.
- **When** alle gaten worden verzameld.
- **Then** elk gat heeft een `gap_note`; een steekproef bevestigt concrete gaten (bv. `Afkoopmoment` mist 'emigratie'; `Voorportaal_verplicht` mist verplicht/vrijwillig).
- **Verwacht:** 23 onderwerpen met een gemotiveerd model-gat (in de 102-testset).
- **Status:** geslaagd.

### TST-007 — Embeddings verhogen de dekking (DLV-GEN-007)
- **Given** de RAG-stack (embeddings + Qdrant) geïnstalleerd en aangesloten op de onderdeel-modus.
- **When** dezelfde 133 vraag-instanties opnieuw draaien.
- **Then** het aantal beantwoorde instanties is hoger dan de keyword-baseline (40/133), bij gelijke of hogere accuraatheid en zonder verlies van bronverificatie.
- **Verwacht:** dekking > 40/133; bronnen blijven geverifieerd.
- **Status:** nog te draaien.

### TST-008 — Onderdeel-modus via de API (DLV-GEN-008)
- **Given** de nieuwe API-endpoint voor de onderdeel-analyse.
- **When** aangeroepen met de golden-testset.
- **Then** het JSON-resultaat is gelijk aan dat van de standalone runner en is zichtbaar in de frontend.
- **Verwacht:** endpoint retourneert per onderwerp waarde + bron + confidence; UI toont ze.
- **Status:** nog te draaien.

### TST-009 — Standaardkant is correct en meervoudig (DLV-GEN-009)
- **Given** een onderwerp waar de IG&H-standaard meerdere opties toestaat (bv. `type regeling` = basis- én excedentregeling).
- **When** de standaardkant-analyse draait op PDC (kolom D) + Specificatie + AnalyseQwik.
- **Then** alle door IG&H toegestane waarden komen terug, met de bron, en bij tegenspraak wint de hoogste prioriteit (PDC → Specificatie → AnalyseQwik).
- **Verwacht:** meerdere waarden waar de standaard breder is dan een individueel fonds.
- **Status:** nog te draaien.

### TST-010 — Vergelijking benoemt het juiste verschiltype (DLV-GEN-010)
- **Given** een fondswaarde-set en de standaard-set per onderwerp.
- **When** de vergelijking draait.
- **Then** fonds ⊆ standaard → "past binnen standaard"; fonds bevat waarde buiten standaard → "echte afwijking"; standaard heeft extra opties → "standaard biedt meer"; ontbrekende kant → dekking-gat.
- **Verwacht:** correcte classificatie per onderwerp, met de bronnen van beide kanten.
- **Status:** nog te draaien.

## Open vragen en aannames
- **Aanname:** de PDC-SPF-antwoorden (kolom F) zijn de grondwaarheid voor de fondskant; enkele daarvan zijn eenheid-hints (`jaren`) i.p.v. echte waarden en worden als `n.v.t.` behandeld — te bevestigen door deskundigen.
- **Aanname:** de SPF-fondscorpus (FPR/ABTN/Implementatieplan/Operating Manual) is de juiste bron voor het fondsantwoord; onderdelen die enkel in inrichtings-/implementatiedocumenten staan vallen nu deels buiten de dekking.
- **Open:** streefwaarden voor accuraatheid en dekking (nu baseline ~64% op de beantwoorde, toetsbare instanties) — vast te stellen door de deskundigen.
- **Open:** de 8 afwijkende antwoorden en 7 `buiten_format`-gevallen — expertreview bepaalt of het tool-nuances of ontologie-correcties zijn (zie `4-reviewlijst.md`).
