import streamlit as st
import pandas as pd

st.set_page_config(page_title="Globalna Baza Zawodników", layout="centered")

# --- KONFIGURACJA ---
# Skopiuj link do swojego arkusza Google i zamień końcówkę /edit... na /export?format=csv
SHEET_ID = "TUTAJ_WSTAW_ID_TWOJEGO_ARKUSZA" # Znajdziesz je w linku między /d/ a /edit
SHEET_URL = f"https://docs.google.com/spreadsheets/d/10vOqcwAtnBtznQ1nEUX2L27W3Xz2ZC1A/export?format=csv"

st.title("🏃 Globalna Wyszukiwarka Zawodników")
st.write("Dane są pobierane w czasie rzeczywistym z centralnej bazy.")

# Funkcja pobierania danych (z cache, żeby nie przeciążać serwera)
@st.cache_data(ttl=60) # Dane odświeżają się co 60 sekund
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    df.columns = df.columns.str.strip()
    
    # Lupka
    search_query = st.text_input("Wpisz numer startowy:", "")

    if search_query:
        df['Numer Startowy'] = df['Numer Startowy'].astype(str)
        result = df[df['Numer Startowy'] == str(search_query)]
        
        if not result.empty:
            for index, row in result.iterrows():
                st.success(f"Znaleziono: {row['Imię']} {row['Nazwisko']}")
                st.write(f"📍 Miejscowość: {row['Miejscowość']} | 🛡️ Klub: {row['Klub']}")
        else:
            st.warning("Brak zawodnika o tym numerze.")
            
except Exception as e:
    st.error("Błąd połączenia z bazą danych. Sprawdź link do arkusza.")
