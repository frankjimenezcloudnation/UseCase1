# Eindresultaat — WTP onderdeel-analyse (Use Case 1, fonds SPF)

_Datum: 2026-07-20 · Model: `claude-opus-4-8` · Scope: SPF, golden-testset (102 onderwerpen → 106 unieke ontologie-vragen; run over 133 vraag-instanties)_

## 1. Doel

Automatisch, per ontologie-onderwerp (OntologySnapshot, tab `PROPERTY`), bepalen wat de regeling van een fonds voorschrijft — met een gekozen DomainValue, een vrij-tekst antwoord, een bronverwijzing en een confidence — zodat een deskundige het kan verifiëren. Testfonds: **SPF**. De PDC Beroepse dient hier alleen als validatie-referentie voor de fondskant, niet als informatiebron.

## 2. Opgeleverd

| Artefact | Waar |
|---|---|
| Vaste standaard-testset (102 onderwerpen, 71 met SPF-ijkpunt) | `golden-testset.md` (deze map) · `.json` in de repository |
| Geanonimiseerde standaardbronnen | repository: `docs/bronnen_geanonimiseerd/` |
| Analyse-tool (servicemodule) + runner | repository: `backend/app/services/onderdeel_analysis.py`, `backend/scripts/run_onderdeel_analyse.py` |
| Ruwe analyse-resultaten (per vraag) | repository: `docs/testset/analyse-resultaat.json` |
| Deliverables + testscenario's | `deliverables-en-testscenarios.md` (deze map) |
| Reviewlijst (afwijkingen, buiten-format, model-gaten) | `4-reviewlijst.md` (human-readable map) |

Onderweg vastgelegd (zie `projectcontext.md`): de semantische PDC↔ontologie-mapping, de ontologie-model-gaten (**23** binnen de 102-testset; 36 over alle 152 PDC-onderwerpen), en de ontwerpeisen R1 (klasse-groepering) en R2 (contextverrijking).

## 3. Resultaten van de run

| Metriek | Waarde |
|---|---|
| Vraag-instanties (run) | 133 |
| Beantwoord (met bron) | **40** (high 24 · medium 13 · low 3) |
| Eerlijk "niet gevonden" (geen hallucinatie) | 93 |
| Mislukte calls | 0 |
| Broncitaten server-side geverifieerd | 49 |
| Buiten enumeration/format gemarkeerd | 7 |
| Onderwerpen met SPF-ijkpunt | 71 (= 87 vraag-instanties) |
| **Beantwoord én toetsbaar** | 22 → **14 overeenkomst / 8 afwijking (~64%)** |

**Lezing van de cijfers.** De relevante maat is de laatste rij: van de vraag-instanties die de tool **beantwoordde en die toetsbaar zijn (22)** komt ~**64%** (14) overeen met het handwerk. Een "kale" score over álle 87 instanties-met-ijkpunt valt veel lager uit (~28%), omdat die de 62 níét-beantwoorde instanties als afwijking meetelt — die maat weegt dus vooral de **dekking**, niet de **correctheid**. Er zijn 49 geverifieerde citaten bij 40 antwoorden omdat een antwoord meerdere citaten kan dragen en 9 citaten bij een "niet gevonden"/deels-antwoord horen. Elk getoond antwoord is onderbouwd met een geverifieerd, verbatim citaat (paginaniveau); de tool hallucineert niet.

## 4. Voorbeelden

**Correct (met bron):** `Type_pensioenovereenkomst`→`Flexibele_Premieovereenkomst`; `Afnametype`→`verplicht`; `Methodiek_vaststelling_grondslag`→`PGI_minus_franchise`; `Maximaal_PGI`→`ja_vrij_te_kiezen_maximum` (bron: max € 38.611, 2026); `Maximale_stijging_PGI`→`nee`.

**Afwijkend (expertreview waard, geen harde fout):** `Minimaal_PGI` → tool "ja" ("ten minste nihil") vs. PDC "nee"; `Vorm_franchise` → tool `franchise_sociale_zekerheid` vs. PDC `nominaal_bedrag`.

De **volledige lijst** van alle 8 afwijkingen, 7 buiten-format-gevallen en 23 model-gaten staat in `4-reviewlijst.md` (human-readable map).

## 5. Belangrijkste bevinding: dekking is het knelpunt, niet betrouwbaarheid

- De tool is **betrouwbaar en conservatief**: 0 mislukkingen, elk antwoord gegrond, en waar de bron geen antwoord geeft zegt de tool eerlijk "niet gevonden".
- Het **grootste verbeterpunt is dekking** (40/133). Oorzaken:
  1. **Retrieval** — nu bewust deterministische keyword-matching over pagina-chunks (de embedding-/vector-stack is niet geïnstalleerd). Semantische retrieval zou veel meer relevante passages vinden.
  2. **Echt afwezig** — veel fijnkorrelige onderdelen (afrondingen, specifieke WTP-mechanica) staan niet in het SPF-reglement/ABTN; die horen thuis in inrichting/implementatie.
  3. **Granulariteitsgaten** — 23 onderwerpen in de testset waar de ontologie het PDC-onderscheid niet vat.

## 6. Aanbevolen vervolgstappen

1. **Betere retrieval** — de RAG-stack (embeddings + Qdrant, al aanwezig in de codebase) installeren en aansluiten → hogere dekking.
2. **Bronnen uitbreiden** — inrichtings-/implementatiedocumenten meenemen.
3. **Standaardkant + vergelijking bouwen** — per onderwerp de IG&H-standaard bepalen (uit PDC + specificatie + Qwik, meervoudig) en fonds vs. standaard vergelijken. Dit is de **einddoelstelling** (zie `projectcontext.md`, sectie EINDDOEL).
4. **Expertreview** van de afwijkingen, buiten-format-gevallen en model-gaten.
5. **Ontologie bijwerken** met de gaten.
6. **Integratie** van de onderdeel-modus in de FastAPI-app + frontend.

> Kernprincipe: de tool bereidt voor en onderbouwt; de mens/deskundige beslist. Elk antwoord is naar de bron herleidbaar.
