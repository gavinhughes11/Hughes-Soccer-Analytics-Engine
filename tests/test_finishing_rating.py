import pandas as pd
import pytest
from metrics.finishing_rating import combine_player_rows, shrink, season_scores


def test_shrink():
    assert shrink(3, 1, 10, 0, 0)


def test_shrink_with_no_shots_gives_league_average():
    assert shrink(0, 0, 0, 0.05, 10)
