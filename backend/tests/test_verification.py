"""Unit tests for the anti-hallucination evidence verifier."""

from pathlib import Path

from app.schemas.comparison import (
    EntitlementComparison,
    FundComparisonReport,
    ProvisionSource,
)
from app.services.documents import Document
from app.services.verification import verify_report


def _doc(doc_id: str, role: str, filename: str) -> Document:
    return Document(id=doc_id, filename=filename, role=role, doc_type=role,
                    source="builtin", path=Path(filename))


FUND_TEXT = (
    "--- page 13 ---\n"
    "Het deel van de pensioenpremie dat SPF op uw persoonlijke pensioenrekening zet, "
    "is in 2026 gelijk aan 14,25% van uw pensioengrondslag als u in loondienst werkt."
)
BENCH_TEXT = (
    "--- page 4 ---\n"
    "De standaard flexibele premieovereenkomst hanteert een vlak premiepercentage dat "
    "als beschikbare premie op de persoonlijke pensioenrekening wordt gestort."
)

FUND = _doc("fund-1", "fund", "SPF Flexibele Premieregeling 2026.1_def.pdf")
BENCH = _doc("bench-1", "benchmark", "Specificatie Flexibele premieovereenkomst 0.08.docx")


def _report(current_sources, standard_sources) -> FundComparisonReport:
    return FundComparisonReport(
        fund_name="Test", target_transition_date="2026-01-01",
        entitlements=[
            EntitlementComparison(
                area="Opbouw", gap_detected=True, deviation_severity="High",
                impact_explanation="test",
                current_sources=current_sources, standard_sources=standard_sources,
            )
        ],
    )


def test_verbatim_quote_on_correct_side_verifies() -> None:
    report = _report(
        current_sources=[ProvisionSource(
            document_name=FUND.filename, section="4.1.1", page_number=13,
            quote="is in 2026 gelijk aan 14,25% van uw pensioengrondslag als u in loondienst werkt",
        )],
        standard_sources=[ProvisionSource(
            document_name=BENCH.filename, section="spec", page_number=4,
            quote="een vlak premiepercentage dat als beschikbare premie op de persoonlijke pensioenrekening wordt gestort",
        )],
    )
    verified = verify_report(report, [(FUND, FUND_TEXT)], [(BENCH, BENCH_TEXT)])
    item = verified.entitlements[0]
    assert item.current_sources[0].verified is True
    assert item.standard_sources[0].verified is True
    assert item.evidence_verified is True


def test_hallucinated_quote_is_rejected() -> None:
    report = _report(
        current_sources=[ProvisionSource(
            document_name=FUND.filename, section="x", page_number=13,
            quote="dit citaat staat nergens in het document en is volledig verzonnen onzin tekst",
        )],
        standard_sources=[],
    )
    verified = verify_report(report, [(FUND, FUND_TEXT)], [(BENCH, BENCH_TEXT)])
    item = verified.entitlements[0]
    assert item.current_sources[0].verified is False
    assert item.evidence_verified is False


def test_fund_number_cited_as_standard_is_rejected() -> None:
    """The core bug: the fund's own premie quoted on the STANDARD side must NOT verify."""
    report = _report(
        current_sources=[],
        standard_sources=[ProvisionSource(
            document_name=FUND.filename, section="4.1.1", page_number=13,
            quote="is in 2026 gelijk aan 14,25% van uw pensioengrondslag als u in loondienst werkt",
        )],
    )
    verified = verify_report(report, [(FUND, FUND_TEXT)], [(BENCH, BENCH_TEXT)])
    item = verified.entitlements[0]
    # Quote is real, but it's a FUND document cited on the STANDARD side -> rejected.
    assert item.standard_sources[0].verified is False
    assert item.evidence_verified is False
