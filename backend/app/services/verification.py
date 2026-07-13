"""Evidence verification — the anti-hallucination guard.

After Claude returns a FundComparisonReport, we do NOT trust its citations blindly.
For every ProvisionSource we check two things against the ACTUAL extracted document text:

  1. Grounding: the quote must genuinely occur in the cited document (exact normalised
     substring, or — to survive PDF extraction noise like hyphenation/spacing — a high
     token-overlap match).
  2. Side integrity: a fund-side citation must point at a FUND document and a standard-side
     citation at a BENCHMARK document. This is what stops the fund's own FPR numbers from
     being presented as "the standard product".

A source that fails either check is marked verified=False. A comparison is
evidence_verified only when BOTH sides carry at least one verified source (or a side
legitimately makes no factual claim). Unverified findings are surfaced as such in the UI
so pension experts can see exactly what is and isn't grounded.
"""

from __future__ import annotations

import re

from app.schemas.comparison import EntitlementComparison, FundComparisonReport, ProvisionSource
from app.services.documents import Document

# Minimum fraction of a quote's word-tokens that must appear (in order-independent form)
# in the cited document for a fuzzy match, when an exact normalised substring is not found.
_TOKEN_OVERLAP_THRESHOLD = 0.85
# Quotes shorter than this (in tokens) are only accepted via exact substring — too short
# to trust a fuzzy overlap on.
_MIN_TOKENS_FOR_FUZZY = 6


def _normalise(text: str) -> str:
    text = text.lower().replace("­", "")  # drop soft hyphens
    text = re.sub(r"[^0-9a-zà-ÿ%]+", " ", text)  # keep letters/digits/percent
    return re.sub(r"\s+", " ", text).strip()


def _tokens(text: str) -> list[str]:
    return _normalise(text).split()


class SourceIndex:
    """Maps a model-supplied document_name to a real Document + its extracted, normalised text."""

    def __init__(self, docs_with_text: list[tuple[Document, str]]):
        self._entries = [
            {
                "doc": doc,
                "norm": _normalise(text),
                "tokens": set(_tokens(text)),
            }
            for doc, text in docs_with_text
        ]

    def match(self, document_name: str) -> dict | None:
        """Best-effort match of a cited name to an indexed document."""
        want = document_name.lower().strip()
        want_stem = re.sub(r"\.(pdf|docx|xlsx|xls)$", "", want)
        best = None
        best_score = 0.0
        for e in self._entries:
            fname = e["doc"].filename.lower()
            fstem = re.sub(r"\.(pdf|docx|xlsx|xls)$", "", fname)
            dtype = e["doc"].doc_type.lower()
            if fname == want or fstem == want_stem:
                return e
            score = 0.0
            if want_stem and (want_stem in fstem or fstem in want_stem):
                score = 0.9
            else:
                # token overlap on the name/label as a weak fallback
                wt = set(_tokens(want))
                ft = set(_tokens(fstem)) | set(_tokens(dtype))
                if wt:
                    score = len(wt & ft) / len(wt)
            if score > best_score:
                best_score, best = score, e
        return best if best_score >= 0.5 else None


def _quote_grounded(quote: str, entry: dict) -> str:
    """Return 'exact', 'fuzzy' or 'none' for how the quote matches the document text."""
    q_norm = _normalise(quote)
    if not q_norm:
        return "none"
    if q_norm in entry["norm"]:
        return "exact"
    q_tokens = _tokens(quote)
    if len(q_tokens) < _MIN_TOKENS_FOR_FUZZY:
        return "none"  # too short to fuzzy-match safely
    present = sum(1 for t in set(q_tokens) if t in entry["tokens"])
    return "fuzzy" if present / len(set(q_tokens)) >= _TOKEN_OVERLAP_THRESHOLD else "none"


def _verify_source(src: ProvisionSource, index: SourceIndex, required_role: str) -> str:
    entry = index.match(src.document_name)
    if entry is None:
        return "none"
    if entry["doc"].role != required_role:
        return "none"  # side integrity: cited the wrong kind of document
    return _quote_grounded(src.quote, entry)


# Points awarded per side by match quality, and corroboration bonus.
_SIDE_POINTS = {"exact": 40, "fuzzy": 25, "none": 0}


def _best_side_points(sources) -> int:
    return max((_SIDE_POINTS[s.match_quality] for s in sources), default=0)


def verify_report(
    report: FundComparisonReport,
    fund_docs_text: list[tuple[Document, str]],
    benchmark_docs_text: list[tuple[Document, str]],
) -> FundComparisonReport:
    """Set per-source verified/match_quality and per-comparison evidence_verified/score/level."""
    index = SourceIndex(fund_docs_text + benchmark_docs_text)

    for item in report.entitlements:
        for src in item.current_sources:
            src.match_quality = _verify_source(src, index, required_role="fund")
            src.verified = src.match_quality != "none"
        for src in item.standard_sources:
            src.match_quality = _verify_source(src, index, required_role="benchmark")
            src.verified = src.match_quality != "none"

        current_ok = any(s.verified for s in item.current_sources)
        standard_ok = any(s.verified for s in item.standard_sources)
        item.evidence_verified = current_ok and standard_ok

        # Evidence strength: each side contributes up to 40 (exact) / 25 (fuzzy), plus a
        # corroboration bonus for multiple independent verified sources.
        verified_count = sum(s.verified for s in item.current_sources) + sum(
            s.verified for s in item.standard_sources
        )
        corroboration = 20 if verified_count >= 3 else 10 if verified_count == 2 else 0
        score = _best_side_points(item.current_sources) + _best_side_points(item.standard_sources)
        score = min(100, score + corroboration)
        item.evidence_score = score
        item.evidence_level = "Hoog" if score >= 80 else "Middel" if score >= 50 else "Laag"

    return report


def verification_summary(item: EntitlementComparison) -> dict:
    """Small helper for logging/debugging which sources grounded."""
    return {
        "area": item.area,
        "evidence_verified": item.evidence_verified,
        "current_verified": sum(s.verified for s in item.current_sources),
        "standard_verified": sum(s.verified for s in item.standard_sources),
    }
