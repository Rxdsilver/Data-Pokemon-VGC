from collections import Counter
from parser.models import Tournament

def compute_pokemon_usage(tournament: Tournament) -> Counter:
    usage = Counter()
    for player in tournament.players:
        for pokemon in player.team.pokemons:
            usage[pokemon.name] += 1
    return usage
