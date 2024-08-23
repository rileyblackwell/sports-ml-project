import sqlite3
from html.parser import HTMLParser
import os

class RookieSeasonsParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.first_td = True
        self.data = []
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:                   
            if self.first_td:
                self.data.append(f'{data}\n')
                self.first_td = False

def get_player_stats_html_from_db(player):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the player's stats html
    cursor.execute("""
        SELECT stats_html 
        FROM player_stats_html 
        WHERE player_url = ?
    """, (player,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def write_player_rookie_seasons_to_db(player, data):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the player's rookie seasons into the database
    cursor.execute("""
        INSERT OR REPLACE INTO player_rookie_season (player_url, data)
        VALUES (?, ?)
    """, (player, ''.join(data)))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()

def get_player_urls_from_db():
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get all player URLs
    cursor.execute("SELECT player_url FROM player_urls")
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return [result[0] for result in results]

def main():
    player_urls = get_player_urls_from_db()
    for player in player_urls:
        parser = RookieSeasonsParser()
        stats_html = get_player_stats_html_from_db(player)
        if stats_html:
            parser.feed(stats_html)
        write_player_rookie_seasons_to_db(player, parser.data)

if __name__ == '__main__':
    main()