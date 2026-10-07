import streamlit as st
from app.data import load_player_stats

league = st.session_state["league"]
season = st.session_state["season"]

stats = load_player_stats(league, season)

st.title("Player")
st.write(f"{len(stats)} qualified players")
st.dataframe(
    stats[
        [
            "player_name",
            "team_name",
            "general_position",
            "minutes_played",
            "goals",
            "xgoals",
        ]
    ],
    hide_index=True,
)
