import json
from datetime import datetime, timezone
import requests

POOL = {
    "Brian": ["Yankees", "Braves", "Astros", "Phillies", "Mariners"],
    "Porter": ["Dodgers", "Cubs", "Rangers", "Mets", "Twins"],
    "Perry": ["Orioles", "Red Sox", "Blue Jays", "Padres", "Brewers"],
    "Rice": ["Guardians", "Tigers", "Giants", "Diamondbacks", "Rays"],
    "Pav": ["Cardinals", "Reds", "Royals", "Pirates", "Angels"],
    "Hudson": ["Athletics", "Nationals", "Marlins", "Rockies", "White Sox"]
}

TEAM_ALIASES = {
    "Yankees": "New York Yankees",
    "Braves": "Atlanta Braves",
    "Astros": "Houston Astros",
    "Phillies": "Philadelphia Phillies",
    "Mariners": "Seattle Mariners",
    "Dodgers": "Los Angeles Dodgers",
    "Cubs": "Chicago Cubs",
    "Rangers": "Texas Rangers",
    "Mets": "New York Mets",
    "Twins": "Minnesota Twins",
    "Orioles": "Baltimore Orioles",
    "Red Sox": "Boston Red Sox",
    "Blue Jays": "Toronto Blue Jays",
    "Padres": "San Diego Padres",
    "Brewers": "Milwaukee Brewers",
    "Guardians": "Cleveland Guardians",
    "Tigers": "Detroit Tigers",
    "Giants": "San Francisco Giants",
    "Diamondbacks": "Arizona Diamondbacks",
    "Rays": "Tampa Bay Rays",
    "Cardinals": "St. Louis Cardinals",
    "Reds": "Cincinnati Reds",
    "Royals": "Kansas City Royals",
    "Pirates": "Pittsburgh Pirates",
    "Angels": "Los Angeles Angels",
    "Athletics": "Athletics",
    "Nationals": "Washington Nationals",
    "Marlins": "Miami Marlins",
    "Rockies": "Colorado Rockies",
    "White Sox": "Chicago White Sox"
}

def get_team_wins():
    url = "https://statsapi.mlb.com/api/v1/standings"
    params = {
        "leagueId": "103,104",
        "standingsTypes": "regularSeason"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    wins = {}
    for group in data.get("records", []):
        for record in group.get("teamRecords", []):
            team_name = record["team"]["name"]
            wins[team_name] = record["wins"]

    return wins

def build_standings():
    wins_by_team = get_team_wins()
    standings = []

    for person, teams in POOL.items():
        total_wins = 0
        team_results = []

        for short_name in teams:
            official_name = TEAM_ALIASES[short_name]
            team_wins = wins_by_team.get(official_name, 0)
            total_wins += team_wins
            team_results.append({
                "team": short_name,
                "wins": team_wins
            })

        standings.append({
            "person": person,
            "teams": team_results,
            "total_wins": total_wins
        })

    standings.sort(key=lambda x: x["total_wins"], reverse=True)

    for i, entry in enumerate(standings, start=1):
        entry["rank"] = i

    return standings

def main():
    standings = build_standings()

    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "standings": standings
    }

    with open("standings.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

if __name__ == "__main__":
    main()
