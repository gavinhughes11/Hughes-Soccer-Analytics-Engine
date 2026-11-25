import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from metrics.prospects import COUNT_COLUMNS

# Features every model gets: how old the player is and how much they played.
BASE_FEATURES = ["age", "minutes_played", "target_minutes"]

# Within-league percentiles from metrics/prospects.py (blank ones were filled with 50).
PCT_FEATURES = [f"{stat}_per90_pct" for stat in COUNT_COLUMNS]

STAT_FEATURES = BASE_FEATURES + PCT_FEATURES + ["affiliated", "has_stats"]

# Model name -> (number columns, category columns that become 0/1 columns).
MODELS = {
    "opportunity": (BASE_FEATURES, ["source"]),
    "full": (STAT_FEATURES, ["source", "general_position"]),
}

TEST_SEASONS = [2024, 2025]


def feature_matrix(rows, numeric, categories, age_fill, columns=None):
    x = rows[numeric].astype(float)
    x["age"] = x["age"].fillna(age_fill)
    dummies = pd.get_dummies(rows[categories], dtype=float)
    x = x.join(dummies)
    if columns is not None:
        x = x.reindex(columns=columns, fill_value=0)
    return x


def fit_model(train, numeric, categories):
    age_fill = train["age"].median()
    x = feature_matrix(train, numeric, categories, age_fill)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    model.fit(x, train["breakout"])
    return model, list(x.columns), age_fill


def predict(fitted, rows, numeric, categories):
    model, columns, age_fill = fitted
    x = feature_matrix(rows, numeric, categories, age_fill, columns)
    return model.predict_proba(x)[:, 1]


def precision_at_k(breakout, probability, k=25):
    table = pd.DataFrame({"breakout": list(breakout), "probability": list(probability)})
    table = table.nlargest(k, "probability")
    breakout = table["breakout"]
    return float(breakout.mean())


def backtest(table, target, test_seasons=TEST_SEASONS):
    data = table[(table["target"] == target) & (table["breakout"].notna())].copy()
    data["breakout"] = data["breakout"].astype(bool)
    data["season"] = data["season"].astype(int)
    records = []
    for season in test_seasons:
        train = data[data["season"] < season]
        test = data[data["season"] == season]
        for name, (numeric, categories) in MODELS.items():
            fitted = fit_model(train, numeric, categories)
            probability = predict(fitted, test, numeric, categories)
            records.append(
                {
                    "season": season,
                    "model": name,
                    "base_rate": test["breakout"].mean(),
                    "p_at_25": precision_at_k(test["breakout"], probability),
                    "auc": roc_auc_score(test["breakout"], probability),
                }
            )
    return pd.DataFrame(records)


def predict_next_season(table, target, model="full"):
    data = table[table["target"] == target].copy()
    data["season"] = data["season"].astype(int)
    train = data[data["breakout"].notna()].copy()
    train["breakout"] = train["breakout"].astype(bool)
    latest = data[data["season"] == data["season"].max()].copy()
    numeric, categories = MODELS[model]
    fitted = fit_model(train, numeric, categories)
    latest["probability"] = predict(fitted, latest, numeric, categories)
    return latest.sort_values("probability", ascending=False)


def similar_breakouts(table, target, player, n=3):
    # Past breakouts at the same position with the closest per-90 percentile profile.
    past = table[
        (table["target"] == target)
        & table["breakout"].eq(True)
        & table["has_stats"]
        & (table["general_position"] == player["general_position"])
    ].copy()
    # One row of a mixed table comes out as text-like "object", so make it numbers.
    gaps = past[PCT_FEATURES] - player[PCT_FEATURES].astype(float)
    past["distance"] = (gaps**2).sum(axis=1) ** 0.5
    return past.nsmallest(n, "distance")
