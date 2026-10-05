import pandas as pd
from config import (
    FINISHING_K,
    MIN_SHOTS,
    FINISHING_WEIGHT,
    VOLUME_WEIGHT,
    SEASON_WEIGHTS,
)
from metrics.per90 import add_per90, filter_min_minutes


def combine_player_rows(stats):
    columns = ["minutes_played", "shots", "goals", "xgoals"]
    return stats.groupby(["player_id", "player_name"], as_index=False)[columns].sum()


def shrink(goals, xgoals, shots, league_avg, k):
    return (goals - xgoals + k * league_avg) / (shots + k)


def season_scores(stats, k=FINISHING_K):
    stats = combine_player_rows(stats)
    league_avg = (stats["goals"].sum() - stats["xgoals"].sum()) / stats["shots"].sum()
    stats = filter_min_minutes(stats)
    stats = stats[stats["shots"] >= MIN_SHOTS]
    stats["finishing"] = shrink(
        stats["goals"], stats["xgoals"], stats["shots"], league_avg, k
    )
    stats = add_per90(stats, ["shots"])
    stats["finishing_pct"] = stats["finishing"].rank(pct=True) * 100
    stats["volume_pct"] = stats["shots_per90"].rank(pct=True) * 100
    stats["season_score"] = (
        FINISHING_WEIGHT * stats["finishing_pct"] + VOLUME_WEIGHT * stats["volume_pct"]
    )
    return stats


def finishing_rating(current, previous, two_back):
    previous = previous[["player_id", "season_score"]].rename(
        columns={"season_score": "prev_score"}
    )
    two_back = two_back[["player_id", "season_score"]].rename(
        columns={"season_score": "prev2_score"}
    )
    rating = current.merge(previous, on=["player_id"], how="left")
    rating = rating.merge(two_back, on=["player_id"], how="left")
    rating["prev_score"] = rating["prev_score"].fillna(rating["season_score"])
    rating["prev2_score"] = rating["prev2_score"].fillna(rating["season_score"])
    rating["finishing_rating"] = (
        SEASON_WEIGHTS[0] * rating["season_score"]
        + SEASON_WEIGHTS[1] * rating["prev_score"]
        + SEASON_WEIGHTS[2] * rating["prev2_score"]
    )
    return rating


if __name__ == "__main__":
    current = season_scores(pd.read_parquet("data/player_xgoals_mls_2026.parquet"))
    previous = season_scores(pd.read_parquet("data/player_xgoals_mls_2025.parquet"))
    two_back = season_scores(pd.read_parquet("data/player_xgoals_mls_2024.parquet"))

    rating = finishing_rating(current, previous, two_back)
    print(len(rating))
    top = rating.sort_values("finishing_rating", ascending=False).head(10)
    print(
        top[
            [
                "player_name",
                "shots",
                "goals",
                "xgoals",
                "season_score",
                "finishing_rating",
            ]
        ].round(1)
    )
