import os
import sys
import json
from collections import defaultdict
from analysis.loader import load_tournament

def compute_usage_stats(tournament):
    # Structure pour accumuler stats
    stats = {}

    for player in tournament.players:
        for pkmn in player.team.pokemons:
            if pkmn.name not in stats:
                stats[pkmn.name] = {
                    "usage": 0,
                    "tera_type": defaultdict(int),
                    "ability": defaultdict(int),
                    "item": defaultdict(int),
                    "move": defaultdict(int)
                }

            pkmn_stats = stats[pkmn.name]
            pkmn_stats["usage"] += 1
            pkmn_stats["tera_type"][pkmn.tera_type] += 1
            pkmn_stats["ability"][pkmn.ability] += 1
            pkmn_stats["item"][pkmn.item] += 1
            for move in pkmn.moves:
                pkmn_stats["move"][move] += 1

    # Convert defaultdicts to dict for JSON serialization
    for pkmn_name, pkmn_stats in stats.items():
        pkmn_stats["tera_type"] = dict(pkmn_stats["tera_type"])
        pkmn_stats["ability"] = dict(pkmn_stats["ability"])
        pkmn_stats["item"] = dict(pkmn_stats["item"])
        pkmn_stats["move"] = dict(pkmn_stats["move"])

    return stats

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.compute_usage <tournament_code>")
        sys.exit(1)
    
    tournament_code = sys.argv[1]
    
    base_path = "data"
    info_path = os.path.join(base_path, f"{tournament_code}_info.json")
    pairings_path = os.path.join(base_path, f"{tournament_code}_pairings.json")
    players_path = os.path.join(base_path, f"{tournament_code}_players.json")
    
    tournament = load_tournament(info_path, pairings_path, players_path)
    
    stats = compute_usage_stats(tournament)

    usage_dir = os.path.join(base_path, "usage")
    os.makedirs(usage_dir, exist_ok=True)

    output_file = os.path.join(usage_dir, f"{tournament_code}_usage_stats.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"✅ Usage stats saved to {output_file}")

if __name__ == "__main__":
    main()
