import unittest
from web_scrapper.skill_scores.main import main

class TestCreateSkillScores(unittest.TestCase):
    def test_main(self):
        main(input_file = 'web_scrapper/player_urls/test_player_urls.out', 
             output_file = 'web_scrapper/skill_scores/skill_scores_tests.out')

if __name__ == '__main__':
    unittest.main()