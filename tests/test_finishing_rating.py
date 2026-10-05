import pandas as pd
import pytest
from metrics.finishing_rating import (
    shrink,
    finishing_rating,
)


def test_shrink():
    assert shrink(3, 1, 10, 0, k=10)


def test_shrink_with_no_shots_gives_league_average():
    assert shrink(0, 0, 0, 0.05, 10) == pytest.approx(0.05)


def test_finishing_rating_blends_seasons():
    current = pd.DataFrame({"player_id": ["a", "b"], "season_score": [80, 60]})
    previous = pd.DataFrame({"player_id": ["a"], "season_score": [50]})
    two_back = pd.DataFrame({"player_id": ["z"], "season_score": [99]})
    result = finishing_rating(current, previous, two_back)
    assert result["finishing_rating"].tolist() == pytest.approx([74, 60])
