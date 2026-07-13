"""Use Case 1 analysis engine.

Builds the fund corpus + benchmark context, runs the "Pension Entitlement Auditor" via
Claude structured outputs (client.messages.parse) to produce a FundComparisonReport, then
VERIFIES every citation against the actual document text before returning. Falls back to a
grounded demo report when no Anthropic credentials are configured.

Two hard invariants keep the comparison honest:
  1. The fund side is described ONLY from fund documents; the standard side ONLY from
     benchmark documents (enforced in the prompt AND checked in verification).
  2. Every claim is backed by a verbatim quote whose presence is verified server-side.
"""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

from app.core.config import settings
from app.services import ontology
from app.services.documents import Document
from app.services.extraction import extract_text
from app.services.verification import verify_report
from app.schemas.comparison import (
    AnalysisResponse,
    EntitlementComparison,
    EntitlementComparisonLLM,
    FundComparisonReport,
    OntologyConcept,
    ProvisionSource,
    ReportMetaLLM,
)

# How many per-theme analysis calls run concurrently. 11 themes + 1 metadata call = 12 tasks;
# running them in a single wave keeps wall-clock close to one call instead of summing them.
MAX_PARALLEL = 12

# Bump this whenever the prompt or analysis logic changes, so the on-disk result cache is
# invalidated and old runs are not served with new logic.
PROMPT_VERSION = "4"

SYSTEM_PROMPT = """\
You are an expert actuarial auditor for the Dutch Wet toekomst pensioenen (Wtp) transition. \
You compare a specific pension fund's rules against a STANDARD product, for pension experts \
who must be able to trust and audit every statement.

=== TWO SEPARATE SIDES — NEVER MIX THEM ===
The corpus is split into two clearly labelled parts:
  • FUND CORPUS      → the fund's own rules ("huidige regeling van het fonds").
  • BENCHMARK / STANDARD PRODUCT REFERENCES → the standard AllVida/Qwik product.

ABSOLUTE RULE: describe the FUND side (current_points, current_detail, current_sources) using \
ONLY the FUND CORPUS, and the STANDARD side (standard_points, standard_detail, standard_sources) \
using ONLY the BENCHMARK references. NEVER take a number, percentage or rule from a fund \
document and present it as the standard product (and vice versa). If the benchmark documents do \
not state something about the standard product, say so plainly rather than borrowing the fund's \
figures. Mixing the two sides is the single worst error you can make.

=== EVIDENCE IS MANDATORY ===
Every factual claim must be backed by a source in current_sources / standard_sources with:
  • document_name = the EXACT filename as shown in the corpus header ("file: <name>").
  • page_number   = the number from the nearest "--- page N ---" marker.
  • quote         = text copied VERBATIM, character-for-character, from that document.
Do NOT invent, paraphrase, round, or "improve" quotes. If you cannot find a verbatim quote in \
the correct corpus to support a point, do not assert that point. A server-side check will reject \
any quote it cannot find in the cited document — unsupported claims will be flagged, so grounding \
protects your credibility.

=== OUTPUT STYLE ===
  • Write ALL member-facing text in clear, plain Dutch.
  • current_points and standard_points are the PRIMARY output and the FIRST thing the reader sees. \
For EVERY area you include you MUST fill BOTH lists with at least one, preferably 2-4, short \
scannable bullets (one concise sentence each). NEVER leave them empty and never write "niet \
vermeld" — if you can cite a source for a side, you can write a bullet for it. The bullets, not \
the impact text, must let the reader see the difference at a glance.
  • impact_explanation is a SHORT secondary summary (2-4 sentences) — it must NOT be the only place \
the facts appear. Put the facts in the bullets first. PLAIN DUTCH WORDS only; absolutely NO \
formulas, LaTeX, or math symbols (no "$", "\\sum", subscripts, etc.).
  • key_differences: the concrete differences only. See the consistency rule below.
  • current_detail / standard_detail: optional longer background (shown in a dropdown).
  • required_qwik_configuration: a compact JSON string of Qwik rule-engine parameters.

=== WHAT COUNTS AS A GAP (consistency is mandatory) ===
Set gap_detected=true and a non-None severity ONLY for a genuine difference between the fund rule \
and the standard product. A difference the standard can absorb via parameters (coverage %, \
grondslag-definitie, a separate risicopremie, overgangsrechten) that leaves NOTHING actually \
different is NOT a gap: set gap_detected=false, deviation_severity="None", AND key_differences=[].
HARD RULE — these must always agree:
  • If key_differences is non-empty → gap_detected MUST be true and deviation_severity MUST be \
Low, Medium or High (never "None"). A card that lists a difference can never be counted as "geen \
afwijking".
  • If gap_detected is false → key_differences MUST be empty and deviation_severity MUST be "None".
Use severity Low for differences that fully fit the standard but deserve a note (e.g. an \
implementation/build item), Medium for a configuration choice that needs deliberate attention, \
High for a structural gap the standard cannot represent.

=== STANDARD PRODUCT ONTOLOGY ===
A section "STANDARD PRODUCT ONTOLOGY (relevant concepts per theme)" gives you authoritative \
definitions and domain values from the single source of truth (the OntologySnapshot). Prefer it \
for grounding the STANDARD side. You MAY quote from it verbatim; when you do, set document_name to \
the ontology filename shown in the corpus.

Grounding checks and the ontology proof are added by the system afterwards — you only need to \
produce the comparison fields and their verbatim sources. Output must exactly match the schema."""


