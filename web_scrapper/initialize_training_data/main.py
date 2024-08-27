from web_scrapper.initialize_training_data.player_data import create_player_data
from web_scrapper.initialize_training_data.data_output import create_data_csv
from web_scrapper.initialize_training_data.create_params import (
    create_dst_rankings_dictionary,
    create_dst_id_dictionary,
    create_team_ids,
    create_depth_chart,
    create_fantasy_points,
    create_roster,
    create_seasons_played,
    create_skill_score
)

if __name__ == '__main__':
    dst_rankings = create_dst_rankings_dictionary()
    dst_ids = create_dst_id_dictionary()
    skill_scores = create_skill_score()
    seasons_played = create_seasons_played()
    team_ids = create_team_ids(dst_ids)
    depth_chart = create_depth_chart(create_roster(team_ids), create_fantasy_points(), skill_scores)

    player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, team_ids, depth_chart, 18)
    create_data_csv(player_data)