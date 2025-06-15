import json
from parser.models import Tournament, Player, Team, Pokemon, Pairing, PairingStatus
from typing import List

def load_players(filepath: str) -> List[Player]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    players = []
    for p in data:
        pokemons = [
            Pokemon(
                name=pkmn["name"],
                tera_type=pkmn["tera_type"],
                ability=pkmn["ability"],
                item=pkmn["item"],
                moves=pkmn["moves"]
            )
            for pkmn in p["team"]["pokemons"]
        ]
        team = Team(pokemons=pokemons)
        player = Player(name=p["name"], team=team)
        players.append(player)
    return players

def load_pairings(filepath: str) -> List[List[Pairing]]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    pairings = []
    for round_pairings in data:
        round_list = []
        for pair in round_pairings:
            pair_obj = Pairing(
                player1=pair["player1"],
                player2=pair["player2"],
                status=PairingStatus(pair["status"]),
                is_bye=pair["is_bye"]
            )
            round_list.append(pair_obj)
        pairings.append(round_list)
    return pairings

def load_info(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # dict avec name, url, start_date, end_date

def load_tournament(info_path: str, pairings_path: str, players_path: str) -> Tournament:
    info = load_info(info_path)
    pairings = load_pairings(pairings_path)
    players = load_players(players_path)
    
    tournament = Tournament(
        name=info["name"],
        url=info["url"],
        start_date=info["start_date"],
        end_date=info["end_date"],
        pairings=pairings,
        players=players
    )
    return tournament
