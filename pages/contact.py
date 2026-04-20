import streamlit as st

st.title("Contact")

if st.button("Change Tournament"):
    st.session_state.database = None
    st.switch_page("app.py")

st.write("Contact information...")  # Placeholder