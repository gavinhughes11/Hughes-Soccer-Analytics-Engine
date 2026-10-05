import pandas as pd
from mplsoccer import VerticalPitch

from charts.team_colors import team_color
from config import CHART_COLORS


def plot_shot_map(shots, title, color=CHART_COLORS["goal"]):
    goals = shots[shots["goal"] == 1]
    no_goals = shots[shots["goal"] == 0]

    pitch = VerticalPitch(
        pitch_type="opta",
        half=True,
        pitch_color=CHART_COLORS["surface"],
        line_color=CHART_COLORS["lines"],
    )
    fig, ax = pitch.draw(figsize=(8, 7))

    pitch.scatter(
        no_goals["shot_location_x"],
        no_goals["shot_location_y"],
        s=no_goals["shot_xg"] * 1000 + 50,
        c="none",
        edgecolors=CHART_COLORS["miss"],
        linewidths=1.5,
        label="No goal",
        ax=ax,
    )
    pitch.scatter(
        goals["shot_location_x"],
        goals["shot_location_y"],
        s=goals["shot_xg"] * 1000 + 50,
        c=color,
        edgecolors=CHART_COLORS["surface"],
        linewidths=1,
        label="Goal",
        ax=ax,
    )

    fig.set_facecolor(CHART_COLORS["surface"])

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 0.0),
        ncols=2,
        frameon=False,
        labelcolor=CHART_COLORS["subtext"],
        markerscale=0.5,
        fontsize=11,
    )

    shot_count = len(shots)
    goal_count = shots["goal"].sum()
    total_xg = shots["shot_xg"].sum()
    subtitle = (
        f"{shot_count} shots - {goal_count} goals - {total_xg:.1f} xG - dot size = xG"
    )

    fig.suptitle(title, fontsize=16, color=CHART_COLORS["text"])
    ax.set_title(subtitle, fontsize=11, color=CHART_COLORS["subtext"])

    return fig


if __name__ == "__main__":
    shots = pd.read_parquet("data/shots_mls_2026.parquet")
    messi = shots[shots["shooter_player_name"] == "Lionel Messi"]
    color = team_color(messi["team_id"].iloc[0])
    fig = plot_shot_map(messi, "Lionel Messi - MLS 2026", color=color)
    fig.savefig("images/messi_2026_shot_map.png", dpi=200, bbox_inches="tight")
