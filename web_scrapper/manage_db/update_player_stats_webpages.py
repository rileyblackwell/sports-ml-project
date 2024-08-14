import sqlite3
import requests

def fetch_and_store_player_stats_html():
    conn = sqlite3.connect("../player_stats.db")
    cursor = conn.cursor()

    cursor.execute("SELECT player_url FROM player_urls")
    player_urls = cursor.fetchall()

    for url in player_urls:
        player_url = url[0]
        webpage_url = f"https://www.fantasypros.com/nfl/stats/{player_url}.php"

        try:
            response = requests.get(webpage_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            webpage = response.text
    
            cursor.execute("INSERT OR REPLACE INTO player_stats_html (player_url, stats_html) VALUES (?, ?)", (player_url, webpage))
            conn.commit()
            print(f"Player stats HTML webpage fetched and stored for {player_url}")
    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player stats HTML webpage for {player_url}: {e}")
    
    conn.close()

if __name__ == '__main__':
    fetch_and_store_player_stats_html()