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

def get_latest_docs_sorted(fetch_limit=500, display_limit=25):
    # 1. Haal eerst het totaal aantal op
    r = requests.get(f"{API_BASE}documents?limit=1")
    if r.status_code != 200:
        return None
    total = int(r.json()['result']['totalCount'])
    
    # 2. Haal een grotere batch op (bijv. de laatste 500 ID's) 
    # om te zorgen dat we de meest recente datums ook echt vangen
    offset = max(0, total - fetch_limit)
    r = requests.get(f"{API_BASE}documents?limit={fetch_limit}&offset={offset}")
    docs = r.json()['result']['documents']
    
    # 3. Data opschonen en datums omzetten voor sortering
    processed = []
    for d in docs:
        raw_date = d.get('publicationDate', {}).get('date', '')
        if not raw_date: continue
        
        # Converteer naar echt datetime object voor betrouwbare sortering
        try:
            date_obj = datetime.strptime(raw_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
        except:
            continue

        # Curator Regel: Verbeter de titel als deze 'besluit.pdf' is
        titel = d.get('description') or d.get('fileName')
        if not titel or titel.lower() == "besluit.pdf":
            titel = f"[{d.get('documentTypeLabel')}] - {d.get('fileName')}"
            
        doc_id = d.get('id')
        download_url = f"https://ris.gemeenteraadhuizen.nl/api/v2/documents/{doc_id}/download"
        
        processed.append({
            "Datum_Sort": date_obj, # Voor sortering achter de schermen
            "Datum": date_obj.strftime('%d-%m-%Y'),
            "Onderwerp / Titel": titel,
            "Type": d.get('documentTypeLabel'),
            "Download": f"[Download PDF]({download_url})"
        })

    # 4. Sorteer de hele batch op Datum_Sort (Nieuwste bovenaan)
    df = pd.DataFrame(processed)
    df = df.sort_values(by="Datum_Sort", ascending=False)
    
    # Verwijder de hulpkolom en geef de top X terug
    return df.drop(columns=["Datum_Sort"]).head(display_limit)

# UI sectie
with st.spinner('Data ophalen uit Huizen...'):
    df_docs = get_latest_docs_sorted(fetch_limit=500, display_limit=30)

if df_docs is not None:
    st.write(f"Overzicht van de laatste documenten (gesorteerd op publicatiedatum):")
    
    # Render de tabel met klikbare links
    st.write(df_docs.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.info("Let op: Deze lijst is samengesteld uit de laatste 500 toevoegingen aan het RIS en gesorteerd op datum.")
else:
    st.error("Kon geen data ophalen.")
