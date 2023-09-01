import unittest
from create_team_id import main

class TestCreateTeamId(unittest.TestCase):
    def test_main(self):
        main(input_filename = '../player_urls/test_player_urls.out', output_filename = 'team_id_tests.out')

if __name__ == '__main__':
    unittest.main()

