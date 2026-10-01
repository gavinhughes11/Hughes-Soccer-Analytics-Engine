from itscalledsoccer import AmericanSoccerAnalysis

asa = AmericanSoccerAnalysis()

teams = asa.get_teams(leagues = "mls")

print(len(teams))
print(teams.columns)
print(teams.head(10))
