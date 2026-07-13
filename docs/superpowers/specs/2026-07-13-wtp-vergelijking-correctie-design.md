# WTP-vergelijking — correctie, bewijsvoering en documentbeheer

## Probleem
- **Foutieve vergelijking**: De kolom "STANDAARD WTP-PRODUCT" toont ten onrechte de eigen FPR-cijfers van het fonds (bijv. 14,25% / 10%) in plaats van de benchmarkgegevens van AllVida/Qwik.
- **Bronverwarring**: Fonds- en standaardproductgegevens worden door elkaar gebruikt zonder duidelijke scheiding.
- **Presentatieproblemen**:
  - Rauwe LaTeX-formules (`$A=\sum...$`) renderen niet correct.
  - Teksten zijn te lang en onoverzichtelijk.
  - Het aantal "onderzochte onderdelen" is onverklaard en lijkt willekeurig.
- **Geen documentbeheer**: Functionaliteit voor uploaden, verwijderen of beheren van bronnen ontbreekt.

---

## Doelen
1. **Harde scheiding tussen bronnen**:
   - Huidige regeling: uitsluitend gebaseerd op fondsdocumenten.
   - Standaardproduct: uitsluitend gebaseerd op benchmarkdocumenten.
   - Elke kant heeft eigen broncitaten.

2. **Bewijsvoering tegen hallucinatie**:
   - Letterlijke citaten verplicht in prompts.
   - Backend verifieert of elk citaat voorkomt in de geëxtraheerde tekst van het genoemde document en aan de juiste kant staat.
   - Niet-geverifieerde bevindingen worden gedegradeerd en gemarkeerd.

3. **Verbeterde presentatie**:
   - Korte bullets per kant (huidig vs. standaard) + een "Verschil"-strook.
   - Impact beschreven in platte Nederlandse taal (geen LaTeX).
   - Lange details en broncitaten verplaatst naar een "Meer informatie"-dropdown.

4. **Transparantie over onderzochte onderdelen**:
   - Dynamisch aantal onderzochte onderdelen blijft behouden.
   - UI toont expliciet welke thema's zijn onderzocht, afgezet tegen een vaste WTP-checklist (wel/niet gedekt).
   - Uitleg over de herkomst van het getal.

5. **Documentbeheer**:
   - Uploaden (opslag op server-schijf).
   - Verwijderen, rol/type wijzigen.
   - Volgorde aanpassen via drag & drop.

---

## Schemawijzigingen

### `EntitlementComparison`
- `area` (string)
- `current_points[]` (array van bullets)
- `standard_points[]` (array van bullets)
- `key_differences[]` (array van strings)
- `current_detail` (lange tekst)
- `standard_detail` (lange tekst)
- `gap_detected` (boolean)
- `deviation_severity` (enum: High/Medium/Low/None)
- `impact_explanation` (platte Nederlandse tekst)
- `required_qwik_configuration` (string)
- `current_sources[]` (array van `ProvisionSource`, alleen fondsbronnen)
- `standard_sources[]` (array van `ProvisionSource`, alleen benchmarkbronnen)
- `evidence_verified` (boolean, door backend gezet)

### `ProvisionSource` (blijft ongewijzigd)
- `document_name` (string)
- `section` (string)
- `page_number` (number)
- `quote` (string)

---

## Backend
- **Nieuwe uploads-map**: schrijfbare map voor documentopslag op de server.
- **Endpoints**:
  - `POST /documents`: uploaden van documenten.
  - `DELETE /documents/{id}`: verwijderen van (geüploade) documenten.
  - `PATCH /documents/{id}`: wijzigen van rol/type.
- **Metadata-opslag**: klein JSON-bestand voor overrides/uploads-metadata.
- **Verificatieservice**: controleert of citaten daadwerkelijk voorkomen in de geëxtraheerde tekst van het genoemde document en aan de juiste kant (fonds/benchmark) staan; markeert niet-geverifieerde bevindingen.
- **Herschreven system-prompt**: strikte scheiding tussen fonds- en benchmarkbronnen, verplichte letterlijke citaten, platte Nederlandse taal (geen LaTeX).
- **Herschreven demo-rapport**: gegrond op de daadwerkelijke documenten.

---

## Frontend
- **`EntitlementCard`**: opnieuw opgebouwd met bullets per kant, een "Verschil"-strook, een evidence-badge (geverifieerd/niet-geverifieerd), een "Meer informatie"-dropdown, en geen LaTeX.
- **`SummaryPanel`**: nieuw "Wat is onderzocht?"-dekkingspaneel dat onderzochte thema's afzet tegen een vaste WTP-checklist en het getal uitlegt.
- **`DocumentSelector`**: toevoegen/verwijderen/wijzigen (rol/type) en volgorde via drag & drop (zonder externe library).
- **`ComparisonPage`**: bedraad met bovenstaande componenten.
- **Geen nieuwe dependencies** (geen KaTeX, geen drag-library).

---

## Niet in scope
- De DB/DC-framing ("beoogde overgangsdatum") blijft ongewijzigd, aangezien dit geen onderdeel was van de klacht van de expert.
