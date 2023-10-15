import unittest
from create_team_id import main

class TestCreateTeamId(unittest.TestCase):
    def test_main(self):
        main(input_filename = 'web_scrapper/player_urls/test_player_urls.out', 
             output_filename = 'web_scrapper/team_id/team_id_tests.out')

if __name__ == '__main__':
    unittest.main()

