from pathlib import Path

import pandas as pd
from matplotlib.colors import to_rgb

from config import CHART_COLORS

TEAM_COLORS_FILE = Path("data/team_colors.csv")


def load_team_colors():
    if not TEAM_COLORS_FILE.exists():
        return {}
    table = pd.read_csv(TEAM_COLORS_FILE).dropna(subset=["color"])
    return dict(zip(table["team_id"], table["color"]))


TEAM_COLORS = load_team_colors()


def team_color(team_id):
    return TEAM_COLORS.get(team_id, CHART_COLORS["goal"])


def luminance(hex_color):
    channels = []
    for c in to_rgb(hex_color):
        if c <= 0.04045:
            channels.append(c / 12.92)
        else:
            channels.append(((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(color_a, color_b):
    lighter = max(luminance(color_a), luminance(color_b))
    darker = min(luminance(color_a), luminance(color_b))
    return (lighter + 0.05) / (darker + 0.05)
