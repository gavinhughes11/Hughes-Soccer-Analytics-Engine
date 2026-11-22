import sys
from datetime import date
from pathlib import Path

from config import SEASONS
from data_sources.asa import (
    get_goalkeeper_goals_added,
    get_goalkeeper_xgoals,
    get_player_bios,
    get_player_goals_added,
    get_player_xgoals,
    get_shots,
)

DATA_DIR = Path("data")

STAGES = {"": ["Regular Season", "Playoffs"], "_regular": ["Regular Season"]}


# The weekly refresh only re-downloads each league's latest seasons, because
# older seasons don't change. The previous season is included so late
# corrections still arrive after a new season starts.
RECENT_SEASONS = 2


def main(all_seasons=False):
    DATA_DIR.mkdir(exist_ok=True)

    for league, seasons in SEASONS.items():
        if not all_seasons:
            seasons = seasons[-RECENT_SEASONS:]
        for season in seasons:
            for (
                suffix,
                stages,
            ) in STAGES.items():
                print("League:", league, "Season:", season, "Stages:", stages)
                xgoals = get_player_xgoals(league=league, season=season, stages=stages)
                xgoals_path = (
                    DATA_DIR / f"player_xgoals_{league}_{season}{suffix}.parquet"
                )
                xgoals.to_parquet(xgoals_path, index=False)
                print("xG rows:", len(xgoals))
                shots = get_shots(league=league, season=season, stages=stages)
                shots_path = DATA_DIR / f"shots_{league}_{season}{suffix}.parquet"
                shots.to_parquet(shots_path, index=False)
                print("shots:", len(shots))
                gplus = get_player_goals_added(
                    league=league, season=season, stages=stages
                )
                gplus_path = (
                    DATA_DIR / f"player_goals_added_{league}_{season}{suffix}.parquet"
                )
                gplus.to_parquet(gplus_path, index=False)
                print("g+ rows:", len(gplus))
                gk_xgoals = get_goalkeeper_xgoals(
                    league=league, season=season, stages=stages
                )
                gk_xgoals_path = (
                    DATA_DIR / f"goalkeeper_xgoals_{league}_{season}{suffix}.parquet"
                )
                gk_xgoals.to_parquet(gk_xgoals_path, index=False)
                print("GK xG rows:", len(gk_xgoals))

                gk_gplus = get_goalkeeper_goals_added(
                    league=league, season=season, stages=stages
                )
                gk_gplus_path = (
                    DATA_DIR
                    / f"goalkeeper_goals_added_{league}_{season}{suffix}.parquet"
                )
                gk_gplus.to_parquet(gk_gplus_path, index=False)
                print("GK g+ rows:", len(gk_gplus))

    for league in SEASONS:
        bios = get_player_bios(league=league)
        bios_path = DATA_DIR / f"players_{league}.parquet"
        bios.to_parquet(bios_path, index=False)
        print("Bios: ", len(bios))
    today = date.today()
    updated = f"{today:%b} {today.day}, {today.year}"
    path = DATA_DIR / "last_updated.txt"
    path.write_text(updated)
    print(f"Data updated: {updated}")


if __name__ == "__main__":
    # Run with --all once to download every season; the weekly refresh omits it.
    main(all_seasons="--all" in sys.argv)
