import matplotlib.pyplot as plt

from charts.credit import add_credit
from config import CHART_COLORS, GPLUS_LABELS, POSITION_LABELS


def plot_gplus(player, title, league_name, color=CHART_COLORS["goal"]):
    columns = list(GPLUS_LABELS)[::-1]
    labels = [GPLUS_LABELS[c] for c in columns]
    values = [player[f"{c}_per90"] for c in columns]
    percentiles = [player[f"{c}_per90_pct"] for c in columns]
    colors = [color if v >= 0 else CHART_COLORS["miss"] for v in values]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.set_facecolor(CHART_COLORS["surface"])
    ax.set_facecolor(CHART_COLORS["surface"])
    positions = range(len(columns))
    ax.barh(positions, values, color=colors, height=0.6)
    ax.set_yticks(positions, labels)
    ax.axvline(0, color=CHART_COLORS["lines"], linewidth=1)

    limit = max(abs(v) for v in values) * 1.6
    ax.set_xlim(-limit, limit)
    for y, (value, pct) in enumerate(zip(values, percentiles)):
        side = "left" if value >= 0 else "right"
        ax.text(
            value,
            y,
            f"  {value:+.3f}  ({pct:.0f})  "
            if value >= 0
            else f"  ({pct:.0f})  {value:+.3f}  ",
            ha=side,
            va="center",
            fontsize=10,
            color=CHART_COLORS["subtext"],
        )
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=11, labelcolor=CHART_COLORS["text"])

    position = POSITION_LABELS[player["general_position"]]
    subtitle = (
        f"g+ above average per 90 - total {player['gplus_per90']:+.3f} - "
        f"(number) = percentile vs. {league_name} {position}"
    )
    fig.suptitle(title, fontsize=16, color=CHART_COLORS["text"])
    ax.set_title(subtitle, fontsize=11, color=CHART_COLORS["subtext"])
    add_credit(fig)
    return fig
