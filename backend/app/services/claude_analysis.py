"""Use Case 1 analysis engine.

Builds the fund corpus + benchmark context, then runs the "Pension Entitlement
Auditor" via Claude structured outputs (client.messages.parse) to produce a
FundComparisonReport. Falls back to a grounded demo report when no Anthropic
credentials are configured, so the prototype runs end-to-end out of the box.
"""

from __future__ import annotations

from app.core.config import settings
from app.services.documents import Document
from app.services.extraction import extract_text
from app.schemas.comparison import (
    AnalysisResponse,
    EntitlementComparison,
    FundComparisonReport,
    ProvisionSource,
)

SYSTEM_PROMPT = """\
You are an expert actuarial auditor and semantic compliance system specialising in the \
Dutch Wet toekomst pensioenen (Wtp) transition.

YOUR TASK:
1. Intake the provided unstructured fund documents (FPR, ABTN, Operating Manual, \
Transition Plan, Compensation Plan).
2. Read the standard specification reference documents (IG&H AllVida and Feniqs Qwik \
capabilities, and the ontology snapshot).
3. Cross-reference the fund's historical rules (average/final-wage DB structures, custom \
partner risk coverage, discretionary indexation) with the standard DC product models.
4. Highlight gaps: risk of insurance holes (verzekeringsgaten) for slapers, transition \
costs, custom lifecycles, and fiscal premium-room compliance (max 30% + 3% compensation).
5. Produce one EntitlementComparison per thematic area. Cover at least: Opbouwsystematiek, \
Partnerpensioen, Indexatie/Toeslagen, Compensatie doorsneesystematiek, and Beleggingsrisico.
6. Every comparison MUST cite its sources with document name, section/article, page number \
and a verbatim quote — provenance is mandatory for auditability (DNB/AFM).
7. Use LaTeX notation for mathematical/actuarial implications where applicable.
8. Propose concrete Qwik rule-engine configuration parameters for each deviation.

Be precise and conservative: only assert a gap when the fund rule and the standard offering \
genuinely differ. A difference that the standard product can fully represent through \
configuration / parameterisation — e.g. coverage percentages, grondslag-definitie \
(PGI_deeltijd, 5-jaars gemiddelde voor zelfstandigen), a separate risicopremie-opslag, or \
overgangsrechten zoals het omzetten van opgebouwd partnerpensioen in variabel LPPF — is NOT \
a material deviation: set gap_detected=false and deviation_severity="None" for such items. \
Reserve gaps for structural differences that the standard product cannot parameterise away. \
Output must exactly match the required schema."""


def _build_context(fund_docs: list[Document], benchmark_docs: list[Document]) -> str:
    parts: list[str] = ["# FUND CORPUS (specific fund — 'waar hebben mensen recht op')\n"]
    for d in fund_docs:
        text = extract_text(d.path, settings.MAX_DOC_CHARS)
        parts.append(f"\n## [{d.doc_type}] file: {d.filename}\n{text}\n")
    parts.append("\n\n# BENCHMARK / STANDARD PRODUCT REFERENCES\n")
    for d in benchmark_docs:
        text = extract_text(d.path, settings.MAX_DOC_CHARS)
        parts.append(f"\n## [{d.doc_type}] file: {d.filename}\n{text}\n")
    return "".join(parts)


