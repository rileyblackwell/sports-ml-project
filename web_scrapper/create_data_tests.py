import unittest
from create_data import create_player_data, create_dst_rankings_dictionary, create_dst_id_dictionary
from create_data import create_skill_score, create_data_txt, create_seasons_played

class TestCreateData(unittest.TestCase):
    def test_create_player_data(self):
        dst_rankings = create_dst_rankings_dictionary()
        dst_ids = create_dst_id_dictionary()
        skill_scores = create_skill_score('skill_scores/skill_scores_tests.out')
        seasons_played = create_seasons_played('rookie_seasons/rookie_seasons_data_tests.out')
        player_data = create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played,
                                          11, 'weekly_data/weekly_data_tests.out')
        create_data_txt(player_data, 'create_data_tests.out')
         
if __name__ == '__main__':
    unittest.main()