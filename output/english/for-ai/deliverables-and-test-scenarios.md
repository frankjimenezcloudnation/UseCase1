# Deliverables & test scenarios — WTP component analysis (Use Case 1, fund SPF)

Status: klaar_voor_review
Date: 2026-07-20

This table follows the skill contract for the Deliverables table (10 columns). Each deliverable has a linked test scenario below (Given/When/Then) with a verifiable acceptance criterion. The theme is usually `generic`: this use case followed the per-topic route instead of the 5 pension themes. Test-set size: 102 topics → 106 unique ontology questions; a run goes through 133 question instances.

## Deliverables

| business req | agreed interpretation | deliverable | technical translation | theme | priority | owner/dev agent | dependencies | acceptance criterion | status |
|---|---|---|---|---|---|---|---|---|---|
| Answer all ~2600 PROPERTY topics per fund automatically | Start with a fixed, validatable sample (SPF) | DLV-GEN-001 — Fixed golden test set (102 topics) | `golden-testset.json`/`.md`, derived from the PDC↔PROPERTY mapping | generic | Must | data-ontology / orchestrator | OntologySnapshot, PDC Beroepse | 102 topics with an ontology question; 71 with `spf_ground_truth`; reusable | final |
| Tool must work for new funds, without fund-specific leakage | Anonymize standard sources (masking) | DLV-GEN-002 — Anonymized standard sources | docx anonymizer: `[FONDS]` masking + red blocks/"Funds" sections (origineel: "Fondsen") removed | generic | Must | compliance-risk | Specificatie, AnalyseQwik | 0 remaining fund names in the output | final |
| Link PDC topics to the correct ontology questions | Semantic linking via class hierarchy (R1) | DLV-GEN-003 — Semantic PDC↔ontology mapping | 4 parallel LLM agents over class-scoped candidates | generic | Must | data-ontology | DLV-GEN-001 | 102/152 mapped; per topic a minimal set + confidence | final |
| Determine the fund answer per topic, traceably | DomainValue + free text + source + confidence (R2) | DLV-GEN-004 — Component-analysis engine (fund side) | `extraction` + keyword retrieval + Claude structured output + `verification` (repository: backend) | generic | Must | technical-architect | DLV-GEN-001, DLV-GEN-002 | per question: value/free text + verified source + confidence + `buiten_format` | final |
| Test answers against ground truth | Validation against PDC SPF answers | DLV-GEN-005 — Validation report | comparison with `spf_ground_truth` (ja/nee variants, unit hints) | generic | Must | test-designer | DLV-GEN-004 | accuracy + coverage + #verified citations reported | final |
| Improve the ontology where it does not capture the PDC distinction | Mark model gaps explicitly, human decides | DLV-GEN-006 — Ontology model gaps (23 in the test set) | `granularity_gap` + explanation per topic | generic | Should | ontology-guardian | DLV-GEN-003 | each gap with substantiation; ready for expert review | aligned |
| Higher coverage than the 40/133 baseline | Semantic instead of keyword retrieval | DLV-GEN-007 — RAG embeddings retrieval | connect the existing `rag/` stack (embeddings + Qdrant) | generic | Should | technical-architect | DLV-GEN-004 | embeddings active; coverage > keyword baseline | divergent |
| Usable in the product flow | Component mode in the app | DLV-GEN-008 — API/frontend integration | route + schema + UI for the component analysis | generic | Could | technical-architect | DLV-GEN-004 | endpoint + visible results in the frontend | divergent |
| Determine what the IG&H standard offers per topic | Same per-topic approach, multiple values | DLV-GEN-009 — Standard-side analysis (IG&H) | source in priority: PDC (column D `IG&H Standaard Horizon`) → Specificatie → AnalyseQwik; multiple DomainValues | generic | Must | technical-architect | DLV-GEN-001, DLV-GEN-002 | per topic the value(s) allowed by IG&H with source | divergent |
| Identify the difference fund ↔ IG&H standard (end goal) | Set-vs-set comparison | DLV-GEN-010 — Comparison fund↔standard | per topic: fits-within / true-deviation / standard-offers-more / coverage-gap | generic | Must | technical-architect | DLV-GEN-004, DLV-GEN-009 | per topic difference type + sources from both sides | divergent |

## Test scenarios

### TST-001 — Golden test set complete & reusable (DLV-GEN-001)
- **Given** the frozen `golden-testset.json` (in the repository; `golden-testset.md` in this package).
- **When** the frozen test set is reloaded.
- **Then** it contains 102 topics (106 unique ontology questions), each with ≥1 `ontology_questions` entry; 71 have an `spf_ground_truth`. Reloading yields a content-identical list (reproducibility = reloading the recorded file, not re-running the non-deterministic LLM mapping).
- **Expected:** 102 topics · 106 unique questions · 133 question instances · 71 with an SPF reference point.
- **Status:** passed.

