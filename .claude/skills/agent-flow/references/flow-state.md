# Flow-state en routing

## Deel 1 — status.yaml-schema

Bestand `docs/agent-flow/status.yaml` is de bron van waarheid voor routing en gates. **Alleen de orchestrator schrijft het** — subagents nooit.

> **Thema's — 5 vs 6.** De canvas-Scope en de golden dataset dekken de **5 inhoudelijke vergelijkingsthema's** (opbouwsystematiek, partnerpensioen, indexatie, compensatie, beleggingsrisico). `gate_2.themas` en de spec-codes kennen er **6**: het extra thema `generiek` (GEN) is de technische/overkoepelende keten (inlezen, extractie, vergelijking, presentatie + NFR's) — dat wordt wél gespecificeerd en getest, maar hoort niet in de inhoudelijke scope-tabel of de golden dataset. Dit verschil is bewust.

```yaml
artefacten:
  <naam>:                      # canvas, vragen, validatietesten, acceptatietesten, golden_dataset, red_team
    status: ontbreekt|concept|klaar_voor_review|goedgekeurd   # canvas
        # vragen: ontbreekt|open|beantwoord
        # overige: ontbreekt|aanwezig
    laatst_bijgewerkt: <YYYY-MM-DD>
  dod:                         # per thema getrackt (DoD wordt per thema geproduceerd), net als gate_2.themas
    themas:
      <thema>: { status: ontbreekt|aanwezig, laatst_bijgewerkt: <YYYY-MM-DD> }
gates:
  gate_1:
    status: open|signed_off
    signed_off_by: []          # namen van deskundigen
    datum: <YYYY-MM-DD>
  gate_2:
    themas:                    # per thema, niet alles-of-niets
      <thema>:                 # opbouwsystematiek, partnerpensioen, indexatie, compensatie, beleggingsrisico, generiek
        status: open|specs_klaar|goedgekeurd
        goedgekeurd_door: <naam>
        datum: <YYYY-MM-DD>
  gate_3:
    status: open|signed_off
    golden_dataset_gefixeerd: true|false
    streefwaarden_gefixeerd: true|false
    signed_off_by: []
    datum: <YYYY-MM-DD>
overrides:                     # alleen op expliciet user-verzoek
  - {gate: <1|2|3>, datum: <YYYY-MM-DD>, reden: <tekst>, bevestigd_door_user: true}
verouderd: []                  # artefactpaden die door een wijziging stale zijn (Station 4)
```

---

## Deel 2 — routingtabel

| Situatie | Actie | Agent/Gate |
|----------|-------|------------|
| Canvas ontbreekt | Dispatch context-analyst | context-analyst |
| Canvas status `concept`, geen open vragenlijst | Dispatch domain-interviewer (vragen-modus) | domain-interviewer |
| Vragenlijst `open`, nog geen antwoorden | Wachttoestand — wacht op de expertsessie; geen dispatch (de status `open` latcht tot antwoorden binnen zijn) | — |
| Vragenlijst `open` én antwoorden beschikbaar | Dispatch domain-interviewer (verwerk-modus) | domain-interviewer |
| Canvas `klaar_voor_review` | Gate 1: user om sign-off vragen (naam + datum), registreren in `status.yaml`; bij sign-off canvas-status → `goedgekeurd` (zodat deze rij daarna niet meer matcht) | Gate 1 |
| Gate 1 `signed_off` (canvas `goedgekeurd`), thema zonder specs | Dispatch requirements-engineer per thema (onafhankelijke thema's parallel), daarna ontology-guardian over de nieuwe specs; thema-status → `specs_klaar` | requirements-engineer + ontology-guardian |
| Thema `specs_klaar` | Gate 2 voor dat thema: goedkeuring registreren (naam + datum) | Gate 2 |
| Thema `goedgekeurd`, `dod.themas.<thema>` nog `ontbreekt` | Dispatch dod-composer + test-designer voor dat thema; daarna red-team-critic zodra specs én tests bestaan | dod-composer + test-designer + red-team-critic |
| Golden dataset gevuld door experts + streefwaarden voorgesteld | Gate 3: fixatie registreren | Gate 3 |
| Gate 3 `signed_off` | Station 4 beheermodus (wijzigingen → impactanalyse via `traceability.yaml` → gerichte her-runs) | Beheer |

---

### Gate-handhaving

- Dispatch naar Station *N* wordt **geweigerd** zolang gate *N−1* open is. Gate 2 geldt per thema: een goedgekeurd thema mag door naar Station 3 terwijl een ander thema nog in review is.
- Uitzondering alleen bij expliciete user-override ("override gate X"): vraag de reden, log in `overrides`, en zorg dat het deliverable bovenin de waarschuwingsbanner **"VOORLOPIG — gate X niet gepasseerd"** krijgt.

### Feedbackloops

- Canvas-wijziging na Gate 1 (bv. inzicht uit Gate 2/3-review): canvas terug naar `concept` of `klaar_voor_review`, getroffen thema's terug naar `open`, downstream artefacten in `verouderd`. Wijzigt het begrip zelf, laat Gate 1 dan opnieuw aftekenen.
