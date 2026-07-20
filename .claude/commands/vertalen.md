---
description: Activeer de WTP agent-flow en start Station 2 (Vertalen) — vertaal het Gate-1-canvas naar een geconsolideerde deliverables-tabel via een interpretatieteam + vertaalchat
argument-hint: [optionele sturing, bv. een divergentie waar je al een besluit over hebt]
---

Activeer de **`agent-flow`**-skill (Skill-tool) en volg de **Vertaal-modus (Station 2)** exact. Doel: de use case-behoefte uit het Gate-1-canvas vertalen naar **definitieve deliverables + hun technische kant**, via een team van interpretatie-agents en een vertaalchat met de gebruiker, culminerend in een geconsolideerde deliverables-tabel.

1. **Preconditie:** `gates.gate_1.status: signed_off` in `status.yaml`. Zo niet: meld dat Station 1 (Begrijpen, `/begrijpen`) eerst moet worden afgerond — tenzij de gebruiker expliciet een override vraagt.
2. **Parallelle interpretatie:** dispatch in één bericht de 4 lens-agents (business-analist, technisch-architect, data-ontologie, compliance-risico) op het canvas.
3. **Synthese:** dispatch de vertaal-synthesizer (synthese-modus) → de deliverables-tabel + de mens-samenvatting. Conflicten tussen lenzen worden divergenties.
4. **Vertaalchat (dit is de kern):** zolang er open divergenties zijn, leg de gebruiker **een kleine batch tegelijk** (±3–5) voor, in gewone zakelijke taal: benoem het conflict tussen de lenzen en de concrete keuzeopties. Koppel na elke batch terug wat je begrepen hebt en laat corrigeren. Persisteer bevestigde besluiten in `context/projectcontext.md` met attributie. Dispatch daarna de vertaal-synthesizer (verwerk-modus) om de besluiten te verwerken. Herhaal tot er geen open divergenties meer zijn.
5. **Valideer** elk deliverable tegen `references/output-contracts.md` vóór je het toont.
6. **Gate Vertalen:** bied sign-off aan zodra er geen open divergenties zijn en elke rij thema + prioriteit + acceptatiecriterium heeft. **Blijf binnen Station 2** — ga niet door naar specificeren (Station 3) zolang deze gate niet is afgetekend.
7. **De mens beslist.** Elke divergentie is een keuze voor de gebruiker/deskundigen, nooit voor de agents.

## Wat de gebruiker meegaf voor deze aanroep

$ARGUMENTS
