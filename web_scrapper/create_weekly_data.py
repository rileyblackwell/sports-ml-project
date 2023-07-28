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
                    output.write('\n')
                if data == 'Week 1':
                    output.write('\n')
                if data[:34] == 'Player does not have any game data': 
                    output.write('\n\n')
                           
            output.write(f"{data}, ")
            self.start_of_data = True           
               
if __name__ == '__main__':
    parser = MyHTMLParser()
    output = open('weekly_data.out', 'w')
    
    i = 0
    with open('player_urls.out', 'r') as f: 
        for player in f:
            player = player.strip() 
            for season in range(2020, 2022):                   
                parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php?season={season}'))
            parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php'))               
            if i == 20:
                break
            i += 1  
    output.close()
