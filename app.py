import streamlit as st
import data_connector
import matcher
import re
from bson import ObjectId

# Set page config
st.set_page_config(page_title="Swiss Beach", page_icon="🏐", layout="wide")

# Initialize session state
if 'database' not in st.session_state:
    st.session_state.database = None

# Main content - Welcome page
st.title("Der flexible Turniermanager")
st.write("""
Willkommen zu Swiss Beach, dem Turniermanager für Beachvolleyball, Spikeball und mehr.
Mit diesem System kannst du dein Turnier für Sportarten im Modus 2 gegen 2 organisieren.
Mit Swiss Beach...
- ändern sich Teams kontinuierlich
- werden spannende Matches auf Basis der Rangliste zugelost
- können Spielerinnen und Spieler jederzeit einsteigen oder pausieren
- hat jeder zu jeder Zeit eine Übersicht der kommenden Matches und der Rangliste
- ist die Orga kostenlos und direkt einsetzbar
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Demo")
    st.write("Experimentiere mit einem vorhanden Turnier, um besser zu verstehen, wie du Swiss Beach nutzen kannst.")
    if st.button("Demo Turnier"):
        st.session_state.database = 'demo'
        st.switch_page("pages/players.py")

with col2:
    st.subheader("Dein Turnier")
    st.write("Start dein eigenes Turnier! Wähle einen Namen und starte.")
    with st.form("start_tournament"):
        tournament_name = st.text_input("Name")
        submitted = st.form_submit_button("Start")
        if submitted and tournament_name:
            tournament_name = re.sub(r'\W+', '', tournament_name)
            st.session_state.database = tournament_name
            st.switch_page("pages/players.py")
