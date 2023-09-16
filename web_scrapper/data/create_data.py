from create_params import create_dst_rankings_dictionary, create_dst_id_dictionary, create_team_ids 
from create_params import create_skill_score, create_seasons_played, create_game_average, create_depth_chart
from create_params import create_fantasy_points, create_roster

def initialize_params(num_params):
    """
    Initializes a list of parameters with empty strings.

    Args:
        num_params (int): The number of parameters to initialize.

    Returns:
        list: A list of empty strings representing parameters.
    """
    params = []
    for _ in range(num_params):
        params.append('')
    return params

def add_player_data(player_data, params):
    """
    Adds player data to a list by appending parameter values to it.

    Args:
        player_data (list): The list to which player data will be added.
        params (list): A list of parameter values to add to the player data.

    Returns:
        list: The updated player data list.
    """
    for param in params:
        player_data.append(f'{param[:-2]}\n')
    return player_data

def player_missed_season(params, num_games):
    """
    Updates the parameters for a player to indicate missed games in a season.

    Args:
        params (list): A list of player parameters.
        num_games (int): The number of games to mark as missed.
        player_id (str): The unique identifier of the player.

    Returns:
        list: The updated list of player parameters with missed games marked.
    """
    new_params = []
    for param in params:
        param += '0, ' * num_games
        new_params.append(param)
    return new_params


def create_player_data(dst_rankings, dst_encodings, skill_scores, seasons_played,
                       teams_ids, depth_chart, num_params, filename = '../weekly_data/weekly_data.out'):
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
            for i in range(3, 10): # 3 game average to 9 game average
                params[i + 5] = create_game_average(params[0], i) 
            player_data = add_player_data(player_data, params)
            params = initialize_params(num_params)
            player += 1
            season = 1       
        
        if line[0][:34] == 'Player does not have any game data':         
            num_games = 16
            if season >= 2: # NFL changed schedule to 17 games in 2021
                num_games = 17                      
            params = player_missed_season(params, num_games)     
        else:               
            try: 
                dst = line[1][1:].replace('@ ', '').replace('vs. ', '') # Removes @ and vs. from dst name
                try:
                    dst_rank = dst_rankings[(season, week, dst)]
                    dst_encode = dst_encodings[dst]        
                    params[2] += f'{week}, '
                    params[1] += f'{season}, '
                    if len(line) == 20: # Handles error with data for joe mixon and devin singletary   
                        fantasy_points = line[17][1:]
                    else:
                        fantasy_points = '-'    
                    params[5] += f'{skill_scores[player]}, '
                    params[6] += f'{seasons_played[player][season - 1]}, '
                    params[7] += f'{player + 1}, '                    
                    try:
                        params[15] += f'{teams_ids[player][season]}, '
                    except KeyError:
                        params[15] += '0, ' # Player did not play in the season
                    week += 1   
                    if fantasy_points == '-':              
                        params[0] += '0, '
                        params[3] += '0, '
                        params[4] += '0, ' 
                        params[16] += '0, '                                          
                    else:
                        params[0] += fantasy_points + ', ' 
                        params[3] += dst_rank + ', '
                        params[4] += dst_encode + ', '
                        params[16] += f'{depth_chart[(player + 1, season)][week - 2]}, ' # -2 because week starts at 0                                                                          
                except KeyError:
                    pass              
            except IndexError:
                pass
    return player_data

def create_data_txt(player_data, filename='data.txt'):
    """
    Creates a text file with player data.

    Args:
        player_data (list): List of player data lines, where each line is a string.
        filename (str): The name of the output text file (default is 'data.txt').

    Writes:
        A text file with player data.

    """
    with open(filename, 'w') as output:
        player_data = [line.split() for line in player_data]
        for line in player_data:
            for item in line:
                output.write(item + ' ')
            output.write('\n')

    
if __name__ == '__main__':
    dst_rankings = create_dst_rankings_dictionary()
    dst_ids = create_dst_id_dictionary()
    skill_scores = create_skill_score()
    seasons_played = create_seasons_played()
    team_ids = create_team_ids(dst_ids)
    depth_chart =  create_depth_chart(create_roster(team_ids), create_fantasy_points())   
    
    player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, team_ids, 
                                     depth_chart, 17)
    create_data_txt(player_data)
      