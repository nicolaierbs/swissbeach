import streamlit as st

st.title("Kontakt")

if st.session_state.database:
    st.subheader(f"Aktuelles Turnier: {st.session_state.database}")

if st.button("Turnier wechseln"):
    st.session_state.database = None
    st.switch_page("app.py")

st.header("Kontaktinformationen")

st.write("Für Fragen, Feedback oder Support zu Swiss Beach:")

st.subheader("Entwickler")
st.write("**Nicolai Erbs**")

st.subheader("Adresse")
st.write("""
Roßdörfer Str. 117  
64287 Darmstadt  
Deutschland
""")

st.subheader("E-Mail")
st.write("📧 [swissbeach@erbs.eu](mailto:swissbeach@erbs.eu)")

st.subheader("Über Swiss Beach")
st.write("""
Swiss Beach ist ein kostenloses Turniermanagementsystem für Beachvolleyball, Spikeball und andere 2-gegen-2-Sportarten.
Es wurde entwickelt, um Turniere einfach und effizient zu organisieren.
""")

st.subheader("Support")
st.write("""
Bei technischen Problemen oder Fragen zur Nutzung, bitte eine E-Mail senden.
Antworten werden in der Regel innerhalb von 24 Stunden gegeben.
""")