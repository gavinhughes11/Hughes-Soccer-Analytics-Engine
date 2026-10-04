from config import PER90_STATS, MIN_MINUTES
import pandas as pd


def add_per90(stats, columns=PER90_STATS):
    stats = stats.copy()
    for column in columns:
        stats[f"{column}_per90"] = stats[column] * 90 / stats["minutes_played"]
    return stats


def filter_min_minutes(stats, min_minutes=MIN_MINUTES):
    return stats[stats["minutes_played"] >= min_minutes]


if __name__ == "__main__":
    stats = pd.read_parquet("data/player_xgoals_mls_2026.parquet")
    stats = filter_min_minutes(stats)
    stats = add_per90(stats)
    print(len(stats))
    top = stats.sort_values("xgoals_per90", ascending=False).head(10)
    print(top[["player_name", "team_name", "minutes_played", "xgoals_per90"]])
