# WTP onderdeel-analyse — volledig leesbaar document

_Use Case 1 · testfonds SPF · 20 juli 2026_

Dit document bevat de volledige, in gewone taal geschreven beschrijving van wat we hebben gebouwd: een hulpmiddel dat automatisch, per onderwerp uit het pensioen-ontologiemodel, bepaalt wat de regeling van een fonds voorschrijft — met bronvermelding, zodat een deskundige elk antwoord kan controleren. Bedoeld voor pensioendeskundigen, product owners en betrokkenen die geen techniek hoeven te lezen.

## Inhoudsopgave

- [Deel 1 — Samenvatting en resultaten](#deel-1--samenvatting-en-resultaten)
- [Deel 2 — Aanpak en bouw](#deel-2--aanpak-en-bouw)
- [Deel 3 — Deliverables en vervolg](#deel-3--deliverables-en-vervolg)
- [Deel 4 — Reviewlijst voor deskundigen](#deel-4--reviewlijst-voor-deskundigen)
- [Onderliggende bestanden](#onderliggende-bestanden)

---

# Deel 1 — Samenvatting en resultaten

## Waar gaat dit over?

Een pensioenfonds moet onder de Wet toekomst pensioenen (Wtp) laten vastleggen hoe zijn regeling precies in elkaar zit. In het onderliggende **ontologiemodel** staan ongeveer 2.600 losse onderwerpen (bijvoorbeeld: "is er een minimum pensioengevend inkomen?", "hoe wordt de datum afgerond?"). Bij elk onderwerp hoort een vraag en vaak een lijstje toegestane antwoorden.

Tot nu toe werd zo'n analyse **met de hand** gedaan. Het doel van dit project: dat werk **automatiseren** — de tool leest de documenten van een fonds en beantwoordt per onderwerp de vraag, met een bronverwijzing en een betrouwbaarheidsscore erbij.

Als test hebben we het gedaan voor één fonds (**SPF**) en een vaste, controleerbare selectie van **102 onderwerpen** (samen **106 unieke vragen**; omdat sommige onderwerpen meerdere vragen bevatten, worden er in een run **133 vraag-instanties** doorlopen).

## Wat is er gemaakt?

- Een **vaste testset** van 102 onderwerpen; bij **71** daarvan bestaat een handmatig SPF-antwoord dat als ijkpunt dient.
- Een **koppeling** tussen de handmatige productbeschrijving (PDC) en het ontologiemodel.
- **Geanonimiseerde** versies van twee standaarddocumenten, zodat de tool ook voor nieuwe fondsen bruikbaar is zonder dat er antwoorden van een ander fonds "meelekken".
- De **analyse-tool** zelf, die per onderwerp een antwoord met bron en betrouwbaarheid geeft.

## De resultaten van de test

De tool doorliep 133 vraag-instanties:

| Wat | Uitkomst |
|---|---|
| Vraag-instanties behandeld | 133 |
| Beantwoord (met bron) | 40 (waarvan 24 hoge, 13 midden, 3 lage betrouwbaarheid) |
| Eerlijk "niet gevonden" | 93 |
| Analyses die faalden | 0 |
| Gecontroleerde broncitaten | 49 |
| Instanties met een SPF-ijkpunt | 87 (van de 71 onderwerpen met ijkpunt) |
| Beantwoord **én** toetsbaar tegen het handwerk | 22 → **14 kloppen, 8 wijken af (~64%)** |

**Hoe u de cijfers leest.** De eerlijke maat is de laatste rij: van de instanties die de tool **wél beantwoordde en die we konden nakijken (22)**, klopte er ongeveer **twee derde (14)**. Een "kale" score over álle 87 instanties-met-ijkpunt valt veel lager uit (~28%), maar die telt de 62 níét-beantwoorde instanties mee als fout — die maat zegt dus meer over de **dekking** dan over de **correctheid**. Bij álle getoonde antwoorden geldt: er is een letterlijk citaat uit een fondsdocument dat automatisch is gecontroleerd. De tool verzint dus niets. (Er zijn 49 gecontroleerde citaten bij 40 antwoorden, omdat een antwoord meerdere citaten kan hebben en er ook citaten zijn bij enkele "niet gevonden"/deels-antwoorden.)

## Voorbeelden

**Goed beantwoord (met bron):**
- Soort overeenkomst → *Flexibele premieovereenkomst*.
- Deelname aan de regeling → *verplicht*.
- Maximaal pensioengevend inkomen → *ja, een door het fonds gekozen maximum* (met vindplaats: € 38.611 in 2026).
- Grondslag → *pensioengevend inkomen min franchise*.

**Wijkt af — de moeite van het nakijken waard (geen harde fout):**
- Minimum pensioengevend inkomen: de tool zegt "ja" op basis van "ten minste nihil"; het handwerk zegt "nee". Interpretatieverschil.
- Vorm van de franchise: de tool koos "sociale zekerheid / AOW-franchise"; het handwerk zegt "nominaal bedrag".

De volledige lijst van alle 8 afwijkingen staat in Deel 4.

## De belangrijkste conclusie

- De tool is **betrouwbaar en voorzichtig**: geen mislukkingen, elk antwoord onderbouwd, en waar de documenten geen antwoord geven zegt ze eerlijk "niet gevonden" in plaats van te gokken.
- De grootste verbeterkans is de **dekking** (40 van de 133): de tool zoekt nu op trefwoorden (de slimmere "betekenis"-zoekmethode staat nog niet aan) en sommige details staan simpelweg niet in het reglement.
- De afwijkende antwoorden zijn vooral **nuances** die om een expertoordeel vragen — de tool bereidt voor, de deskundige beslist.
- De **einddoelstelling** — het fonds vergelijken met de IG&H-standaard per onderwerp — is nog een vervolgstap (Deel 3).

---

# Deel 2 — Aanpak en bouw

Vijf stappen.

## Stap 1 — De bouwstenen: het ontologiemodel en de PDC

- **Het ontologiemodel** (`OntologySnapshot`) is de gezamenlijke "taal" voor pensioenproducten: ~2.600 **onderwerpen**, elk met een naam, een vraag en vaak een lijstje toegestane antwoorden, gegroepeerd in **klassen**.
- **De PDC Beroepse** is de handmatige productbeschrijving: per onderwerp en per fonds is aangevinkt welk antwoord geldt. Dit is het **ijkpunt** waartegen we de tool controleren — géén bron waaruit de tool antwoorden voor het fonds mag halen.

## Stap 2 — Een vaste, controleerbare testset

We beginnen met een **vaste selectie van 102 gekoppelde onderwerpen**. Bij **71** daarvan bestaat een handmatig SPF-antwoord (ijkpunt); die laten ons de tool nakijken. De 102 zijn geselecteerd omdat ze koppelbaar bleken tussen PDC en ontologie, niet omdat ze allemaal een ijkpunt hebben.

Koppelen kon niet één-op-één op naam (16 directe treffers), omdat de PDC bedrijfsnamen gebruikt en de ontologie technische namen. Daarom koppelden we op **klasse-niveau** en met de toegestane antwoorden.

## Stap 3 — De koppeling (mapping) door taalbegrip

Een taalmodel vergeleek de **betekenis** (niet alleen de woorden). Resultaat: **102 van de 152** PDC-onderwerpen gekoppeld, elk met een betrouwbaarheidsscore (48 zonder koppeling, 2 zonder duidelijke uitkomst).

Daarbij kwamen **model-gaten** aan het licht: de PDC maakt een onderscheid dat het ontologiemodel (nog) niet kan uitdrukken. Binnen de 102-testset zijn dat er **23** (over alle 152 PDC-onderwerpen 36). Voorbeelden: "afkoopmoment" mist *emigratie*; "voorportaal" mist *verplicht/vrijwillig*.

## Stap 4 — Anonimiseren van de standaarddocumenten

Twee documenten (standaard-productspecificatie en een technische analyse) bevatten al fondsspecifieke antwoorden. Omdat de tool ook voor **nieuwe fondsen** bruikbaar moet zijn — en omdat deze twee straks de **IG&H-standaardkant** voeden — zijn ze **geanonimiseerd**: fondsnamen → `[FONDS]`, fondsspecifieke/"Fondsen"-blokken verwijderd. Controle: **nul** fondsnamen meer; originelen ongewijzigd.

## Stap 5 — De tool

Per onderwerp: (1) **zoeken** in de fondsdocumenten; (2) **antwoorden** via een taalmodel (kies de best passende waarde + korte uitleg); (3) **onderbouwen** met een letterlijk, automatisch gecontroleerd citaat; (4) **eerlijk zijn** ("niet gevonden" i.p.v. gokken); (5) een **betrouwbaarheidsscore** + markering bij "buiten format". De tool beslist niets definitief; de deskundige beoordeelt.

## Waar dit naartoe gaat: fonds vs. IG&H-standaard

De uiteindelijke bedoeling is een **vergelijking**: dezelfde analyse ook voor de **IG&H-standaard** (uit de PDC, de standaardspecificatie en de Qwik-analyse), en dan per onderwerp bepalen waar het fonds afwijkt. De standaard heeft vaak **meerdere** mogelijke waarden per onderwerp (een "menu"); een fonds maakt meestal één keuze. Deze fondskant is de eerste helft; de standaardkant en de vergelijking zijn de volgende stap.

---

# Deel 3 — Deliverables en vervolg

## Wat is er opgeleverd?

| # | Opgeleverd | Wat het is | Status |
|---|---|---|---|
| 1 | Vaste testset (102 onderwerpen) | 71 met een handmatig SPF-antwoord als ijkpunt | Klaar |
| 2 | Geanonimiseerde standaardbronnen | Standaarddocumenten zonder fondsspecifieke informatie | Klaar |
| 3 | PDC ↔ ontologie-koppeling | Welke ontologie-vraag hoort bij welk PDC-onderwerp (met betrouwbaarheid) | Klaar |
| 4 | Analyse-tool (fondskant) | Beantwoordt per onderwerp met bron + betrouwbaarheid | Klaar |
| 5 | Validatierapport | Vergelijkt de tool-antwoorden met het handwerk | Klaar |
| 6 | Lijst van 23 model-gaten | Waar het ontologiemodel het PDC-onderscheid niet vat | Klaar (voor review) |
| 7 | Slimmere "betekenis"-zoekmethode | Verhoogt de dekking | Nog te doen |
| 8 | Inbouw in de applicatie | Onderdeel-analyse via de webapplicatie | Nog te doen |
| 9 | Standaardkant-analyse (IG&H) | Wat IG&H aanbiedt per onderwerp, uit PDC + specificatie + Qwik (meervoudig) | Nog te doen |
| 10 | Vergelijking fonds ↔ IG&H-standaard | Verschillen per onderwerp — de einddoelstelling | Nog te doen |

## Testscenario's per deliverable

In gewone taal (de technische Given/When/Then-versie staat in de **voor-ai** map, `deliverables-en-testscenarios.md`):

1. **Testset compleet & herbruikbaar** — 102 onderwerpen (106 unieke vragen), 71 met ijkpunt; opnieuw inladen van de bevroren testset geeft dezelfde lijst. → **Geslaagd**.
2. **Anonimisering lekt geen fondsnamen** — 0 fondsnamen in de output; originelen ongewijzigd. → **Geslaagd**.
3. **Koppeling verwijst alleen naar bestaande onderwerpen** — 102 gekoppeld, 0 verzonnen. → **Geslaagd**.
4. **De tool onderbouwt en verzint niet** — juist antwoord met gecontroleerd citaat; anders "niet gevonden". → **Geslaagd** (0 mislukkingen · 49 citaten).
5. **De validatie telt eerlijk** — ja/nee-varianten en eenheid-hints correct behandeld. → **Geslaagd** (~64% op 22 toetsbare).
6. **Model-gaten zijn onderbouwd** — elk van de 23 gaten heeft een uitleg. → **Geslaagd**.
7. **Betekenis-zoekmethode verhoogt de dekking** — meer beantwoord dan 40/133, zonder verlies van betrouwbaarheid. → **Nog te draaien**.
8. **Onderdeel-analyse via de applicatie** — zelfde resultaat als de losse tool, zichtbaar in de interface. → **Nog te draaien**.
9. **Standaardkant klopt en is meervoudig** — alle door IG&H toegestane waarden, uit de juiste bron (PDC vóór specificatie vóór Qwik). → **Nog te draaien**.
10. **Vergelijking benoemt de juiste verschillen** — fondswaarde binnen standaard → "past binnen standaard"; erbuiten → "echte afwijking". → **Nog te draaien**.

## Wat vragen we van de deskundigen?

De concrete lijsten staan in Deel 4:
1. **De 8 afwijkende antwoorden** — klopt het handwerk of de tool?
2. **De 7 gevallen "buiten format"** — mogelijk ontologie aanpassen.
3. **De 23 model-gaten** — uitbreiden of overbodig?
4. **De streefwaarden** voor accuraatheid en dekking.

## Vervolgstappen

1. **Dekking verhogen** (betekenis-zoekmethode aanzetten).
2. **Meer bronnen** (inrichtings-/implementatiedocumenten).
3. **Standaardkant + vergelijking bouwen** (de einddoelstelling).
4. **Expertreview** verwerken.
5. **Ontologiemodel bijwerken**.
6. **Opschalen** en **inbouwen** in de applicatie.

---

# Deel 4 — Reviewlijst voor deskundigen

De volledige, concrete lijsten (alle 8 afwijkende antwoorden met tool-antwoord vs. ijkpunt en citaat, alle 7 gevallen "buiten format", en alle 23 model-gaten) staan in het aparte document **`4-reviewlijst.md`** in deze map. Kort:
- **8 afwijkende antwoorden** — waar de tool afwijkt van het PDC-ijkpunt; per stuk het tool-antwoord, het ijkpunt en het citaat.
- **7 "buiten format"** — waar het antwoord niet in de keuzelijst/het format past (kandidaten voor ontologie-aanpassing).
- **23 model-gaten** — met per gat de uitleg van wat er mist.

---

## Onderliggende bestanden

In dit documentatiepakket (twee mappen):
- **human-readable/** — dit document plus `README.md`, `1-samenvatting-en-resultaten.md`, `2-aanpak-en-bouw.md`, `3-deliverables-en-vervolg.md`, `4-reviewlijst.md`.
- **voor-ai/** — `projectcontext.md`, `golden-testset.md` (de volledige testset met ijkpunten), `deliverables-en-testscenarios.md`, `eindresultaat.md`.

Niet in dit pakket (staan in de projectrepository): de ruwe resultaten `analyse-resultaat.json`, de testset als `.json`, de geanonimiseerde bronbestanden (`.docx`) en de backend-code.
