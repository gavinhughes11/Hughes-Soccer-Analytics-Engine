from config import CHART_COLORS, CHART_CREDIT


def add_credit(fig):
    fig.text(
        x=0.98,
        y=0.01,
        s=CHART_CREDIT,
        ha="right",
        va="bottom",
        fontsize=8,
        color=CHART_COLORS["subtext"],
    )
