# Final result — WTP component analysis (Use Case 1, fund SPF)

_Date: 2026-07-20 · Model: `claude-opus-4-8` · Scope: SPF, golden-testset (102 subjects → 106 unique ontology questions; run over 133 question instances)_

## 1. Goal

Automatically determine, per ontology subject (OntologySnapshot, tab `PROPERTY`), what a fund's scheme prescribes — with a chosen DomainValue, a free-text answer, a source reference and a confidence — so that an expert can verify it. Test fund: **SPF**. The PDC Beroepse serves here only as a validation reference for the fund side, not as an information source.

## 2. Delivered

| Artefact | Where |
|---|---|
| Fixed standard test set (102 subjects, 71 with SPF benchmark) | `golden-testset.md` (this folder) · `.json` in the repository |
| Anonymized standard sources | repository: `docs/bronnen_geanonimiseerd/` |
| Analysis tool (service module) + runner | repository: `backend/app/services/onderdeel_analysis.py`, `backend/scripts/run_onderdeel_analyse.py` |
| Raw analysis results (per question) | repository: `docs/testset/analyse-resultaat.json` |
| Deliverables + test scenarios | `deliverables-and-test-scenarios.md` (this folder) |
| Review list (deviations, out-of-format, model gaps) | `4-review-list.md` (human-readable folder) |

Recorded along the way (see `project-context.md`): the semantic PDC↔ontology mapping, the ontology model gaps (**23** within the 102 test set; 36 across all 152 PDC subjects), and the design requirements R1 (class grouping) and R2 (context enrichment).

## 3. Results of the run

| Metric | Value |
|---|---|
| Question instances (run) | 133 |
| Answered (with source) | **40** (high 24 · medium 13 · low 3) |
| Honest "not found" (origineel: "niet gevonden") (no hallucination) | 93 |
| Failed calls | 0 |
| Source citations verified server-side | 49 |
| Marked outside enumeration/format | 7 |
| Subjects with SPF benchmark | 71 (= 87 question instances) |
| **Answered and verifiable** | 22 → **14 match / 8 deviation (~64%)** |

**Reading the figures.** The relevant measure is the last row: of the question instances that the tool **answered and that are verifiable (22)**, ~**64%** (14) match the manual work. A "bare" score over all 87 instances-with-benchmark comes out much lower (~28%), because it counts the 62 non-answered instances as deviations — that measure therefore mainly weighs **coverage**, not **correctness**. There are 49 verified citations for 40 answers because one answer can carry multiple citations and 9 citations belong to a "not found" (origineel: "niet gevonden")/partial answer. Every displayed answer is substantiated with a verified, verbatim citation (page level); the tool does not hallucinate.

## 4. Examples

**Correct (with source):** `Type_pensioenovereenkomst`→`Flexibele_Premieovereenkomst`; `Afnametype`→`verplicht`; `Methodiek_vaststelling_grondslag`→`PGI_minus_franchise`; `Maximaal_PGI`→`ja_vrij_te_kiezen_maximum` (source: max € 38.611, 2026); `Maximale_stijging_PGI`→`nee`.

**Deviating (worth expert review, not a hard error):** `Minimaal_PGI` → tool "yes" (origineel: "ja") ("at least nil" (origineel: "ten minste nihil")) vs. PDC "no" (origineel: "nee"); `Vorm_franchise` → tool `franchise_sociale_zekerheid` vs. PDC `nominaal_bedrag`.

The **complete list** of all 8 deviations, 7 out-of-format cases and 23 model gaps is in `4-review-list.md` (human-readable folder).

## 5. Key finding: coverage is the bottleneck, not reliability

- The tool is **reliable and conservative**: 0 failures, every answer grounded, and where the source gives no answer the tool honestly says "not found" (origineel: "niet gevonden").
- The **biggest improvement point is coverage** (40/133). Causes:
  1. **Retrieval** — currently deliberately deterministic keyword matching over page chunks (the embedding/vector stack is not installed). Semantic retrieval would find many more relevant passages.
  2. **Genuinely absent** — many fine-grained components (roundings, specific WTP mechanics) are not in the SPF regulations/ABTN; those belong in configuration/implementation.
  3. **Granularity gaps** — 23 subjects in the test set where the ontology does not capture the PDC distinction.

## 6. Recommended next steps

1. **Better retrieval** — install and connect the RAG stack (embeddings + Qdrant, already present in the codebase) → higher coverage.
2. **Expand sources** — include configuration/implementation documents.
3. **Build the standard side + comparison** — determine the IG&H standard per subject (from PDC + specification + Qwik, multi-source) and compare fund vs. standard. This is the **end objective** (see `project-context.md`, section FINAL GOAL).
4. **Expert review** of the deviations, out-of-format cases and model gaps.
5. **Update the ontology** with the gaps.
6. **Integration** of the component mode into the FastAPI app + frontend.

> Core principle: the tool prepares and substantiates; the human/expert decides. Every answer is traceable to the source.
