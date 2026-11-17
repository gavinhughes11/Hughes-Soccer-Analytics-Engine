import matplotlib.pyplot as plt
import streamlit as st

from app.data import (
    load_finishing_ratings,
    load_goalkeeper_stats,
    load_player_stats,
    load_raw_goalkeeper_stats,
    load_raw_stats,
    load_shots,
)
from charts.export import to_png
from charts.gplus import plot_gplus
from charts.pizza import plot_pizza
from charts.shot_map import plot_shot_map
from charts.team_colors import team_color
from config import GK_GPLUS_LABELS, SEASONS
from metrics.goalkeeping import add_goalkeeper_metrics

league = st.session_state["league"]
season = st.session_state["season"]
playoffs = st.session_state["playoffs"]

stats = load_player_stats(league, season, playoffs)

names = sorted(stats["player_name"].unique())
name = st.selectbox("Player", names)

rows = stats[stats["player_name"] == name]
player = rows.sort_values("minutes_played").iloc[-1]
raw = load_raw_stats(league, season, playoffs)
all_rows = raw[raw["player_id"] == player["player_id"]]
file_start = f"{name}-{league}-{season}".lower().replace(" ", "-")
color = team_color(player["team_id"])
is_keeper = player["general_position"] == "GK"

st.title(name)
st.caption(
    f"{player['team_name']} - {player['general_position']} - {league.upper()} {season}"
)

if is_keeper:
    keepers = load_goalkeeper_stats(league, season, playoffs)
    keeper = keepers[
        (keepers["player_id"] == player["player_id"])
        & (keepers["team_id"] == player["team_id"])
    ].iloc[0]
    raw_keepers = load_raw_goalkeeper_stats(league, season, playoffs)
    keeper_rows = raw_keepers[raw_keepers["player_id"] == player["player_id"]]
    totals = keeper_rows[
        [
            "minutes_played",
            "shots_faced",
            "saves",
            "goals_conceded",
            "xgoals_gk_faced",
            "gk_gplus",
        ]
    ].sum()
    totals = add_goalkeeper_metrics(totals)

    cols = st.columns(6)
    cols[0].metric("Minutes", int(totals["minutes_played"]))
    cols[1].metric("Shots faced", int(totals["shots_faced"]))
    cols[2].metric("Saves", int(totals["saves"]))
    cols[3].metric(
        "Save %",
        f"{totals['save_pct']:.1f}%",
        help="Saves ÷ (saves + goals conceded).",
    )
    cols[4].metric(
        "Goals prevented",
        f"{totals['goals_prevented']:+.1f}",
        help="xG faced minus goals conceded. Positive means the keeper let in fewer "
        "goals than the shots they faced deserved.",
    )
    cols[5].metric(
        "Keeper g+",
        f"{totals['gk_gplus']:+.2f}",
        help="Goals added above average from American Soccer Analysis's goalkeeper "
        "model: shot-stopping, claiming crosses, sweeping, handling, fielding and "
        "passing, compared with an average keeper's actions.",
    )

    st.subheader("Goals added (g+)")
    left, right = st.columns(2)
    with left:
        fig = plot_gplus(
            keeper,
            f"{name} - {season}",
            league.upper(),
            color=color,
            labels=GK_GPLUS_LABELS,
            total="gk_gplus",
        )
        png = to_png(fig)
        plt.close(fig)
        st.image(png, width="stretch")
        st.download_button(
            label="Download PNG",
            data=png,
            file_name=f"{file_start}-keeper-gplus.png",
            mime="image/png",
            on_click="ignore",
        )
else:
    rating = "-"

    if season == SEASONS[league][-1]:
        ratings = load_finishing_ratings(league, playoffs)
        match = ratings[ratings["player_id"] == player["player_id"]]
        if len(match) > 0:
            rating = int(round(match["finishing_rating"].iloc[0], 0))

    cols = st.columns(6)
    cols[0].metric("Minutes", int(all_rows["minutes_played"].sum()))
    cols[1].metric("Goals", int(all_rows["goals"].sum()))
    cols[2].metric("xG", f"{all_rows['xgoals'].sum():.1f}")
    cols[3].metric("Shots", int(all_rows["shots"].sum()))
    cols[4].metric(
        "Finishing Rating",
        rating,
        help="0 to 100. Needs 20+ shots and 450+ minutes. Latest season only.",
    )
    cols[5].metric(
        "g+",
        f"{all_rows['gplus'].sum():+.2f}",
        help="Goals added above average: how much a player's actions changed their "
        "team's chances of scoring and conceding, compared with an average player.",
    )

    shots = load_shots(league, season, playoffs)
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

    st.subheader("Goals added (g+)")
    left, right = st.columns(2)
    with left:
        fig = plot_gplus(player, f"{name} - {season}", league.upper(), color=color)
        png = to_png(fig)
        plt.close(fig)
        st.image(png, width="stretch")
        st.download_button(
            label="Download PNG",
            data=png,
            file_name=f"{file_start}-gplus.png",
            mime="image/png",
            on_click="ignore",
        )
