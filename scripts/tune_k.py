import pandas as pd
from config import SEASONS
from metrics.finishing_rating import combine_player_rows, shrink


if __name__ == "__main__":
    candidates = [0, 10, 20, 40, 60, 100, 150, 200, 250, 275, 300, 350, 500, 1000]

    results = []

    pairs = 0

    for league, seasons in SEASONS.items():
        for i in range(len(seasons) - 1):
            this_path = f"data/player_xgoals_{league}_{seasons[i]}.parquet"
            next_path = f"data/player_xgoals_{league}_{seasons[i + 1]}.parquet"
            this = combine_player_rows(pd.read_parquet(this_path))
            nxt = combine_player_rows(pd.read_parquet(next_path))
            avg_this = (this["goals"].sum() - this["xgoals"].sum()) / this[
                "shots"
            ].sum()
            avg_next = (nxt["goals"].sum() - nxt["xgoals"].sum()) / nxt["shots"].sum()
            this = this[this["shots"] >= 1]
            nxt = nxt[nxt["shots"] >= 10]
            both = this.merge(nxt, on="player_id", suffixes=("_this", "_next"))
            pairs += len(both)
            actual = (both["goals_next"] - both["xgoals_next"]) / (
                both["shots_next"]
            ) - avg_next
            average_error = (both["shots_next"] * actual**2).sum()
            results.append(
                {
                    "k": "average",
                    "error": average_error,
                    "weight": both["shots_next"].sum(),
                }
            )
            for k in candidates:
                predicted = (
                    shrink(
                        both["goals_this"],
                        both["xgoals_this"],
                        both["shots_this"],
                        avg_this,
                        k,
                    )
                    - avg_this
                )
                error = (both["shots_next"] * ((predicted - actual) ** 2)).sum()
                results.append(
                    {"k": k, "error": error, "weight": both["shots_next"].sum()}
                )
    table = pd.DataFrame(results).groupby("k", sort=False).sum()
    error_rate = table["error"] / table["weight"]
    vs_average = 100 * (error_rate["average"] - error_rate) / error_rate["average"]
    print("Player-season pairs:", pairs)
    print(vs_average.round(3))
