import streamlit as st
import pandas as pd

# Ustawienia strony
st.set_page_config(page_title="Wyszukiwarka Zawodników by Arkadiusz KUBAŚ - parkrun Skórzec", page_icon="🌳", layout="centered")

# Niestandardowy styl CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .athlete-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 10px solid #00af41;
        margin-bottom: 20px;
    }
    .card-label {
        color: #666;
        font-size: 14px;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .card-value {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    h2 { color: #00af41 !important; margin-top: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- KONFIGURACJA BAZY ---
SHEET_ID = "10vOqcwAtnBtznQ1nEUX2L27W3Xz2ZC1A"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/10vOqcwAtnBtznQ1nEUX2L27W3Xz2ZC1A/export?format=csv"

# Logo parkrun Polska i nagłówek
st.image("https://images.parkrun.com/website/generic/logo_white_background.png", width=220)
st.title("🌳 parkrun Skórzec")
st.subheader("Wyszukiwarka numerów startowych")

@st.cache_data(ttl=30)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        st.error(f"Błąd bazy danych: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    with st.container():
        st.write("---")
        search_query = st.number_input("Wpisz numer startowy:", min_value=1, max_value=99999, step=1, value=None, placeholder="Wpisz numer...")
        st.write("---")

    if search_query:
        df['Numer Startowy'] = df['Numer Startowy'].astype(str)
        result = df[df['Numer Startowy'] == str(int(search_query))]
        
        if not result.empty:
            for index, row in result.iterrows():
                # Wyświetlanie wszystkich danych w jednej estetycznej ramce
                st.markdown(f"""
                <div class="athlete-card">
                    <div class="card-label">Zawodnik:</div>
                    <h2>{row['Imię']} {row['Nazwisko']}</h2>
                    
                    <div class="card-label">Numer ID:</div>
                    <div class="card-value">#{row['Numer Startowy']}</div>
                    
                    <div class="card-label">Klub:</div>
                    <div class="card-value">{row['Klub']}</div>
                    
                    <div class="card-label">Miejscowość:</div>
                    <div class="card-value">{row['Miejscowość']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Brak tego numeru w bazie parkrun Skórzec.")
else:
    st.info("Łączenie z bazą danych parkrun...")
