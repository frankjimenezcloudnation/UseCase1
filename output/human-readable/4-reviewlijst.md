# Reviewlijst voor deskundigen — WTP onderdeel-analyse (SPF)

Dit document maakt de review zelfstandig uitvoerbaar: het somt de punten op die om een menselijk oordeel vragen. Bron: de analyse-run over de golden-testset.

## A. Afwijkende beantwoorde antwoorden (8) — tool wijkt af van het handmatige PDC-ijkpunt

Klopt het handwerk, of heeft de tool een goed punt?

| PDC-onderwerp | Tool-antwoord | PDC-ijkpunt | Onderbouwing (citaat) |
|---|---|---|---|
| Minimaal_pensioengevend_inkomen_toegestaan | ja | nee | SPF Flexibele Premieregeling 2026.1_def.pdf (p.16): "Uw pensioengevend inkomen wordt ten minste vastgesteld op nihil." |
| Hoogte_Maximaal_pensioengevend_inkomen_toegestaan | Er gelden twee maxima (2026): € 38.611 voor werknemers/waarnemers met kortdurend | fiscaal_maximum | SPF Flexibele Premieregeling 2026.1_def.pdf (p.15): "Werkt u als werknemer in dienstverband of als waarnemer met kortdurende dienstverbanden bij verschillende werkgevers (als bedoeld onder a)? " |
| Vorm_franchise | franchise_sociale_zekerheid | nominaal_bedrag | 2025.12.18 Abtn 2026 SPF DEF.pdf (p.19): "Franchise Gelijk aan de AOW-franchise artikel 10aa, eerste lid, UBLB voor spaarpremies onder 27,216% en wordt jaarlijks geïndexeerd. In 2026" |
| Vrijwillige_voortzetting_volledige_verzekering | ja_hele_regeling | nee | 2025.12.18 Abtn 2026 SPF DEF.pdf (p.19): "Het bestuur heeft de bevoegdheid om individuele (voormalige) deelnemers toestemming te verlenen om hun deelname aan de regeling van het fond" |
| Soort_premie | beschikbare_premie | vaste_premie | SPF Flexibele Premieregeling 2026.1_def.pdf (p.14): "SPF heeft op basis van de risicohouding (zie artikel 15.3) verschillende life cycles vastgesteld. Volgens welke life cycle we uw pensioenkap" |
| Methode_bepaling_aanspraak | kapitaalsopbouw | salaris | SPF Flexibele Premieregeling 2026.1_def.pdf (p.5): "U blijft dan pensioenkapitaal opbouwen zolang u voldoet aan de voorwaarden." |
| Moment_periodieke_overgang_individueel_collectief | persoonlijk | collectief | 2025 Implementatieplan WTP SPF v1.0.pdf (p.14): "de wijze en het moment waarop de definitieve persoonlijke pensioenvermogens worden bepaald" |
| Aanspraak_gebaseerd_op_staffel | kapitaalsopbouw | nee | SPF Flexibele Premieregeling 2026.1_def.pdf (p.5): "U blijft dan pensioenkapitaal opbouwen zolang u voldoet aan de voorwaarden." |

## B. Antwoorden buiten enumeration/format (7) — mogelijk ontologie aanpassen

| PDC-onderwerp | Vraag | Tool-antwoord | Toelichting |
|---|---|---|---|
| Minimale_toetredingsleeftijd | Wat is de minimale toetredingsleeftijd in jaren? | Niet van toepassing; er geldt geen minimale toetredingsleeftijd. Toetr | In de ABTN wordt bij de kenmerken van de regeling vermeld dat de toetredingsleeftijd 'niet |
| Maximale_Toetredingsleeftijd | Wat is de maximale toetredingsleeftijd? | Niet van toepassing; er geldt geen maximale toetredingsleeftijd. Toetr | In de ABTN staat expliciet dat de toetredingsleeftijd niet van toepassing is en dat toetre |
| Hoogte_Maximaal_pensioengevend_inkomen_toegestaan | Wat is de waarde van het maximum pensioengevend inkomen? | Er gelden twee maxima (2026): € 38.611 voor werknemers/waarnemers met  | Er is geen enkel maximum PGI-bedrag; het fonds hanteert twee verschillende maxima afhankel |
| Periodiciteit_automatisch_rebalancen_vast | Met welke periodiciteit wordt daadwerkelijk rebalancing toeg | Niet expliciet vastgesteld. De documenten beschrijven een handelskalen | In de fondsdocumenten wordt wel gesproken over een handelskalender met een eindemaand hand |
| Keuzerecht_hoog_laag | Is het mogelijkheid om de hoogte van het pensioen te variëre | In de aangeleverde passages is geen expliciete regeling gevonden over  | De documenten beschrijven een variabel pensioen dat jaarlijks kan veranderen, en de keuze  |
| Koersbepaling | Op welk moment wordt de koers bepaald? | De documenten beschrijven zowel maandorders als intra-maandorders en d | In de Operating Manual worden zowel maand- en intra-maandorders genoemd als een dagelijkse |
| Methode_bepaling_aanspraak | Is er sprake van een salarisdiensttijd regeling op basis van | Niet vast te stellen op basis van de aangeleverde passages. De documen | In de aangeleverde fondspassages wordt gesproken over de flexibele pensioenregeling onder  |

## C. Model-gaten (23) — ontologie vat het PDC-onderscheid niet volledig