def _theme_instruction(theme: str, ontology_block: str) -> str:
    """The per-theme user instruction (the fund/benchmark corpus is sent as a cached block)."""
    return (
        f"=== STANDARD PRODUCT ONTOLOGY — relevant concepts for this theme ===\n{ontology_block}\n\n"
        f"=== YOUR TASK ===\nProduce exactly ONE EntitlementComparison for the theme: '{theme}'. "
        f"Set `area` to '{theme}'. Describe the fund side ONLY from the FUND CORPUS and the standard "
        "side ONLY from the BENCHMARK references + the ontology concepts above, each with verbatim "
        "quotes. Follow the gap/consistency rules exactly."
    )


META_SYSTEM = (
    "You extract two facts from the provided Dutch pension corpus: the fund name and the intended "
    "transition date. Return fund_name (the pension fund this corpus is about) and "
    "target_transition_date (ISO YYYY-MM-DD if possible, else the date as written)."
)


def _extract_all(docs: list[Document]) -> list[tuple[Document, str]]:
    return [(d, extract_text(d.path, settings.MAX_DOC_CHARS)) for d in docs]


def _is_ontology(d: Document) -> bool:
    return "ontology" in d.filename.lower() or "ontology" in d.doc_type.lower()


def _prepare_corpus(
    fund_docs: list[Document], benchmark_docs: list[Document]
) -> tuple[list[tuple[Document, str]], list[tuple[Document, str]], list[tuple[Document, str]], list]:
    """Return (fund_texts, benchmark_index, benchmark_prompt, ontology_concepts).

    For the ontology the VERIFICATION index gets the full rendering (so any quoted concept can
    be checked), while the PROMPT only gets the deterministically retrieved concepts per theme
    (bounded, so context stays focused). The loaded concepts are also returned so the backend can
    attach verbatim rows to each finding for visible proof.
    """
    fund_docs_text = _extract_all(fund_docs)
    benchmark_index: list[tuple[Document, str]] = []
    benchmark_prompt: list[tuple[Document, str]] = []
    ontology_concepts: list = []
    for d in benchmark_docs:
        if _is_ontology(d):
            concepts = ontology.load_concepts(d.path)
            ontology_concepts = concepts
            benchmark_index.append((d, ontology.full_text(concepts, 10_000_000)))
            benchmark_prompt.append((d, ontology.retrieve(concepts)))
        else:
            txt = extract_text(d.path, settings.MAX_DOC_CHARS)
            benchmark_index.append((d, txt))
            benchmark_prompt.append((d, txt))
    return fund_docs_text, benchmark_index, benchmark_prompt, ontology_concepts


