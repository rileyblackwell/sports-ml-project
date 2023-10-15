import unittest
from create_rookie_seasons import main

class TestCreateRookieSeasons(unittest.TestCase):
    def test_main(self):
        main(input_file = 'web_scrapper/player_urls/test_player_urls.out',
              output_file = 'web_scrapper/rookie_seasons/rookie_seasons_data_tests.out')

if __name__ == '__main__':
    unittest.main()        
