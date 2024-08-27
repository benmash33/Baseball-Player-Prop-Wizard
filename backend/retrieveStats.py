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
    xbh = stats.get('XBH', 0)
    
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

# Example usage
result = get_player_vs_pitcher_stats("Pete Alonso", "Max Fried")
print(result)