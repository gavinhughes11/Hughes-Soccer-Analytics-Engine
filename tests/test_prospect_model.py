import pandas as pd

from metrics.prospect_model import feature_matrix, precision_at_k


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
