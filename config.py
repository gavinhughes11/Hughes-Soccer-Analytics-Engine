DATA_UPDATED = "Oct 2, 2026"

LEAGUES = {
    "mls": "Major League Soccer",
    "nwsl": "National Women's Soccer League",
    "uslc": "USL Championship",
    "usl1": "USL League One",
    "usls": "USL Super League",
}

CURRENT_SEASON = "2026"

MIN_MINUTES = 450

SEASONS = {
    "mls": ["2024", "2025", "2026"],
    "nwsl": ["2024", "2025", "2026"],
    "uslc": ["2024", "2025", "2026"],
    "usl1": ["2024", "2025", "2026"],
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
