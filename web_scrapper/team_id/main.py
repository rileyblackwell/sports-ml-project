import sqlite3
from html.parser import HTMLParser

class PlayerTeamIdParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.teams = []
        self.counter = 0
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:
            if self.counter % 10 == 0 or self.counter % 10 == 1:
                self.teams.append(f"{data}, ") 
            self.counter += 1 

def get_player_stats_html_from_db(player):
    conn = sqlite3.connect("../player_stats.db")
    cursor = conn.cursor()

    cursor.execute("SELECT stats_html FROM player_stats_html WHERE player_url = ?", (player,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def main(input_filename = '../player_urls/player_urls.out', output_filename = '../team_id/team_id.out'):
    with open(output_filename, 'w') as output:
        parser = PlayerTeamIdParser()
        with open(input_filename, 'r') as player_urls_input:
            for player in player_urls_input:
                player = player.strip()
                stats_html = get_player_stats_html_from_db(player)
                if stats_html:
                    parser.feed(stats_html)
                else:
                    print(f"No stats found for player {player}")
                    continue
                
                teams = parser.teams[:len(parser.teams) // 2]
                if len(teams) % 2 == 1:
                    teams = parser.teams[:(len(parser.teams) + 2) // 2]
              
                # outputs the team id for the last 3 seasons   
                if len(teams) >= 8:
                    for team in teams[-10:-4]: # teams played for 2020, 2021, 2022
                        output.write(team)
                elif len(teams) == 6:
                    for team in teams[-8:-4]:
                        output.write(team)
                elif len(teams) == 4:
                    for team in teams[-6:-4]:
                        output.write(team)
                
                output.write('\n')
                parser.counter = 0 # resets the counter for the next player
                parser.teams.clear() # clears the list for the next player
    
if __name__ == '__main__':
    main()
