import streamlit as st
import matcher

st.title("Config")

if not st.session_state.database:
    st.error("No tournament selected.")
    st.stop()

if st.button("Change Tournament"):
    st.session_state.database = None
    st.switch_page("app.py")

config = matcher.tournament_config(st.session_state.database)
st.json(config)