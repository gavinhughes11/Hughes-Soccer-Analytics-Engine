from pathlib import Path

import pandas as pd

from config import PROSPECT_LADDERS, SEASONS
from metrics.prospects import add_features, add_label, candidates

DATA_DIR = Path("data")
OUTPUT = DATA_DIR / "prospect_table.parquet"


def load_bios():
    # One row per player across every league's bios file.
    bios = pd.concat(
        [pd.read_parquet(path) for path in DATA_DIR.glob("players_*.parquet")]
    )
    return bios.drop_duplicates("player_id").set_index("player_id")


def main():
    bios = load_bios()
    tables = []

    for target in PROSPECT_LADDERS:
        seasons = SEASONS[target]
        for i, season in enumerate(seasons):
            # The latest season has no next season yet, so it stays unlabelled.
            next_season = seasons[i + 1] if i + 1 < len(seasons) else None
            rows = candidates(target, season)
            rows = add_label(rows, target, next_season)
            rows = add_features(rows, bios, season)
            rows["target"] = target
            rows["season"] = season
            tables.append(rows)

    table = pd.concat(tables).rename_axis("player_id").reset_index()
    table.to_parquet(OUTPUT, index=False)

    labelled = table[table["breakout"].notna()]
    summary = labelled.groupby(["target", "source"])["breakout"].agg(
        ["size", "sum", "mean"]
    )
    print(summary.round(3))
    print(
        "Labelled rows:", len(labelled), "Breakouts:", int(labelled["breakout"].sum())
    )
    print("Unlabelled rows:", table["breakout"].isna().sum())
    print(f"Saved {len(table)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
