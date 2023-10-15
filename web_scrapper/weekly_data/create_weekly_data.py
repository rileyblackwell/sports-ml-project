import requests
from html.parser import HTMLParser

def get_web_page(url):
    return requests.get(url).content.decode('utf-8')

class WeeklyDataParser(HTMLParser):
    def __init__(self, output):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.output = output
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:              
            if self.start_of_data:
                if data[:4] == 'Week' or data == 'Totals':                    
                    self.output.write('\n')
                if data == 'Week 1':
                    self.output.write('\n')
                if data[:34] == 'Player does not have any game data': 
                    self.output.write('\n\n')                        
            
            self.output.write(f"{data}, ")
            self.start_of_data = True           

def main(input_file = 'web_scrapper/player_urls/player_urls.out', output_file = 'web_scrapper/weekly_data/weekly_data.out'):
    with open(output_file, 'w') as output:
        parser = WeeklyDataParser(output)
        with open(input_file, 'r') as f: 
            for player in f:
                player = player.strip() 
                for season in range(2020, 2023):                   
                    parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php?season={season}'))              
        output.write('\n\n') # prevents a bug in create_data.py where player data isn't outputted.               

if __name__ == '__main__':
    main()        
  