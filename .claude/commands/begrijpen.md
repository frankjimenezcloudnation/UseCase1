---
description: Leg de aangeleverde informatie vast en laat de agents de use case zo optimaal mogelijk begrijpen (Station 1 van de WTP agent-flow)
argument-hint: [plak hier alle info die je wilt geven — of zet die in het bericht vlak vóór /begrijpen]
---

Doel: de gebruiker levert alle informatie die zij willen geven, typt `/begrijpen`, en de agents gaan aan de slag om de use case **zo optimaal mogelijk te begrijpen**. Dit is Station 1 (Begrijpen) van de WTP agent-flow — de brainstorm-/begripsfase, vóór er iets gespecificeerd wordt.

## Stap 0 — Leg de aangeleverde informatie vast (verplicht, eerst)

1. **Verzamel alle input van de gebruiker voor deze aanroep:** de tekst achter het commando (`$ARGUMENTS`) én relevante informatie uit het bericht/de berichten vlak vóór deze aanroep in het gesprek. Neem ook expliciet genoemde bestanden mee.
2. **Persisteer die input als ankerdocument** `context/projectcontext.md`:
   - Bestaat het nog niet → maak het aan met de aangeleverde informatie, netjes gestructureerd (doel, scope/thema's, aannames, cijfers, en losse opmerkingen — laat niets weg).
   - Bestaat het al → **voeg een gedateerde sectie toe** (`## Aanvullende input — <YYYY-MM-DD>`) met de nieuwe informatie; overschrijf bestaande context niet. Recente input wint bij tegenstrijdigheid; laat de agents die tegenstrijdigheid signaleren.
   - `context/` is gitignored, dus dit wordt niet gepusht.
3. **Bevestig kort** aan de gebruiker wat is vastgelegd (paar bullets), zodat zij kan corrigeren.
4. Heeft de gebruiker géén informatie aangeleverd en bestaat er nog geen `context/projectcontext.md`? Vraag dan om de informatie, of bied aan om corpus-only door te gaan. Nooit stil doorgaan.

## Stap 1 — Activeer de agent-flow (Station 1)

Activeer daarna de **`agent-flow`**-skill (Skill-tool) en volg die **Interview-modus (Station 1)** exact. Het doel is dat zowel de agents als de gebruiker de behoefte scherp krijgen: de **huidige situatie (IST)** en de **gewenste situatie (SOLL)**, telkens in **zakelijke én technische** termen.

1. **Bootstrap + dashboard** zoals de skill voorschrijft.
2. **Startbegrip:** dispatch **context-analyst** → eerste Use Case Canvas uit `context/projectcontext.md` + corpus + ontologie, mét de secties `Huidige situatie (IST)`, `Gewenste situatie (SOLL)` (elk zakelijk + technisch) en `Behoeften en gap`. Lees grondig; maak `Onduidelijkheden en ambiguïteiten` zo volledig mogelijk.
3. **Interview de gebruiker interactief** (dit is de kern):
   - Dispatch **domain-interviewer** (vragen-modus) voor een geprioriteerde vragenlijst, geordend langs IST vs. SOLL en zakelijk vs. technisch.
   - Stel de gebruiker **een kleine batch tegelijk** (±3–5 vragen) in gewone taal; maak per vraag duidelijk of het over de huidige of gewenste situatie gaat en of het zakelijk of technisch is. Overval niet met de hele lijst.
   - **Koppel terug** wat je begrepen hebt ("dus als ik je goed begrijp…") en laat corrigeren — zo groeit ook het begrip van de gebruiker. Persisteer bevestigde antwoorden in `context/projectcontext.md`.
   - Dispatch **domain-interviewer** (verwerk-modus) om de antwoorden met attributie in het canvas te verwerken; herhaal tot IST/SOLL helder zijn en alleen nog echte expertvragen open staan.
4. **Valideer** elk deliverable tegen `references/output-contracts.md` vóór je het toont.
5. **Gate 1:** zet het canvas op `klaar_voor_review` en bied sign-off door de deskundigen aan. **Blijf binnen Station 1** — ga niet door naar specificeren (Station 2) zolang Gate 1 niet is afgetekend. Voor de volledige orkestratie is er `/agent-flow`.
6. **De mens beslist.** Elke agent-output eindigt met open vragen en aannames; jij vat samen en legt de keuzes bij de gebruiker/deskundigen.

## Wat de gebruiker meegaf voor deze aanroep

$ARGUMENTS
