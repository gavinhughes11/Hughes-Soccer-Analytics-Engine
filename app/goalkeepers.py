import matplotlib.pyplot as plt
import streamlit as st

from app.data import load_goalkeeper_stats
from charts.export import to_png
from charts.leaderboard import plot_leaderboard
from config import GK_GPLUS_LABELS

league = st.session_state["league"]
season = st.session_state["season"]
playoffs = st.session_state["playoffs"]
stats = load_goalkeeper_stats(league, season, playoffs)

labels = {
    "goals_prevented": "Goals prevented",
    "goals_prevented_per90": "Goals prevented per 90",
    "save_pct": "Save %",
    "gk_gplus_per90": "Keeper g+ per 90",
}
for column, name in GK_GPLUS_LABELS.items():
    labels[f"{column}_per90"] = f"Keeper g+ {name} per 90"

st.title("Goalkeepers")
stat = st.selectbox("Stat", list(labels), format_func=labels.get)
n = st.slider("Number of keepers", 5, min(25, len(stats)), min(10, len(stats)))

table = stats.dropna(subset=[stat])

fig = plot_leaderboard(
    table,
    stat,
    f"Top {n} - {labels[stat]} - {league.upper()} {season}",
    "Min. 450 minutes - goalkeepers - bar color = team",
    n=n,
)
png = to_png(fig)
plt.close(fig)
st.image(png, width="stretch")
st.download_button(
    label="Download PNG",
    data=png,
    file_name=f"{league}-{season}-top-{n}-{stat}-goalkeepers.png",
    mime="image/png",
    on_click="ignore",
)

st.caption(
    "**Goals prevented** = xG faced minus goals conceded. Positive means the keeper "
    "let in fewer goals than the shots they faced deserved. "
    "**Save %** = saves ÷ (saves + goals conceded). "
    "**Keeper g+** is American Soccer Analysis's goals added model for keepers."
)

st.dataframe(
    table.sort_values(stat, ascending=False).head(n)[
        ["player_name", "team_name", "minutes_played", stat]
    ],
    hide_index=True,
)
