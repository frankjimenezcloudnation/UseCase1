# Project context — WTP agent-flow (Use Case 1)

> **Note (upon delivery in the documentation package):** paths to `backend/`, `frontend/`, `.xlsx` sources, `.json` outputs and `docs/bronnen_geanonimiseerd/` refer to the **source repository** and are not included in this package. Included in the package are the Markdown documents (human-readable set + for-ai set).

## Additional input — 2026-07-20

**Mode:** corpus-only. The user has not (yet) supplied a separate project description or implementation plan; the agents work on the source documents present in `UseCase1/`. This section is the anchor document; new input is added below with a date (never overwrite, recent input wins).

**Invocation:** `/begrijpen` from the `cloudnation` folder (wrapper command that uses `UseCase1/` as the project base).

### Available corpus in `UseCase1/`
- `2023-12-07 DPD – Transitieplan versie 1.0.pdf`
- `2025 Implementatieplan WTP SPF v1.0.pdf`
- `2025.09.15 Transitieplan Wtp DPF V1.3.pdf`
- `2025.12.18 Abtn 2026 SPF DEF.pdf`
- `AnalyseQwik_FPR_202508.docx`
- `Bijlage g- FPR Operating Manual APS-AIM v1.0 SPF.pdf`
- `OntologySnapshot.xlsx`
- `Overzicht_PDC_Beroepse_202600611.xlsx`
- `PRESENTATIE.md`
- `SPF Flexibele Premieregeling 2026.1_def.pdf`
- `Specificatie Flexibele premieovereenkomst 0.08.docx`
- Codebase: `backend/` (FastAPI) and `frontend/` (Vite/React), including `backend/app/services/ontology.py` and `extraction.py`.

### Still to be confirmed by the user/experts
- Whether one specific document is leading (e.g. the Specificatie Flexibele premieovereenkomst or the Implementatieplan WTP).
- The concrete scope/need of the WTP tool being refined (IST/SOLL) — this must be sharpened during the sparring.

## FINAL GOAL (clarified by user — 2026-07-20, leading)

The core use case is a **comparison between the fund and the IG&H standard**, per ontology topic:
1. **Fund side:** determine per ontology topic the fund's value, EXCLUSIVELY from the fund-specific files (FPR, ABTN, implementation plan, operating manual).
2. **IG&H standard side:** determine per topic what the IG&H standard offers, from `Specificatie Flexibele premieovereenkomst` + `AnalyseQwik` (anonymized).
3. **Compare** both (both mapped onto the ontology) and identify the **differences** between fund and standard.

**Crucial nuance — multiplicity (both sides):** the IG&H standard is a "menu" that often has **multiple** possible values per topic (more broadly specialized). But **a fund can also have multiple values** per topic — e.g. `basis premievrijstelling` can be determined in multiple ways (see PDC). Both sides are therefore **sets of values**. Example where the standard is broader: `type regeling` → IG&H = {basisregeling, excedentregeling, …}, fund = usually one of those.

**Sources + priority (leading in case of contradiction; higher wins):**
- **Fund side (fund-specific only):** 1. scheme rules (FPR) · 2. ABTN · 3. FPR Operating Manual · 4. implementation plan · 5. transition plan. For additionally supplied documents: let the **user** determine the priority. NB: for SPF, the transition plans present belong to other funds (DPF/DPD) → do not use.
- **IG&H standard side:** 1. **PDC Beroepse** — column D `IG&H Standaard Horizon` (most recent/correct) · 2. `Specificatie Flexibele premieovereenkomst` · 3. `AnalyseQwik`. The **PDC may be used exclusively for the standard side**, NEVER for the fund side.

**Comparison logic (set-vs-set):** fund ⊆ standard → *fits within the standard* (no deviation); fund contains value(s) outside the standard → *true deviation* (custom/not supported); standard has extra options → *standard offers more* (informative). Plus coverage signals (not found in fund / not found in standard).

**Status relative to this final goal:** the fund-side engine exists (`onderdeel_analysis.py`, single-value). STILL TO DO: (a) have the fund side return multiple values + document priority; (b) **standard-side analysis** (PDC column D + Specificatie + AnalyseQwik, multi-value); (c) **comparison step** fund↔standard as the final deliverable.

## Additional input — 2026-07-20 (scope recalibration; recent input wins)

The user recalibrates the setup. The core use case is **not** a generic document comparison, but a **complete, automated analysis of all topics in `OntologySnapshot.xlsx`, tab `PROPERTY`** (~2611 rows = ~2600 topics), applied to fund documents.

