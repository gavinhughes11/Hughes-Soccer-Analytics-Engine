import streamlit as st
import matplotlib.pyplot as plt
from config import (
    GPLUS_LABELS,
    PER90_STATS,
    POSITION_LABELS,
    SEASONS,
    STAT_LABELS,
)
from app.data import load_raw_stats, load_finishing_ratings, load_player_stats
from charts.leaderboard import plot_leaderboard
from charts.export import to_png

league = st.session_state["league"]
season = st.session_state["season"]
playoffs = st.session_state["playoffs"]
stats = load_player_stats(league, season, playoffs)

labels = {f"{s}_per90": f"{STAT_LABELS[s]} per 90" for s in PER90_STATS}
labels["gplus_per90"] = "g+ per 90"
for column, name in GPLUS_LABELS.items():
    labels[f"{column}_per90"] = f"g+ {name} per 90"
if season == SEASONS[league][-1]:
    labels = {"finishing_rating": "Finishing Rating"} | labels

positions = {"all": "All positions"} | {
    code: name.capitalize() for code, name in POSITION_LABELS.items()
}

st.title("Leaderboard")
stat = st.selectbox("Stat", list(labels), format_func=labels.get)
position = st.selectbox("Position", list(positions), format_func=positions.get)
n = st.slider("Number of players", 5, 25, 10)

if stat == "finishing_rating":
    ratings = load_finishing_ratings(league, playoffs)
    teams = (
        load_raw_stats(league, season, playoffs)
        .sort_values("minutes_played")
        .drop_duplicates("player_id", keep="last")
    )
    table = ratings.merge(
        teams[["player_id", "team_id", "team_name", "general_position"]],
        on="player_id",
        how="left",
    )
    minimum = "Min. 450 minutes and 20 shots"
else:
    table = stats
    minimum = "Min. 450 minutes"

if position != "all":
    table = table[table["general_position"] == position]
table = table.dropna(subset=[stat])

if len(table) == 0:
    st.info(f"No {positions[position].lower()} qualify for this stat.")
    st.stop()

subtitle = f"{minimum} - {positions[position].lower()} - bar color = team"
fig = plot_leaderboard(
    table, stat, f"Top {n} - {labels[stat]} - {league.upper()} {season}", subtitle, n=n
)
png = to_png(fig)
plt.close(fig)
st.image(png, width="stretch")
st.download_button(
    label="Download PNG",
    data=png,
    file_name=f"{league}-{season}-top-{n}-{stat}-{position}.png",
    mime="image/png",
    on_click="ignore",
)

st.dataframe(
    table.sort_values(stat, ascending=False).head(n)[
        ["player_name", "team_name", stat]
    ],
    hide_index=True,
)
