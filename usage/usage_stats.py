from itertools import combinations
from collections import Counter
from parser.models import Tournament

def get_usage_rate(tournament: Tournament, combo_size: int = 2):
    counter = Counter()
    total_teams = len(tournament.players)

    for player in tournament.players:
        names = [p.name for p in player.team.pokemons]
        unique_names = sorted(set(names))
        for combo in combinations(unique_names, combo_size):
            counter[combo] += 1

    return counter, total_teams
