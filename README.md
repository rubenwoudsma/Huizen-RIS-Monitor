# 📊 Huizen RIS Monitor

**De brug tussen open data en een toegankelijke lokale democratie.**

Dit project ontsluit de open data van de Gemeente Huizen (via het Raadsinformatiesysteem - RIS) op een manier die daadwerkelijk bruikbaar is voor inwoners. 

## 🎯 Het Doel
Hoewel de Gemeente Huizen informatie openbaar maakt via een API conform de VNG-standaard, is de toegankelijkheid in de praktijk vaak beperkt. Inwoners stuiten regelmatig op lijsten met anonieme titels zoals `besluit.pdf`, zonder context of duidelijke herkomst.

De **Huizen RIS Monitor** fungeert als een 'digitale curator'. Het doel is:
1. **Chronologisch overzicht:** De meest recente documenten direct zichtbaar maken zonder complexe zoekopdrachten.
2. **Context herstellen:** Slimme logica die anonieme bestandsnamen probeert te koppelen aan de juiste metadata (zoals agendapunten en commissies).
3. **Digitale Soevereiniteit:** Het onafhankelijk ontsluiten van publieke informatie zonder tussenkomst van gesloten commerciële platformen.

## 🛠 Techniek
Deze applicatie is gebouwd met:
* **Python 3.x**
* **Streamlit** (voor de frontend interface)
* **Pandas** (voor dataverwerking)
* **Requests** (voor de communicatie met de RIS API v2 van Huizen)

De monitor maakt gebruik van de officiële API-endpoint van de gemeente Huizen: `https://ris.gemeenteraadhuizen.nl/api/v2/`

## 🚀 Installatie & Gebruik
Je kunt de live-versie van deze monitor bekijken op:
*TODO*

### Lokaal draaien:
1. Clone de repository: 
   ```bash
   git clone [https://github.com/rubenwoudsma/huizen-ris-monitor.git](https://github.com/rubenwoudsma/huizen-ris-monitor.git)
