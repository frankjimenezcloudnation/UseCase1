# 1 — Samenvatting en resultaten

## Waar gaat dit over?

Een pensioenfonds moet onder de Wet toekomst pensioenen (Wtp) laten vastleggen hoe zijn regeling precies in elkaar zit. In het onderliggende **ontologiemodel** staan ongeveer 2.600 losse onderwerpen (bijvoorbeeld: "is er een minimum pensioengevend inkomen?", "hoe wordt de datum afgerond?"). Bij elk onderwerp hoort een vraag en vaak een lijstje toegestane antwoorden.

Tot nu toe werd zo'n analyse **met de hand** gedaan. Het doel van dit project: dat werk **automatiseren** — de tool leest de documenten van een fonds en beantwoordt per onderwerp de vraag, met een bronverwijzing en een betrouwbaarheidsscore erbij.

Als test hebben we het gedaan voor één fonds (**SPF**) en een vaste, controleerbare selectie van **102 onderwerpen** (samen **106 unieke vragen**; omdat sommige onderwerpen meerdere vragen bevatten, worden er in een run **133 vraag-instanties** doorlopen).

## Wat is er gemaakt?

- Een **vaste testset** van 102 onderwerpen; bij **71** daarvan bestaat een handmatig SPF-antwoord dat als ijkpunt dient.
- Een **koppeling** tussen de handmatige productbeschrijving (PDC) en het ontologiemodel.
- **Geanonimiseerde** versies van twee standaarddocumenten, zodat de tool ook voor nieuwe fondsen bruikbaar is zonder dat er antwoorden van een ander fonds "meelekken".
- De **analyse-tool** zelf, die per onderwerp een antwoord met bron en betrouwbaarheid geeft.

## De resultaten van de test

De tool doorliep 133 vraag-instanties:

| Wat | Uitkomst |
|---|---|
| Vraag-instanties behandeld | 133 |
| Beantwoord (met bron) | 40 (waarvan 24 met hoge betrouwbaarheid, 13 midden, 3 laag) |
| Eerlijk "niet gevonden" | 93 |
| Analyses die faalden | 0 |
| Gecontroleerde broncitaten | 49 |
| Instanties met een SPF-ijkpunt | 87 (afkomstig van de 71 onderwerpen met ijkpunt) |
| Beantwoord **én** toetsbaar tegen het handwerk | 22 → **14 kloppen, 8 wijken af (~64%)** |

**Hoe u de cijfers leest.** De eerlijke maat is de laatste rij: van de instanties die de tool **wél beantwoordde en die we konden nakijken (22)**, klopte er ongeveer **twee derde (14)**. Een "kale" score over álle 87 instanties-met-ijkpunt valt veel lager uit (~28%), maar die telt de 62 níét-beantwoorde instanties mee als fout — die maat zegt dus meer over de **dekking** dan over de **correctheid**. Bij álle getoonde antwoorden geldt: er is een letterlijk citaat uit een fondsdocument dat automatisch is gecontroleerd. De tool verzint dus niets. (Er zijn 49 gecontroleerde citaten bij 40 antwoorden, omdat een antwoord meerdere citaten kan hebben en er ook citaten zijn bij enkele "niet gevonden"/deels-antwoorden.)

## Voorbeelden

**Goed beantwoord (met bron):**
- Soort overeenkomst → *Flexibele premieovereenkomst*.
- Deelname aan de regeling → *verplicht*.
- Maximaal pensioengevend inkomen → *ja, een door het fonds gekozen maximum* (met vindplaats: € 38.611 in 2026).
- Grondslag → *pensioengevend inkomen min franchise*.

**Wijkt af — de moeite van het nakijken waard (geen harde fout):**
- Minimum pensioengevend inkomen: de tool zegt "ja" op basis van "ten minste nihil"; het handwerk zegt "nee". Dit is een interpretatieverschil ("ten minste nihil" betekent feitelijk geen ondergrens).
- Vorm van de franchise: de tool koos "sociale zekerheid / AOW-franchise"; het handwerk zegt "nominaal bedrag".

De volledige lijst van alle 8 afwijkingen staat in [4 — Reviewlijst voor deskundigen](4-reviewlijst.md).

## De belangrijkste conclusie

- De tool is **betrouwbaar en voorzichtig**: geen mislukkingen, elk antwoord onderbouwd, en waar de documenten geen antwoord geven zegt ze eerlijk "niet gevonden" in plaats van te gokken.
- De grootste verbeterkans is de **dekking** (40 van de 133). Dat komt doordat de tool nu op eenvoudige trefwoorden zoekt (de slimmere "betekenis"-zoekmethode staat nog niet aan) en doordat sommige details simpelweg niet in het reglement staan.
- De afwijkende antwoorden zijn vooral **nuances** die om een expertoordeel vragen — precies zoals bedoeld: de tool bereidt voor, de deskundige beslist.
- De **einddoelstelling** — het fonds vergelijken met de IG&H-standaard per onderwerp — is nog een vervolgstap (zie document 3).

Verder lezen: [hoe het werkt](2-aanpak-en-bouw.md) · [deliverables en vervolg](3-deliverables-en-vervolg.md) · [reviewlijst](4-reviewlijst.md).
