---
description: Activeer de agent-flow en start Station 2 (Vertalen) — vertaal het Gate-1-canvas naar een geconsolideerde deliverables-tabel via een interpretatieteam + vertaalchat
argument-hint: [optionele sturing, bv. een divergentie waar je al een besluit over hebt]
---

Activeer de **`agent-flow`**-skill (Skill-tool) en volg de **Vertaal-modus (Station 2)** exact. Doel: de use case-behoefte uit het Gate-1-canvas vertalen naar **definitieve deliverables + hun technische kant**, via een team van interpretatie-agents en een vertaalchat met de gebruiker, culminerend in een geconsolideerde deliverables-tabel.

1. **Preconditie:** `gates.gate_1.status: signed_off`. Zo niet: meld dat Station 1 (Begrijpen, `/begrijpen`) eerst moet — tenzij de gebruiker expliciet een override vraagt.
2. **Parallelle interpretatie:** dispatch in één bericht de 4 lens-agents (business-analist, technisch-architect, data-domein, compliance-risico) op het canvas.
3. **Synthese:** dispatch de vertaal-synthesizer (synthese-modus) → deliverables-tabel + mens-samenvatting. Conflicten tussen lenzen worden divergenties.
4. **Vertaalchat (de kern):** zolang er open divergenties zijn, leg de gebruiker **±3–5 divergenties per batch** voor in gewone taal (conflict + keuzeopties). Koppel terug, laat corrigeren, persisteer besluiten in `context/projectcontext.md` met attributie, en dispatch de vertaal-synthesizer (verwerk-modus). Herhaal tot 0 open divergenties.
5. **Valideer** elk deliverable tegen `references/output-contracts.md`.
6. **Gate Vertalen:** bied sign-off aan zodra er 0 open divergenties zijn en elke rij area + prioriteit + acceptatiecriterium heeft. **Blijf binnen Station 2** — niet door naar Station 3 zonder sign-off.
7. **De mens beslist.** Elke divergentie is een keuze voor de gebruiker/experts, nooit voor de agents.

## Wat de gebruiker meegaf voor deze aanroep

$ARGUMENTS
