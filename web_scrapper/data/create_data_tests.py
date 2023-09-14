import unittest
from create_params import create_dst_rankings_dictionary, create_dst_id_dictionary, create_skill_score
from create_params import create_seasons_played, create_team_ids, create_fantasy_points, create_roster, create_depth_chart
from create_data import create_player_data, create_data_txt

class TestCreateData(unittest.TestCase):
    def test_create_player_data(self):
        dst_rankings = create_dst_rankings_dictionary()
        dst_ids = create_dst_id_dictionary()
        skill_scores = create_skill_score('../skill_scores/skill_scores_tests.out')
        seasons_played = create_seasons_played('../rookie_seasons/rookie_seasons_data_tests.out')
        team_ids = create_team_ids(create_dst_id_dictionary(), '../team_id/team_id_tests.out')
        player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played,
                                         team_ids, 16, '../weekly_data/weekly_data_tests.out')
        create_data_txt(player_data, 'create_data_tests.out')

    def test_create_team_ids(self):
        teams_ids = create_team_ids(create_dst_id_dictionary())     

    def test_create_fantasy_points(self):
        fantasy_points = create_fantasy_points('../weekly_data/weekly_data_tests.out')
        
    def test_create_roster(self):
        teams_ids = create_team_ids(create_dst_id_dictionary(), '../team_id/team_id_tests.out')
        roster = create_roster(teams_ids)

    def test_create_depth_chart(self):
        teams_ids = create_team_ids(create_dst_id_dictionary())
        depth_chart = create_depth_chart(create_roster(teams_ids), create_fantasy_points())
       

if __name__ == '__main__':
    unittest.main()