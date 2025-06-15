# download_tournament.py

from parser.parser import create_tournament
from parser.save import save_players, save_pairings, save_info

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Download and save tournament data from rk9.gg")
    parser.add_argument("code", help="Tournament code (e.g. WCS02wi0zpmUDdrwWkd1)")
    args = parser.parse_args()

    tournament_code = args.code
    print(f"📥 Starting download for tournament: {tournament_code}...")

    tournament = create_tournament(tournament_code)

    save_players(tournament)
    save_pairings(tournament.pairings, tournament.url)
    save_info(tournament)

if __name__ == "__main__":
    main()
