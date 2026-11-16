def add_goalkeeper_metrics(stats):
    stats = stats.copy()
    stats["goals_prevented"] = stats["xgoals_gk_faced"] - stats["goals_conceded"]
    stats["save_pct"] = (
        stats["saves"] / (stats["saves"] + stats["goals_conceded"])
    ) * 100
    return stats
