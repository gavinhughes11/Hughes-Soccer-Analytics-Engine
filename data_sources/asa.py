from itscalledsoccer import AmericanSoccerAnalysis

asa = AmericanSoccerAnalysis()


def get_teams(league):
    return asa.get_teams(leagues=league)


def get_players(league):
    return asa.get_players(leagues=league)


def get_player_xgoals(league, season):
    stats = asa.get_player_xgoals(
        leagues=league, season_name=season, split_by_teams=True
    )
    players = get_players(league)
    players = players[["player_id", "player_name"]]
    teams = get_teams(league)
    teams = teams[["team_id", "team_name"]]
    stats = stats.merge(players, how="left", on="player_id")
    stats = stats.merge(teams, how="left", on="team_id")
    return stats


if __name__ == "__main__":
    mls_xg = get_player_xgoals("mls", "2026")
    print(mls_xg)
