from pathlib import Path
from config import SEASONS
from data_sources.asa import get_player_xgoals

DATA_DIR = Path("data")


def main():
    DATA_DIR.mkdir(exist_ok=True)

    for league, seasons in SEASONS.items():
        for season in seasons:
            print("League:", league, "Season:", season)
            stats = get_player_xgoals(league=league, season=season)
            path = DATA_DIR / f"player_xgoals_{league}_{season}.parquet"
            stats.to_parquet(path, index=False)
            print(len(stats))


if __name__ == "__main__":
    main()
