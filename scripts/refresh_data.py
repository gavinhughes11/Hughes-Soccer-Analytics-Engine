from pathlib import Path
from config import SEASONS
from data_sources.asa import get_player_xgoals, get_shots

DATA_DIR = Path("data")


def main():
    DATA_DIR.mkdir(exist_ok=True)

    for league, seasons in SEASONS.items():
        for season in seasons:
            print("League:", league, "Season:", season)
            xgoals = get_player_xgoals(league=league, season=season)
            xgoals_path = DATA_DIR / f"player_xgoals_{league}_{season}.parquet"
            xgoals.to_parquet(xgoals_path, index=False)
            print("xG rows:", len(xgoals))
            shots = get_shots(league=league, season=season)
            shots_path = DATA_DIR / f"shots_{league}_{season}.parquet"
            shots.to_parquet(shots_path, index=False)
            print("shots:", len(shots))


if __name__ == "__main__":
    main()
