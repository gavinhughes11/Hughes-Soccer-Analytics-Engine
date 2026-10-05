import pandas as pd
from mplsoccer import PyPizza

from charts.team_colors import team_color
from config import (
    CHART_COLORS,
    MIN_MINUTES,
    PER90_STATS,
    POSITION_LABELS,
    STAT_LABELS,
)
from metrics.per90 import add_per90, filter_min_minutes
from metrics.percentiles import add_percentiles


def plot_pizza(player, title, league_name, color=CHART_COLORS["goal"]):
    labels = [STAT_LABELS[stat] for stat in PER90_STATS]
    values = [round(player[f"{stat}_per90_pct"]) for stat in PER90_STATS]
    position = POSITION_LABELS[player["general_position"]]

    baker = PyPizza(
        params=labels,
        background_color=CHART_COLORS["surface"],
        straight_line_color=CHART_COLORS["lines"],
        straight_line_lw=1,
        last_circle_color=CHART_COLORS["lines"],
        last_circle_lw=1,
        other_circle_color=CHART_COLORS["lines"],
        other_circle_lw=1,
        other_circle_ls="-",
    )

    fig, ax = baker.make_pizza(
        values,
        figsize=(7, 7.5),
        param_location=113,
        kwargs_slices=dict(
            facecolor=color,
            edgecolor=CHART_COLORS["surface"],
            linewidth=2,
            zorder=2,
        ),
        kwargs_params=dict(color=CHART_COLORS["text"], fontsize=11, va="center"),
        kwargs_values=dict(
            color=CHART_COLORS["text"],
            fontsize=11,
            zorder=3,
            bbox=dict(
                edgecolor=color,
                facecolor=CHART_COLORS["surface"],
                boxstyle="round,pad=0.2",
                lw=1,
            ),
        ),
    )

    subtitle = (
        f"Percentile vs. {league_name} {position} - per 90 - min. {MIN_MINUTES} minutes"
    )
    fig.text(0.5, 0.97, title, ha="center", fontsize=16, color=CHART_COLORS["text"])
    fig.text(
        0.5, 0.935, subtitle, ha="center", fontsize=11, color=CHART_COLORS["subtext"]
    )
    return fig


if __name__ == "__main__":
    stats = pd.read_parquet("data/player_xgoals_mls_2026.parquet")
    stats = add_per90(filter_min_minutes(stats))
    stats = add_percentiles(stats, [f"{stat}_per90" for stat in PER90_STATS])
    player = stats[stats["player_name"] == "Hugo Cuypers"].iloc[0]
    color = team_color(player["team_id"])
    fig = plot_pizza(player, "Hugo Cuypers · MLS 2026", "MLS", color=color)
    fig.savefig("images/cuypers_2026_pizza.png", dpi=200, bbox_inches="tight")
