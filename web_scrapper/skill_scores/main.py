from html.parser import HTMLParser
import os
import sqlite3

class SKillScoreParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.totals_row = float('inf')
        self.games_played = 0
        self.weeks_row = float('inf')
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
                if data[:4] == 'Week':
                    self.weeks_row = 0
                self.weeks_row += 1                         
                if self.weeks_row == 17:
                    if data != '-':
                        self.games_played += 1
                              
                if data == 'Totals':
                    self.totals_row = 0
                    self.data.append(f'{self.games_played}, ')
                    self.games_played = 0                        
                self.totals_row += 1  
                if self.totals_row == 17:                       
                    self.data.append(f"{data}\n")
          
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

def write_player_skill_scores_to_db(player, data):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, '..', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the player's skill scores into the database
    cursor.execute("""
        INSERT OR REPLACE INTO player_skill_scores (player_url, data)
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
        parser = SKillScoreParser()
        for season in range(2018, 2023):                   
            webpage = get_player_webpage_from_db(player, season)
            if webpage:
                parser.feed(webpage)
        write_player_skill_scores_to_db(player, parser.data)

if __name__ == '__main__':
    main()