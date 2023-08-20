def create_dst_rankings_dictionary():
    with open('dst_id_and_rankings/dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_rankings = {}
    week, season = 1, 1
    for line in data:
        if line[0] == '':
            week += 1
        elif line[0] == 'end of season':
            season += 1
            week = 1    
        else:
            dst_rankings[(season, week, line[1][1:])] = line[0]           
    return dst_rankings

def create_dst_id_dictionary():
    with open('dst_id_and_rankings/dst_id.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_encodings = {}
    for line in data:
        dst_encodings[line[1][1:]] = line[0]
    return dst_encodings

def create_skill_score(filename = 'skill_scores/skill_scores.out'):
    with open(filename) as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    skill_scores = []
    skill_score, seasons = 0, 0
    for line in data:
        if line[0] == '':
            skill_scores.append(str(round(skill_score / seasons, 2)))
            skill_score, seasons = 0, 0
        else:     
            try:
                skill_score += float(line[1]) / float(line[0])        
            except ZeroDivisionError:
                if float(line[0]) != 0 and float(line[1]) != 0: # Error occurs when dividing 0 points scored / 0 games played.
                    raise ZeroDivisionError
            seasons += 1      
    return skill_scores        

def create_seasons_played(filename = 'rookie_seasons/rookie_seasons_data.out'):
    def create_rookie_season():
        with open(filename) as f:
            data = f.readlines()
            data = [line.strip() for line in data]
            data = [line.split(',') for line in data]
        rookie_seasons = []
        for line in data:
            rookie_seasons.append(line[0][2:])
        return rookie_seasons
    
    rookie_seasons = create_rookie_season()
    seasons_played = []
    for rookie_season in rookie_seasons:
        seasons = []
        for i in range(2, -1, -1):
            current_season = max(23 - int(rookie_season) - i, 0) 
            seasons.append(str(current_season))
        seasons_played.append(seasons)    
    return seasons_played

# NOTE - 7 game average will also include games from the previous season
def create_game_average(fantasy_points, num_games):
    games = fantasy_points[:-2].split(', ')
    games = [float(game) for game in games]
    game_data = ''
    for i in range(len(games)):
        games_played = 0
        game_average = 0.0
        for j in range(i-num_games, i):
            if j >= 0:
                game_average += games[j]
                if games[j] != 0.0:
                    games_played += 1
        if games_played != 0:
            game_data += str(round(game_average / games_played, 2)) + ', '
        else:
            game_data += '0.0' + ', '                                          
    return game_data

def initialize_params(num_params):
    params = []
    for _ in range(num_params):
        params.append('')
    return params

def add_player_data(player_data, params):
    for param in params:
        player_data.append(f'{param[:-2]}\n')
    return player_data

def player_missed_season(params, num_games, player_id):
    new_params = []
    for param in params[:-1]:
        param += '0, ' * num_games
        new_params.append(param)
    params[-1] += f'{player_id}, ' * num_games
    new_params.append(params[-1])   
    return new_params

def create_player_data(dst_rankings, dst_encodings, skill_scores, seasons_played, 
                       num_params, filename = 'weekly_data/weekly_data.out'):
    with open(filename) as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    
    params = initialize_params(num_params)
    player_data = []
    player, week, season = 0, 1, 1
    for line in data:  
        if line[0] == '':             
            week = 1
            season += 1       
        
        if season == 4:
            params[8] = create_game_average(params[0], 3)
            params[9] = create_game_average(params[0], 5)
            params[10] = create_game_average(params[0], 7)
            params[11] = create_game_average(params[0], 9)
            player_data = add_player_data(player_data, params)
            params = initialize_params(num_params)
            player += 1
            season = 1       
        
        if line[0][:34] == 'Player does not have any game data':         
            num_games = 16
            if season >= 2: # NFL changed schedule to 17 games in 2021
                num_games = 17                      
            params = player_missed_season(params, num_games, player + 1)     
        else:               
            try: 
                dst = line[1][1:].replace('@ ', '').replace('vs. ', '') # Remove @ and vs. from dst name
                try:
                    dst_rank = dst_rankings[(season, week, dst)]
                    dst_encode = dst_encodings[dst]        
                    params[2] += f'{week}, '
                    params[1] += f'{season}, '
                    if len(line) == 20: # handles error with data for joe mixon and devin singletary   
                        fantasy_points = line[17][1:]
                    else:
                        fantasy_points = '-'    
                    params[5] += skill_scores[player] + ', '
                    params[6] += seasons_played[player][season - 1] + ', '
                    params[7] += f'{player + 1}, '
                    week += 1   
                    if fantasy_points == '-':              
                        params[0] += '0, '
                        params[3] += '0, '
                        params[4] += '0, '                                           
                    else:
                        params[0] += fantasy_points + ', ' 
                        params[3] += dst_rank + ', '
                        params[4] += dst_encode + ', '                                                   
                except KeyError:
                    pass              
            except IndexError:
                pass
    return player_data

def create_data_txt(player_data, filename = 'data.txt'):
    with open(filename, 'w') as output:
        player_data = [line.split() for line in player_data]     
        for line in player_data:
            for item in line:
                output.write(item + ' ')
            output.write('\n')
    
if __name__ == '__main__':   
    player_data = create_player_data(create_dst_rankings_dictionary(), create_dst_id_dictionary(),
                                     create_skill_score(), create_seasons_played(), 12)
    create_data_txt(player_data)
      