**Verified data structure — PROPERTY tab (2611 × 28), column headers in row 1:**
- `G = Name` — name of the topic (e.g. `Aanlevering_premies`, `Leidende_premie`, `Aansluiting_pensioenfonds`).
- `H = Definition`, `I = Clarification`, `J = Goal`, `K = Source`, `L = Type` (e.g. `enumeration`) — explanatory info per topic.
- `M = Multiplicity` (e.g. `0..n`).
- `N = Question` — the question to be answered literally per topic (e.g. "Which premiums are supplied?" (origineel: "Welke premies worden aangeleverd?")).
- `O = Category` — category; together with `C = ClassExternalId` / `D = SubClassExternalId` usable to group topics and answer them faster in batches.
- `P = DomainValue` — expected answer values, comma-separated (e.g. `Reguliere_premie,Bijspaarpremie,Anders`).

**Desired output per topic:** the answer to the question (`N`), preferably mapped to one of the allowed values from `P`. If mapping to `P` does not succeed, still return the free answer to the question/value. Use categories to arrive at answers more efficiently (in batches).

**Manual reference elaboration:** `Overzicht_PDC_Beroepse_202600611.xlsx`, tab `Product inrichting` (312 rows). Row 1: columns `D through I` = funds (`IG&H Standaard Horizon`, `SPH&P`, `SPF`, `SPD`, `SPV`, `SPOA`). Per row: `B = topic`, `C = candidate value`, per fund (D–I) a marking indicating whether that value applies; `J` = product code reference. This was done by hand for part of the topics and a number of funds — the tool must scale this to all ~2600 topics.

### Still to be confirmed (recalibration)
- For which **fund(s)** should the tool run first? The corpus in the repo appears to be mainly **SPF** (FPR SPF, ABTN SPF, transition plan). Which documents belong to which fund?
- Desired **output format** (per fund × topic: DomainValue + fallback free text; with **source reference/provenance** and **confidence** for verification by experts?).
- Categorization: primarily via `O = Category` or via the class hierarchy (`C`/`D`)?

### Confirmed decisions — 2026-07-20 (by user)
- **Test scope:** only fund **SPF**; a sample of **~200 topics** from the PROPERTY tab (smaller = easier to verify).
- **Fixed selection:** the ~200 topics are chosen **once** and then **reused every test round** (reproducible; fixed seed / recorded list).
- **PDC Beroepse is NOT an information source** for the analysis. The model may not use `Overzicht_PDC_Beroepse` as input; it serves only as reference/validation (and possibly to choose the test selection).
- **Anonymization:** `AnalyseQwik_FPR_202508.docx` and `Specificatie Flexibele premieovereenkomst 0.08.docx` must be **anonymized** — they already contain fund-specific filled-in information. Goal: the tool must be usable for **new funds** that want their scheme rules analyzed against "our standard". (Still to be detailed: what exactly counts as fund-specific and must be removed.)
- **Output format per topic (test phase):**
  1. one chosen **DomainValue from `P`** (for enumerations),
  2. a **source reference** (document + location),
  3. a **confidence**,
  4. during testing also a **free-text answer** that shows how the tool analyzes the topic.
- **Non-enumeration topics:** answer according to the indicated **`Type` (column L)** / format (free text, number, date, etc.). **Explicitly mark** when the answer does not fit within the enumeration or the indicated format — that is a signal to possibly adjust the ontology model.
- **"Done" = the described sample** fully completed (SPF, ~200 topics).

### Linkage analysis PDC ↔ ontology (verified 2026-07-20)
- PDC `Product inrichting`: **152 unique topics** (column B), 12 categories.
- Directly linkable 1:1 to the PROPERTY name: **16**. Partial/fuzzy overlap: ~69. No match: 67.
- Column `J` (product code/note) does **not** map to PROPERTY `ExternalId` (0 exact matches; partly free text).
- Cause: PDC uses business/CLASS names; PROPERTY uses specific property names (e.g. PDC `Lumpsum_uitkering` ↔ PROPERTY `Indicatie_lumpsum`; PDC `Vervroeging`/`Deeltijdpensioen` are CLASSes, not properties). Clean 1:1 linkage is therefore limited.

