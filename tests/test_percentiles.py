import pandas as pd
import pytest
from metrics.percentiles import add_percentiles


def test_add_percentiles_by_position():
    stats = pd.DataFrame(
        {
            "player_name": ["A", "B", "C", "D"],
            "general_position": ["ST", "ST", "CB", "CB"],
            "shots_per90": [4, 2, 1, 0],
        }
    )
    result = add_percentiles(stats, ["shots_per90"])
    assert result["shots_per90_pct"].tolist() == pytest.approx([100, 50, 100, 50])
