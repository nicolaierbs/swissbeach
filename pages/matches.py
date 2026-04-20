import streamlit as st
import data_connector
import matcher
import pandas as pd

st.title("Matches")

if not st.session_state.database:
    st.error("No tournament selected.")
    st.stop()

if st.button("Change Tournament"):
    st.session_state.database = None
    st.switch_page("app.py")

# Next game button
if st.button("Next Game"):
    next_match = matcher.next_match(data_connector.free_players(st.session_state.database), st.session_state.database)
    if next_match:
        data_connector.new_match(next_match, st.session_state.database)
        st.success("New match created")
    else:
        st.warning("Not enough players")
    st.rerun()

# Show matches as dataframe
matches = data_connector.matches_with_names(st.session_state.database)
if matches:
    # Prepare data for dataframe
    data = []
    for match in matches:
        result = match.get('result', {})
        winner = ""
        if result.get('team_a_won'):
            winner = "Team A"
        elif result.get('team_b_won'):
            winner = "Team B"
        data.append({
            'Team A': ', '.join(match['team_a_names']),
            'Team B': ', '.join(match['team_b_names']),
            'Inserted': match['inserted'],
            'Active': match.get('active', True),
            'Winner': winner
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # Actions for active matches
    active_matches = [m for m in matches if m.get('active', True)]
    if active_matches:
        st.subheader("Active Match Actions")
        for match in active_matches:
            st.write(f"Match: {', '.join(match['team_a_names'])} vs {', '.join(match['team_b_names'])}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Team A Wins", key=f"win_a_{match['_id']}"):
                    data_connector.match_result(match['_id'], True, False, st.session_state.database)
                    st.rerun()
            with col2:
                if st.button("Team B Wins", key=f"win_b_{match['_id']}"):
                    data_connector.match_result(match['_id'], False, True, st.session_state.database)
                    st.rerun()
            with col3:
                if st.button("Delete", key=f"delete_{match['_id']}"):
                    data_connector.delete_match(match['_id'], st.session_state.database)
                    st.rerun()
else:
    st.write("No matches yet.")