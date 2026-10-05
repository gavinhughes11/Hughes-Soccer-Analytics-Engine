import pandas as pd
from config import FINISHING_K, MIN_SHOTS, FINISHING_WEIGHT, VOLUME_WEIGHT
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


if __name__ == "__main__":
    stats = pd.read_parquet("data/player_xgoals_mls_2026.parquet")
    stats = season_scores(stats)
    scores = stats.sort_values("season_score", ascending=False).head(10)[
        ["player_name", "shots", "goals", "xgoals", "season_score"]
    ]
    print(len(scores))
    print(scores)
