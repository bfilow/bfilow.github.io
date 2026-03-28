import json
from datetime import datetime, timezone
import requests

POOL = {
    "Brian": ["Cubs", "Red Sox", "Rangers", "Reds", "Marlins"],
    "Porter": ["Braves", "Mets", "Royals", "Giants", "Rockies"],
    "Perry": ["Mariners", "Tigers", "Orioles", "Athletics", "White Sox"],
    "Rice": ["Yankees", "Brewers", "Astros", "Rays", "Nationals"],
    "Tim": ["Phillies", "Blue Jays", "D-backs", "Pirates", "Cardinals"],
    "Hudson": ["Dodgers", "Padres", "Guardians", "Twins", "Angels"]
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

def get_team_records():
    url = "https://statsapi.mlb.com/api/v1/standings"
    params = {
        "leagueId": "103,104",
        "season": 2026,
        "standingsTypes": "regularSeason"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    records = {}

    for group in data.get("records", []):
        for record in group.get("teamRecords", []):
            team = record.get("team", {})
            wins = record.get("wins", 0)
            losses = record.get("losses", 0)

            possible_names = []

            if team.get("name"):
                possible_names.append(team["name"])

            if team.get("teamName"):
                possible_names.append(team["teamName"])

            if team.get("clubName"):
                possible_names.append(team["clubName"])

            if team.get("locationName") and team.get("teamName"):
                possible_names.append(f'{team["locationName"]} {team["teamName"]}')

            for name in possible_names:
                records[name] = {
                    "wins": wins,
                    "losses": losses
                }

    return records

def build_standings():
    records_by_team = get_team_records()
    standings = []

    for person, teams in POOL.items():
        total_wins = 0
        total_losses = 0
        team_results = []

        for short_name in teams:
            team_data = records_by_team.get(short_name)

            if team_data is None:
                full_name = TEAM_ALIASES.get(short_name)
                if full_name is not None:
                    team_data = records_by_team.get(full_name)

            if team_data is None:
                team_data = {"wins": 0, "losses": 0}

            wins = team_data["wins"]
            losses = team_data["losses"]

            total_wins += wins
            total_losses += losses

            team_results.append({
                "team": short_name,
                "wins": wins,
                "losses": losses
            })

        total_games = total_wins + total_losses
        win_pct = total_wins / total_games if total_games > 0 else 0

        standings.append({
            "person": person,
            "teams": team_results,
            "total_wins": total_wins,
            "total_losses": total_losses,
            "win_pct": f"{win_pct:.3f}".lstrip("0")
        })

    standings.sort(key=lambda x: x["win_pct"], reverse=True)

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
