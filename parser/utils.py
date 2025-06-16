from datetime import datetime
import re
from typing import Tuple


BASE_URL = "https://rk9.gg"

def build_roster_url(tournament_code: str) -> str:
    return f"{BASE_URL}/roster/{tournament_code}"

def build_pairings_url(tournament_code: str, pod: int = 2, round_number: int = None) -> str:
    url = f"{BASE_URL}/pairings/{tournament_code}?pod={pod}"
    if round_number is not None:
        url += f"&rnd={round_number}"
    return url

def build_tournament_url(tournament_code: str) -> str:
    return f"{BASE_URL}/tournament/{tournament_code}"

def build_player_url(player_name: str) -> str:
    player_name = player_name.replace(" ", "-").lower()
    return f"{BASE_URL}/player/{player_name}"

def build_team_url(base_url: str, team_relative_url: str) -> str:
    """
    Build the full URL to a team page by combining the base tournament URL
    and the relative team URL.

    Parameters:
    - base_url: str, the base URL of the tournament, e.g. "https://rk9.gg"
    - team_relative_url: str, the relative URL of the team, e.g. "/teamlist/public/..."

    Returns:
    - Full absolute URL as a string.
    """

    # If the relative URL is already a full URL, just return it
    if team_relative_url.startswith("http"):
        return team_relative_url

    # Ensure base_url does not end with a slash
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    # Ensure relative URL starts with a slash
    if not team_relative_url.startswith("/"):
        team_relative_url = "/" + team_relative_url

    # print(f"Fetching team URL: {base_url + team_relative_url}")
    return base_url + team_relative_url

def parse_tournament_dates(date_str: str) -> Tuple[str, str]:
    """
    Parse a tournament date string like 'August 16-18, 2024' or 'May 31–June 1, 2025'
    and return a tuple of (start_date, end_date) in 'YYYY-MM-DD' format.
    """
    try:
        date_str = date_str.strip().replace("–", "-")  

        if "-" not in date_str:
            parts = date_str.split(", ")
            start_day = end_day = parts[0].split()[1]
            year = parts[1]
            month = parts[0].split()[0]

            start_str = f"{month} {start_day}, {year}"
            end_str = start_str
        else:
            match = re.match(r"(?P<month1>\w+)\s(?P<day1>\d+)-(?:(?P<month2>\w+)\s)?(?P<day2>\d+),\s(?P<year>\d{4})", date_str)
            if not match:
                raise ValueError(f"Unrecognized date format: {date_str}")

            parts = match.groupdict()
            month1 = parts["month1"]
            day1 = parts["day1"]
            month2 = parts["month2"] if parts["month2"] else month1
            day2 = parts["day2"]
            year = parts["year"]

            start_str = f"{month1} {day1}, {year}"
            end_str = f"{month2} {day2}, {year}"

        fmt_in = "%B %d, %Y"
        fmt_out = "%Y-%m-%d"
        start_date = datetime.strptime(start_str, fmt_in).strftime(fmt_out)
        end_date = datetime.strptime(end_str, fmt_in).strftime(fmt_out)

        return start_date, end_date

    except Exception as e:
        print(f"[ERROR] Failed to parse tournament dates: {date_str}")
        raise e

