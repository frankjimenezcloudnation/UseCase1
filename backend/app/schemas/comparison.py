"""Structured extraction schema for Use Case 1 — Pension Fund vs Standard Product.

Mirrors the Pydantic schema in the WTP Prototyping Engine technical specification
(FundComparisonReport). Claude is forced to emit exactly this shape via structured
outputs, so downstream consumers (the Qwik rule engine, Checkmate) get typed data.
"""

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["High", "Medium", "Low", "None"]


class ProvisionSource(BaseModel):
    """Provenance for a single extracted clause — the audit trail to the source PDF."""

    document_name: str = Field(description="Source document, e.g. 'FPR', 'ABTN', 'Compensatieplan'")
    section: str = Field(description="Specific section or article reference")
    page_number: int = Field(description="Page number in the PDF where the clause is found")
    quote: str = Field(description="Verbatim text containing the rule")


class EntitlementComparison(BaseModel):
    """One thematic comparison between the fund's rules and the standard product."""

    area: str = Field(
        description="Thematic area, e.g. 'Opbouwsystematiek', 'Partnerpensioen', "
        "'Indexatie', 'Compensatie', 'Beleggingsrisico'"
    )
    current_entitlement_description: str = Field(
        description="What rights members have under the legacy fund rules (FPR/ABTN)"
    )
    standard_offering_description: str = Field(
        description="The standard out-of-the-box configuration under AllVida / Qwik"
    )
    gap_detected: bool = Field(
        description="True if there is a discrepancy between the entitlement and the standard offering"
    )
    deviation_severity: Severity = Field(
        description="Impact severity if transitioned to the standard: High, Medium, Low or None"
    )
    actuarial_implication: str = Field(
        description="Mathematical / actuarial impact of the conversion (LaTeX allowed)"
    )
    required_qwik_configuration: str = Field(
        description="Proposed configuration parameters for the Qwik rule engine to model this deviation"
    )
    sources: list[ProvisionSource] = Field(
        default_factory=list, description="Provenance for the clauses behind this comparison"
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
    report: FundComparisonReport


class AnalysisRequest(BaseModel):
    """Which documents to analyse. Empty lists fall back to the full default set."""

    fund_document_ids: list[str] = Field(default_factory=list)
    benchmark_document_ids: list[str] = Field(default_factory=list)
