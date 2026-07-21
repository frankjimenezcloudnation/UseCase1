# Review list for experts — WTP component analysis (SPF)

This document makes the review independently executable: it lists the points that call for a human judgment. Source: the analysis run over the golden test set.

## A. Deviating answers given (8) — the tool deviates from the manual PDC benchmark

Is the manual work correct, or does the tool have a good point?

| PDC topic | Tool answer | PDC benchmark | Substantiation (quote) |
|---|---|---|---|
| Minimaal_pensioengevend_inkomen_toegestaan | yes | no | SPF Flexibele Premieregeling 2026.1_def.pdf (p.16): "Your pensionable income is set at no less than nil." (origineel: "Uw pensioengevend inkomen wordt ten minste vastgesteld op nihil.") |
| Hoogte_Maximaal_pensioengevend_inkomen_toegestaan | Two maxima apply (2026): € 38.611 for employees/locums with short-term | fiscaal_maximum | SPF Flexibele Premieregeling 2026.1_def.pdf (p.15): "Do you work as an employee in salaried employment or as a locum with short-term employment contracts with different employers (as referred to under a)? " (origineel: "Werkt u als werknemer in dienstverband of als waarnemer met kortdurende dienstverbanden bij verschillende werkgevers (als bedoeld onder a)? ") |
| Vorm_franchise | franchise_sociale_zekerheid | nominaal_bedrag | 2025.12.18 Abtn 2026 SPF DEF.pdf (p.19): "Franchise Equal to the AOW franchise of Article 10aa, first paragraph, UBLB for savings premiums below 27,216% and is indexed annually. In 2026" (origineel: "Franchise Gelijk aan de AOW-franchise artikel 10aa, eerste lid, UBLB voor spaarpremies onder 27,216% en wordt jaarlijks geïndexeerd. In 2026") |
| Vrijwillige_voortzetting_volledige_verzekering | ja_hele_regeling | no | 2025.12.18 Abtn 2026 SPF DEF.pdf (p.19): "The board has the authority to grant individual (former) participants permission to continue their participation in the scheme of the fund" (origineel: "Het bestuur heeft de bevoegdheid om individuele (voormalige) deelnemers toestemming te verlenen om hun deelname aan de regeling van het fond") |
| Soort_premie | beschikbare_premie | vaste_premie | SPF Flexibele Premieregeling 2026.1_def.pdf (p.14): "SPF has established various life cycles based on the risk attitude (see Article 15.3). According to which life cycle your pension cap" (origineel: "SPF heeft op basis van de risicohouding (zie artikel 15.3) verschillende life cycles vastgesteld. Volgens welke life cycle we uw pensioenkap") |
| Methode_bepaling_aanspraak | kapitaalsopbouw | salary | SPF Flexibele Premieregeling 2026.1_def.pdf (p.5): "You then continue to accrue pension capital as long as you meet the conditions." (origineel: "U blijft dan pensioenkapitaal opbouwen zolang u voldoet aan de voorwaarden.") |
| Moment_periodieke_overgang_individueel_collectief | personal | collective | 2025 Implementatieplan WTP SPF v1.0.pdf (p.14): "the manner and the moment at which the definitive personal pension capitals are determined" (origineel: "de wijze en het moment waarop de definitieve persoonlijke pensioenvermogens worden bepaald") |
| Aanspraak_gebaseerd_op_staffel | kapitaalsopbouw | no | SPF Flexibele Premieregeling 2026.1_def.pdf (p.5): "You then continue to accrue pension capital as long as you meet the conditions." (origineel: "U blijft dan pensioenkapitaal opbouwen zolang u voldoet aan de voorwaarden.") |

## B. Answers outside enumeration/format (7) — possibly adjust the ontology

| PDC topic | Question | Tool answer | Explanation |
|---|---|---|---|
| Minimale_toetredingsleeftijd | What is the minimum entry age in years? | Not applicable; there is no minimum entry age. Entr | In the ABTN, the characteristics of the scheme state that the entry age is 'not |
| Maximale_Toetredingsleeftijd | What is the maximum entry age? | Not applicable; there is no maximum entry age. Entr | The ABTN explicitly states that the entry age is not applicable and that entr |
| Hoogte_Maximaal_pensioengevend_inkomen_toegestaan | What is the value of the maximum pensionable income? | Two maxima apply (2026): € 38.611 for employees/locums with  | There is no single maximum PGI amount; the fund applies two different maxima dependin |
| Periodiciteit_automatisch_rebalancen_vast | With what periodicity is rebalancing actually appl | Not explicitly established. The documents describe a trading calen | The fund documents do speak of a trading calendar with an end-of-month trad |
| Keuzerecht_hoog_laag | Is it possible to vary the level of the pension | In the passages provided, no explicit rule was found on  | The documents describe a variable pension that can change annually, and the choice  |
| Koersbepaling | At what moment is the price determined? | The documents describe both month orders and intra-month orders and d | The Operating Manual mentions both month and intra-month orders as well as a daily |
| Methode_bepaling_aanspraak | Is there a salary-service-time scheme based on | Cannot be determined on the basis of the passages provided. The documen | The fund passages provided speak of the flexible pension scheme under  |

## C. Model gaps (23) — the ontology does not fully capture the PDC distinction

