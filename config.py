LEAGUES = {
    "mls": "Major League Soccer",
    "mlsnp": "MLS NEXT Pro",
    "nwsl": "National Women's Soccer League",
    "uslc": "USL Championship",
    "usl1": "USL League One",
    "usls": "USL Super League",
}

CURRENT_SEASON = "2026"

# MLS NEXT Pro reserve teams and their MLS parent clubs. Teams not listed here
# (Carolina Core, Chattanooga FC, Connecticut United FC) are independent.
MLSNP_PARENTS = {
    "Atlanta United 2": "Atlanta United FC",
    "Austin FC II": "Austin FC",
    "Chicago Fire FC II": "Chicago Fire FC",
    "Colorado Rapids 2": "Colorado Rapids",
    "Columbus Crew 2": "Columbus Crew",
    "Crown Legacy FC": "Charlotte FC",
    "FC Cincinnati 2": "FC Cincinnati",
    "Houston Dynamo FC 2": "Houston Dynamo FC",
    "Huntsville City FC": "Nashville SC",
    "Inter Miami CF II": "Inter Miami CF",
    "Los Angeles FC 2": "Los Angeles FC",
    "Minnesota United FC 2": "Minnesota United FC",
    "New England Revolution II": "New England Revolution",
    "New York City FC II": "New York City FC",
    "New York Red Bulls II": "New York Red Bulls",
    "North Texas SC": "FC Dallas",
    "Orlando City B": "Orlando City SC",
    "Philadelphia Union II": "Philadelphia Union",
    "Portland Timbers 2": "Portland Timbers FC",
    "Real Monarchs": "Real Salt Lake",
    "San Jose Earthquakes II": "San Jose Earthquakes",
    "Sporting Kansas City II": "Sporting Kansas City",
    "St. Louis City SC 2": "St. Louis City SC",
    "Tacoma Defiance": "Seattle Sounders FC",
    "Toronto FC II": "Toronto FC",
    "Vancouver Whitecaps FC 2": "Vancouver Whitecaps FC",
    "Ventura County FC": "LA Galaxy",
}

MIN_MINUTES = 450


def seasons_from(first_year, skip=()):
    # Every season from first_year to CURRENT_SEASON, as strings.
    years = range(first_year, int(CURRENT_SEASON) + 1)
    return [str(year) for year in years if year not in skip]


# Each league starts at its first season in American Soccer Analysis's data.
# NWSL 2020 is skipped: it had no regular season, only the Challenge Cup
# and the Fall Series.
SEASONS = {
    "mls": seasons_from(2013),
    "mlsnp": seasons_from(2022),
    "nwsl": seasons_from(2016, skip=[2020]),
    "uslc": seasons_from(2017),
    "usl1": seasons_from(2019),
    "usls": ["2024-25", "2025-26", "2026"],
}

CHART_COLORS = {
    "goal": "#2a78d6",
    "miss": "#898781",
    "surface": "#fcfcfb",
    "lines": "#c3c2b7",
    "text": "#0b0b0b",
    "subtext": "#52514e",
}

PER90_STATS = [
    "shots",
    "shots_on_target",
    "goals",
    "xgoals",
    "key_passes",
    "primary_assists",
    "xassists",
]

GPLUS_STATS = [
    "gplus",
    "gplus_dribbling",
    "gplus_fouling",
    "gplus_interrupting",
    "gplus_passing",
    "gplus_receiving",
    "gplus_shooting",
]

GK_GPLUS_STATS = [
    "gk_gplus",
    "gk_gplus_claiming",
    "gk_gplus_fielding",
    "gk_gplus_handling",
    "gk_gplus_passing",
    "gk_gplus_shotstopping",
    "gk_gplus_sweeping",
]

GK_PER90_STATS = ["goals_prevented"] + GK_GPLUS_STATS

GPLUS_LABELS = {
    "gplus_dribbling": "Dribbling",
    "gplus_fouling": "Fouling",
    "gplus_interrupting": "Interrupting",
    "gplus_passing": "Passing",
    "gplus_receiving": "Receiving",
    "gplus_shooting": "Shooting",
}

GK_GPLUS_LABELS = {
    "gk_gplus_claiming": "Claiming",
    "gk_gplus_fielding": "Fielding",
    "gk_gplus_handling": "Handling",
    "gk_gplus_passing": "Passing",
    "gk_gplus_shotstopping": "Shot-stopping",
    "gk_gplus_sweeping": "Sweeping",
}

FINISHING_K = 300

MIN_SHOTS = 20

FINISHING_WEIGHT = 0.7

VOLUME_WEIGHT = 0.3

SEASON_WEIGHTS = [0.7, 0.2, 0.1]

STAT_LABELS = {
    "shots": "Shots",
    "shots_on_target": "On target",
    "goals": "Goals",
    "xgoals": "xG",
    "key_passes": "Key passes",
    "primary_assists": "Assists",
    "xassists": "xA",
}

POSITION_LABELS = {
    "GK": "goalkeepers",
    "CB": "center backs",
    "FB": "fullbacks",
    "DM": "defensive midfielders",
    "CM": "central midfielders",
    "AM": "attacking midfielders",
    "W": "wingers",
    "ST": "strikers",
}

CHART_CREDIT = "Data: American Soccer Analysis"
