import streamlit as st

st.title("Data Usage")

if st.button("Change Tournament"):
    st.session_state.database = None
    st.switch_page("app.py")

st.write("Information about data usage...")  # Placeholder