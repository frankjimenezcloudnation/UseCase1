# 2 — Approach and build

This document explains in plain language how the tool came about. Five steps.

## Step 1 — The building blocks: the ontology model and the PDC

- **The ontology model** (`OntologySnapshot`) is the shared "language" for pension products. It contains ~2,600 **topics** (properties), each with a name, a question and — where applicable — a short list of permitted answers. The topics are grouped into **classes** (for example the class "Pre-portal" (origineel: "Voorportaal") with a handful of questions under it).
- **The PDC Beroepse** is the manual product description: for each topic and each fund, the applicable answer has been ticked. This is the **benchmark** against which we check the tool — it is expressly not a source from which the tool may draw answers for the fund.

## Step 2 — A fixed, verifiable test set

We do not start with all 2,600 topics, but with a **fixed selection of 102 linked topics**. For **71** of these, a manual SPF answer exists that serves as a benchmark; those 71 allow us to check the tool's answers. (The 102 were selected because they proved linkable between PDC and ontology, not because they all have a benchmark.)

Those 102 came about by linking the manual PDC to the ontology model. That turned out not to be possible one-to-one on name alone (16 direct matches), because the PDC uses business names and the ontology uses technical names. We therefore linked at **class level** and with the help of the permitted answers.

## Step 3 — The linking (mapping) through language understanding

To link the PDC topics reliably to the right ontology questions, we had a language model compare the **meaning** (not just the words). Result: **102 of the 152** PDC topics linked, each with a confidence score (48 did not reach a link, 2 did not yield a clear outcome).

This also brought **model gaps** to light: cases where the PDC makes a distinction that the ontology model cannot (yet) express. Within the test set of 102 topics there are **23** of these (across all 152 PDC topics there were 36). Examples: for "commutation moment" (origineel: "afkoopmoment") the option *emigration* (origineel: "emigratie") is missing; for "pre-portal" (origineel: "voorportaal") the distinction *mandatory/voluntary* (origineel: "verplicht/vrijwillig") is missing. This is valuable input for improving the model.

## Step 4 — Anonymizing the standard documents

Two documents (the standard product specification and a technical analysis) already contain fund-specific answers. If the tool were to use those as a source for a fund, it would be "cheating". Because the tool must also be usable for **new funds** — and because these two documents will later feed the **IG&H standard side** — we **anonymized** them:

- fund names (SPF, SPD, AKZO, …) replaced by a neutral designation `[FONDS]`;
- the fund-specific text blocks and separate "Funds" (origineel: "Fondsen") paragraphs removed.

Check afterwards: **zero** fund names left in the anonymized versions. The originals are unchanged.

## Step 5 — The tool

For each topic, the tool does the following:

1. **Search** the fund documents (regulations, ABTN, implementation plan, operating manual) for relevant passages.
2. **Answer** via a language model: it chooses — if there is a choice list — the best-fitting value, and always also gives a short explanation in plain language.
3. **Substantiate** with a literal quote (with page number). That quote is **automatically checked**: does it really appear in the named document? If not, it is marked as unverified.
4. **Be honest**: if no substantiation can be found, the tool says "not found" (origineel: "niet gevonden") instead of guessing.
5. Every answer gets a **confidence score** (high/medium/low), and a flag if the answer falls outside the expected choice list or format.

Important principle: the tool decides nothing definitively. It prepares and makes everything traceable; the expert judges.

## Where this is heading: fund vs. IG&H standard

The ultimate intention is a **comparison**: performing the same per-topic analysis for the **IG&H standard** as well (from the PDC, the standard specification and the Qwik analysis), and then determining per topic where the fund deviates from what IG&H offers. Here the standard often has **multiple** possible values per topic (a "menu"), while a fund usually makes one concrete choice. This fund-side analysis is the first half of that; the standard side and the comparison are the next step (see document 3).

Further reading: [summary and results](1-summary-and-results.md) · [deliverables and next steps](3-deliverables-and-next-steps.md) · [review list](4-review-list.md).