def analyse(fund_docs: list[Document], benchmark_docs: list[Document]) -> AnalysisResponse:
    fund_names = [d.filename for d in fund_docs]
    bench_names = [d.filename for d in benchmark_docs]

    if not settings.has_ai_credentials:
        return AnalysisResponse(
            mode="demo",
            model=None,
            fund_documents=fund_names,
            benchmark_documents=bench_names,
            report=_demo_report(fund_docs),
        )

    import anthropic

    # Pass the key from settings (loaded from backend/.env) so the client sees it
    # even when it was never exported to the OS environment. Falls back to the
    # SDK's own resolution (ANTHROPIC_API_KEY env var / ant profile) otherwise.
    client = (
        anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        if settings.ANTHROPIC_API_KEY
        else anthropic.Anthropic()
    )
    context = _build_context(fund_docs, benchmark_docs)

    user_prompt = (
        "Analyse the following corpus and produce the FundComparisonReport.\n\n"
        f"{context}"
    )

    message = client.messages.parse(
        model=settings.CLAUDE_MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        output_format=FundComparisonReport,
    )
    report = message.parsed_output
    if report is None:
        # Structured parse failed (e.g. refusal / truncation) — degrade gracefully.
        return AnalysisResponse(
            mode="demo",
            model=settings.CLAUDE_MODEL,
            fund_documents=fund_names,
            benchmark_documents=bench_names,
            report=_demo_report(fund_docs),
        )

    return AnalysisResponse(
        mode="live",
        model=settings.CLAUDE_MODEL,
        fund_documents=fund_names,
        benchmark_documents=bench_names,
        report=report,
    )


