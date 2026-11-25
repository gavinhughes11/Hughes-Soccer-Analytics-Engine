import pandas as pd

from metrics.prospect_model import (
    PROFILE_FEATURES,
    feature_matrix,
    precision_at_k,
    similar_breakouts,
)


def test_precision_at_k():
    assert precision_at_k([True, False, True, False], [0.9, 0.8, 0.2, 0.1], k=2) == 0.5


def test_feature_matrix_lines_up_columns():
    rows = pd.DataFrame({"age": [22, None], "source": ["mlsnp", "mlsnp"]})
    x = feature_matrix(
        rows,
        ["age"],
        ["source"],
        age_fill=23,
        columns=["age", "source_mlsnp", "source_uslc"],
    )
    assert list(x.columns) == ["age", "source_mlsnp", "source_uslc"]
    assert (x["source_uslc"] == 0).all()
    assert x["age"].iloc[1] == 23


def test_similar_breakouts_keeps_closest_same_position_breakouts():
    profile = {column: [50.0] * 5 for column in PROFILE_FEATURES}
    profile[PROFILE_FEATURES[0]] = [60.0, 90.0, 61.0, None, 60.0]
    table = pd.DataFrame(
        {
            "player_name": ["close", "far", "not a breakout", "no profile", "keeper"],
            "target": "mls",
            "breakout": [True, True, False, True, True],
            "general_position": ["ST", "ST", "ST", "ST", "GK"],
            **profile,
        }
    )
    player = table.iloc[0].copy()
    player[PROFILE_FEATURES[0]] = 62.0

    similar = similar_breakouts(table, "mls", player, n=5)

    assert list(similar["player_name"]) == ["close", "far"]
    assert similar["distance"].iloc[0] == 2.0
