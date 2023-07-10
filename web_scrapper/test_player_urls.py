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
        self.start_of_data = 0
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):     
        if self.in_td_tag:
            if self.start_of_data == 3:
                if data[:2] == 'RB':
                    output.write(f'{player}\n')
                else:
                    output.write(f'{player}-rb\n')               
            self.start_of_data += 1

parser = MyHTMLParser()
output = open('test_player_urls.out', 'w')
with open('players_urls.out') as f:
    players = f.readlines()
    players = [x.strip() for x in players]

for player in players:
    parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/rankings/{player}.php'))
    parser.start_of_data = 0

output.close()

