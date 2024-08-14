from web_scrapper.data.create_params import create_dst_rankings_dictionary, create_dst_id_dictionary, create_team_ids 
from web_scrapper.data.create_params import create_skill_score, create_seasons_played, create_game_average, create_depth_chart
from web_scrapper.data.create_params import create_fantasy_points, create_roster
import sqlite3

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

def player_missed_season(params, season):
    """
    Updates the parameters for a player to indicate missed games in a season.

    Args:
        params (list): A list of player parameters.
        season (int): The season in which the player missed games.

    Returns:
        list: The updated list of player parameters with missed games marked.
    """
    num_games = 16
    if season >= 2: # NFL changed schedule to 17 games in 2021
        num_games = 17 
    new_params = []
    for param in params:
        param += '0, ' * num_games
        new_params.append(param)
    return new_params

def create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played,
                       teams_ids, depth_chart, num_params):
    conn = sqlite3.connect("web_scrapper/player_stats.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player_weekly_data")
    rows = cursor.fetchall()
    
    conn.close()

    data = []
    for row in rows:
        row_str = row[1].split('\n')
        data.append([''])
        for row in row_str:
            data.append(row.split(','))

    params = initialize_params(num_params)
    player_data = []
    player, week, season = 0, 1, 1
    # Ignore the first blank line. Data for first player starts at data[1]. 
    for row in data[1:]:  
        if row[0] == '':             
            week = 1
            season += 1       
            if season == 4:
                for i in range(3, 10): # 3 game average to 9 game average
                    params[i + 5] = create_game_average(params[0], i) 
                player_data = add_player_data(player_data, params)
                params = initialize_params(num_params)
                player += 1
                season = 1
            continue           
        
        if row[0][:34] == 'Player does not have any game data':                                          
            params = player_missed_season(params, season)     
        else:               
            dst = row[1][1:].replace('@ ', '').replace('vs. ', '') # Removes @ and vs. from dst name    
            try:
                dst_rank = dst_rankings[(season, week, dst)]
                dst_id = dst_ids[dst]
            except KeyError: # Handles bye weeks and season totals
                continue         
            
            params[2] += f'{week}, '
            params[1] += f'{season}, '
            if len(row) == 20: # Handles error with data for joe mixon and devin singletary   
                fantasy_points = row[17][1:]
            else:
                fantasy_points = '-'                    
            params[5] += f'{skill_scores[player]}, '
            params[6] += f'{seasons_played[player][season - 1]}, '
            params[7] += f'{player + 1}, '                    
            try:
                params[15] += f'{teams_ids[player][season]}, '
            except KeyError:
                params[15] += '0, ' # Player did not play in the season
            
            if fantasy_points == '-':              
                for i in (0, 3, 4, 16): # 0 is fantasy points, 3 is dst rank, 4 is dst encoding, 16 is depth chart
                    params[i] += '0, '                                          
            else:
                params[0] += fantasy_points + ', ' 
                params[3] += dst_rank + ', '
                params[4] += dst_id + ', '
                try:
                    params[16] += f'{depth_chart[(player + 1, season)][week - 1]}, ' 
                except KeyError: # fixes error with jk dobbins data
                    params[16] += '0, '  
            week += 1                                                                                            
    return player_data

def create_data_csv(player_data, filename='fantasy_football/data.csv'):
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
    depth_chart =  create_depth_chart(create_roster(team_ids), create_fantasy_points(),
                                      skill_scores)   
    
    player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, team_ids, 
                                     depth_chart, 17)
    create_data_csv(player_data)
      