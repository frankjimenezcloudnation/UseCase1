# WTP component analysis — complete readable document

_Use Case 1 · test fund SPF · 20 July 2026_

This document contains the complete, plain-language description of what we have built: a tool that automatically determines, per topic from the pension ontology model, what a fund's scheme prescribes — with source references, so that an expert can verify every answer. Intended for pension experts, product owners and stakeholders who do not need to read anything technical.

## Table of contents

- [Part 1 — Summary and results](#part-1--summary-and-results)
- [Part 2 — Approach and build](#part-2--approach-and-build)
- [Part 3 — Deliverables and next steps](#part-3--deliverables-and-next-steps)
- [Part 4 — Review list for experts](#part-4--review-list-for-experts)
- [Underlying files](#underlying-files)

---

# Part 1 — Summary and results

## What is this about?

Under the Future Pensions Act (Wet toekomst pensioenen, Wtp), a pension fund must have it recorded precisely how its scheme is put together. The underlying **ontology model** contains approximately 2.600 separate topics (for example: "is there a minimum pensionable income?" (origineel: "is er een minimum pensioengevend inkomen?"), "how is the date rounded?" (origineel: "hoe wordt de datum afgerond?")). Each topic comes with a question and often a list of allowed answers.

Until now, such an analysis was done **by hand**. The goal of this project: to **automate** that work — the tool reads a fund's documents and answers the question per topic, with a source reference and a confidence score attached.

As a test, we did this for one fund (**SPF**) and a fixed, verifiable selection of **102 topics** (together **106 unique questions**; because some topics contain multiple questions, **133 question instances** are processed in a run).

## What has been made?

- A **fixed test set** of 102 topics; for **71** of them a manual SPF answer exists that serves as a benchmark.
- A **link** between the manual product description (PDC) and the ontology model.
- **Anonymised** versions of two standard documents, so that the tool is also usable for new funds without answers from another fund "leaking in".
- The **analysis tool** itself, which gives an answer with source and confidence per topic.

## The results of the test

The tool processed 133 question instances:

| What | Outcome |
|---|---|
| Question instances handled | 133 |
| Answered (with source) | 40 (of which 24 high, 13 medium, 3 low confidence) |
| Honest "not found" | 93 |
| Analyses that failed | 0 |
| Verified source quotations | 49 |
| Instances with an SPF benchmark | 87 (from the 71 topics with a benchmark) |
| Answered **and** verifiable against the manual work | 22 → **14 correct, 8 deviate (~64%)** |

**How to read the figures.** The honest measure is the last row: of the instances the tool **did answer and that we were able to check (22)**, roughly **two thirds (14)** were correct. A "bare" score across all 87 instances-with-benchmark comes out much lower (~28%), but that one counts the 62 unanswered instances as errors — so that measure says more about **coverage** than about **correctness**. For all displayed answers the following holds: there is a literal quotation from a fund document that was automatically verified. So the tool does not make anything up. (There are 49 verified quotations for 40 answers, because an answer can have multiple quotations and there are also quotations for a few "not found"/partial answers.)

## Examples

**Answered correctly (with source):**
- Type of agreement → *Flexible premium agreement* (origineel: "Flexibele premieovereenkomst").
- Participation in the scheme → *mandatory* (origineel: "verplicht").
- Maximum pensionable income → *yes, a maximum chosen by the fund* (origineel: "ja, een door het fonds gekozen maximum") (with source location: € 38.611 in 2026).
- Basis → *pensionable income minus franchise* (origineel: "pensioengevend inkomen min franchise").

**Deviates — worth checking (not a hard error):**
- Minimum pensionable income: the tool says "yes" on the basis of "at least nil" (origineel: "ten minste nihil"); the manual work says "no". A difference of interpretation.
- Form of the franchise: the tool chose "social security / AOW franchise" (origineel: "sociale zekerheid / AOW-franchise"); the manual work says "nominal amount" (origineel: "nominaal bedrag").

The complete list of all 8 deviations is in Part 4.

## The main conclusion

- The tool is **reliable and cautious**: no failures, every answer substantiated, and where the documents give no answer it honestly says "not found" instead of guessing.
- The biggest opportunity for improvement is **coverage** (40 of the 133): the tool currently searches on keywords (the smarter "meaning"-based search method is not yet enabled) and some details are simply not in the regulations.
- The deviating answers are mainly **nuances** that call for an expert judgement — the tool prepares, the expert decides.
- The **final objective** — comparing the fund with the IG&H standard per topic — is still a next step (Part 3).

---

# Part 2 — Approach and build

Five steps.

## Step 1 — The building blocks: the ontology model and the PDC

- **The ontology model** (`OntologySnapshot`) is the shared "language" for pension products: ~2.600 **topics**, each with a name, a question and often a list of allowed answers, grouped into **classes**.
- **The PDC Beroepse** is the manual product description: per topic and per fund, the applicable answer has been ticked. This is the **benchmark** against which we check the tool — not a source from which the tool may draw answers for the fund.

## Step 2 — A fixed, verifiable test set

We start with a **fixed selection of 102 linked topics**. For **71** of them a manual SPF answer (benchmark) exists; those let us check the tool. The 102 were selected because they proved linkable between PDC and ontology, not because they all have a benchmark.

Linking could not be done one-to-one by name (16 direct matches), because the PDC uses business names and the ontology uses technical names. We therefore linked at **class level** and using the allowed answers.

## Step 3 — The link (mapping) through language understanding

A language model compared the **meaning** (not just the words). Result: **102 of the 152** PDC topics linked, each with a confidence score (48 without a link, 2 without a clear outcome).

In doing so, **model gaps** came to light: the PDC makes a distinction that the ontology model cannot (yet) express. Within the 102 test set there are **23** of these (36 across all 152 PDC topics). Examples: "commutation moment" (origineel: "afkoopmoment") lacks *emigration* (origineel: "emigratie"); "waiting area" (origineel: "voorportaal") lacks *mandatory/voluntary* (origineel: "verplicht/vrijwillig").

## Step 4 — Anonymising the standard documents

Two documents (standard product specification and a technical analysis) already contained fund-specific answers. Because the tool must also be usable for **new funds** — and because these two will later feed the **IG&H standard side** — they have been **anonymised**: fund names → `[FONDS]`, fund-specific / "Funds" (origineel: "Fondsen") blocks removed. Check: **zero** fund names remaining; originals unchanged.

## Step 5 — The tool

Per topic: (1) **search** the fund documents; (2) **answer** via a language model (pick the best-fitting value + a short explanation); (3) **substantiate** with a literal, automatically verified quotation; (4) **be honest** ("not found" instead of guessing); (5) a **confidence score** + a flag for "outside format". The tool decides nothing definitively; the expert judges.

## Where this is heading: fund vs. IG&H standard

The ultimate intention is a **comparison**: the same analysis for the **IG&H standard** as well (from the PDC, the standard specification and the Qwik analysis), and then determining per topic where the fund deviates. The standard often has **multiple** possible values per topic (a "menu"); a fund usually makes one choice. This fund side is the first half; the standard side and the comparison are the next step.

---

# Part 3 — Deliverables and next steps

## What has been delivered?

| # | Delivered | What it is | Status |
|---|---|---|---|
| 1 | Fixed test set (102 topics) | 71 with a manual SPF answer as benchmark | Done |
| 2 | Anonymised standard sources | Standard documents without fund-specific information | Done |
| 3 | PDC ↔ ontology link | Which ontology question belongs to which PDC topic (with confidence) | Done |
| 4 | Analysis tool (fund side) | Answers per topic with source + confidence | Done |
| 5 | Validation report | Compares the tool answers with the manual work | Done |
| 6 | List of 23 model gaps | Where the ontology model does not capture the PDC distinction | Done (for review) |
| 7 | Smarter "meaning"-based search method | Increases coverage | To do |
| 8 | Integration into the application | Component analysis via the web application | To do |
| 9 | Standard-side analysis (IG&H) | What IG&H offers per topic, from PDC + specification + Qwik (multi-valued) | To do |
| 10 | Comparison fund ↔ IG&H standard | Differences per topic — the final objective | To do |

## Test scenarios per deliverable

In plain language (the technical Given/When/Then version is in the **for-ai** folder, `deliverables-and-test-scenarios.md`):

1. **Test set complete & reusable** — 102 topics (106 unique questions), 71 with benchmark; reloading the frozen test set yields the same list. → **Passed**.
2. **Anonymisation leaks no fund names** — 0 fund names in the output; originals unchanged. → **Passed**.
3. **Link refers only to existing topics** — 102 linked, 0 invented. → **Passed**.
4. **The tool substantiates and does not invent** — correct answer with verified quotation; otherwise "not found". → **Passed** (0 failures · 49 quotations).
5. **The validation counts honestly** — yes/no variants and unit hints handled correctly. → **Passed** (~64% on 22 verifiable).
6. **Model gaps are substantiated** — each of the 23 gaps has an explanation. → **Passed**.
7. **Meaning-based search method increases coverage** — more answered than 40/133, without loss of reliability. → **Still to run**.
8. **Component analysis via the application** — same result as the standalone tool, visible in the interface. → **Still to run**.
9. **Standard side is correct and multi-valued** — all values allowed by IG&H, from the right source (PDC before specification before Qwik). → **Still to run**.
10. **Comparison identifies the right differences** — fund value within the standard → "fits within standard"; outside it → "genuine deviation". → **Still to run**.

## What do we ask of the experts?

The concrete lists are in Part 4:
1. **The 8 deviating answers** — is the manual work correct, or the tool?
2. **The 7 "outside format" cases** — possibly adjust the ontology.
3. **The 23 model gaps** — extend, or unnecessary?
4. **The target values** for accuracy and coverage.

## Next steps

1. **Increase coverage** (enable the meaning-based search method).
2. **More sources** (set-up/implementation documents).
3. **Build the standard side + comparison** (the final objective).
4. Process the **expert review**.
5. **Update the ontology model**.
6. **Scale up** and **integrate** into the application.

---

# Part 4 — Review list for experts

The complete, concrete lists (all 8 deviating answers with tool answer vs. benchmark and quotation, all 7 "outside format" cases, and all 23 model gaps) are in the separate document **`4-review-list.md`** in this folder. In brief:
- **8 deviating answers** — where the tool deviates from the PDC benchmark; for each, the tool answer, the benchmark and the quotation.
- **7 "outside format"** — where the answer does not fit the answer list/format (candidates for ontology adjustment).
- **23 model gaps** — with, for each gap, an explanation of what is missing.

---

## Underlying files

In this documentation package (two folders):
- **human-readable/** — this document plus `README.md`, `1-summary-and-results.md`, `2-approach-and-build.md`, `3-deliverables-and-next-steps.md`, `4-review-list.md`.
- **for-ai/** — `project-context.md`, `golden-testset.md` (the full test set with benchmarks), `deliverables-and-test-scenarios.md`, `final-result.md`.

Not in this package (they are in the project repository): the raw results `analyse-resultaat.json`, the test set as `.json`, the anonymised source files (`.docx`) and the backend code.
