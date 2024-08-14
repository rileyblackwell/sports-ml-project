import sqlite3
from html.parser import HTMLParser
import os

class WeeklyDataParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.data = []
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:              
            if self.start_of_data:
                if data[:4] == 'Week' or data == 'Totals':                    
                    self.data.append('\n')
                if data == 'Week 1':
                    self.data.append('\n')
                if data[:34] == 'Player does not have any game data': 
                    self.data.append('\n\n')                        
            
            self.data.append(f"{data}, ")
            self.start_of_data = True           

def get_player_webpage_from_db(player, season):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the player's webpage
    cursor.execute("""
        SELECT webpage_html 
        FROM webpage_html 
        WHERE player_url = ? AND webpage_year = ?
    """, (player, season))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def write_player_weekly_data_to_db(player, data):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the player's weekly data into the database
    cursor.execute("""
        INSERT OR REPLACE INTO player_weekly_data (player_url, data)
        VALUES (?, ?)
    """, (player, ''.join(data)))
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()

def main(input_file = '../player_urls/player_urls.out'):
    with open(input_file, 'r') as f: 
        for player in f:
            player = player.strip() 
            parser = WeeklyDataParser()
            for season in range(2020, 2023):                   
                webpage = get_player_webpage_from_db(player, season)
                if webpage:
                    parser.feed(webpage)
            write_player_weekly_data_to_db(player, parser.data)

if __name__ == '__main__':
    main()