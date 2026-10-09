import streamlit as st
import matplotlib.pyplot as plt
from app.data import (
    load_player_stats,
    load_finishing_ratings,
    load_shots,
    load_raw_stats,
)
from charts.pizza import plot_pizza
from charts.shot_map import plot_shot_map
from charts.team_colors import team_color
from config import SEASONS
from charts.export import to_png

league = st.session_state["league"]
season = st.session_state["season"]

stats = load_player_stats(league, season)

names = sorted(stats["player_name"].unique())
name = st.selectbox("Player", names)

rows = stats[stats["player_name"] == name]
player = rows.sort_values("minutes_played").iloc[-1]
raw = load_raw_stats(league, season)
all_rows = raw[raw["player_id"] == player["player_id"]]
file_start = f"{name}-{league}-{season}".lower().replace(" ", "-")
color = team_color(player["team_id"])

st.title(name)
st.caption(
    f"{player['team_name']} - {player['general_position']} - {league.upper()} {season}"
)

rating = "-"

if season == SEASONS[league][-1]:
    ratings = load_finishing_ratings(league)
    match = ratings[ratings["player_id"] == player["player_id"]]
    if len(match) > 0:
        rating = int(round(match["finishing_rating"].iloc[0], 0))

cols = st.columns(5)
cols[0].metric("Minutes", int(all_rows["minutes_played"].sum()))
cols[1].metric("Goals", int(all_rows["goals"].sum()))
cols[2].metric("xG", f"{all_rows['xgoals'].sum():.1f}")
cols[3].metric("Shots", int(all_rows["shots"].sum()))
cols[4].metric(
    "Finishing Rating",
    rating,
    help="0 to 100. Needs 20+ shots and 450+ minutes. Latest season only.",
)

shots = load_shots(league, season)
player_shots = shots[shots["shooter_player_id"] == player["player_id"]]

left, right = st.columns(2)
with left:
    fig = plot_shot_map(player_shots, f"{name} - {season}", color=color)
    png = to_png(fig)
    plt.close(fig)
    st.image(png, width="stretch")
    st.download_button(
        label="Download PNG",
        data=png,
        file_name=f"{file_start}-shot-map.png",
        mime="image/png",
        on_click="ignore",
    )
with right:
    fig = plot_pizza(player, f"{name} - {season}", f"{league.upper()}", color=color)
    png = to_png(fig)
    plt.close(fig)
    st.image(png, width="stretch")
    st.download_button(
        label="Download PNG",
        data=png,
        file_name=f"{file_start}-pizza.png",
        mime="image/png",
        on_click="ignore",
    )
