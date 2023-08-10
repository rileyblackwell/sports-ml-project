import requests
from html.parser import HTMLParser

def create_dst_rankings_dictionary():
    with open('dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_rankings = {}
    week = 0
    season = 0
    for line in data:
        if line[0] == '':
            week += 1
        elif line[0] == 'end of season':
            season += 1
            week = 0    
        else:
            dst_rankings[(season, week, line[1][1:])] = line[0]           
    return dst_rankings

def create_dst_encodings_dictionary():
    with open('dst_encodings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_encodings = {}
    for line in data:
        dst_encodings[line[1][1:]] = line[0]
    return dst_encodings

def create_skill_score():
    with open('skill_scores.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    skill_scores = []
    skill_score = 0
    seasons = 0
    for line in data:
        if line[0] == '':
            skill_scores.append(str(round(skill_score / seasons, 2)))
            skill_score = 0
            seasons = 0
        else:     
            try:
                skill_score += float(line[1]) / float(line[0])        
            except ZeroDivisionError:
                if float(line[0]) != 0 and float(line[1]) != 0: # Error occurs when dividing 0 points scored / 0 games played.
                    raise ZeroDivisionError
            seasons += 1      
    return skill_scores        

def create_player_data(dst_rankings, dst_encodings, skill_scores):
    with open('weekly_data.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    player_dst_rankings, player_dst_encodings, player_fantasy_points, player_skill_score  = '', '', '', ''
    player_weeks_encodings, player_season_encodings = '', ''
    player_data = []
    player = 0
    week = 0
    year = 0
    for line in data:  
        if line[0] == '':             
            week = 0
            year += 1
        if year == 3:
            player_data.append(f'{player_dst_rankings[:-2]}\n')
            player_data.append(f'{player_dst_encodings[:-2]}\n')
            player_data.append(f'{player_fantasy_points[:-2]}\n')
            player_data.append(f'{player_skill_score[:-2]}\n')
            player_data.append(f'{player_weeks_encodings[:-2]}\n')
            player_data.append(f'{player_season_encodings[:-2]}\n')
            player_dst_rankings, player_dst_encodings, player_fantasy_points, player_skill_score  = '', '', '', ''
            player_weeks_encodings, player_season_encodings = '', ''
            player += 1
            year = 0
        
        if line[0][:34] == 'Player does not have any game data':         
            num_games = 16
            if year >= 1: # NFL changed schedule to 17 games in 2021
                num_games = 17                      
            player_dst_rankings +=  '0, ' * num_games 
            player_dst_encodings += '0, ' * num_games
            player_fantasy_points += '0, ' * num_games
            player_weeks_encodings += '0, ' * num_games
            player_season_encodings += '0, ' * num_games
            skill_score = skill_scores[player]
            player_skill_score += f'{skill_score}, ' * num_games        
        else:               
            try: 
                dst = line[1][1:]
                dst = dst.replace('@ ', '')
                dst = dst.replace('vs. ', '')
                try:
                    dst_rank = dst_rankings[(year, week, dst)]
                    dst_encode = dst_encodings[dst]
                    week += 1
                    player_weeks_encodings += f'{week}, '
                    player_season_encodings += f'{year}, '   
                    fantasy_points = line[17][1:]
                    skill_score = skill_scores[player]   
                    if fantasy_points != '-':              
                        player_dst_rankings += dst_rank + ', '
                        player_dst_encodings += dst_encode + ', '
                        player_fantasy_points += fantasy_points + ', '
                        player_skill_score += skill_score + ', '
                    else:
                        player_dst_rankings += '0, '
                        player_dst_encodings += '0, '
                        player_fantasy_points += '0, '
                        player_skill_score += skill_score + ', '                              
                except KeyError:
                    pass              
            except IndexError:
                pass
    return player_data

def create_data_txt(player_data):
    output = open('data.txt', 'w')
    player_data = [line.split() for line in player_data]     
    for line in player_data:
        for item in line:
            output.write(item + ' ')
        output.write('\n')
    output.close() 
  
def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

class WeeklyDataParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
         
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
                    weekly_data_output.write('\n')
                if data == 'Week 1':
                    weekly_data_output.write('\n')
                if data[:34] == 'Player does not have any game data': 
                    weekly_data_output.write('\n\n')
                           
            weekly_data_output.write(f"{data}, ")
            self.start_of_data = True           

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

class SKillScoreParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.totals_row = float('inf')
        self.games_played = 0
        self.weeks_row = float('inf')
         
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
                    skill_scores_output.write(f'{self.games_played}, ')
                    self.games_played = 0                        
                self.totals_row += 1  
                if self.totals_row == 17:                       
                    skill_scores_output.write(f"{data}\n")
          
            self.start_of_data = True

if __name__ == '__main__':  
    valid_output = open('valid_urls.out', 'w')                       
    error_output = open('error_urls.out', 'w')

    i = 0
    with open('player_urls.out', 'r') as f: 
        for player in f:
            player = player.strip() 
            
            weekly_data_output = open('weekly_data.out', 'w')
            weekly_data_parser = WeeklyDataParser()
            for season in range(2020, 2022):                   
                weekly_data_parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php?season={season}'))
            weekly_data_parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php'))
            weekly_data_output.write('\n\n') # prevents a bug in create_data.py where player data isn't outputted. 
            weekly_data_output.close()
            
            skill_scores_output = open('skill_scores.out', 'w')
            skill_scores_parser = SKillScoreParser()
            season = 2018
            while season <= 2021:
                skill_scores_parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php?season={season}'))
                season += 1
            skill_scores_parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php'))
            skill_scores_output.write('\n')                
          
            skill_scores_output.close()
            player_data = create_player_data(create_dst_rankings_dictionary(), create_dst_encodings_dictionary(),
                                     create_skill_score())
            create_data_txt(player_data)
            
           
            with open('data.txt', 'r') as f:
                data = f.read()
                data = data.split('\n')
             
                if len(data) == 7:
                    valid_lines = 0
                    for line in data:
                        line = line.split()
                        if len(line) == 50:
                            valid_lines += 1
                    if valid_lines == 6:
                        valid_output.write(player + '\n')
                    else:
                        error_output.write(player + '\n')

            
            if i == 4:
                break
            i += 1
                
    valid_output.close()
    error_output.close() 
    