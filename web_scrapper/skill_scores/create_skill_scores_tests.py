import unittest
from create_skill_scores import main

class TestCreateSkillScores(unittest.TestCase):
    def test_main(self):
        main(input_file = '../player_urls/test_player_urls.out', output_file = 'skill_scores_tests.out')

if __name__ == '__main__':
    unittest.main()