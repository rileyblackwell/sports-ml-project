def create_dst_rankings_dictionary():
    with open('dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_rankings = {}
    week = 0
    season = 1
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

def create_seasons_played():
    def create_rookie_season():
        with open('rookie_seasons_data.out') as f:
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

def create_player_data(dst_rankings, dst_encodings, skill_scores, seasons_played):
    with open('weekly_data.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    player_dst_rankings, player_dst_encodings, player_fantasy_points, player_skill_score  = '', '', '', ''
    player_weeks_encodings, player_season_encodings, player_seasons_played = '', '', ''
    player_data = []
    player = 0
    week = 0
    season = 1
    for line in data:  
        if line[0] == '':             
            week = 0
            season += 1
        if season == 4:
            player_data.append(f'{player_dst_rankings[:-2]}\n')
            player_data.append(f'{player_dst_encodings[:-2]}\n')
            player_data.append(f'{player_fantasy_points[:-2]}\n')
            player_data.append(f'{player_skill_score[:-2]}\n')
            player_data.append(f'{player_weeks_encodings[:-2]}\n')
            player_data.append(f'{player_season_encodings[:-2]}\n')
            player_data.append(f'{player_seasons_played[:-2]}\n')
            player_dst_rankings, player_dst_encodings, player_fantasy_points, player_skill_score  = '', '', '', ''
            player_weeks_encodings, player_season_encodings, player_seasons_played = '', '', ''
            player += 1
            season = 1
        
        if line[0][:34] == 'Player does not have any game data':         
            num_games = 16
            if season >= 2: # NFL changed schedule to 17 games in 2021
                num_games = 17                      
            player_dst_rankings +=  '0, ' * num_games 
            player_dst_encodings += '0, ' * num_games
            player_fantasy_points += '0, ' * num_games
            player_weeks_encodings += '0, ' * num_games
            player_season_encodings += '0, ' * num_games
            player_skill_score += '0, ' * num_games
            player_seasons_played += '0, ' * num_games       
        else:               
            try: 
                dst = line[1][1:]
                dst = dst.replace('@ ', '')
                dst = dst.replace('vs. ', '')
                try:
                    dst_rank = dst_rankings[(season, week, dst)]
                    dst_encode = dst_encodings[dst]
                    week += 1
                    player_weeks_encodings += f'{week}, '
                    player_season_encodings += f'{season}, '   
                    fantasy_points = line[17][1:]
                    player_skill_score += skill_scores[player] + ', '
                    player_seasons_played += seasons_played[player][season - 1] + ', '   
                    if fantasy_points != '-':              
                        player_dst_rankings += dst_rank + ', '
                        player_dst_encodings += dst_encode + ', '
                        player_fantasy_points += fantasy_points + ', '                      
                    else:
                        player_dst_rankings += '0, '
                        player_dst_encodings += '0, '
                        player_fantasy_points += '0, '                              
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

if __name__ == '__main__':   
    player_data = create_player_data(create_dst_rankings_dictionary(), create_dst_encodings_dictionary(),
                                     create_skill_score(), create_seasons_played())
    create_data_txt(player_data)
      