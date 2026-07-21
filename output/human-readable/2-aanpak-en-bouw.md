# 2 — Aanpak en bouw

Dit document legt in gewone taal uit hoe de tool tot stand kwam. Vijf stappen.

## Stap 1 — De bouwstenen: het ontologiemodel en de PDC

- **Het ontologiemodel** (`OntologySnapshot`) is de gezamenlijke "taal" voor pensioenproducten. Het bevat ~2.600 **onderwerpen** (properties), elk met een naam, een vraag en — waar van toepassing — een lijstje toegestane antwoorden. De onderwerpen zijn gegroepeerd in **klassen** (bijvoorbeeld de klasse "Voorportaal" met een handvol vragen eronder).
- **De PDC Beroepse** is de handmatige productbeschrijving: per onderwerp en per fonds is aangevinkt welk antwoord geldt. Dit is het **ijkpunt** waartegen we de tool controleren — het is uitdrukkelijk géén bron waaruit de tool antwoorden voor het fonds mag halen.

## Stap 2 — Een vaste, controleerbare testset

We beginnen niet met alle 2.600 onderwerpen, maar met een **vaste selectie van 102 gekoppelde onderwerpen**. Bij **71** daarvan bestaat een handmatig SPF-antwoord dat als ijkpunt dient; die 71 laten ons de tool-antwoorden nakijken. (De 102 zijn geselecteerd omdat ze koppelbaar bleken tussen PDC en ontologie, niet omdat ze allemaal een ijkpunt hebben.)

Die 102 kwamen tot stand door de handmatige PDC te koppelen aan het ontologiemodel. Dat bleek niet één-op-één te kunnen op naam alleen (16 directe treffers), omdat de PDC bedrijfsnamen gebruikt en de ontologie technische namen. Daarom koppelden we op **klasse-niveau** en met behulp van de toegestane antwoorden.

## Stap 3 — De koppeling (mapping) door taalbegrip

Om de PDC-onderwerpen betrouwbaar aan de juiste ontologie-vragen te koppelen, hebben we een taalmodel de **betekenis** laten vergelijken (niet alleen de woorden). Resultaat: **102 van de 152** PDC-onderwerpen gekoppeld, elk met een betrouwbaarheidsscore (48 kwamen niet tot een koppeling, 2 leverden geen duidelijke uitkomst).

Daarbij kwamen ook **model-gaten** aan het licht: gevallen waarin de PDC een onderscheid maakt dat het ontologiemodel (nog) niet kan uitdrukken. Binnen de testset van 102 onderwerpen zijn dat er **23** (over alle 152 PDC-onderwerpen waren het er 36). Voorbeelden: bij "afkoopmoment" ontbreekt de keuze *emigratie*; bij "voorportaal" ontbreekt het onderscheid *verplicht/vrijwillig*. Dit is waardevolle input om het model te verbeteren.

## Stap 4 — Anonimiseren van de standaarddocumenten

Twee documenten (de standaard-productspecificatie en een technische analyse) bevatten al fondsspecifieke antwoorden. Als de tool die als bron voor een fonds zou gebruiken, zou ze "spieken". Omdat de tool ook voor **nieuwe fondsen** bruikbaar moet zijn — en omdat deze twee documenten straks de **IG&H-standaardkant** voeden — hebben we ze **geanonimiseerd**:

- fondsnamen (SPF, SPD, AKZO, …) vervangen door een neutrale aanduiding `[FONDS]`;
- de fondsspecifieke tekstblokken en losse "Fondsen"-paragrafen verwijderd.

Controle achteraf: **nul** fondsnamen meer in de geanonimiseerde versies. De originelen zijn ongewijzigd.

## Stap 5 — De tool

Per onderwerp doet de tool dit:

1. **Zoeken** in de fondsdocumenten (reglement, ABTN, implementatieplan, operating manual) naar relevante passages.
2. **Antwoorden** via een taalmodel: het kiest — als er een keuzelijst is — de best passende waarde, en geeft altijd ook een korte uitleg in gewone taal.
3. **Onderbouwen** met een letterlijk citaat (met paginanummer). Dat citaat wordt **automatisch gecontroleerd**: staat het echt in het genoemde document? Zo niet, dan wordt het als ongecontroleerd gemarkeerd.
4. **Eerlijk zijn**: is er geen onderbouwing te vinden, dan zegt de tool "niet gevonden" in plaats van te gokken.
5. Elk antwoord krijgt een **betrouwbaarheidsscore** (hoog/midden/laag), en een markering als het antwoord buiten de verwachte keuzelijst of het format valt.

Belangrijk principe: de tool beslist niets definitief. Ze bereidt voor en maakt alles herleidbaar; de deskundige beoordeelt.

## Waar dit naartoe gaat: fonds vs. IG&H-standaard

De uiteindelijke bedoeling is een **vergelijking**: dezelfde per-onderwerp-analyse ook doen voor de **IG&H-standaard** (uit de PDC, de standaardspecificatie en de Qwik-analyse), en dan per onderwerp bepalen waar het fonds afwijkt van wat IG&H aanbiedt. Daarbij geldt dat de standaard vaak **meerdere** mogelijke waarden per onderwerp heeft (een "menu"), terwijl een fonds meestal één concrete keuze maakt. Deze fondskant-analyse is de eerste helft daarvan; de standaardkant en de vergelijking zijn de volgende stap (zie document 3).

Verder lezen: [samenvatting en resultaten](1-samenvatting-en-resultaten.md) · [deliverables en vervolg](3-deliverables-en-vervolg.md) · [reviewlijst](4-reviewlijst.md).
