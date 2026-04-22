import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuratie
API_BASE = "https://ris.gemeenteraadhuizen.nl/api/v2/"
ST_TITLE = "Huizen RIS Monitor (Fase 1)"

st.set_page_config(page_title=ST_TITLE, layout="wide")

st.title("📊 Huizen RIS Monitor")
st.markdown(f"Ontsluiting van de [Open Data van de Gemeente Huizen]({API_BASE})")

def get_latest_docs(limit=20):
    # 1. Haal totaal aantal op
    r = requests.get(f"{API_BASE}documents?limit=1")
    if r.status_code != 200:
        return None
    total = r.json()['result']['totalCount']
    
    # 2. Haal de laatste batch op (nieuwste eerst)
    offset = max(0, int(total) - limit)
    r = requests.get(f"{API_BASE}documents?limit={limit}&offset={offset}")
    docs = r.json()['result']['documents']
    
    # 3. Draai de lijst om (nieuwste boven)
    docs.reverse()
    return docs

docs = get_latest_docs()

if docs:
    processed_data = []
    for d in docs:
        # Curator Regel: Als beschrijving leeg of 'besluit.pdf' is, gebruik type
        titel = d.get('description')
        if not titel or titel.lower() == "besluit.pdf":
            titel = f"[{d.get('documentTypeLabel')}] - Bestand: {d.get('fileName')}"
        
        # Datum formatten
        raw_date = d.get('publicationDate', {}).get('date', '')
        date_obj = datetime.strptime(raw_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
        
        # Download link bouwen (De 'magic' link)
        doc_id = d.get('id')
        download_url = f"https://ris.gemeenteraadhuizen.nl/api/v2/documents/{doc_id}/download"
        
        processed_data.append({
            "Datum": date_obj.strftime('%d-%m-%Y'),
            "Onderwerp / Titel": titel,
            "Type": d.get('documentTypeLabel'),
            "Bestand": f"[Download PDF]({download_url})"
        })

    df = pd.DataFrame(processed_data)
    
    # Weergave in Streamlit
    st.write(f"Tonen van de laatste {len(docs)} gepubliceerde documenten:")
    st.table(df) # Of gebruik st.dataframe(df) voor een interactieve tabel
else:
    st.error("Kon geen data ophalen uit de API van Huizen.")

st.info("Tip: Deze monitor haalt live data op. Vernieuw de pagina voor de laatste stand.")
