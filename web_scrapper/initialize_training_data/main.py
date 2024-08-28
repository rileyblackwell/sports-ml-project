from web_scrapper.initialize_training_data.data_output import create_data_csv
from web_scrapper.initialize_training_data.player_data import create_player_data
from web_scrapper.initialize_training_data.database import read_player_urls_from_db
from web_scrapper.initialize_training_data.player_data_utils import shuffle_player_urls

from web_scrapper.initialize_training_data.initialize_dst_params import (
    initialize_dst_rankings_dictionary,
    initialize_dst_id_dictionary
)
from web_scrapper.initialize_training_data.initialize_params import (
    create_team_ids,
    create_depth_chart,
    create_fantasy_points,
    create_roster,
    create_seasons_played,
    create_skill_score
)


if __name__ == '__main__':
    player_urls = read_player_urls_from_db()
    dst_rankings = initialize_dst_rankings_dictionary()
    dst_ids = initialize_dst_id_dictionary()
    skill_scores = create_skill_score(player_urls)
    seasons_played = create_seasons_played(player_urls)
    team_ids = create_team_ids(dst_ids, player_urls)
    depth_chart = create_depth_chart(create_roster(team_ids), create_fantasy_points(), skill_scores)

    player_data = create_player_data(player_urls, dst_rankings, dst_ids, skill_scores, seasons_played, team_ids, depth_chart, 18)
    create_data_csv(player_data)