| PDC topic | What is missing / the gap |
|---|---|
| Afkoopmoment | The PDC choice 'emigration' (origineel: 'emigratie') is missing from the enumeration of Afkoopmoment (pensioeningang/echtscheiding/fiscale_bovenmatigheid/einde_dienstverband). Emigration as a surren |
| Bijsparen | The PDC choice 'yes, fiscal maximum at scheme level' (origineel: 'ja, fiscaal maximum op regelingniveau') contains a qualification (fiscal maximum, at scheme level) that the yes/no indication cannot express. In |
| Afrondingsmethode_toetredingsdatum | The PDC value 'none' (origineel: 'geen') (no rounding) cannot be expressed within the generic Afronding class; that indication sits elsewhere. Moreover, these are generic roundin |
| Standaard pensioenleeftijd | The choice 'years' (origineel: 'jaren') maps to the unit (Periode_leeftijd). A dedicated property for the value of the standard retirement age itself is missing from the candidate set;  |
| Vorm_sociale_zekerheid_AOW | The three AOW variants (low=married single, middle=unmarried, high=married double) require a combination of two properties; there is no single property that captures this composi |
| Afwijkende_premie_en_aanspraak_grondslag | The PDC asks for a yes/no indication 'does the premium basis deviate from the entitlement (pension) basis' (origineel: 'wijkt de premiegrondslag af van de aanspraak(pensioen)grondslag'). The ontology has no explicit yes/no indication for this; |
| Indexatie_grondslag_vrijstelling | The property is generic indexation of the basis; the 'exemption' (origineel: 'vrijstelling') aspect (continuation of indexation during non-contributory continuation/premium waiver) is n |
| Uitruil_bij_pensioeningang_vorm | PDC value LOP_AOW_overbrugging (exchange toward AOW bridging) is missing from the DomainValues; only LOP↔LPP variants and withdrawing NP from investment value  |
| AOW_overbrugging_in_combinatie_met_vaste_stijging_of_daling | The ontology only has a generic Indicatie_AOW-overbrugging; the specific distinction 'AOW bridging IN COMBINATION WITH fixed increase/decrease (high-lo |
| Moment_keuze_stijging_daling | PDC value 'moment_toetreding_collectief' is missing from the DomainValues (only bij_/voor_pensioeningang). The collective entry moment cannot be expresse |
| Vulling_risicodelingsreserve_uit_premie | Indicatie_vulregel_premie is generic for the reserve and not scoped to specifically the risk-sharing reserve. The ontology has no yes/no filling rule per reserve typ |
| Lifecycles_vast | DomainValues are buckets (1_lifecycle, max_3, max_6), not exact numbers. PDC 'three' (origineel: 'drie') ↔ max_3 is approximate; PDC 'two' (origineel: 'twee') has no corresponding value. Th |
| Lifecycles_variabel | Value mismatch: PDC choices 'two'/'three' (origineel: 'twee'/'drie') do not align with the ontology enumeration 1_lifecycle/max_3/max_6. The exact numbers two and three are not as separ |
| Verdubbeling_volle_wees | There is no property that specifically captures 'doubling full orphan' (origineel: 'verdubbeling volle wees') as a distinction. The yes/no is generic (doubling of the benefit) and the 'full orphan' situatio |
| Expiratieleeftijd | PDC choice 'yes' (origineel: 'ja') is an indication (applicable). The ontology only has the numeric value property Expiratieleeftijd_pensioensoort, no separate yes/no indi |
| Voorportaal_verplicht | The ontology only knows 'is there a voorportaal' (origineel: 'is er sprake van een voorportaal') (existence/being allowed), not the mandatory vs. voluntary distinction that the PDC expresses with 'Voorportaal_verplicht |
| Moment_periodieke_overgang_individueel_collectief | The candidates express the level (individual/collective), but not the 'moment of periodic transition' from individual to collective. Peilmoment_period |
| Deeltijdpensioen_in_combinatie_met_AOW_overbrugging | The DomainValues (vervroegen, uitstellen, hoog/laag, uitruil) contain no 'AOW bridging' (origineel: 'AOW-overbrugging'). Also, the PDC value 'alleen_met_eenmalig_vastgestelde_wisseldatum' is  |
| Deeltijdpensioen_in_combinatie_met_vaste_stijging_of_daling | The ontology expresses combinations as a single set property, not as a yes/no per specific combination. Moreover, 'fixed increase or decrease' (origineel: 'vaste stijging of daling') does not match 1- |
| Indicatie_flexibele_eigen_bijdrage | The PDC asks about a FLEXIBLE own contribution (the participant can vary the amount). The ontology only knows Indicatie_eigen_bijdrage (yes/no), Type_eigen_bijdrage  |
| Spreiding_toestaan | The generic 'Spreiding_toestaan' (in the WTP context often spreading of financial shocks/results) cannot be covered. Candidates only offer spreading for supplemen |
| Aanspraak_gebaseerd_op_staffel | Methode_bepaling_aanspraak has domain vooraf_vastgestelde_aanspraak/grondslag/kapitaalsopbouw/sociale_zekerheid, but NO value 'staffel'. The ontology can |
| Maximering_wezenpensioen | The PDC asks about a general capping of the orphan's pension (no). The only related candidate limits the NUMBER of children/beneficiaries, not a generic maxi |

## Open questions and assumptions
- The target values for accuracy and coverage are set by the experts.
- Some PDC benchmarks are a unit hint (e.g. 'years' (origineel: 'jaren')) instead of an actual value; in the validation those were treated as 'n/a' (origineel: 'n.v.t.').
