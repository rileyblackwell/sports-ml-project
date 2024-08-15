import unittest
from web_scrapper.weekly_data.main import main

class TestCreateWeeklyData(unittest.TestCase):
    def test_main(self):
        main(input_file = 'web_scrapper/player_urls/test_player_urls.out', 
             output_file = 'web_scrapper/weekly_data/weekly_data_tests.out')

if __name__ == '__main__':
    unittest.main()