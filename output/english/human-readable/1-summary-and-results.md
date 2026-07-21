# 1 — Summary and results

## What is this about?

Under the Future Pensions Act (Wet toekomst pensioenen, Wtp), a pension fund must document exactly how its scheme is structured. The underlying **ontology model** contains approximately 2,600 individual topics (for example: "is there a minimum pensionable income?", "how is the date rounded?"). Each topic comes with a question and often a list of permitted answers.

Until now, such an analysis was done **by hand**. The goal of this project: to **automate** that work — the tool reads a fund's documents and answers the question for each topic, with a source reference and a confidence score attached.

As a test, we did this for one fund (**SPF**) and a fixed, verifiable selection of **102 topics** (together **106 unique questions**; because some topics contain multiple questions, **133 question instances** are processed in a run).

## What has been built?

- A **fixed test set** of 102 topics; for **71** of these, a manual SPF answer exists that serves as a benchmark.
- A **link** between the manual product description (PDC) and the ontology model.
- **Anonymised** versions of two standard documents, so that the tool can also be used for new funds without answers from another fund "leaking through".
- The **analysis tool** itself, which provides an answer with source and confidence for each topic.

## The results of the test

The tool processed 133 question instances:

| What | Outcome |
|---|---|
| Question instances processed | 133 |
| Answered (with source) | 40 (of which 24 with high confidence, 13 medium, 3 low) |
| Honestly "not found" | 93 |
| Analyses that failed | 0 |
| Verified source citations | 49 |
| Instances with an SPF benchmark | 87 (originating from the 71 topics with a benchmark) |
| Answered **and** verifiable against the manual work | 22 → **14 correct, 8 deviate (~64%)** |

**How to read the figures.** The honest measure is the last row: of the instances that the tool **did answer and that we could check (22)**, roughly **two thirds (14)** were correct. A "raw" score across all 87 instances with a benchmark comes out much lower (~28%), but that counts the 62 unanswered instances as errors — so that measure says more about **coverage** than about **correctness**. For all displayed answers the following holds: there is a literal citation from a fund document that has been automatically verified. So the tool does not make anything up. (There are 49 verified citations for 40 answers, because an answer can have multiple citations and there are also citations for a few "not found"/partial answers.)

## Examples

**Answered correctly (with source):**
- Type of agreement → *Flexible premium agreement* (origineel: "Flexibele premieovereenkomst").
- Participation in the scheme → *mandatory*.
- Maximum pensionable income → *yes, a maximum chosen by the fund* (with source location: € 38,611 in 2026).
- Basis → *pensionable income minus franchise*.

**Deviates — worth checking (not a hard error):**
- Minimum pensionable income: the tool says "yes" based on "at least nil" (origineel: "ten minste nihil"); the manual work says "no". This is a difference in interpretation ("at least nil" effectively means no lower limit).
- Form of the franchise: the tool chose "social security / AOW franchise"; the manual work says "nominal amount".

The full list of all 8 deviations is in [4 — Review list for experts](4-review-list.md).

## The main conclusion

- The tool is **reliable and cautious**: no failures, every answer substantiated, and where the documents provide no answer it honestly says "not found" instead of guessing.
- The biggest opportunity for improvement is **coverage** (40 out of 133). This is because the tool currently searches on simple keywords (the smarter "meaning"-based search method is not yet enabled) and because some details are simply not in the regulations.
- The deviating answers are mainly **nuances** that call for expert judgment — exactly as intended: the tool prepares, the expert decides.
- The **end objective** — comparing the fund with the IG&H standard per topic — is still a next step (see document 3).

Further reading: [how it works](2-approach-and-build.md) · [deliverables and next steps](3-deliverables-and-next-steps.md) · [review list](4-review-list.md).
