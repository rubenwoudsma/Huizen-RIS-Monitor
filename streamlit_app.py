import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuratie
API_BASE = "https://ris.gemeenteraadhuizen.nl/api/v2/"
ST_TITLE = "Huizen RIS Monitor"

st.set_page_config(page_title=ST_TITLE, layout="wide")

# Sidebar voor instellingen (Pagination alternatief)
st.sidebar.header("Instellingen")
fetch_n = st.sidebar.slider("Aantal op te halen items uit database", 100, 1000, 500)
show_n = st.sidebar.slider("Aantal te tonen in tabel", 10, 100, 25)

st.title("📊 Huizen RIS Monitor")
st.markdown(f"Ontsluiting van de [Open Data van de Gemeente Huizen]({API_BASE})")

@st.cache_data(ttl=600) # Cache resultaten voor 10 minuten om API te ontlasten
def get_data(fetch_limit):
    # 1. Totaal ophalen
    try:
        r = requests.get(f"{API_BASE}documents?limit=1")
        total = int(r.json()['result']['totalCount'])
        
        # 2. Batch ophalen
        offset = max(0, total - fetch_limit)
        r = requests.get(f"{API_BASE}documents?limit={fetch_limit}&offset={offset}")
        return r.json()['result']['documents']
    except Exception as e:
        st.error(f"Fout bij ophalen data: {e}")
        return []

docs = get_data(fetch_n)

if docs:
    processed = []
    for d in docs:
        raw_date = d.get('publicationDate', {}).get('date', '')
        if not raw_date: continue
        
        date_obj = datetime.strptime(raw_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
        
        # Verbeterde Curator Logica
        titel = d.get('description') or d.get('fileName') or "Geen titel"
        doc_type = d.get('documentTypeLabel', 'Onbekend')
        
        # Als de titel te generiek is, voeg type toe
        if titel.lower() in ["besluit", "besluit.pdf", "bijlage", "bijlage.pdf"]:
            titel = f"{doc_type}: {titel}"
            
        doc_id = d.get('id')
        download_url = f"https://ris.gemeenteraadhuizen.nl/api/v2/documents/{doc_id}/download"
        
        processed.append({
            "Datum_Sort": date_obj,
            "Datum": date_obj.strftime('%d-%m-%Y'),
            "Onderwerp / Titel": titel,
            "Type": doc_type,
            "Bestand": download_url
        })

    df = pd.DataFrame(processed).sort_values(by="Datum_Sort", ascending=False)
    df_display = df.drop(columns=["Datum_Sort"]).head(show_n)

    # Weergave met de nieuwe st.dataframe config voor klikbare links
    st.dataframe(
        df_display,
        column_config={
            "Bestand": st.column_config.LinkColumn(
                "Download PDF",
                help="Klik om het originele document te downloaden",
                validate="^https://.*",
                display_text="Download PDF"
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.caption(f"Tabel toont de nieuwste {show_n} documenten uit een steekproef van de laatste {fetch_n} toevoegingen.")

else:
    st.warning("Geen documenten gevonden.")
