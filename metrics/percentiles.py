import pandas as pd
from config import PER90_STATS
from metrics.per90 import add_per90, filter_min_minutes


def add_percentiles(stats, columns, group_column="general_position"):
    stats = stats.copy()
    for column in columns:
        stats[f"{column}_pct"] = (
            stats.groupby(group_column)[column].rank(pct=True) * 100
        )
    return stats


if __name__ == "__main__":
    stats = pd.read_parquet("data/player_xgoals_mls_2026.parquet")
    stats = filter_min_minutes(stats)
    stats = add_per90(stats)
    per90_columns = [f"{column}_per90" for column in PER90_STATS]
    stats = add_percentiles(stats, per90_columns)

    show = [
        "player_name",
        "general_position",
        "xgoals_per90_pct",
        "xassists_per90_pct",
        "key_passes_per90_pct",
        "shots_per90_pct",
    ]
    for name in ["Lionel Messi", "Hugo Cuypers"]:
        player = stats[stats["player_name"] == name]
        print(player[show])
