import pandas as pd
import pytest

from charts.team_colors import TEAM_COLORS_FILE, contrast
from config import CHART_COLORS


def test_contrast_extremes():
    assert contrast("#000000", "#ffffff") == pytest.approx(21)
    assert contrast("#fcfcfb", "#fcfcfb") == pytest.approx(1)


def test_team_colors_are_readable():
    table = pd.read_csv(TEAM_COLORS_FILE).dropna(subset=["color"])
    for name, color in zip(table["team_name"], table["color"]):
        ratio = contrast(color, CHART_COLORS["surface"])
        assert ratio >= 3, f"{name}: {color} is too light ({ratio:.1f}:1)"
