import requests
from bs4 import BeautifulSoup
import re

def format_player_name(name):
    return name.replace(" ", "-").lower()

def get_player_vs_pitcher_stats(batter, pitcher):
    batter_formatted = format_player_name(batter)
    pitcher_formatted = format_player_name(pitcher)
    
    url = f"https://www.statmuse.com/mlb/ask/{batter_formatted}-vs-{pitcher_formatted}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Failed to retrieve data. Status code: {response.status_code}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the summary card
    summary_card = soup.find('div', class_=lambda x: x and 'bg-team-primary' in x)
    if not summary_card:
        return "Could not find summary information on the page."
    
    summary_text = summary_card.get_text(strip=True)
    
    # Find the detailed stats row
    stats_row = soup.find('div', class_=lambda x: x and 'overflow-x-auto' in x)
    if not stats_row:
        return "Could not find detailed stats on the page."
    
    # Extract stats from the row
    stats = {}
    headers = stats_row.find_all('th')
    values = stats_row.find_all('td')
    
    for header, value in zip(headers, values):
        stats[header.text.strip()] = value.text.strip()
    
    # Calculate batting average
    # hits = int(stats.get('H', 0))
    at_bats = int(stats.get('AB', 0))
    batting_average = stats.get('AVG', 0)
    ops = stats.get('OPS', 0)
    xbh = int(stats.get('XBH', 0))
    
    return {
        "batter": batter,
        "pitcher": pitcher,
        "at_bats": at_bats,
        # "summary": summary_text,
        "batting_average": batting_average,
        "ops": ops,
        "xbh": xbh
        # "additional_stats": stats
    }

def get_pitcher_vs_team_stats(pitcher, team):
    pitcher_formatted = format_player_name(pitcher)
    team_formatted = format_player_name(team)

    url = f"https://www.statmuse.com/mlb/ask/{pitcher_formatted}-vs-{team_formatted}"

    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to retrieve data. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Try to find the stats table
    stats_table = soup.find('table', class_='min-w-full')
    if not stats_table:
        return "Could not find stats table on the page."

    # Get all rows from the table
    rows = stats_table.find_all('tr')
    
    if len(rows) < 2:
        return "Could not find enough rows in the stats table."

    # Get headers from the first row
    headers = [th.text.strip() for th in rows[0].find_all('th')]

    # Initialize a dictionary to store accumulated stats
    accumulated_stats = {header: 0 for header in headers if header not in ["NAME", "DATE", "TM", "OPP", "DEC"]}

    # Accumulate stats from all rows except the header row
    for row in rows[1:]:
        cells = row.find_all('td')
        for header, cell in zip(headers, cells):
            if header in accumulated_stats:
                try:
                    value = float(cell.text.strip() or 0)
                    accumulated_stats[header] += value
                except ValueError:
                    # If conversion to float fails, skip this cell
                    pass

    # Calculate averages for rate stats
    games = accumulated_stats.get('G', 1)  # Use 1 as default to avoid division by zero
    for stat in ['ERA', 'WHIP']:
        if stat in accumulated_stats:
            accumulated_stats[stat] = accumulated_stats[stat] / games

    return {
        "pitcher": pitcher,
        "team": team,
        "games": int(accumulated_stats.get('G', 0)),
        "innings_pitched": accumulated_stats.get('IP', 0),
        "era": accumulated_stats.get('ERA', 0),
        "strikeouts": int(accumulated_stats.get('SO', 0)),
        "whip": accumulated_stats.get('WHIP', 0),
        "wins": int(accumulated_stats.get('W', 0)),
        "losses": int(accumulated_stats.get('L', 0)),
        "additional_stats": accumulated_stats
    }

result = get_pitcher_vs_team_stats("Max Fried", "Mets")
print(result)
# Example usage
#result = get_player_vs_pitcher_stats("Francisco Lindor", "Max Fried")
#print(result)