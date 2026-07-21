# WTP onderdeel-analyse — leesbare documentenset

_Use Case 1 · testfonds SPF · 20 juli 2026_

Deze set beschrijft in gewone taal wat we hebben gebouwd: een hulpmiddel dat automatisch, per onderwerp uit het pensioen-ontologiemodel, bepaalt wat de regeling van een fonds voorschrijft — met bronvermelding, zodat een deskundige elk antwoord kan controleren.

Bedoeld voor pensioendeskundigen, product owners en betrokkenen die geen techniek hoeven te lezen.

## Leeswijzer

| Document | Waarover |
|---|---|
| [1 — Samenvatting en resultaten](1-samenvatting-en-resultaten.md) | Wat er is gemaakt, de uitkomsten van de test, en wat die betekenen. Begin hier. |
| [2 — Aanpak en bouw](2-aanpak-en-bouw.md) | Hoe het werkt: het ontologiemodel, de testset, de koppeling met de PDC, de anonimisering en de tool — in gewone taal. |
| [3 — Deliverables en vervolg](3-deliverables-en-vervolg.md) | Wat er precies is opgeleverd, hoe het is getest, wat de deskundigen moeten beoordelen en de vervolgstappen. |
| [4 — Reviewlijst voor deskundigen](4-reviewlijst.md) | De concrete punten die om een oordeel vragen: alle 8 afwijkende antwoorden, 7 gevallen "buiten format" en 23 model-gaten. |

## Wat zit er in dit pakket?

Dit pakket bestaat uit twee mappen (zie `LEESMIJ.md` in de zip):
- **human-readable/** — deze set (documenten 1 t/m 4 + dit overzicht).
- **voor-ai/** — de technische/gestructureerde documenten voor AI-agents en ontwikkelaars: `projectcontext.md`, `golden-testset.md` (de volledige testset met ijkpunten), `deliverables-en-testscenarios.md`, `eindresultaat.md`.

De onderliggende **data- en codebestanden** (de ruwe resultaten `analyse-resultaat.json`, de golden-testset als `.json`, de geanonimiseerde bronbestanden, en de backend-code) zitten **niet in dit pakket** — die staan in de projectrepository.

## In één zin

De tool is betrouwbaar en voorzichtig (ze verzint niets en verwijst altijd naar de bron); de winst zit nu vooral in het vergroten van de **dekking** — het aantal onderwerpen waarvoor ze een antwoord vindt — en in de nog te bouwen **vergelijking tussen het fonds en de IG&H-standaard**.
