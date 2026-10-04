import pandas as pd
import pytest
from metrics.per90 import add_per90, filter_min_minutes


def test_add_per90():
    stats = pd.DataFrame(
        {
            "player_name": ["A", "B"],
            "minutes_played": [900, 450],
            "goals": [5, 5],
        }
    )
    result = add_per90(stats, ["goals"])
    assert result["goals_per90"].tolist() == pytest.approx([0.5, 1.0])


def test_filter_min_minutes():
    stats = pd.DataFrame(
        {
            "player_name": ["A", "B", "C"],
            "minutes_played": [100, 450, 2000],
        }
    )
    result = filter_min_minutes(stats, 450)
    assert result["player_name"].tolist() == ["B", "C"]
