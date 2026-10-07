import pandas as pd
import streamlit as st
from config import PER90_STATS, SEASONS
from metrics.per90 import add_per90, filter_min_minutes
from metrics.percentiles import add_percentiles
from metrics.finishing_rating import finishing_rating, season_scores


@st.cache_data
def load_player_stats(league, season):
    stats = pd.read_parquet(f"data/player_xgoals_{league}_{season}.parquet")
    stats = filter_min_minutes(stats)
    stats = add_per90(stats)
    stats = add_percentiles(stats, [f"{stat}_per90" for stat in PER90_STATS])
    return stats


@st.cache_data
def load_shots(league, season):
    return pd.read_parquet(f"data/shots_{league}_{season}.parquet")


@st.cache_data
def load_finishing_ratings(league):
    seasons = SEASONS[league]
    current = season_scores(
        pd.read_parquet(f"data/player_xgoals_{league}_{seasons[-1]}.parquet")
    )
    previous = season_scores(
        pd.read_parquet(f"data/player_xgoals_{league}_{seasons[-2]}.parquet")
    )
    two_back = season_scores(
        pd.read_parquet(f"data/player_xgoals_{league}_{seasons[-3]}.parquet")
    )

    return finishing_rating(current, previous, two_back)


@st.cache_data
def load_raw_stats(league, season):
    return pd.read_parquet(f"data/player_xgoals_{league}_{season}.parquet")
