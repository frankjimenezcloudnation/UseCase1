# WTP component analysis — human-readable document set

_Use Case 1 · test fund SPF · 20 July 2026_

This set describes in plain language what we have built: a tool that automatically determines, for each topic from the pension ontology model, what a fund's scheme prescribes — with source references, so that an expert can verify every answer.

Intended for pension experts, product owners, and stakeholders who do not need to read technical details.

## Reading guide

| Document | About |
|---|---|
| [1 — Summary and results](1-summary-and-results.md) | What has been created, the test outcomes, and what they mean. Start here. |
| [2 — Approach and build](2-approach-and-build.md) | How it works: the ontology model, the test set, the link with the PDC, the anonymization, and the tool — in plain language. |
| [3 — Deliverables and next steps](3-deliverables-and-next-steps.md) | What exactly has been delivered, how it was tested, what the experts need to assess, and the next steps. |
| [4 — Review list for experts](4-review-list.md) | The specific points requiring judgment: all 8 deviating answers, 7 "out-of-format" cases, and 23 model gaps. |

## What is included in this package?

This package consists of two folders (see `README.md` in the zip):
- **human-readable/** — this set (documents 1 through 4 + this overview).
- **for-ai/** — the technical/structured documents for AI agents and developers: `project-context.md`, `golden-testset.md` (the complete test set with benchmarks), `deliverables-and-test-scenarios.md`, `final-result.md`.

The underlying **data and code files** (the raw results `analyse-resultaat.json`, the golden test set as `.json`, the anonymized source files, and the backend code) are **not included in this package** — they are located in the project repository.

## In one sentence

The tool is reliable and cautious (it does not invent anything and always refers to the source); the benefit now lies primarily in increasing the **coverage** — the number of topics for which it finds an answer — and in the yet-to-be-built **comparison between the fund and the IG&H standard**.
