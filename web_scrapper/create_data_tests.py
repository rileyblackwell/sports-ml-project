import unittest
from create_data import create_player_data, create_dst_rankings_dictionary, create_dst_encodings_dictionary
from create_data import create_skill_score, create_data_txt, create_seasons_played


class TestCreateData(unittest.TestCase):
    # def test_create_player_data(self):
    #     dst_rankings = create_dst_rankings_dictionary()
    #     dst_encodings = create_dst_encodings_dictionary()
    #     skill_scores = create_skill_score()
    #     player_data = create_player_data(dst_rankings, dst_encodings, skill_scores)
    #     create_data_txt(player_data)

    def test_create_seasons_played(self):
        seasons_played = create_seasons_played()
        print(seasons_played)


if __name__ == '__main__':
    unittest.main()