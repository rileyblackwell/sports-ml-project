import requests
from html.parser import HTMLParser

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.totals_row = float('inf')
        self.games_played = 0
        self.weeks_row = float('inf')
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:              
            if self.start_of_data:               
                if data[:4] == 'Week':
                    self.weeks_row = 0
                self.weeks_row += 1                         
                if self.weeks_row == 17:
                    if data != '-':
                        self.games_played += 1
                              
                if data == 'Totals':
                    self.totals_row = 0
                    output.write(f'{self.games_played}, ')
                    self.games_played = 0                        
                self.totals_row += 1  
                if self.totals_row == 17:                       
                    output.write(f"{data}\n")
          
            self.start_of_data = True           
               
if __name__ == '__main__':
    parser = MyHTMLParser()
    output = open('skill_scores.out', 'w')

    with open('players_urls.out', 'r') as f:  
        i = 0
        for player in f:           
            player = player.strip() 
            season = 2018
            while season <= 2021:
                parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php?season={season}'))
                season += 1
            parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php'))
            output.write('\n')               
            if i == 10:
                break
            i += 1  
    output.close()


