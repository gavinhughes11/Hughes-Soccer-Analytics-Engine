import pandas as pd

from config import (
    GPLUS_STATS,
    MIN_MINUTES,
    MLSNP_PARENTS,
    PER90_STATS,
    PROSPECT_LADDERS,
    SEASONS,
)
from metrics.per90 import add_per90
from metrics.percentiles import add_percentiles

COUNT_COLUMNS = PER90_STATS + GPLUS_STATS


def season_totals(league, season):
    xgoals = pd.read_parquet(f"data/player_xgoals_{league}_{season}_regular.parquet")
    gplus = pd.read_parquet(
        f"data/player_goals_added_{league}_{season}_regular.parquet"
    )
    stats = xgoals.merge(gplus, on=["player_id", "team_id"], how="left")
    stats = stats.sort_values(by="minutes_played")

    rules = {col: (col, "sum") for col in ["minutes_played"] + COUNT_COLUMNS}
    rules["player_name"] = ("player_name", "last")
    rules["team_name"] = ("team_name", "last")
    rules["general_position"] = ("general_position", "last")

    totals = stats.groupby("player_id").agg(**rules)
    totals = add_per90(totals, COUNT_COLUMNS)

    per90_columns = [f"{stat}_per90" for stat in COUNT_COLUMNS]
    pool = totals[totals["minutes_played"] >= MIN_MINUTES]
    pool = add_percentiles(pool, per90_columns)
    pct_columns = [f"{column}_pct" for column in per90_columns]
    totals = totals.join(pool[pct_columns])
    return totals


def candidates(target, season):
    target_totals = season_totals(target, season)

    lower = []
    for source in PROSPECT_LADDERS[target]:
        if season in SEASONS[source]:
            s = season_totals(source, season)
            s = s[s["minutes_played"] >= MIN_MINUTES]
            s["source"] = source
            lower.append(s)
    if not lower:
        lower = target_totals.iloc[0:0].assign(source="")
    else:
        lower = pd.concat(lower)
        lower = lower.sort_values(by="minutes_played")
        lower = lower.groupby(level=0).last()

    established = target_totals[target_totals["minutes_played"] >= MIN_MINUTES]
    lower = lower[~lower.index.isin(established.index)]
    bench = target_totals[
        (target_totals["minutes_played"] > 0)
        & (target_totals["minutes_played"] < MIN_MINUTES)
        & ~target_totals.index.isin(lower.index)
    ]
    bench = bench.assign(source=f"{target} bench")
    rows = pd.concat([lower, bench])
    rows["target_minutes"] = (
        target_totals["minutes_played"].reindex(rows.index).fillna(0)
    )

    return rows


def add_label(rows, target, next_season):
    if next_season is None:
        rows["breakout"] = None
    else:
        rows["next_minutes"] = season_totals(target, next_season)["minutes_played"]
        rows["breakout"] = (
            rows["next_minutes"].reindex(rows.index).fillna(0) >= MIN_MINUTES
        )
    return rows


def add_features(rows, bios, season):
    rows = rows.join(bios)
    rows["age"] = (
        pd.Timestamp(f"{season}-07-01") - pd.to_datetime(rows["birth_date"])
    ).dt.days / 365.25
    rows["affiliated"] = rows["team_name"].isin(MLSNP_PARENTS)
    rows["has_stats"] = rows["gplus_per90_pct"].notna()
    pct_columns = [c for c in rows.columns if c.endswith("_pct")]
    rows[pct_columns] = rows[pct_columns].fillna(50)
    return rows
