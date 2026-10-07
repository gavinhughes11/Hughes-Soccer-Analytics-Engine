import pandas as pd
import matplotlib.pyplot as plt
from charts.team_colors import team_color
from config import CHART_COLORS
from metrics.per90 import add_per90, filter_min_minutes


def plot_leaderboard(table, stat, title, subtitle, n=10):
    top = table.sort_values(stat).tail(n)
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.set_facecolor(CHART_COLORS["surface"])
    ax.set_facecolor(CHART_COLORS["surface"])
    colors = [team_color(team_id) for team_id in top["team_id"]]
    ax.barh(top["player_name"], top[stat], color=colors, height=0.6)
    for y, (value, team) in enumerate(zip(top[stat], top["team_name"])):
        ax.text(
            value,
            y,
            f"  {value:.2f}  -  {team}",
            va="center",
            fontsize=10,
            color=CHART_COLORS["subtext"],
        )
    ax.set_xlim(0, top[stat].max() * 1.7)
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=11, labelcolor=CHART_COLORS["text"])
    fig.suptitle(title, fontsize=16, color=CHART_COLORS["text"])
    ax.set_title(subtitle, fontsize=11, color=CHART_COLORS["subtext"])
    return fig


if __name__ == "__main__":
    stats = pd.read_parquet("data/player_xgoals_mls_2026.parquet")
    stats = add_per90(filter_min_minutes(stats))
    fig = plot_leaderboard(
        stats,
        "xgoals_per90",
        "Top 10 - xG per 90 - MLS 2026",
        "Min. 450 minutes - bar color = team",
    )
    fig.savefig(
        "images/mls_2026_xg_per90_leaderboard.png", dpi=200, bbox_inches="tight"
    )
