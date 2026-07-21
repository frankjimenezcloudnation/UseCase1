# 3 — Deliverables and next steps

## What has been delivered?

| # | Delivered | What it is | Status |
|---|---|---|---|
| 1 | Fixed test set (102 topics) | The set of topics; 71 with a manual SPF answer as benchmark | Done |
| 2 | Anonymized standard sources | Standard documents without fund-specific information | Done |
| 3 | PDC ↔ ontology link | Which ontology question belongs to which PDC topic (with confidence) | Done |
| 4 | Analysis tool (fund side) | Answers per topic with source + confidence | Done |
| 5 | Validation report | Compares the tool answers with the manual work | Done |
| 6 | List of 23 model gaps | Where the ontology model does not capture the PDC distinction | Done (for review) |
| 7 | Smarter "meaning"-based search method | Increases coverage | To do |
| 8 | Integration into the application | Component analysis via the web application | To do |
| 9 | Standard-side analysis (IG&H) | Determines per topic what IG&H offers, from PDC + standard specification + Qwik (multiple values) | To do |
| 10 | Comparison fund ↔ IG&H standard | Sets the fund value against the standard set per topic and identifies the differences — the end objective | To do |

## Test scenarios per deliverable

Every deliverable has a test that checks whether it works — here in plain language (the technical Given/When/Then version is in the accompanying **for-ai** folder, file `deliverables-and-test-scenarios.md`):

1. **Test set complete & reusable** (for deliverable 1). The recorded test set contains 102 topics (106 unique questions), each with an ontology question; 71 have an SPF benchmark. Reloading the frozen test set yields exactly the same list. → **Passed**.
2. **Anonymization leaks no fund names** (2). The anonymized documents no longer contain any fund names; the originals are unchanged. → **Passed** (0 fund names).
3. **Link refers only to existing topics** (3). Every linked ontology property actually exists and has a confidence score. → **Passed** (102 linked, 0 invented).
4. **The tool substantiates and does not invent** (4). For a topic that is in the regulations, the tool gives the correct answer with a verified citation; for a topic that is not, it honestly says "not found". → **Passed** (0 failures · 49 verified citations).
5. **The validation counts honestly** (5). "Yes" variants (origineel: "Ja") count as "yes" (origineel: "ja"); unit hints such as "years" (origineel: "jaren") are not counted as errors. → **Passed** (~64% on the 22 answered, verifiable instances).
6. **Model gaps are substantiated** (6). Each of the 23 gaps has an explanation (for example: "commutation moment" (origineel: "afkoopmoment") lacks the option *emigration* (origineel: "emigratie")). → **Passed** (23 gaps).
7. **Meaning-based search method increases coverage** (7). With the smarter search method, more topics are answered than the current 40 of 133, without loss of reliability. → **Still to run**.
8. **Component analysis via the application** (8). Via the web application, an analysis yields the same result as the standalone tool and displays it in the interface. → **Still to run**.
9. **Standard side is correct and multi-valued** (9). For a topic where IG&H allows multiple options (e.g. type of scheme), the standard side yields all allowed values, from the right source (PDC before specification before Qwik). → **Still to run**.
10. **Comparison identifies the correct differences** (10). For a topic where the fund value falls within the standard → "fits within standard"; if it falls outside → "genuine deviation". → **Still to run**.

In short: the delivered components (1 through 6) have **passed**; 7 through 10 are still open because those components are yet to be built.

## What do we ask of the experts?

The tool does the preparatory work; these points require human judgment. The full, concrete lists are in [4 — Review list for experts](4-review-list.md):

1. **The 8 deviating answers.** Is the manual work right, or does the tool have a good point? Example: does SPF have a minimum pensionable income or not ("at least nil" (origineel: "ten minste nihil"))?
2. **The 7 "out of format" cases.** Here the answer found does not fit neatly into the prescribed choice list — the ontology model may need to be adjusted.
3. **The 23 model gaps.** For each gap: should the ontology model be extended, or is the distinction unnecessary?
4. **The target values.** What accuracy and coverage do we consider "good enough"? (Currently: ~64% on the answered, verifiable instances.)

## Next steps (proposal)

1. **Increase coverage** — enable the smarter search method (meaning instead of keywords); it is already in place in the codebase.
2. **More sources** — also include set-up/implementation documents for topics that are not in the regulations.
3. **Build the standard side + comparison** — determine the IG&H standard per topic and compare fund vs. standard (the end objective).
4. **Incorporate the expert review** of the points above.
5. **Update the ontology model** with the findings.
6. **Scale up** from 102 to more topics, and **integrate** into the application for daily use.

Further reading: [summary and results](1-summary-and-results.md) · [approach and build](2-approach-and-build.md) · [review list](4-review-list.md).