def _demo_report(fund_docs: list[Document]) -> FundComparisonReport:
    """Grounded sample derived from the WTP research report's comparison table.

    Used when no Anthropic API key is configured so the UI is fully demonstrable.
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
                current_entitlement_description=(
                    "Toezeggingen op basis van dienstjaren en salaris (middelloon) met een "
                    "doorsneepremie; uitkeringsovereenkomst (DB)."
                ),
                standard_offering_description=(
                    "Beschikbare premieregeling (DC) met vlakke premie en "
                    "leeftijdscohort-specifiek beleggingsbeleid (AllVida/Qwik)."
                ),
                gap_detected=True,
                deviation_severity="High",
                actuarial_implication=(
                    "Vereist actuariële conversie via de standaardmethode of de "
                    "Value-based Actuarial (VBA) methode: $TV_{DC} = \\sum_x a_x \\cdot PV_x$."
                ),
                required_qwik_configuration=(
                    '{"regeling":"SPR","premie":"vlak","opbouw":"kapitaal",'
                    '"conversie":"VBA"}'
                ),
                sources=[
                    ProvisionSource(
                        document_name=fpr, section="Art. 5 Opbouw",
                        page_number=12,
                        quote="De pensioenopbouw geschiedt volgens het middelloonstelsel.",
                    )
                ],
            ),
            EntitlementComparison(
                area="Partnerpensioen bij overlijden voor pensioendatum",
                current_entitlement_description=(
                    "Risicopartnerpensioendekking $LPPRF = dekkingsprc \\cdot PGI_{deeltijd}$. "
                    "Voor zelfstandigen geldt een 5-jaars gemiddelde pensioengrondslag "
                    "$PG_{ovl} = \\frac{\\sum_{i=1}^{5} PGI_i \\cdot pt_i}{\\sum_{i=1}^{5} pt_i}$. "
                    "De risicopremie is een separate opslag (premie on top). Het tot de "
                    "transitiedatum opgebouwde partnerpensioen blijft als aanspraak behouden "
                    "(overgangsrecht)."
                ),
                standard_offering_description=(
                    "Partnerpensioen op risicobasis als percentage van de pensioengrondslag, "
                    "met een separate risicopremie; het opgebouwde partnerpensioen wordt bij "
                    "overlijden vóór pensioendatum omgezet in variabel LPPF."
                ),
                gap_detected=False,
                deviation_severity="None",
                actuarial_implication=(
                    "Geen materiële afwijking van de standaard; de parameterisering dekt dit af. "
                    "Dekkingsgrondslag $PGI_{deeltijd}$, 5-jaars gemiddelde voor zelfstandigen, "
                    "separate risicopremie en de omzetting van het opgebouwde partnerpensioen in "
                    "variabel LPPF (overgangsrecht) zijn alle instelbaar in het standaardproduct."
                ),
                required_qwik_configuration=(
                    '{"partnerpensioen":"risicobasis","dekkingsgrondslag":"PGI_deeltijd",'
                    '"grondslag_zelfstandigen":"5jaars_gemiddelde",'
                    '"risicopremie":"separate_opslag","overgangsrecht_opbouw":true,'
                    '"omzetting_bij_overlijden":"variabel_LPPF"}'
                ),
                sources=[
                    ProvisionSource(
                        document_name=fpr, section="Art. 8 Nabestaandenpensioen",
                        page_number=21,
                        quote="De risicodekking partnerpensioen bedraagt een percentage van de "
                        "pensioengrondslag; de risicopremie wordt als separate opslag geheven.",
                    )
                ],
            ),
            EntitlementComparison(
                area="Indexatie en Toeslagen",
                current_entitlement_description=(
                    "Voorwaardelijke toeslagverlening gekoppeld aan de beleidsdekkingsgraad, "
                    "gefinancierd uit overrendement (bijv. max 5% prijsindex)."
                ),
                standard_offering_description=(
                    "Rendementsbijschrijving direct in het persoonlijke pensioenvermogen, "
                    "gestuurd door de risicohouding per leeftijdscohort."
                ),
                gap_detected=True,
                deviation_severity="Medium",
                actuarial_implication=(
                    "FTK-dempingsregels vervallen; schommelingen worden opgevangen via de "
                    "solidariteitsreserve. Beleidsdekkingsgraad "
                    "$\\overline{DG} = \\frac{1}{12}\\sum_{t=1}^{12} DG_t$ vervalt als sturing."
                ),
                required_qwik_configuration=(
                    '{"toeslag":"rendementsbijschrijving","solidariteitsreserve":true,'
                    '"ftk_demping":false}'
                ),
                sources=[
                    ProvisionSource(
                        document_name=abtn, section="Hfd. Toeslagbeleid",
                        page_number=34,
                        quote="Toeslagverlening vindt voorwaardelijk plaats op basis van de beleidsdekkingsgraad.",
                    )
                ],
            ),
            EntitlementComparison(
                area="Compensatie afschaffing doorsneesystematiek",
                current_entitlement_description=(
                    "Maatwerk compensatieregeling voor actieve deelnemers in de "
                    "leeftijdscategorie 40-50 jaar, vastgelegd in het compensatieplan."
                ),
                standard_offering_description=(
                    "Tijdelijke verhoging van de fiscale premieruimte met max. 3% van de "
                    "pensioengrondslag (Art. 38s Wet LB)."
                ),
                gap_detected=True,
                deviation_severity="Medium",
                actuarial_implication=(
                    "Toetsen aan de fiscale grens: $PR_{max} = 30\\% + C_{transitie}$, "
                    "met $0 \\le C_{transitie} \\le 3\\%$ (SHACL sh:maxInclusive 33.0)."
                ),
                required_qwik_configuration=(
                    '{"compensatie":true,"opslag_pct":3,"doelgroep":"40-50",'
                    '"fiscale_toets":"33pct"}'
                ),
                sources=[
                    ProvisionSource(
                        document_name=abtn, section="Compensatieopzet",
                        page_number=41,
                        quote="Compensatie wordt toegekend aan deelnemers geboren tussen 1975 en 1985.",
                    )
                ],
            ),
            EntitlementComparison(
                area="Beleggingsrisico en Risicobereidheid",
                current_entitlement_description=(
                    "Collectieve risicodeling waarbij het bestuur de mate van beleggingsrisico "
                    "centraal bepaalt voor het gehele fonds."
                ),
                standard_offering_description=(
                    "Gedifferentieerd beleggingsbeleid via lifecycles (bijv. van 95% zakelijke "
                    "waarden dalend naar 25% bij pensionering)."
                ),
                gap_detected=True,
                deviation_severity="Medium",
                actuarial_implication=(
                    "Risicoprofielen van deelnemers moeten worden gemapt op de "
                    "lifecycle-instellingen in de Qwik-rule engine."
                ),
                required_qwik_configuration=(
                    '{"beleggingsbeleid":"lifecycle","zakelijk_start_pct":95,'
                    '"zakelijk_eind_pct":25,"cohort_mapping":true}'
                ),
                sources=[
                    ProvisionSource(
                        document_name=abtn, section="Beleggingsbeleid",
                        page_number=28,
                        quote="Het bestuur stelt het strategisch beleggingsbeleid vast voor het collectief.",
                    )
                ],
            ),
        ],
    )
