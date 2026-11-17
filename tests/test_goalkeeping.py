import pandas as pd
import pytest

from metrics.goalkeeping import add_goalkeeper_metrics


def test_add_goalkeeper_metrics():
    stats = pd.DataFrame(
        {
            "player_name": ["A", "B"],
            "xgoals_gk_faced": [12.5, 8.0],
            "goals_conceded": [10, 11],
            "saves": [30, 33],
        }
    )
    result = add_goalkeeper_metrics(stats)
    assert result["goals_prevented"].tolist() == pytest.approx([2.5, -3.0])
    assert result["save_pct"].tolist() == pytest.approx([75.0, 75.0])


def test_add_goalkeeper_metrics_on_season_totals():
    # The Player page sums a keeper's rows for every team into one Series.
    rows = pd.DataFrame(
        {
            "xgoals_gk_faced": [6.0, 4.0],
            "goals_conceded": [5, 2],
            "saves": [15, 6],
        }
    )
    totals = add_goalkeeper_metrics(rows.sum())
    assert totals["goals_prevented"] == pytest.approx(3.0)
    assert totals["save_pct"] == pytest.approx(75.0)


def test_add_goalkeeper_metrics_does_not_change_input():
    stats = pd.DataFrame(
        {"xgoals_gk_faced": [1.0], "goals_conceded": [1], "saves": [3]}
    )
    add_goalkeeper_metrics(stats)
    assert "goals_prevented" not in stats.columns
