import streamlit as st

from app.data import load_prospects
from config import LEAGUES, PROSPECT_LADDERS

st.title("Prospect finder")
st.caption(
    "This page ignores the sidebar's league and season. It always predicts next "
    "season from the newest finished one."
)

target = st.segmented_control(
    "Breaking into",
    list(PROSPECT_LADDERS),
    format_func=LEAGUES.get,
    default="mls",
    required=True,
)
prospects = load_prospects(target)
latest_season = prospects["season"].max()
next_season = latest_season + 1


def source_name(source):
    # "mlsnp" -> "MLS NEXT Pro", "mls bench" -> "Major League Soccer bench"
    if source.endswith(" bench"):
        return f"{LEAGUES[target]} bench"
    return LEAGUES[source]


st.subheader(f"Who gets 450+ {LEAGUES[target]} minutes in {next_season}?")

with st.container(horizontal=True):
    options = sorted(prospects["source"].unique())
    sources = st.pills(
        f"Played in {latest_season}",
        options,
        selection_mode="multi",
        default=options,
        format_func=source_name,
    )
    max_age = st.slider("Max age", 16, 35, 23)
    n = st.slider("Number of players", 10, 100, 25)

board = prospects[
    prospects["source"].isin(sources) & (prospects["age"] <= max_age)
].head(n)
board = board.assign(source=board["source"].map(source_name))

st.dataframe(
    board[
        [
            "player_name",
            "team_name",
            "source",
            "general_position",
            "age",
            "minutes_played",
            "target_minutes",
            "probability",
        ]
    ],
    hide_index=True,
    column_config={
        "player_name": "Player",
        "team_name": f"{latest_season} team",
        "source": "Played in",
        "general_position": "Position",
        "age": st.column_config.NumberColumn("Age", format="%.1f"),
        "minutes_played": st.column_config.NumberColumn(
            f"{latest_season} minutes", format="%d"
        ),
        "target_minutes": st.column_config.NumberColumn(
            f"{LEAGUES[target]} minutes", format="%d"
        ),
        "probability": st.column_config.ProgressColumn(
            "Chance of 450+ minutes",
            format="percent",
            min_value=0,
            max_value=1,
        ),
    },
    alt=f"Top {n} prospects to play 450+ {LEAGUES[target]} minutes in {next_season}",
)

st.caption(
    f"**Breakout** = 450+ regular-season {LEAGUES[target]} minutes next season. "
    "The model is a logistic regression on age, minutes, where the player played, "
    "position, and per-90 percentiles. It predicts **who gets picked**, not how well "
    "they play. In the backtest, its top 25 MLS picks for 2025 hit 52% against a "
    "6% base rate. Ages are on July 1. Players with no birth date are hidden by the "
    "age filter."
)
