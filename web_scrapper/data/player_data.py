from web_scrapper.data.data_processing import process_player_data, initialize_params, add_player_data, player_missed_season
from web_scrapper.data.database import read_player_data_from_db
from web_scrapper.data.create_params import create_game_average
     
def create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, teams_ids, depth_chart, num_params):
    """Creates player data from the processed data and other inputs."""
    rows = read_player_data_from_db()
    data = process_player_data(rows)

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
            try:
                params[5] += f'{skill_scores[player]}, '
            except IndexError:  
                params[5] += '0, '
    
            params[6] += f'{seasons_played[player][season - 1]}, '
            params[7] += f'{player + 1}, '                    
            try:
                params[15] += f'{teams_ids[player][season]}, '
            except (KeyError, IndexError) as e:
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