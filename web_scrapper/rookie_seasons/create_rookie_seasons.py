import requests
from html.parser import HTMLParser

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

class WeeklyDataParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.first_td = True
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:                   
            if self.first_td:
                output.write(f'{data}\n')
                self.first_td = False
                    
if __name__ == '__main__':
    parser = WeeklyDataParser()
    with open('rookie_seasons_data.out', 'w') as output:
        with open('../player_urls/player_urls.out', 'r') as f: 
            for player in f:
                player = player.strip() 
                parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/stats/{player}.php'))             
                parser.first_td = True
                    