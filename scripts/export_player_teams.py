import json
import os
import sys
from pathlib import Path

DATA_DIR = Path("data/")
OUTPUT_DIR = DATA_DIR / "stats"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path: Path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def normalize_filename(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")

def extract_tournament_id(filename: Path) -> str:
    return filename.name.split("_")[0]

def export_player_teams(player_name: str):
    player_teams = []

    for file in DATA_DIR.glob("*_players.json"):
        tournament_id = extract_tournament_id(file)
        players = load_json(file)

        for player in players:
            if player.get("name") == player_name:
                team = player.get("team") or player.get("pokemons") or []
                if team:
                    for file in DATA_DIR.glob("*info.json"):
                        if extract_tournament_id(file) == tournament_id:
                            tournament_info = load_json(file)
                            player_teams.append({
                                "tournament": tournament_info.get("name", "Unknown Tournament"),
                                "team": team
                            })
                   
    if not player_teams:
        print(f"❌ No teams found for player '{player_name}'.")
        return

    output_path = OUTPUT_DIR / f"{normalize_filename(player_name)}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(player_teams, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported teams for '{player_name}' to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.export_player_teams 'Player Name'")
    else:
        export_player_teams(sys.argv[1])
