"""Structured extraction schema for Use Case 1 — Pension Fund vs Standard Product.

Claude is forced to emit exactly this shape via structured outputs, so downstream
consumers (the Qwik rule engine, the frontend, Checkmate) get typed data.

Design notes:
- The fund side ("huidige regeling") and the standard side are described in SEPARATE
  bullet lists, each with its OWN citations, so the two can never be conflated.
- All narrative text is plain Dutch — NO LaTeX / math notation.
- `verified` (per source) and `evidence_verified` (per comparison) are SYSTEM fields:
  the backend recomputes them after the model returns by matching each quote against
  the extracted document text. The model must not rely on them.
"""

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["High", "Medium", "Low", "None"]


class ProvisionSource(BaseModel):
    """Provenance for a single extracted clause — the audit trail to the source document."""

    document_name: str = Field(
        description="EXACT filename of the source document as provided in the corpus, "
        "e.g. 'SPF Flexibele Premieregeling 2026.1_def.pdf'. Do not paraphrase the name."
    )
    section: str = Field(description="Specific section or article reference, e.g. 'Art. 4.1.1'")
    page_number: int = Field(description="Page number (from the '--- page N ---' markers) where the clause is found")
    quote: str = Field(
        description="VERBATIM text copied character-for-character from the document. "
        "Never summarise or reword. This exact string must be findable in the source."
    )
    verified: bool = Field(
        default=False,
        description="SYSTEM FIELD — do not set. The backend sets this to true only when the "
        "quote is found in the cited document and the document is on the correct side.",
    )
    match_quality: Literal["exact", "fuzzy", "none"] = Field(
        default="none",
        description="SYSTEM FIELD — do not set. How the quote matched the source: 'exact' "
        "(verbatim substring), 'fuzzy' (high word overlap) or 'none' (not found / wrong side).",
    )


class EntitlementComparison(BaseModel):
    """One thematic comparison between the fund's rules and the standard product."""

    area: str = Field(
        description="Thematic area, e.g. 'Opbouwsystematiek', 'Partnerpensioen', "
        "'Indexatie', 'Compensatie', 'Beleggingsrisico'"
    )
    current_points: list[str] = Field(
        default_factory=list,
        description="Short scannable bullet points describing the FUND's rule, derived ONLY from "
        "fund documents (FPR/ABTN/Transitieplan). Each bullet one concise Dutch sentence, no LaTeX.",
    )
    standard_points: list[str] = Field(
        default_factory=list,
        description="Short scannable bullet points describing the STANDARD product, derived ONLY from "
        "benchmark documents (AllVida-spec/Qwik/Ontology/PDC). One concise Dutch sentence each, no LaTeX.",
    )
    key_differences: list[str] = Field(
        default_factory=list,
        description="The concrete differences between fund and standard, as short Dutch bullets. "
        "Empty if the fund rule fully fits the standard product.",
    )
    current_detail: str = Field(
        default="",
        description="Longer plain-Dutch explanation of the fund rule (shown in a 'more info' dropdown). No LaTeX.",
    )
    standard_detail: str = Field(
        default="",
        description="Longer plain-Dutch explanation of the standard product (shown in a dropdown). No LaTeX.",
    )
    gap_detected: bool = Field(
        description="True only if the fund rule genuinely differs from what the standard product can represent"
    )
    deviation_severity: Severity = Field(
        description="Impact severity if transitioned to the standard: High, Medium, Low or None"
    )
    impact_explanation: str = Field(
        description="What the difference means for the member and the transition, in PLAIN DUTCH. "
        "No formulas, no LaTeX, no math symbols — explain the effect in words."
    )
    required_qwik_configuration: str = Field(
        default="",
        description="Proposed configuration parameters for the Qwik rule engine (JSON string)",
    )
    current_sources: list[ProvisionSource] = Field(
        default_factory=list,
        description="Provenance for the FUND-side claims. Must cite FUND documents only.",
    )
    standard_sources: list[ProvisionSource] = Field(
        default_factory=list,
        description="Provenance for the STANDARD-side claims. Must cite BENCHMARK documents only.",
    )
    evidence_verified: bool = Field(
        default=False,
        description="SYSTEM FIELD — do not set. Backend sets true when both sides have at least one "
        "verified source.",
    )
    evidence_score: int = Field(
        default=0,
        description="SYSTEM FIELD — do not set. Backend-computed evidence strength (0-100) based on "
        "whether each side has a verified quote, exact vs fuzzy match, and corroboration.",
    )
    evidence_level: Literal["Hoog", "Middel", "Laag"] = Field(
        default="Laag",
        description="SYSTEM FIELD — do not set. Band of evidence_score: Hoog (>=80), Middel (50-79), "
        "Laag (<50). Laag findings need expert review.",
    )


class FundComparisonReport(BaseModel):
    """Top-level result returned to the frontend."""

    fund_name: str
    target_transition_date: str = Field(description="Expected transition date, e.g. '2026-01-01'")
    entitlements: list[EntitlementComparison]


class AnalysisResponse(BaseModel):
    """API envelope: the report plus run metadata."""

    mode: Literal["live", "demo"] = Field(
        description="'live' = analysed by Claude; 'demo' = grounded sample (no API key configured)"
    )
    model: str | None = Field(default=None, description="Claude model used (live mode only)")
    fund_documents: list[str] = Field(description="Fund-corpus documents analysed")
    benchmark_documents: list[str] = Field(description="Benchmark/standard reference documents used")
    cached: bool = Field(
        default=False,
        description="True when this result was returned from cache (identical to the previous run "
        "on the same document set) rather than recomputed.",
    )
    report: FundComparisonReport


class AnalysisRequest(BaseModel):
    """Which documents to analyse. Empty lists fall back to the full default set."""

    fund_document_ids: list[str] = Field(default_factory=list)
    benchmark_document_ids: list[str] = Field(default_factory=list)


class DocumentPatch(BaseModel):
    """Editable fields for a document (role / human label)."""

    role: Literal["fund", "benchmark"] | None = None
    doc_type: str | None = None