def _match_theme(area: str) -> str | None:
    """Map a finding's area to a canonical theme (exact, else substring/first-word)."""
    a = area.strip().lower()
    for t in ontology.CANONICAL_THEMES:
        if t.lower() == a:
            return t
    for t in ontology.CANONICAL_THEMES:
        tl = t.lower()
        if tl in a or a in tl or a.split()[0] == tl.split()[0]:
            return t
    return None


def _cap(text: str, limit: int) -> str:
    text = " ".join(text.split())  # collapse whitespace/newlines for compact display
    return text[:limit].rstrip() + "…" if len(text) > limit else text


def _attach_ontology(report: FundComparisonReport, concepts: list) -> FundComparisonReport:
    """Attach verbatim ontology rows (Name/Definition/Clarification) per finding — visible proof
    pulled straight from the snapshot. Definitions/clarifications are capped to a readable preview
    (the ExternalId lets an expert look up the full row); a handful of concepts per theme keeps it
    scannable rather than a wall of text."""
    if not concepts:
        return report
    by_theme = ontology.retrieve_structured(concepts, per_theme=4)
    for item in report.entitlements:
        theme = _match_theme(item.area)
        rows = by_theme.get(theme, []) if theme else []
        item.ontology_concepts = [
            OntologyConcept(
                external_id=c.external_id, name=c.name.replace("_", " "),
                definition=_cap(c.definition, 320), clarification=_cap(c.clarification, 480),
            )
            for c in rows
        ]
    return report


def _shared_context(
    fund_docs_text: list[tuple[Document, str]],
    benchmark_prompt: list[tuple[Document, str]],
) -> str:
    """The corpus shared by every per-theme call (sent as a cached block). The ontology is NOT
    included here — the relevant ontology concepts are injected per theme in the instruction."""
    parts: list[str] = ["# FUND CORPUS (the specific fund — 'waar hebben mensen recht op')\n"]
    for d, text in fund_docs_text:
        parts.append(f"\n## [{d.doc_type}] file: {d.filename}\n{text}\n")
    parts.append("\n\n# BENCHMARK / STANDARD PRODUCT REFERENCES (the standard to compare against)\n")
    for d, text in benchmark_prompt:
        if _is_ontology(d):
            continue  # ontology concepts are injected per-theme
        parts.append(f"\n## [{d.doc_type}] file: {d.filename}\n{text}\n")
    return "".join(parts)


# --- Result cache: same document set -> identical result (deterministic repeat runs) ------

def _cache_dir():
    return settings.uploads_path / "_analysis_cache"


