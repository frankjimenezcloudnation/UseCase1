# WTP golden testset (Use Case 1)

- Versie: 1 — 2026-07-20
- Fondsscope: **SPF**
- Onderwerpen: **102** → **106** unieke ontologie-vragen. Doordat sommige onderwerpen meerdere vragen bevatten, worden in een analyse-run **133 vraag-instanties** doorlopen.
- SPF-ijkpunt (handmatig PDC-antwoord) aanwezig bij **71** van de 102 onderwerpen.
- Confidence: high 40, medium 45, low 17.
- Model-gaten (⚠): **23** onderwerpen waar de ontologie het PDC-onderscheid niet volledig vat.

> PDC dient uitsluitend als referentie/validatie, NIET als informatiebron voor de analyse. 'granularity_gap'=true: gekoppeld maar ontologie kan het PDC-onderscheid niet volledig vatten (input voor ontologie-verbetering).

| # | PDC-onderwerp | Ontologie-vraag/vragen | SPF-ijkpunt | Confidence | Gap |
|---|---|---|---|---|---|
| 1 | Type_pensioenovereenkomst | Karakter_Pensioenovereenkomst | Flexibele Premieovereenkomst | high |  |
| 5 | Afnametype_regeling_werknemer | Afnametype | verplicht | high |  |
| 7 | Minimale_toetredingsleeftijd | Minimale_toetredingsleeftijd | jaren | high |  |
| 8 | Maximale_Toetredingsleeftijd | Maximale_toetredingsleeftijd | jaren | high |  |
| 22 | Minimaal_pensioengevend_inkomen_toegestaan | Indicatie_minimeren_PGI | nee | high |  |
| 23 | Maximaal_pensioengevend_inkomen_toegestaan | Indicatie_maximeren_PGI | ja | high |  |
| 24 | Hoogte_Maximaal_pensioengevend_inkomen_toegestaan | Indicatie_maximeren_PGI + Vrij_te_kiezen_maximum_PGI | fiscaal_maximum | high |  |
| 25 | Maximale_stijging_PGI_van_toepassing | Indicatie_maximeren_stijging_PGI | nee | high |  |
| 29 | Gemiddeld_pensioengevend_inkomen_van_toepassing | Indicatie_gemiddeld_PGI | ja, nee | high |  |
| 34 | Methodiek_vaststelling_grondslag | Basis_grondslag_berekening | PGI_minus_franchise | high |  |
| 35 | Middeling_grondslag | Indicatie_middeling_grondslag | nee | high |  |
| 38 | Aanlevering_parttime dienstverband | Formaat_aanlevering_dienstverbandgegevens | percentage, uurbasis | high |  |
| 39 | Maximering_100% | Maximering_100%_deelnemingspercentage | per_deelnemingsvorm | high |  |
| 44 | Peilmoment_grondslag_premievrijstelling | Peilmoment_grondslag | dag_voor_aanvang_AO | high |  |
| 50 | Soort_pensioenuitkering | Indicatie_soort_pensioenuitkering + Shoprecht | vast (Shoprecht), variabel | high |  |
| 51 | Moment_herziening_keuze_vast_variabel | Moment_herstel_keuzemogelijkheid | periode_voor_pensioeningang, bij_pensioeningang | high |  |
| 55 | Vervroeging_van_toepassing | Indicatie_vervroegen | ja | high |  |
| 56 | Minimale_datum_vervroeging | Eerstmogelijke_ingangsdatum | 10_jaar_voor_AOW | high |  |
| 57 | Vervroeging_toestaan_bij_premievrijstelling | Indicatie_vervroeging_bij_premievrijstelling | ja | high |  |
| 60 | Opbouw_gedurende_uitstel | Indicatie_pensioenopbouw_na_pensioenrichtdatum | nee | high |  |
| 64 | Deeltijdpensioen_van_toepassing | Indicatie_deeltijdpensioen | ja | high |  |
| 69 | Afkoopgrens | Soort_afkoopgrens_klein_pensioen + Afwijkende_afkoopgrens | wettelijk | high |  |
| 70 | Afkoopmoment | Afkoopmoment | pensioeningang, beëindiging_dienstverband, echtscheiding | high | ⚠ |
| 72 | Uitruil_bij_pensioeningang | Indicatie_uitruil_bij_pensioeningang | ja | high |  |
| 75 | AOW_overbrugging_van_toepassing | Indicatie_AOW-overbrugging | nee | high |  |
| 79 | Keuze_hoog_laag | Vorm_hoog_laag | — | high |  |
| 81 | Bepaling_wisselmoment | Moment_vrije_switch | — | high |  |
| 83 | Vaste daling of stijging | Indicatie_vaste_stijging_of_daling | — | high |  |
| 92 | Deeltijdverlof_toegestaan | Indicatie_deeltijd_verlof | nee | high |  |
| 102 | Periodiciteit_incasso | Periodiciteit_incasso | maand | high |  |
| 104 | Risicodelingsreserve | Indicatie_risicodelingsreserve | — | high |  |
| 105 | Soorten_voorzieningen | Soort_reserve | operationele_reserve | high |  |
| 108 | Operationele reserve | Indicatie_operationele_reserve | — | high |  |
| 114 | Compensatiedepot_van_toepassing | Indicatie_compensatiedepot | nee | high |  |
| 123 | Vorm_beleggingsrisico | Vorm_valutering_basis | actual payment | high |  |
| 124 | Beleggingsmethodiek | Beleggingsmethodiek | lifecycle_beleggen | high |  |
| 132 | Moment_koersbepaling | Moment_koersbepaling | forward_pricing | high |  |
| 134 | Automatisch_rebalancen | Automatisch_rebalancen | ja | high |  |
| 135 | Periodiciteit_automatisch_rebalancen_vast | Periodiciteit_rebalancing | maand | high |  |
| 141 | Afnametype | Afnametype | verplicht | high |  |
| 3 | Bijsparen | Indicatie_bijsparen | ja, fiscaal maximum op regelingniveau | medium | ⚠ |
| 9 | Afrondingsmethode_toetredingsdatum | Methode_afronding_datum_in_periode + Methode_afronding_voorwaarde + methode_afronding_datum_periodiciteit | geen | medium | ⚠ |
| 10 | Standaard pensioenleeftijd | Periode_leeftijd | jaren | medium | ⚠ |
| 11 | Afrondingsmethode_standaard_pensioendatum | Methode_afronding_datum_in_periode + Methode_afronding_voorwaarde + methode_afronding_datum_periodiciteit | 1e deze maand | medium |  |
| 12 | Voorportaal | Indicatie_voorportaal_toestaan | — | medium |  |
| 26 | Periode_pensioengevend_inkomen | Periodiciteit_PGI | jaar | medium |  |
| 31 | Vorm_franchise | Vorm_franchise + Bron_franchise | nominaal_bedrag | medium |  |
| 32 | Vorm_sociale_zekerheid_AOW | Grondslag_bedragen + Vermenigvuldigingsfactor_grondslag | — | medium | ⚠ |
| 36 | Afwijkende_premie_en_aanspraak_grondslag | Soort_grondslag | nee | medium | ⚠ |
| 43 | Afnametype_premievrijstelling | Afnametype | vrijwillig | medium |  |
| 45 | Indexatie_grondslag_vrijstelling | Indicatie_verhogen_laatst_vastgestelde_grondslag | ja | medium | ⚠ |
| 49 | AO_percentage | AO_percentage_pensioensoort + Methode_afleiden_percentage_arbeidsongeschiktheid | UWV_staffel | medium |  |
| 63 | Deeltijdpensioen | Indicatie_deeltijdpensioen | — | medium |  |
| 67 | Keuzemoment_deeltijdpensioen | Vaststelling_stappen_deeltijdpensioen + Aantal_stappen_deeltijdpensioen | in_meerdere_stappen_mogelijk | medium |  |
| 71 | Uitruil | Indicatie_uitruilmogelijkheid | — | medium |  |
| 73 | Uitruil_bij_pensioeningang_vorm | Soort_uitruil_bij_pensioeningang | LOP_LPP, LPP_LOP | medium | ⚠ |
| 74 | AOW overbrugging | Indicatie_AOW-overbrugging + Einddatum_AOW-overbrugging | — | medium |  |
| 76 | AOW_overbrugging_in_combinatie_met_vaste_stijging_of_daling | Indicatie_AOW-overbrugging | — | medium | ⚠ |
| 77 | Hoog laag | Indicatie_hoog_laag | — | medium |  |
| 78 | Keuzerecht_hoog_laag | Indicatie_hoog_laag | — | medium |  |
| 80 | AOW_overbrugging_inbouwen | Indicatie_AOW-overbrugging | — | medium |  |
| 85 | Moment_keuze_stijging_daling | Moment_keuze_variatie_pensioenuitkering | bij_pensioeningang | medium | ⚠ |
| 89 | Vrijwillige_voortzetting_volledige_verzekering | Vrijwillige_voortzetting_regeling | nee | medium |  |
| 91 | Vorm_onbetaald_verlof | Voortzettingsoptie_onbetaald_verlof | wettelijke_optie (voortz. risico) | medium |  |
| 95 | Soort_premie | Methode_vaststelling_premie | vaste_premie | medium |  |
| 97 | Financiering_risicopremies | Vaststellen_risicopremie + Methode_incasso_risicofinanciering | onderdeel_van_reguliere_premie | medium |  |
| 98 | Eigen bijdrage | Indicatie_eigen_bijdrage | — | medium |  |
| 99 | Indicatie_vaste_eigen_bijdrage | Type_eigen_bijdrage + Indicatie_eigen_bijdrage | ja | medium |  |
| 101 | Incassotermijn | Periodiciteit_incasso + Moment_incasso | — | medium |  |
| 106 | Vulling_risicodelingsreserve_uit_premie | Indicatie_vulregel_premie | nee | medium | ⚠ |
| 107 | Beleggingsbeleid | Beleggingsbeleid_collectief_vermogen + Beleggingsbeleid_reserve | eigen beleid | medium |  |
| 111 | Periodiciteit_spreidingsperiode | Tijdseenheid_vaste_periode | jaar | medium |  |
| 112 | Eenheid_tijd_spreidingsperiode | Tijdseenheid_vaste_periode | kalenderjaren | medium |  |
| 113 | Compensatiedepot | Indicatie_compensatiedepot + Financiering_compensatiedepot | — | medium |  |
| 125 | Lifecycles_vast | Aantal_lifecycles | drie | medium | ⚠ |
| 126 | Lifecycles_variabel | Aantal_lifecycles | drie | medium | ⚠ |
| 130 | Koersbepaling | Moment_handel + Moment_koersbepaling | — | medium |  |
| 133 | Rebalancing | Rebalancen_van_toepassing + Periodiciteit_rebalancing | — | medium |  |
| 137 | Herverzekering | Indicatie_herverzekering | — | medium |  |
| 139 | Dekking lang leven | Naam_pensioensoort_dekking_leven | — | medium |  |
| 142 | Methode_bepaling_aanspraak | Methode_bepaling_aanspraak + Methode_salaris_diensttijd | salaris | medium |  |
| 143 | Dekking  overlijden | Naam_pensioensoort_dekking_overlijden | — | medium |  |
| 146 | Vorm_afname | Type_nabestaandensysteem | onbepaald | medium |  |
| 149 | Verdubbeling_volle_wees | Indicatie_verdubbeling_uitkering + Situatie_verdubbeling_uitkering | ja | medium | ⚠ |
| 150 | Expiratieleeftijd | Expiratieleeftijd_pensioensoort | ja | medium | ⚠ |
| 6 | Leeftijden en datums | Vaststelling_leeftijd + Leeftijd | — | low |  |
| 13 | Voorportaal_verplicht | Indicatie_voorportaal_toestaan | nee | low | ⚠ |
| 14 | Uitkering_recht | Type_uitkering + Type_periode_uitkering + Indicatie_soort_pensioenuitkering | — | low |  |
| 30 | Franchise | Indicatie_franchise + Bron_franchise | — | low |  |
| 53 | Moment_periodieke_overgang_individueel_collectief | Niveau_vermogen + Soort_toedelingsmechanisme | collectief | low | ⚠ |
| 54 | Vervroeging | Indicatie_vervroegen | — | low |  |
| 58 | Uitstel | Indicatie_uitstellen | — | low |  |
| 65 | Deeltijdpensioen_in_combinatie_met_AOW_overbrugging | Keuzemogelijkheden_combinatie_deeltijd_met | nee | low | ⚠ |
| 66 | Deeltijdpensioen_in_combinatie_met_vaste_stijging_of_daling | Keuzemogelijkheden_combinatie_deeltijd_met | ja | low | ⚠ |
| 68 | Afkoop en waardeoverdracht | Waardeoverdracht_klein_pensioen + Afkoop_klein_pensioen + Toestemming waardeoverdracht + Meewerking_aan_niet-wettelijk_recht_op_waardeoverdracht | — | low |  |
| 90 | Onbetaald verlof | Voortzettingsoptie_onbetaald_verlof + Vormen_onbetaald_verlof | — | low |  |
| 100 | Indicatie_flexibele_eigen_bijdrage | Indicatie_eigen_bijdrage | nee | low | ⚠ |
| 109 | Spreiding | Indicatie_spreidingsperiode | — | low |  |
| 110 | Spreiding_toestaan | Indicatie_spreidingsperiode | ja | low | ⚠ |
| 122 | Beleggingsrisico | Drager_beleggingsrisico + Verwerking_verschil_beleggingsrisico | — | low |  |
| 147 | Aanspraak_gebaseerd_op_staffel | Methode_bepaling_aanspraak | nee | low | ⚠ |
| 151 | Maximering_wezenpensioen | Indicatie_maximum_aantal_kinderen | nee | low | ⚠ |
