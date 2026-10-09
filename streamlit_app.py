import streamlit as st
from config import LEAGUES, SEASONS, DATA_UPDATED

st.set_page_config(page_title="Hughes Soccer Analytics", page_icon="⚽", layout="wide")

league = st.sidebar.selectbox("League", list(LEAGUES), format_func=LEAGUES.get)
season = st.sidebar.selectbox("Season", SEASONS[league][::-1])
st.session_state["league"] = league
st.session_state["season"] = season

st.sidebar.caption(
    "Data: [American Soccer Analysis](https://www.americansocceranalysis.com)"
    f" - regular season + playoffs - updated {DATA_UPDATED}"
)

pages = st.navigation(
    [
        st.Page("app/player.py", title="Player", icon=":material/person:"),
        st.Page(
            "app/leaderboard.py", title="Leaderboard", icon=":material/leaderboard:"
        ),
    ]
)
pages.run()