### Tool design requirements — 2026-07-20 (by user)
- **R1 — Class grouping (one topic → multiple questions).** A business/PDC topic often corresponds to an entire ontology **CLASS**; the tool then handles **all PROPERTY questions within that class** together. Example: PDC "pre-entry stage / pre-entry stage indication" (origineel: "Voorportaal / indicatie voorportaal") = CLASS `Voorportaal` (`25_01.03.42.000`) with ~13 PROPERTY questions (including `Indicatie_voorportaal_toestaan`, `Soort_voorportaal`, `Voorportaal_ivm_wachttijd/_drempelperiode/_jonger_dan_toetredingsleeftijd`, `Dekking_voorportaal`, `Risicodekking_gedurende_voorportaal`). Group via **column C (ClassExternalId) → CLASS.Name** (and `D`/SubClass). This also realizes the previously mentioned "using categories to answer more efficiently".
- **R2 — Context enrichment of generic/context-dependent questions.** Some PROPERTY questions implicitly refer to the topic they fall under (e.g. `Afrondingsmethode_datum` → "How is the date rounded?" (origineel: "Hoe wordt de datum afgerond?")). The tool must add the **parent topic from the hierarchy (column C/D → CLASS/SUBCLASS.Name)** to the question, so that the search is targeted (e.g. rounding of the *entry date* vs the *standard retirement date*). If the granularity expected by the PDC is missing from the ontology, **mark that explicitly** as a granularity gap (input for adjusting the ontology model).

### Standard test set established — 2026-07-20 (approved by user)
The semantic mapping (PDC Beroepse `Product inrichting` ↔ OntologySnapshot `PROPERTY`, via the class hierarchy) is the **fixed standard test set**. Recorded in `docs/testset/golden-testset.json` (machine-readable) and `docs/testset/golden-testset.md` (overview).
- **102 PDC topics** mapped → **106 unique ontology PROPERTY questions** (133 question instances in an analysis run). Confidence: high 40, medium 45, low 17.
- **23** topics carry a **`granularity_gap` marking** within the 102 test set (linked, but the ontology does not fully capture the PDC distinction; across all 152 PDC topics there were 36) → ontology improvement list for the experts.
- Of the 152 PDC topics: **102 mapped, 48 `no_match`, 2 without a clear outcome** (102 + 48 + 2 = 152). No_match is partly a real gap, partly a candidate scope error — to be improved later with a targeted re-run.
- **Scope/DoD adjusted (recent input wins):** the previously mentioned "~200 topics" test scope (lines above) has been adjusted to these **102 PDC-linkable topics** (approved by user), because only 102 of the 152 PDC topics turned out to be linkable. The "~200" therefore no longer reads as an open requirement.
- The mapping was created by 4 parallel LLM agents over pre-extracted JSON (name + question + type + DomainValue per candidate).

### Progress
- ✅ **Step 1 — SPF ground truth** added. Column F (SPF) in `Product inrichting` has been filled in (Wingdings checkmark `ü`=✓, 121 markings). 71 of the 102 test-set topics have an SPF answer; included as `spf_ground_truth` in `docs/testset/golden-testset.json`.
- ✅ **Step 2 — Anonymization** done. `AnalyseQwik` and `Specificatie Flexibele premieovereenkomst` anonymized (masking with `[FONDS]`; red fund blocks + "Funds" sections (origineel: "Fondsen") removed; 0 remaining fund names). Copies in `docs/bronnen_geanonimiseerd/`; originals untouched.
- ⏳ **Step 3 — Tool built (standalone runner), full run in progress.**
  - Service module `backend/app/services/onderdeel_analysis.py`: answers each ontology question from the golden test set based on the SPF fund documents via Claude structured output (`claude-opus-4-8`) → chosen DomainValue + free text + confidence + `buiten_format` + verbatim source reference (server-side verified via `verification.py`). **Deterministic keyword retrieval over page chunks** (no embeddings/Qdrant — those deps are not installed; aligns with the philosophy of `ontology.py`).
  - Runner `backend/scripts/run_onderdeel_analyse.py` (run from `backend/`, `--limit N` for a partial run). Fund corpus = SPF FPR/ABTN/implementation plan/Operating Manual; standard = anonymized Specificatie/AnalyseQwik.
  - Output: `docs/testset/analyse-resultaat.json` + validation summary (compares against `spf_ground_truth`; yes/no variants and unit hints such as 'years' (origineel: "jaren") are handled correctly).
  - Test run (6 topics) validated: pipeline works, sources verified; tool substantively strong. Full run over 102 topics in progress.

### Still to do after the run
- Assess the results + accuracy against the PDC; separate real errors from measurement artifacts.
- Later: full API/frontend integration of the component mode; targeted re-run of the `no_match` links; ontology improvement list (23 `granularity_gap` in the test set); **standard-side analysis + comparison fund↔IG&H standard (final goal, see the FINAL GOAL section).**
