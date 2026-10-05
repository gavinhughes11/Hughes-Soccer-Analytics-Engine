from pathlib import Path

import pandas as pd

from config import LEAGUES
from data_sources.asa import get_teams

OUTPUT = Path("data/team_colors.csv")

# Official club colors from TruColor (trucolor.net). When a club's main color is
# too light to read on the chart background, a darker club color is used instead.
# Clubs that appear in more than one league share one entry (e.g. Lexington SC).
CLUB_COLORS = {
    # MLS
    "Atlanta United FC": "#9D2235",
    "Austin FC": "#010101",
    "CF Montréal": "#003DA5",
    "Charlotte FC": "#0085CA",
    "Chicago Fire FC": "#D50032",
    "Colorado Rapids": "#862633",
    "Columbus Crew": "#010101",
    "D.C. United": "#E4002B",
    "FC Cincinnati": "#FE5000",
    "FC Dallas": "#BF0D3E",
    "Houston Dynamo FC": "#101820",
    "Inter Miami CF": "#010101",
    "LA Galaxy": "#004B87",
    "Los Angeles FC": "#101820",
    "Minnesota United FC": "#010101",
    "Nashville SC": "#201547",
    "New England Revolution": "#0C2340",
    "New York City FC": "#000229",
    "New York Red Bulls": "#C8102E",
    "Orlando City SC": "#5F249F",
    "Philadelphia Union": "#051C2C",
    "Portland Timbers FC": "#2C5234",
    "Real Salt Lake": "#9D2235",
    "San Diego FC": "#051C2C",
    "San Jose Earthquakes": "#003DA5",
    "Seattle Sounders FC": "#0032A0",
    "Sporting Kansas City": "#0C2340",
    "St. Louis City SC": "#E0004D",
    "Toronto FC": "#A6192E",
    "Vancouver Whitecaps FC": "#13294B",
    # NWSL
    "Angel City FC": "#212322",
    "Bay FC": "#051C2C",
    "Boston Legacy FC": "#D00070",
    "Chicago Stars FC": "#0C2340",
    "Denver Summit FC": "#1D6960",
    "Houston Dash": "#101820",
    "Kansas City Current": "#CB333B",
    "NJ/NY Gotham FC": "#010101",
    "North Carolina Courage": "#01426A",
    "Orlando Pride": "#5F249F",
    "Portland Thorns FC": "#93282C",
    "Racing Louisville FC": "#1E1A34",
    "San Diego Wave FC": "#041E42",
    "Seattle Reign FC": "#2E407A",
    "Utah Royals FC": "#13294B",
    "Washington Spirit": "#003A40",
    # USL Championship
    "Birmingham Legion FC": "#101820",
    "Brooklyn FC": "#25282A",
    "Charleston Battery": "#010101",
    "Colorado Springs Switchbacks FC": "#010101",
    "Detroit City FC": "#643335",
    "El Paso Locomotive FC": "#041E42",
    "Hartford Athletic": "#002D72",
    "Indy Eleven": "#0C2340",
    "Las Vegas Lights FC": "#009ACE",
    "Lexington SC": "#154734",
    "Loudoun United FC": "#E4002B",
    "Louisville City FC": "#330072",
    "Monterey Bay FC": "#003865",
    "New Mexico United": "#19191A",
    "Oakland Roots SC": "#EF3340",
    "Orange County SC": "#010101",
    "Phoenix Rising FC": "#D22730",
    "Pittsburgh Riverhounds SC": "#010101",
    "Rhode Island FC": "#0C2340",
    "Sacramento Republic FC": "#7C2629",
    "San Antonio FC": "#C5203E",
    "Tampa Bay Rowdies": "#4C8D2B",
    "The Miami FC": "#10069F",
    # USL League One
    "AV Alta FC": "#13322B",
    "Athletic Club Boise": "#228848",
    "Charlotte Independence": "#003DA5",
    "Chattanooga Red Wolves SC": "#7C2629",
    "Corpus Christi FC": "#071D49",
    "FC Naples": "#1B365D",
    "Fort Wayne FC": "#010101",
    "Forward Madison FC": "#1B365D",
    "Greenville Triumph SC": "#002855",
    "New York Cosmos": "#071D49",
    "One Knoxville SC": "#071D49",
    "Portland Hearts of Pine": "#1D1F2A",
    "Richmond Kickers": "#C8102E",
    "Sarasota Paradise": "#1D1F2A",
    "Spokane Velocity FC": "#0093B2",
    "Union Omaha": "#010101",
    "Westchester SC": "#0047BB",
}


def main():
    if OUTPUT.exists():
        print(f"{OUTPUT} already exists, so it was not overwritten.")
        return

    tables = []
    for league in LEAGUES:
        teams = get_teams(league)[["team_id", "team_name"]].copy()
        teams["league"] = league
        tables.append(teams)

    all_teams = pd.concat(tables, ignore_index=True)
    all_teams["color"] = all_teams["team_name"].map(CLUB_COLORS)
    all_teams = all_teams.sort_values(["league", "team_name"])
    all_teams.to_csv(OUTPUT, index=False)

    print(f"Saved {len(all_teams)} teams to {OUTPUT}")
    print(f"{all_teams['color'].notna().sum()} teams have a color")


if __name__ == "__main__":
    main()
