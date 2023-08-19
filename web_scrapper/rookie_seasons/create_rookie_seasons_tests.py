import unittest
from create_rookie_seasons import main

class TestCreateRookieSeasons(unittest.TestCase):
    def test_main(self):
        main(input_file = '../player_urls/test_player_urls.out', output_file = 'rookie_seasons_data_tests.out')

if __name__ == '__main__':
    unittest.main()        
