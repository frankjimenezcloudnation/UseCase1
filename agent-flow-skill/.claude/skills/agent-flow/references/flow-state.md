# Flow-state en routing (generiek)

## Deel 1 — status.yaml-schema

Bestand `docs/agent-flow/status.yaml` (in het huidige project) is de bron van waarheid voor routing en gates. **Alleen de orchestrator schrijft het** — subagents nooit.

> **Areas zijn projectspecifiek.** De inhoudelijke deelonderwerpen (areas) worden per project bepaald (uit `docs/agent-flow/config.yaml` of voorgesteld door de context-analyst en bevestigd bij Gate 1). `gate_2.themas` en `dod.themas` starten leeg en worden door de orchestrator gevuld zodra de areas vaststaan. Er is altijd een generieke area `GEN` voor overkoepelende/technische zaken. De `thema`/area-kolom in specs en de deliverables-tabel gebruikt deze area-codes.

> **Station↔Gate↔Folder-mapping.** Stationnummers (prosa), gate-keys en mapordinalen zijn ontkoppeld:

| Station | Naam | Folder(s) | Exit-gate |
|---|---|---|---|
| 1 | Begrijpen | `01-canvas`, `02-vragen` | `gate_1` |
| 2 | Vertalen | `02b-vertalen` | `gate_vertalen` |
| 3 | Specificeren | `03-specs` | `gate_2` (per area) |
| 4 | DoD & Testen | `04-dod`, `05-tests`, `06-red-team` | `gate_3` |
| 5 | Beheer | — | — |

```yaml
flow_versie: 1
project: <naam of null>
context_document: context/projectcontext.md
config: docs/agent-flow/config.yaml    # optioneel; areas/glossary/compliance_context
areas: []                              # bevestigd bij Gate 1; codes → naam
artefacten:
  canvas: { status: ontbreekt|concept|klaar_voor_review|goedgekeurd, pad: ..., laatst_bijgewerkt: <YYYY-MM-DD> }
  vragen: { status: ontbreekt|open|beantwoord, laatst_bijgewerkt: <YYYY-MM-DD> }
  vertalen:
    interpretaties:
      <lens>: { status: ontbreekt|aanwezig, pad: ..., laatst_bijgewerkt: <YYYY-MM-DD> }   # business, techniek, data, compliance
    deliverables_tabel: { status: ontbreekt|concept|klaar_voor_review|goedgekeurd, pad: ..., open_divergenties: <int>, laatst_bijgewerkt: <YYYY-MM-DD> }
    deliverables_samenvatting: { status: ontbreekt|aanwezig, pad: ..., laatst_bijgewerkt: <YYYY-MM-DD> }
  dod:
    themas: {}                         # per area gevuld na Gate 1: <area>: { status: ontbreekt|aanwezig, pad: ..., laatst_bijgewerkt: ... }
  validatietesten: { status: ontbreekt|aanwezig, laatst_bijgewerkt: <YYYY-MM-DD> }
  acceptatietesten: { status: ontbreekt|aanwezig, laatst_bijgewerkt: <YYYY-MM-DD> }
  golden_dataset: { status: ontbreekt|aanwezig, laatst_bijgewerkt: <YYYY-MM-DD> }
  red_team: { status: ontbreekt|aanwezig, laatst_bijgewerkt: <YYYY-MM-DD> }
gates:
  gate_1: { status: open|signed_off, signed_off_by: [], datum: <YYYY-MM-DD> }
  gate_vertalen: { status: open|signed_off, signed_off_by: [], datum: <YYYY-MM-DD> }
  gate_2:
    themas: {}                         # per area gevuld na Gate 1: <area>: { status: open|specs_klaar|goedgekeurd, goedgekeurd_door: ..., datum: ... }
  gate_3: { status: open|signed_off, golden_dataset_gefixeerd: false, streefwaarden_gefixeerd: false, signed_off_by: [], datum: <YYYY-MM-DD> }
overrides: []                          # {gate: <naam>, datum, reden, bevestigd_door_user: true}
verouderd: []                          # artefactpaden die door een wijziging stale zijn (Station 5)
```

---

## Deel 2 — routingtabel

| Situatie | Actie | Agent/Gate |
|----------|-------|------------|
| Canvas ontbreekt | Dispatch context-analyst | context-analyst |
| Canvas `concept`, geen open vragenlijst | Dispatch domain-interviewer (vragen-modus) | domain-interviewer |
| Vragenlijst `open`, nog geen antwoorden | Wachttoestand — wacht op user-antwoorden (status `open` latcht) | — |
| Vragenlijst `open` én antwoorden beschikbaar | Dispatch domain-interviewer (verwerk-modus) | domain-interviewer |
| Canvas `klaar_voor_review` | Gate 1: sign-off vragen (naam + datum); bij sign-off canvas → `goedgekeurd` én areas vastleggen in `gate_2.themas`/`dod.themas` | Gate 1 |
| Gate 1 `signed_off`, interpretaties ontbreken | Dispatch de 4 lens-agents **parallel in één bericht** op het canvas | 4 interpreters |
| Alle 4 interpretaties `aanwezig`, `deliverables_tabel` ontbreekt | Dispatch vertaal-synthesizer (synthese-modus) → tabel + samenvatting | vertaal-synthesizer |
| `deliverables_tabel` heeft `open_divergenties > 0` | Vertaalchat (orchestrator ↔ user): batch voorleggen, verwerken via vertaal-synthesizer (verwerk-modus); herhalen tot 0 | orchestrator + vertaal-synthesizer |
| `deliverables_tabel` `klaar_voor_review` (0 open divergenties, volledige rijen) | Gate Vertalen: sign-off; bij sign-off tabel → `goedgekeurd` | Gate Vertalen |
| `gate_vertalen` `signed_off`, area zonder specs | Dispatch requirements-engineer per area (parallel), leest tabel area-geïndexeerd en citeert DLV-id; daarna terminologie-guardian; area → `specs_klaar` | requirements-engineer + terminologie-guardian |
| Area `specs_klaar` | Gate 2 voor die area: goedkeuring registreren | Gate 2 |
| Area `goedgekeurd`, `dod.themas.<area>` nog `ontbreekt` | Dispatch dod-composer + test-designer voor die area; daarna red-team-critic zodra specs én tests bestaan | dod-composer + test-designer + red-team-critic |
| Golden dataset gevuld + streefwaarden voorgesteld | Gate 3: fixatie registreren | Gate 3 |
| Gate 3 `signed_off` | Station 5 beheermodus (wijzigingen → impactanalyse via `traceability.yaml` → gerichte her-runs) | Beheer |

---

### Gate-handhaving

- Keten: `Begrijpen → gate_1 → Vertalen → gate_vertalen → Specificeren → gate_2 (per area) → DoD & Testen → gate_3 → Beheer`. Weiger dispatch naar een station zolang de exit-gate van het vorige station open is.
- Gate Vertalen vereist bovendien `open_divergenties == 0` én dat elke rij area + prioriteit + acceptatiecriterium heeft.
- Uitzondering alleen bij expliciete user-override ("override gate X"): reden loggen in `overrides`, banner **"VOORLOPIG — gate X niet gepasseerd"** in het deliverable.

### Feedbackloops

Canvas-wijziging na Gate 1: canvas terug naar `concept`/`klaar_voor_review`, getroffen areas terug naar `open`, downstream artefacten in `verouderd`. Wijzigt het begrip zelf, laat Gate 1 opnieuw aftekenen.