| PDC-onderwerp | Wat mist / het gat |
|---|---|
| Afkoopmoment | PDC-keuze 'emigratie' ontbreekt in de enumeratie van Afkoopmoment (pensioeningang/echtscheiding/fiscale_bovenmatigheid/einde_dienstverband). Emigratie als afkoo |
| Bijsparen | De PDC-keuze 'ja, fiscaal maximum op regelingniveau' bevat een kwalificatie (fiscaal maximum, op regelingniveau) die de ja/nee-indicatie niet kan uitdrukken. In |
| Afrondingsmethode_toetredingsdatum | De PDC-waarde 'geen' (niet afronden) is binnen de generieke Afronding-klasse niet uit te drukken; die indicatie zit elders. Bovendien zijn dit generieke afrondi |
| Standaard pensioenleeftijd | De keuze 'jaren' mapt op de eenheid (Periode_leeftijd). Een eigen property voor de waarde van de standaard pensioenleeftijd zelf ontbreekt in de kandidatenset;  |
| Vorm_sociale_zekerheid_AOW | De drie AOW-varianten (laag=gehuwd enkel, midden=ongehuwd, hoog=gehuwd dubbel) vergen combinatie van twee properties; er is geen enkele property die deze sameng |
| Afwijkende_premie_en_aanspraak_grondslag | PDC vraagt een ja/nee-indicatie 'wijkt de premiegrondslag af van de aanspraak(pensioen)grondslag'. De ontologie heeft geen expliciete ja/nee-indicatie hiervoor; |
| Indexatie_grondslag_vrijstelling | De property is generieke indexatie van de grondslag; het 'vrijstelling'-aspect (voortzetting indexatie tijdens premievrije voortzetting/premievrijstelling) is n |
| Uitruil_bij_pensioeningang_vorm | PDC-waarde LOP_AOW_overbrugging (uitruil richting AOW-overbrugging) ontbreekt in de DomainValues; alleen LOP↔LPP-varianten en ontrekken NP uit beleggingswaarde  |
| AOW_overbrugging_in_combinatie_met_vaste_stijging_of_daling | De ontologie kent alleen een generieke Indicatie_AOW-overbrugging; het specifieke onderscheid 'AOW-overbrugging IN COMBINATIE MET vaste stijging/daling (hoog-la |
| Moment_keuze_stijging_daling | PDC-waarde 'moment_toetreding_collectief' ontbreekt in de DomainValues (alleen bij_/voor_pensioeningang). Het collectieve toetredingsmoment is niet uit te drukk |
| Vulling_risicodelingsreserve_uit_premie | Indicatie_vulregel_premie is generiek voor de reserve en niet gescopet op specifiek de risicodelingsreserve. De ontologie kent geen ja/nee-vulregel per reservet |
| Lifecycles_vast | DomainValues zijn buckets (1_lifecycle, max_3, max_6), geen exacte aantallen. PDC 'drie' ↔ max_3 is benaderend; PDC 'twee' heeft geen corresponderende waarde. H |
| Lifecycles_variabel | Waarde-mismatch: PDC-keuzes 'twee'/'drie' sluiten niet aan op de ontologie-enumeratie 1_lifecycle/max_3/max_6. De exacte aantallen twee en drie zijn niet als ap |
| Verdubbeling_volle_wees | Er is geen property die specifiek 'verdubbeling volle wees' als onderscheid vastlegt. De ja/nee is generiek (verdubbeling uitkering) en de 'volle wees'-situatie |
| Expiratieleeftijd | PDC-keuze 'ja' is een indicatie (van-toepassing). De ontologie kent alleen de numerieke waarde-property Expiratieleeftijd_pensioensoort, geen aparte ja/nee-indi |
| Voorportaal_verplicht | Ontologie kent alleen 'is er sprake van een voorportaal' (bestaan/toestaan), niet het onderscheid verplicht vs. vrijwillig dat de PDC met 'Voorportaal_verplicht |
| Moment_periodieke_overgang_individueel_collectief | De kandidaten drukken het niveau (individueel/collectief) uit, maar niet het 'moment van periodieke overgang' van individueel naar collectief. Peilmoment_period |
| Deeltijdpensioen_in_combinatie_met_AOW_overbrugging | DomainValues (vervroegen, uitstellen, hoog/laag, uitruil) bevatten geen 'AOW-overbrugging'. Ook de PDC-waarde 'alleen_met_eenmalig_vastgestelde_wisseldatum' is  |
| Deeltijdpensioen_in_combinatie_met_vaste_stijging_of_daling | De ontologie drukt combinaties uit als een enkele set-property, niet als een ja/nee per specifieke combinatie. Bovendien komt 'vaste stijging of daling' niet 1- |
| Indicatie_flexibele_eigen_bijdrage | PDC vraagt naar een FLEXIBELE eigen bijdrage (deelnemer kan hoogte variëren). De ontologie kent alleen Indicatie_eigen_bijdrage (wel/geen), Type_eigen_bijdrage  |
| Spreiding_toestaan | Generiek 'Spreiding_toestaan' (in WTP-context vaak spreiding van financiële schokken/resultaten) is niet dekbaar. Kandidaten bieden alleen spreiding voor toesla |
| Aanspraak_gebaseerd_op_staffel | Methode_bepaling_aanspraak kent domain vooraf_vastgestelde_aanspraak/grondslag/kapitaalsopbouw/sociale_zekerheid, maar GEEN waarde 'staffel'. De ontologie kan h |
| Maximering_wezenpensioen | De PDC vraagt een algemene maximering van het wezenpensioen (nee). De enige verwante kandidaat beperkt het AANTAL kinderen/begunstigden, niet een generieke maxi |

## Open vragen en aannames
- De streefwaarden voor accuraatheid en dekking worden door de deskundigen vastgesteld.
- Enkele PDC-ijkpunten zijn een eenheid-hint (bv. 'jaren') i.p.v. een echte waarde; die zijn in de validatie als 'n.v.t.' behandeld.
