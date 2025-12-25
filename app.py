import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wyszukiwarka Zawodnika", layout="centered")

st.title("🏃 System Wyszukiwania Zawodników")
st.write("Wgraj plik Excel, aby umożliwić wyszukiwanie po numerze startowym.")

# 1. Przesyłanie pliku
uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx"])

if uploaded_file:
    # Wczytanie danych
    df = pd.read_excel(uploaded_file)
    
    # Czyszczenie nazw kolumn (usuwamy spacje)
    df.columns = df.columns.str.strip()
    
    st.success("Plik wczytany pomyślnie!")
    
    # 2. Pole wyszukiwania
    search_query = st.text_input("Wpisz numer startowy zawodnika:", "")

    if search_query:
        # Przeszukiwanie (zamieniamy na string, żeby uniknąć błędów formatowania)
        df['Numer Startowy'] = df['Numer Startowy'].astype(str)
        result = df[df['Numer Startowy'] == str(search_query)]
        
        if not result.empty:
            st.subheader("Wyniki wyszukiwania:")
            # Wyświetlamy ładne karty z danymi
            for index, row in result.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Imię i Nazwisko", f"{row['Imię']} {row['Nazwisko']}")
                    st.write(f"📍 **Miejscowość:** {row['Miejscowość']}")
                with col2:
                    st.write(f"🛡️ **Klub:** {row['Klub']}")
        else:
            st.warning(f"Nie znaleziono zawodnika o numerze: {search_query}")

else:
    st.info("Oczekiwanie na przesłanie pliku...")
