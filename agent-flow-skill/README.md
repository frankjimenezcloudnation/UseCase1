# agent-flow — een generieke, downloadbare Claude Code skill

Een domein-onafhankelijke multi-agent workflow die je een use case laat **begrijpen**,
**vertalen** naar deliverables, en gecontroleerd uitwerken naar **specificaties, een
Definition of Done en testen** — met de mens als beslisser op elk inhoudelijk punt.

Je activeert het met **`/begrijpen`**: je spart met een team van agents (zij stellen
vragen, jij antwoordt en legt uit) tot je zegt dat je **klaar** bent, en daarna doorlopen
de agents de hele flow grondig. Werkt in **elk project** — er zit niets domeinspecifieks in.

> Dit is de generieke variant. De WTP-pensioenvariant (Use Case 1) is een getunede
> versie hiervan; deze skill bevat géén corpus, ontologie of pensioenlogica.

## Installeren (één keer, per persoon)

De skill wordt **user-level** geïnstalleerd in `~/.claude`, zodat hij in al je projecten
beschikbaar is (niet gebonden aan één repo).

```bash
git clone <deze-repo>            # of pull de repo waar deze map in staat
cd agent-flow-skill
./install.sh                     # kopieert skills/agents/commands naar ~/.claude
#   ./install.sh --dry-run       # eerst tonen wat er gebeurt
```

**Windows / handmatig:** kopieer de mappen `.claude/skills/agent-flow`, `.claude/agents/*`
en `.claude/commands/*` uit dit pakket naar je eigen `~/.claude/` (op Windows
`%USERPROFILE%\.claude\`).

Start daarna een **nieuwe** Claude Code-sessie in een willekeurig project en typ `/begrijpen`.

## Gebruiken

- **`/begrijpen`** — hoofdingang: lever je informatie, spar met het team tot je "klaar" bent,
  daarna draaien de agents de hele flow en leveren alle deliverables op.
- **`/vertalen`** — spring direct naar Station 2 (Vertalen) als de use case al begrepen is.
- **`/agent-flow`** — dezelfde flow, maar station-voor-station met een gate-pauze.

De deliverables landen in `docs/agent-flow/` **in het huidige project** (de skill maakt die
map en de state-file aan bij de eerste run).

## Per project configureren (optioneel)

Zero-config: de agents leiden de **areas/thema's** van je use case tijdens Station 1 af en
laten je ze bevestigen. Wil je ze vastpinnen of een begrippenlijst meegeven, maak dan
`docs/agent-flow/config.yaml`:

```yaml
project: "Mijn project"
areas:                     # korte codes → naam; bepalen de REQ-/DLV-id-prefixes
  AUTH: Authenticatie
  BILL: Facturatie
glossary: docs/begrippen.md   # optioneel: pad naar een begrippenlijst (gedeelde taal)
compliance_context: "AVG/GDPR"  # optioneel: relevante regelgeving voor de compliance-lens
```

## Bronmateriaal

De agents lezen `context/projectcontext.md` (door jou gevuld tijdens het sparren) plus de
bestanden die je aanwijst en het project zelf (via de gebruikelijke lees-tools). Tekst,
Markdown en PDF gaan direct; voor binaire office-formaten (`.docx`/`.xlsx`) lever je een
tekst-/Markdown-export of geplakte inhoud aan.

## Wat de skill nooit doet

Inhoudelijke beslissingen voor je nemen, gates zelf passeren, of een divergentie tussen
interpretatie-lenzen stilzwijgend oplossen — dat blijft altijd aan de mens.