### TST-002 — Anonymization does not leak fund names (DLV-GEN-002)
- **Given** the anonymized files (repository: `docs/bronnen_geanonimiseerd/`).
- **When** scanned for fund names (`SPF|SPD|SPH&P|SPV|SPOA|AKZO|ADP|BerPF`).
- **Then** 0 hits; the original source files are unchanged.
- **Expected:** Specificatie 0 hits, AnalyseQwik 0 hits.
- **Status:** passed.

### TST-003 — Mapping refers only to existing properties (DLV-GEN-003)
- **Given** the consolidated mapping / golden test set.
- **When** each selected `property_name` is looked up in the PROPERTY tab.
- **Then** every property exists (no invented names) and every topic has a confidence.
- **Expected:** 102 mapped topics; 0 properties without details.
- **Status:** passed.

### TST-004 — Engine answers grounded and does not hallucinate (DLV-GEN-004)
- **Given** a topic whose answer is explicitly stated in the regulations (e.g. `Type_pensioenovereenkomst`) and a topic that does not appear in the source.
- **When** the engine analyzes both.
- **Then** the first yields the correct answer (`Flexibele_Premieovereenkomst`) with a server-verified verbatim citation (page source) and confidence `high`; the second yields `niet_gevonden=true` without an invented source.
- **Expected:** all displayed sources `verified=true`; no answer without a citation.
- **Status:** passed (0 failed calls, 49 verified citations in the full run).

### TST-005 — Validation counts correctly (ja/nee variants & unit hints) (DLV-GEN-005)
- **Given** the analysis results with `spf_ground_truth`.
- **When** the validation runs.
- **Then** `komt_overeen_met_pdc` ∈ {ja, nee, n.v.t.}; an enum variant such as `ja_vrij_te_kiezen_maximum` counts as 'ja' relative to ground truth 'ja'; a unit hint such as `jaren` becomes `n.v.t.`.
- **Expected:** ~64% on the 22 answered, testable question instances.
- **Status:** passed.

### TST-006 — Model gaps are substantiated (DLV-GEN-006)
- **Given** the mapping/test set with `granularity_gap` markings.
- **When** all gaps are collected.
- **Then** every gap has a `gap_note`; a sample confirms concrete gaps (e.g. `Afkoopmoment` lacks 'emigration' (origineel: "emigratie"); `Voorportaal_verplicht` lacks mandatory/voluntary).
- **Expected:** 23 topics with a substantiated model gap (in the 102 test set).
- **Status:** passed.

### TST-007 — Embeddings increase coverage (DLV-GEN-007)
- **Given** the RAG stack (embeddings + Qdrant) installed and connected to the component mode.
- **When** the same 133 question instances run again.
- **Then** the number of answered instances is higher than the keyword baseline (40/133), with equal or higher accuracy and without loss of source verification.
- **Expected:** coverage > 40/133; sources remain verified.
- **Status:** still to run.

### TST-008 — Component mode via the API (DLV-GEN-008)
- **Given** the new API endpoint for the component analysis.
- **When** called with the golden test set.
- **Then** the JSON result is identical to that of the standalone runner and is visible in the frontend.
- **Expected:** endpoint returns value + source + confidence per topic; the UI displays them.
- **Status:** still to run.

### TST-009 — Standard side is correct and multi-valued (DLV-GEN-009)
- **Given** a topic where the IG&H standard allows multiple options (e.g. `type regeling` = basic as well as excess scheme).
- **When** the standard-side analysis runs on PDC (column D) + Specificatie + AnalyseQwik.
- **Then** all values allowed by IG&H are returned, with the source, and in case of contradiction the highest priority wins (PDC → Specificatie → AnalyseQwik).
- **Expected:** multiple values where the standard is broader than an individual fund.
- **Status:** still to run.

### TST-010 — Comparison identifies the correct difference type (DLV-GEN-010)
- **Given** a fund value set and the standard set per topic.
- **When** the comparison runs.
- **Then** fund ⊆ standard → "fits within standard" (origineel: "past binnen standaard"); fund contains a value outside the standard → "true deviation" (origineel: "echte afwijking"); standard has extra options → "standard offers more" (origineel: "standaard biedt meer"); missing side → coverage gap.
- **Expected:** correct classification per topic, with the sources from both sides.
- **Status:** still to run.

## Open questions and assumptions
- **Assumption:** the PDC SPF answers (column F) are the ground truth for the fund side; some of these are unit hints (`jaren`) instead of real values and are treated as `n.v.t.` — to be confirmed by experts.
- **Assumption:** the SPF fund corpus (FPR/ABTN/Implementation Plan/Operating Manual) is the correct source for the fund answer; components that only appear in configuration/implementation documents currently fall partly outside the coverage.
- **Open:** target values for accuracy and coverage (currently baseline ~64% on the answered, testable instances) — to be determined by the experts.
- **Open:** the 8 deviating answers and 7 `buiten_format` cases — expert review determines whether they are tool nuances or ontology corrections (see `4-review-list.md`).
