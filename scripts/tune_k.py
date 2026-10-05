import pandas as pd
from config import SEASONS
from metrics.finishing_rating import combine_player_rows, shrink


if __name__ == "__main__":
    candidates1 = [0, 10, 20, 40, 60, 100, 150, 200, 300, 500, 1000]
    candidates2 = [250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350]

    results = []

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
            actual = (both["goals_next"] - both["xgoals_next"]) / (
                both["shots_next"]
            ) - avg_next
            for k in candidates2:
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
        table = pd.DataFrame(results).groupby("k").sum()
        print(table["error"] / table["weight"])
