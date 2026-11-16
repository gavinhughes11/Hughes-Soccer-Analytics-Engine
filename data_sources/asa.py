import pandas as pd
import requests
from itscalledsoccer import AmericanSoccerAnalysis

ASA_BASE_URL = "https://app.americansocceranalysis.com/api/v1"

asa = AmericanSoccerAnalysis()


def get_shots(league, season, stages):
    games = get_games(league, season, stages)
    game_ids = games["game_id"].tolist()
    all_shots = []

    for start in range(0, len(game_ids), 100):
        batch = game_ids[start : start + 100]
        url = f"{ASA_BASE_URL}/{league}/games/shots"
        response = requests.get(url, params={"game_id": ",".join(batch)}, timeout=60)
        response.raise_for_status()
        all_shots.extend(response.json())

    return pd.DataFrame(all_shots)


def get_teams(league):
    return asa.get_teams(leagues=league)


def get_games(league, season, stages):
    return asa.get_games(leagues=league, season_name=season, stages=stages)


def get_players(league):
    return asa.get_players(leagues=league)


def get_player_xgoals(league, season, stages):
    stats = asa.get_player_xgoals(
        leagues=league, season_name=season, stage_name=stages, split_by_teams=True
    )
    players = get_players(league)
    players = players[["player_id", "player_name"]]
    teams = get_teams(league)
    teams = teams[["team_id", "team_name"]]
    stats = stats.merge(players, how="left", on="player_id")
    stats = stats.merge(teams, how="left", on="team_id")
    return stats


def get_player_goals_added(league, season, stages):
    stats = asa.get_player_goals_added(
        leagues=league, season_name=season, stage_name=stages, split_by_teams=True
    )
    return flatten_goals_added(stats, "gplus_")


def flatten_goals_added(stats, prefix):
    rows = []
    for _, row in stats.iterrows():
        record = {"player_id": row["player_id"], "team_id": row["team_id"]}
        for action in row["data"]:
            column = f"{prefix}{action['action_type'].lower()}"
            record[column] = action["goals_added_above_avg"]
        rows.append(record)
    flat = pd.DataFrame(rows)
    action_columns = [c for c in flat.columns if c.startswith(prefix)]
    flat[prefix.rstrip("_")] = flat[action_columns].sum(axis=1)
    return flat


def get_goalkeeper_xgoals(league, season, stages):
    stats = asa.get_goalkeeper_xgoals(
        leagues=league, season_name=season, stage_name=stages, split_by_teams=True
    )
    players = get_players(league)
    players = players[["player_id", "player_name"]]
    teams = get_teams(league)
    teams = teams[["team_id", "team_name"]]
    stats = stats.merge(players, how="left", on="player_id")
    stats = stats.merge(teams, how="left", on="team_id")
    return stats


def get_goalkeeper_goals_added(league, season, stages):
    stats = asa.get_goalkeeper_goals_added(
        leagues=league, season_name=season, stage_name=stages, split_by_teams=True
    )
    return flatten_goals_added(stats, "gk_gplus_")


if __name__ == "__main__":
    shots = get_shots("mls", "2026", ["Regular Season"])
    print(shots)
