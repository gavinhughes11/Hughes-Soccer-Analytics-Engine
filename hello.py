from itscalledsoccer import AmericanSoccerAnalysis

asa = AmericanSoccerAnalysis()

teams = asa.get_teams(leagues = "mls").to_pandas()

print(len(teams))
print(teams.columns)
print(teams.head(10))