def _cache_key(
    fund_docs_text: list[tuple[Document, str]],
    benchmark_index: list[tuple[Document, str]],
) -> str:
    h = hashlib.sha256()
    h.update(PROMPT_VERSION.encode())
    h.update((settings.CLAUDE_MODEL or "").encode())
    for d, text in sorted(fund_docs_text + benchmark_index, key=lambda t: t[0].filename):
        h.update(d.filename.encode("utf-8"))
        h.update(b"\0")
        h.update(text.encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()


def _load_cache(key: str) -> FundComparisonReport | None:
    p = _cache_dir() / f"{key}.json"
    if not p.exists():
        return None
    try:
        return FundComparisonReport.model_validate_json(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _store_cache(key: str, report: FundComparisonReport) -> None:
    d = _cache_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{key}.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")


def _finalise(
    report: FundComparisonReport,
    fund_docs_text: list[tuple[Document, str]],
    benchmark_docs_text: list[tuple[Document, str]],
) -> FundComparisonReport:
    """Verify citations, then enforce card/summary consistency so the UI can never contradict
    itself (a card that lists a difference must count as an afwijking, and vice versa)."""
    report = verify_report(report, fund_docs_text, benchmark_docs_text)
    for item in report.entitlements:
        if item.key_differences:
            # A listed difference is always an afwijking of at least Low severity.
            item.gap_detected = True
            if item.deviation_severity == "None":
                item.deviation_severity = "Low"
        elif not item.gap_detected:
            # No gap → no severity, no dangling differences.
            item.deviation_severity = "None"
    return report


def analyse(fund_docs: list[Document], benchmark_docs: list[Document]) -> AnalysisResponse:
    fund_names = [d.filename for d in fund_docs]
    bench_names = [d.filename for d in benchmark_docs]

    fund_docs_text, benchmark_index, benchmark_prompt, ont_concepts = _prepare_corpus(
        fund_docs, benchmark_docs
    )

    if not settings.has_ai_credentials:
        report = _attach_ontology(
            _finalise(_demo_report(fund_docs), fund_docs_text, benchmark_index), ont_concepts
        )
        return AnalysisResponse(
            mode="demo", model=None,
            fund_documents=fund_names, benchmark_documents=bench_names, report=report,
        )

    # Deterministic repeat: identical document set -> return the exact stored result.
    key = _cache_key(fund_docs_text, benchmark_index)
    cached = _load_cache(key)
    if cached is not None:
        return AnalysisResponse(
            mode="live", model=settings.CLAUDE_MODEL, cached=True,
            fund_documents=fund_names, benchmark_documents=bench_names, report=cached,
        )

    import anthropic

    # Extra retries so the concurrent burst rides out transient 429/rate-limit responses.
    client = (
        anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY, max_retries=4)
        if settings.ANTHROPIC_API_KEY
        else anthropic.Anthropic(max_retries=4)
    )
    shared = _shared_context(fund_docs_text, benchmark_prompt)

    def _stream_parse(system: str, user: str, schema, max_tokens: int):
        # Streaming avoids the SDK's non-streaming 10-minute guard.
        with client.messages.stream(
            model=settings.CLAUDE_MODEL, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": user}], output_format=schema,
        ) as stream:
            return stream.get_final_message().parsed_output

    def _call_theme(theme: str):
        try:
            instruction = _theme_instruction(theme, ontology.retrieve_one(ont_concepts, theme))
            return _stream_parse(SYSTEM_PROMPT, shared + "\n\n" + instruction,
                                 EntitlementComparisonLLM, max_tokens=6000)
        except Exception:
            return None

    def _call_meta():
        try:
            return _stream_parse(META_SYSTEM, shared, ReportMetaLLM, max_tokens=500)
        except Exception:
            return None

    # Fan out: one small metadata call + one call per theme, all concurrent. Wall-clock is the
    # slowest wave instead of the sum — much faster than one giant call, and each theme is
    # analysed in isolation so information cannot bleed between subjects.
    themes = ontology.CANONICAL_THEMES
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as ex:
        meta_future = ex.submit(_call_meta)
        theme_futures = [ex.submit(_call_theme, t) for t in themes]
        meta = meta_future.result()
        theme_results = [f.result() for f in theme_futures]

    if all(r is None for r in theme_results):
        # Total failure — degrade to the clearly labelled demo report rather than 500.
        report = _attach_ontology(
            _finalise(_demo_report(fund_docs), fund_docs_text, benchmark_index), ont_concepts
        )
        return AnalysisResponse(
            mode="demo", model=settings.CLAUDE_MODEL,
            fund_documents=fund_names, benchmark_documents=bench_names, report=report,
        )

    entitlements: list[EntitlementComparison] = []
    for theme, result in zip(themes, theme_results):
        if result is not None:
            item = result.to_entitlement()
            if not item.area.strip():
                item.area = theme
        else:
            item = EntitlementComparison(
                area=theme, gap_detected=False, deviation_severity="None",
                impact_explanation="Dit onderwerp kon niet automatisch worden geanalyseerd. "
                "Start de vergelijking opnieuw.",
            )
        entitlements.append(item)

    report = FundComparisonReport(
        fund_name=(meta.fund_name if meta else "") or "Onbekend pensioenfonds",
        target_transition_date=(meta.target_transition_date if meta else "") or "onbekend",
        entitlements=entitlements,
    )

    # Anti-hallucination guard + card/summary consistency + visible ontology proof, then cache.
    report = _attach_ontology(_finalise(report, fund_docs_text, benchmark_index), ont_concepts)
    _store_cache(key, report)

    return AnalysisResponse(
        mode="live", model=settings.CLAUDE_MODEL, cached=False,
        fund_documents=fund_names, benchmark_documents=bench_names, report=report,
    )


def _demo_report(fund_docs: list[Document]) -> FundComparisonReport:
    """Grounded sample used only when no Anthropic API key is configured.

    Citations here are still run through the same verification step, so any quote that does
    not actually occur in the documents is honestly shown as unverified in the UI.
    """
    fpr = next((d.filename for d in fund_docs if "reglement" in d.doc_type.lower()
                or "FPR" in d.doc_type), "FPR")
    abtn = next((d.filename for d in fund_docs if "ABTN" in d.doc_type), "ABTN")

    return FundComparisonReport(
        fund_name="Stichting Pensioenfonds (SPF) — demovergelijking",
        target_transition_date="2026-01-01",
        entitlements=[
            EntitlementComparison(
                area="Opbouwsystematiek",
                current_points=[
                    "Middelloonregeling (uitkeringsovereenkomst) met vaste opbouwpercentages.",
                    "Doorsneesystematiek: leeftijdsonafhankelijke premie/opbouw.",
                ],
                standard_points=[
                    "Beschikbare premieregeling (premieovereenkomst) met een vlak premiepercentage.",
                    "Premie wordt belegd op een persoonlijke pensioenrekening.",
                ],
                key_differences=[
                    "Van een gegarandeerde aanspraak (DB) naar een belegd kapitaal (DC).",
                    "Het beleggingsrisico verschuift naar de deelnemer.",
                ],
                current_detail=(
                    "De legacy-regeling is een geïndexeerde middelloonregeling. De hoogte van het "
                    "pensioen hangt af van dienstjaren en het gemiddelde salaris."
                ),
                standard_detail=(
                    "In het standaardproduct wordt een vast percentage van de grondslag ingelegd en "
                    "belegd; de uitkering volgt uit het opgebouwde kapitaal."
                ),
                gap_detected=True,
                deviation_severity="High",
                impact_explanation=(
                    "De overgang van een gegarandeerde middelloonaanspraak naar een belegd kapitaal is "
                    "structureel: de zekerheid verdwijnt en de deelnemer draagt voortaan het "
                    "beleggingsrisico. Dit vraagt om zorgvuldige communicatie en maatwerk."
                ),
                required_qwik_configuration=(
                    '{"karakter_pensioenovereenkomst":"premieovereenkomst","opbouw":"kapitaal"}'
                ),
                current_sources=[
                    ProvisionSource(
                        document_name=fpr, section="Opbouw",
                        page_number=1,
                        quote="middelloonregeling",
                    )
                ],
                standard_sources=[],
            ),
            EntitlementComparison(
                area="Indexatie en Toeslagen",
                current_points=[
                    "Voorwaardelijke toeslag, gekoppeld aan de beleidsdekkingsgraad.",
                ],
                standard_points=[
                    "Rendement wordt rechtstreeks bijgeschreven op het persoonlijke vermogen.",
                ],
                key_differences=[
                    "Sturing via dekkingsgraad vervalt; schommelingen lopen via de solidariteitsreserve.",
                ],
                current_detail="",
                standard_detail="",
                gap_detected=True,
                deviation_severity="Medium",
                impact_explanation=(
                    "Toeslagverlening op basis van de dekkingsgraad verdwijnt. Het pensioen beweegt "
                    "voortaan mee met het beleggingsrendement, gedempt via de solidariteitsreserve."
                ),
                required_qwik_configuration='{"toeslag":"rendementsbijschrijving"}',
                current_sources=[
                    ProvisionSource(
                        document_name=abtn, section="Toeslagbeleid",
                        page_number=1,
                        quote="toeslag",
                    )
                ],
                standard_sources=[],
            ),
        ],
    )
