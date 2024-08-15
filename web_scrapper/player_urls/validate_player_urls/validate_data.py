from web_scrapper.skill_scores import main as create_skill_scores
from web_scrapper.weekly_data import main as create_weekly_data
from web_scrapper.rookie_seasons import main as create_rookie_seasons
from web_scrapper.team_id import main as create_team_id
from web_scrapper.data.main import create_player_data, create_data_csv, create_depth_chart, create_fantasy_points 
from web_scrapper.data.main import create_dst_rankings_dictionary, create_dst_id_dictionary, create_roster 
from web_scrapper.data.main import create_seasons_played, create_skill_score, create_team_ids

def create_player_outut_files():
    """ Create the output files needed to create the player data for a single player.
    """
    create_skill_scores.main('web_scrapper/player_urls/validate_player_urls/validate_player_url.out', 
                             'web_scrapper/player_urls/validate_player_urls/skill_scores.out')
    
    create_weekly_data.main('web_scrapper/player_urls/validate_player_urls/validate_player_url.out', 
                            'web_scrapper/player_urls/validate_player_urls/weekly_data.out')
    
    create_rookie_seasons.main('web_scrapper/player_urls/validate_player_urls/validate_player_url.out', 
                               'web_scrapper/player_urls/validate_player_urls/rookie_seasons.out')
    
    create_team_id.main('web_scrapper/player_urls/validate_player_urls/validate_player_url.out',
                        'web_scrapper/player_urls/validate_player_urls/team_id.out')

def validate_player_data(valid_output, error_output, player):
    """ Test validate_data.csv to make sure it has the correct number of rows and columns for a single player.
        If player data is valid, write player url to valid_output. Otherwise, write player url to error_output.

        Parameters: valid_output (output stream), error_output (output stream) - output streams for valid and error player urls
                    player (str) - player url
        Mofiies: valid_output, error_output  
    """
    with open('web_scrapper/player_urls/validate_player_urls/validate_data.csv', 'r') as data_file:
        data = data_file.read()
        data = data.split('\n')
        if len(data) == 18:
            valid_lines = 0
            for line in data:
                line = line.split()
                if len(line) == 50:
                    valid_lines += 1
            if valid_lines == 17:
                valid_output.write(player + '\n')
            else:
                error_output.write(player + '\n')
        else:
            error_output.write(player + '\n')
     
def main():
    with open('web_scrapper/player_urls/validate_player_urls/valid_urls.out', 'w') as valid_output:
        with open('web_scrapper/player_urls/validate_player_urls/error_urls.out', 'w') as error_output:   

            with open('web_scrapper/player_urls/validate_player_urls/player_urls.out', 'r') as player_urls_input_file:
                player_urls = player_urls_input_file.readlines() 
            for player in player_urls[:2]:
                player = player.strip()
                # Create an output file containing only a single player url.
                with open('web_scrapper/player_urls/validate_player_urls/validate_player_url.out', 'w') as validate_urls_output:
                    validate_urls_output.write(player)
                
                create_player_outut_files()
                                                       
                dst_rankings = create_dst_rankings_dictionary()
                dst_ids = create_dst_id_dictionary()
                
                try:
                    skill_scores = create_skill_score('web_scrapper/player_urls/validate_player_urls/skill_scores.out')
                except ZeroDivisionError:
                    error_output.write(player + '\n')
                    continue
                
                seasons_played = create_seasons_played('web_scrapper/player_urls/validate_player_urls/rookie_seasons.out')
                team_ids = create_team_ids(dst_ids, 'web_scrapper/player_urls/validate_player_urls/team_id.out')
                
                try:
                    depth_chart = create_depth_chart(create_roster(team_ids), create_fantasy_points('web_scrapper/player_urls/validate_player_urls/weekly_data.out'),
                                                      skill_scores)
                except ValueError:
                    error_output.write(player + '\n')
                    continue   
                
                player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, team_ids, 
                                                 depth_chart, 17, 'web_scrapper/player_urls/validate_player_urls/weekly_data.out')  
                create_data_csv(player_data, 'web_scrapper/player_urls/validate_player_urls/validate_data.csv')
            
                validate_player_data(valid_output, error_output, player)
                
                    
if __name__ == '__main__':    
    main()