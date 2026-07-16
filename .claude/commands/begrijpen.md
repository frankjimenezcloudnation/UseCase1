---
description: Activeer de WTP agent-flow en start Station 1 (Begrijpen) — brainstorm zodat de agents de use case begrijpen
argument-hint: [optionele sturing, bv. een thema of focuspunt]
---

Activeer de WTP agent-flow via de **`agent-flow`**-skill (Skill-tool) en stap in bij **Station 1 — Begrijpen**. Dit is de brainstorm-/begripsfase: het doel is dat de agents scherp krijgen wat we met Use Case 1 bedoelen, vóór er iets gespecificeerd wordt.

Volg de skill exact, maar met deze focus voor deze aanroep:

1. **Bootstrap + contextcheck** zoals de skill voorschrijft (maak `docs/agent-flow/` aan indien nodig; waarschuw expliciet als `context/projectcontext.md` en `context/implementatieplan-agent-flow.md` beide ontbreken — nooit stil doorgaan).
2. **Toon het dashboard** (huidige stand van canvas, gates, verouderde artefacten).
3. **Route naar Station 1:**
   - Canvas ontbreekt → dispatch **context-analyst** om het Use Case Canvas op te bouwen uit projectcontext + fonds- en benchmarkcorpus.
   - Canvas `concept` → dispatch **domain-interviewer** (vragen-modus) om de onduidelijkheden om te zetten in geprioriteerde expertvragen.
   - Antwoorden beschikbaar → dispatch **domain-interviewer** (verwerk-modus).
   - Canvas `klaar_voor_review` → bied **Gate 1** aan (sign-off door de deskundigen).
4. **Blijf binnen Station 1.** Ga niet door naar specificeren (Station 2) zolang Gate 1 niet is afgetekend — dat is het hele punt van deze fase. Wil de gebruiker verder dan begrijpen, verwijs dan naar `/agent-flow` voor de volledige orkestratie.
5. **De mens beslist.** Elke agent-output eindigt met open vragen en aannames; jij vat samen en legt de keuzes bij de gebruiker/deskundigen.

Extra sturing van de gebruiker voor deze aanroep (optioneel): $ARGUMENTS
