from html.parser import HTMLParser
import os
import sqlite3

class SKillScoreParser(HTMLParser):
    def __init__(self, output):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.totals_row = float('inf')
        self.games_played = 0
        self.weeks_row = float('inf')
        self.output = output
         
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
                    self.output.write(f'{self.games_played}, ')
                    self.games_played = 0                        
                self.totals_row += 1  
                if self.totals_row == 17:                       
                    self.output.write(f"{data}\n")
          
            self.start_of_data = True           

def get_player_webpage_from_db(player, season):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create the path to the database file
    db_path = os.path.join(current_dir, 'web_scrapper', 'player_stats.db')
   
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the player's webpage
    cursor.execute(f"SELECT webpage_{season} FROM player_stats WHERE player_url='{player}'")
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def main(input_file = 'web_scrapper/player_urls/player_urls.out', output_file = 'web_scrapper/skill_scores/skill_scores.out'):
    with open(output_file, 'w') as output:
        parser = SKillScoreParser(output)
        with open(input_file, 'r') as f: 
            for player in f:
                player = player.strip() 
                for season in range(2018, 2023):                   
                    webpage = get_player_webpage_from_db(player, season)
                    if webpage:
                        parser.feed(webpage)
                output.write('\n')              

if __name__ == '__main__':
    main()             
       
          