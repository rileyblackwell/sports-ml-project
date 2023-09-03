import unittest
from create_data import create_player_data, create_dst_rankings_dictionary, create_dst_id_dictionary
from create_data import create_skill_score, create_data_txt, create_seasons_played, create_team_ids

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

if __name__ == '__main__':
    unittest.main()