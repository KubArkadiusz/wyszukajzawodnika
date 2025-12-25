import streamlit as st
import pandas as pd

# Ustawienia strony z brandingiem parkrun
st.set_page_config(page_title="Wyszukiwarka Zawodników by Aradiusz KUBAŚ - parkrun Skórzec ", page_icon="🌳", layout="centered")

# Niestandardowy styl CSS dla kart i wymuszenia klawiatury numerycznej
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    /* Styl karty zawodnika parkrun */
    .athlete-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 10px solid #00af41; /* Zielony kolor parkrun */
        margin-bottom: 20px;
    }
    h2 { color: #00af41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- KONFIGURACJA BAZY ---
SHEET_ID = "10vOqcwAtnBtznQ1nEUX2L27W3Xz2ZC1A"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Logo parkrun i nagłówek
st.image("https://images.parkrun.com/website/generic/logo_white_background.png", width=200)
st.title("🌳 parkrun Skórzec")
st.subheader("Wyszukiwarka numerów startowych")

@st.cache_data(ttl=30) # Szybsze odświeżanie dla wyników na żywo
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        st.error(f"Nie udało się pobrać bazy danych: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    with st.container():
        st.write("---")
        # st.number_input wymusza otwarcie klawiatury numerycznej na telefonach (iOS/Android)
        search_query = st.number_input("Wpisz swój numer startowy:", min_value=1, max_value=9999, step=1, value=None, placeholder="Kliknij tutaj, aby wpisać numer...")
        st.write("---")

    if search_query:
        # Konwersja na str do porównania
        df['Numer Startowy'] = df['Numer Startowy'].astype(str)
        result = df[df['Numer Startowy'] == str(int(search_query))]
        
        if not result.empty:
            for index, row in result.iterrows():
                st.balloons()
                st.markdown(f"""
                <div class="athlete-card">
                    <p style='margin-bottom: 0; color: #666;'>ZAWODNIK:</p>
                    <h2 style='margin-top: 0;'>{row['Imię']} {row['Nazwisko']}</h2>
                    <p style='font-size: 18px;'><b>Klub:</b> {row['Klub']}</p>
                    <p style='font-size: 18px;'><b>Miejscowość:</b> {row['Miejscowość']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                c1.metric("Status", "Gotowy do startu")
                c2.metric("Numer ID", f"#{row['Numer Startowy']}")
        else:
            st.error("❌ Brak tego numeru w bazie parkrun Skórzec.")
else:
    st.info("Oczekiwanie na połączenie z Arkuszem Google...")
