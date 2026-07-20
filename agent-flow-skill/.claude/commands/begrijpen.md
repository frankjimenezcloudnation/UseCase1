---
description: Hoofdingang van de agent-flow — spar met het agent-team tot je "klaar" zegt, daarna doorlopen de agents de hele flow grondig
argument-hint: [plak hier alle info die je wilt geven — of zet die in het bericht vlak vóór /begrijpen]
---

Doel: je levert informatie, typt `/begrijpen`, en **spart daarna met het agent-team** — zij stellen vragen, jij antwoordt en legt uit — **tot je zegt klaar te zijn**. Zodra de agents genoeg hebben, doorlopen ze **de hele flow grondig** (Begrijpen → Vertalen → Specificeren → DoD & Testen). Dit is de hoofdingang; één doorlopende sessie. Werkt in elk project.

## Stap 0 — Leg de aangeleverde informatie vast (verplicht, eerst)

1. **Verzamel alle input van de gebruiker voor deze aanroep:** de tekst achter het commando (`$ARGUMENTS`) én relevante informatie uit het bericht/de berichten vlak vóór deze aanroep. Neem ook expliciet genoemde bestanden mee.
2. **Persisteer die input als ankerdocument** `context/projectcontext.md` in het huidige project: bestaat het nog niet → aanmaken, netjes gestructureerd; bestaat het al → een gedateerde sectie `## Aanvullende input — <YYYY-MM-DD>` toevoegen (nooit overschrijven; recente input wint).
3. **Bevestig kort** wat is vastgelegd, zodat de gebruiker kan corrigeren.

## Stap 1 — Activeer de skill en volg de Doorlopende modus

Activeer de **`agent-flow`**-skill (Skill-tool) en volg de sectie **Doorlopende modus (`/begrijpen`)** exact.

**Fase A — Sparren (tot de gebruiker "klaar" zegt).**
1. Dispatch **context-analyst** → eerste Use Case Canvas (Scope/areas, IST/SOLL zakelijk+technisch, Behoeften en gap, onduidelijkheden).
2. Dispatch **domain-interviewer** (vragen-modus) → geprioriteerde vragen; zodra het canvas staat mag je ook de 4 lens-agents draaien en hun divergenties als sparring-materiaal gebruiken.
3. **Spar interactief:** stel de gebruiker **een kleine batch vragen tegelijk** (±3–5), koppel terug ("dus als ik je goed begrijp…"), laat corrigeren, en **persisteer elk bevestigd antwoord** in `context/projectcontext.md`. Verwerk tussentijds via domain-interviewer (verwerk-modus).
4. **Blijf sparren tot de gebruiker expliciet zegt klaar te zijn** ("klaar", "genoeg", "ga maar"). Dwing nooit door.

**Fase B — Uitvoeren (grondig, na "klaar").**
Doorloop de hele flow in één run met de vastgelegde sparring-input als basis:
1. Canvas afronden → **Gate 1** (de "klaar" telt als go); leg de bevestigde areas vast in `status.yaml`.
2. **Station 2 Vertalen** (Vertaal-modus): 4 lenzen parallel → vertaal-synthesizer → deliverables-tabel + -samenvatting. Los divergenties op uit de sparring-context; wat daar niet uit volgt, leg je kort voor of laat je als open DIV staan — nooit stil zelf beslissen. → **Gate Vertalen**.
3. **Station 3 Specificeren** → requirements-engineer per area + terminologie-guardian → **Gate 2** per area.
4. **Station 4 DoD & Testen** → dod-composer + test-designer + red-team-critic → **Gate 3**. Evaluatie-dataset-grondwaarheden alleen als voorstel + skelet, expliciet gemarkeerd als "nog te bevestigen door experts".
5. **Valideer** elk deliverable tegen `references/output-contracts.md`; werk `status.yaml` bij.
6. **Sluit af** met een compact overzicht van de geproduceerde deliverables + wat nog door experts bevestigd moet worden.

**De mens beslist.** Elke inhoudelijke keuze en elke divergentie is voor de gebruiker/experts; de agents bereiden voor en voeren uit, maar verzinnen nooit een besluit dat aan de mens toekomt.

## Wat de gebruiker meegaf voor deze aanroep

$ARGUMENTS
