import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Schema Markup Generator 🛠️",  # Nome dell'app
    page_icon="🛠️",  # Emoji o icona
    layout="centered",  # Layout centrato
    initial_sidebar_state="expanded"  # Sidebar espansa di default
    description="Uno strumento facile e veloce per generare e ottimizzare il markup strutturato delle pagine del suo sito partendo da una URL ottimizzata di un competitor."
)

def estrai_schema_markup(url):
    """Estrai il markup strutturato schema.org da una pagina web."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cerca il markup JSON-LD
        json_ld = soup.find_all('script', {'type': 'application/ld+json'})
        
        schema_data = []
        for script in json_ld:
            if script.string:
                try:
                    # Tenta di caricare il JSON ignorando caratteri non validi
                    schema_data.append(json.loads(script.string))
                except json.JSONDecodeError as e:
                    st.warning(f"JSON malformato trovato e ignorato: {e}")
        return schema_data
    except Exception as e:
        st.error(f"Errore nell'estrazione del markup da {url}: {e}")
        return []

def genera_schema_ottimizzato(schema_cliente, schema_competitor):
    """Genera il markup schema ottimizzato unendo le informazioni del cliente con quelle del competitor."""
    try:
        # Combina i dati del cliente con quelli del competitor (logica personalizzabile)
        schema_ottimizzato = schema_cliente.copy() if schema_cliente else {}

        for item in schema_competitor:
            if isinstance(item, dict):
                for key, value in item.items():
                    if key not in schema_ottimizzato:
                        schema_ottimizzato[key] = value

        return schema_ottimizzato
    except Exception as e:
        st.error(f"Errore nella generazione del markup ottimizzato: {e}")
        return {}

# App Streamlit
st.title("Tool per ottimizzare lo Schema Markup")

# Inserimento URL da parte dell'utente
url_cliente = st.text_input("Inserisci l'URL del sito da ottimizzare:")
url_competitor = st.text_input("Inserisci l'URL della pagina del competitor:")

if st.button("Genera Schema Markup Ottimizzato"):
    if url_cliente and url_competitor:
        # Estrazione schema markup
        schema_cliente = estrai_schema_markup(url_cliente)
        schema_competitor = estrai_schema_markup(url_competitor)

        if schema_competitor:
            st.success("Schema markup estratto dal competitor con successo!")
            schema_ottimizzato = genera_schema_ottimizzato(schema_cliente[0] if schema_cliente else {}, schema_competitor)

            # Risultato finale in JSON
            st.subheader("Markup strutturato ottimizzato:")
            st.json(schema_ottimizzato)
        else:
            st.error("Non è stato possibile estrarre il markup dal competitor.")
    else:
        st.error("Inserisci entrambi gli URL per procedere.")
