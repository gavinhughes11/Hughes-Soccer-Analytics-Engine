import streamlit as st
import matplotlib.pyplot as plt
from config import PER90_STATS, SEASONS, STAT_LABELS
from app.data import load_raw_stats, load_finishing_ratings, load_player_stats
from charts.leaderboard import plot_leaderboard
from charts.export import to_png

league = st.session_state["league"]
season = st.session_state["season"]
stats = load_player_stats(league, season)

labels = {f"{s}_per90": f"{STAT_LABELS[s]} per 90" for s in PER90_STATS}
if season == SEASONS[league][-1]:
    labels = {"finishing_rating": "Finishing Rating"} | labels

st.title("Leaderboard")
stat = st.selectbox("Stat", list(labels), format_func=labels.get)
n = st.slider("Number of players", 5, 25, 10)

if stat == "finishing_rating":
    ratings = load_finishing_ratings(league)
    teams = (
        load_raw_stats(league, season)
        .sort_values("minutes_played")
        .drop_duplicates("player_id", keep="last")
    )
    table = ratings.merge(
        teams[["player_id", "team_id", "team_name"]], on="player_id", how="left"
    )
    subtitle = "Min. 450 minutes and 20 shots - bar color = team"
else:
    table = stats
    subtitle = "Min. 450 minutes - bar color = team"

fig = plot_leaderboard(
    table, stat, f"Top {n} - {labels[stat]} - {league.upper()} {season}", subtitle, n=n
)
png = to_png(fig)
plt.close(fig)
st.image(png, width="stretch")
st.download_button(
    label="Download PNG",
    data=png,
    file_name=f"{league}-{season}-top-{n}-{stat}.png",
    mime="image/png",
    on_click="ignore",
)

st.dataframe(
    table.sort_values(stat, ascending=False).head(n)[
        ["player_name", "team_name", stat]
    ],
    hide_index=True,
)
