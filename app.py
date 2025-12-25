import streamlit as st
import pandas as pd

# 1. Ustawienia strony
st.set_page_config(
    page_title="Wyszukiwarka Zawodników by Arkadiusz KUBAŚ - parkrun Skórzec", 
    page_icon="🌳", 
    layout="centered"
)

# 2. Definicja stylów CSS (Niebieski motyw)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .athlete-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 10px solid #007bff;
        margin-bottom: 20px;
    }
    .card-label {
        color: #666;
        font-size: 13px;
        text-transform: uppercase;
        margin-bottom: 2px;
        font-family: sans-serif;
    }
    .big-blue-value {
        color: #007bff;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 15px;
        line-height: 1.2;
        font-family: sans-serif;
    }
    .id-value {
        font-size: 20px;
        color: #333;
        font-weight: bold;
        margin-bottom: 15px;
        font-family: sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Konfiguracja Bazy Danych
SHEET_ID = "10vOqcwAtnBtznQ1nEUX2L27W3Xz2ZC1A"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 4. Nagłówki i Logo
st.image("https://images.parkrun.com/website/generic/logo_white_background.png", width=200)
st.title("Wyszukiwarka Zawodników by Arkadiusz KUBAŚ")
st.subheader("parkrun Skórzec - zapraszamy w każdą sobotę")

@st.cache_data(ttl=30)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()

# 5. Interfejs wyszukiwania
if not df.empty:
    st.write("---")
    search_query = st.number_input(
        "Wpisz numer startowy:", 
        min_value=1, 
        max_value=99999, 
        step=1, 
        value=None, 
        placeholder="Wpisz numer..."
    )
    st.write("---")

    if search_query:
        df['Numer Startowy'] = df['Numer Startowy'].astype(str)
        result = df[df['Numer Startowy'] == str(int(search_query))]
        
        if not result.empty:
            for index, row in result.iterrows():
                # Budujemy HTML jako jedną czystą zmienną przed wyświetleniem
                karta_html = f"""
                <div class="athlete-card">
                    <div class="card-label">Zawodnik:</div>
                    <div class="big-blue-value">{row['Imię']} {row['Nazwisko']}</div>
                    <div class="card-label">Numer ID:</div>
                    <div class="id-value">#{row['Numer Startowy']}</div>
                    <div class="card-label">Klub:</div>
                    <div class="big-blue-value">{row['Klub']}</div>
                    <div class="card-label">Miejscowość:</div>
                    <div class="big-blue-value">{row['Miejscowość']}</div>
                </div>
                """
                # Wyświetlamy gotową zmienną
                st.markdown(karta_html, unsafe_allow_html=True)
        else:
            st.error("❌ Brak tego numeru w bazie parkrun Skórzec.")
else:
    st.info("Łączenie z bazą danych parkrun...")
