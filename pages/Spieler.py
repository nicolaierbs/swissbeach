import streamlit as st
import data_connector
import pandas as pd

st.title("Spieler")

if not st.session_state.database:
    st.error("No tournament selected.")
    st.stop()

# Display current tournament
st.subheader(f"Aktuelles Turnier: {st.session_state.database}")

if st.button("Turnier wechseln"):
    st.session_state.database = None
    st.switch_page("app.py")

# Add player
with st.form("add_player"):
    name = st.text_input("Spieler Name")
    submitted = st.form_submit_button("Spieler hinzufügen")
    if submitted and name:
        data_connector.new_player(name, st.session_state.database)
        st.success(f"{name} hinzugefügt")
        st.rerun()

# Show players as dataframe
players = data_connector.all_players(st.session_state.database)
if players:
    # Prepare data for dataframe
    data = []
    for player in players:
        stats = player.get('statistics', {})
        data.append({
            'Name': player['name'],
            'Aktiv': player['active'],
            'Matches': stats.get('matches', 0),
            'Gewonnen': stats.get('won', 0),
            'Verloren': stats.get('lost', 0),
            'Prozent': stats.get('percentage', 0),
            'Kind': player['markers']['child'],
            'Weiblich': player['markers']['female'],
            'Männlich': player['markers']['male']
        })
    df = pd.DataFrame(data)
    st.dataframe(df, width='stretch')

    # Actions below dataframe
    st.subheader("Spieler Aktionen")
    for player in players:
        col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
        with col1:
            st.write(player['name'])
        with col2:
            if st.button("Aktiv umschalten", key=f"toggle_{player['_id']}"):
                data_connector.toggle_player(player['_id'], st.session_state.database)
                st.rerun()
        with col3:
            if st.button("Kind", key=f"child_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'child', st.session_state.database)
                st.rerun()
        with col4:
            if st.button("Weiblich", key=f"female_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'female', st.session_state.database)
                st.rerun()
        with col5:
            if st.button("Männlich", key=f"male_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'male', st.session_state.database)
                st.rerun()
else:
    st.write("Noch keine Spieler.")