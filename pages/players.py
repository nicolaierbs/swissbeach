import streamlit as st
import data_connector
import pandas as pd

st.title("Players")

if not st.session_state.database:
    st.error("No tournament selected.")
    st.stop()

if st.button("Change Tournament"):
    st.session_state.database = None
    st.switch_page("app.py")

# Add player
with st.form("add_player"):
    name = st.text_input("Player Name")
    submitted = st.form_submit_button("Add Player")
    if submitted and name:
        data_connector.new_player(name, st.session_state.database)
        st.success(f"Added {name}")
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
            'Active': player['active'],
            'Matches': stats.get('matches', 0),
            'Won': stats.get('won', 0),
            'Lost': stats.get('lost', 0),
            'Percentage': stats.get('percentage', 0),
            'Child': player['markers']['child'],
            'Female': player['markers']['female'],
            'Male': player['markers']['male']
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # Actions below dataframe
    st.subheader("Player Actions")
    for player in players:
        col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
        with col1:
            st.write(player['name'])
        with col2:
            if st.button("Toggle Active", key=f"toggle_{player['_id']}"):
                data_connector.toggle_player(player['_id'], st.session_state.database)
                st.rerun()
        with col3:
            if st.button("Child", key=f"child_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'child', st.session_state.database)
                st.rerun()
        with col4:
            if st.button("Female", key=f"female_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'female', st.session_state.database)
                st.rerun()
        with col5:
            if st.button("Male", key=f"male_{player['_id']}"):
                data_connector.change_marker(player['_id'], 'male', st.session_state.database)
                st.rerun()
else:
    st.write("No players yet.")