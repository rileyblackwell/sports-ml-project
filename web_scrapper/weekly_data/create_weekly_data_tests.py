import unittest
from create_weekly_data import main

class TestCreateWeeklyData(unittest.TestCase):
    def test_main(self):
        main(input_file = '../player_urls/test_player_urls.out', output_file = 'weekly_data_tests.out')

if __name__ == '__main__':
    unittest.main()