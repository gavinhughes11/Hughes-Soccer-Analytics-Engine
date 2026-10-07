import pandas as pd
import streamlit as st
from config import PER90_STATS
from metrics.per90 import add_per90, filter_min_minutes
from metrics.percentiles import add_percentiles


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
