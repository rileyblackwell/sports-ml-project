import requests
from html.parser import HTMLParser

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

class PlayerUrlParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.is_player_name = 0
        self.players = []
    
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:
            try: # data starts recording when a number is encountered
                int(data)
                self.start_of_data = True        
            except ValueError:
                pass
            if self.start_of_data:
                self.is_player_name += 1
                if self.is_player_name == 2:                    
                    data = data.replace('\'', '')
                    data = data.replace(' Jr.', '')
                    data = data.replace('.', '')
                    data = data.replace(' III', '') 
                    data = data.replace(' II', '')                                    
                    data = data.replace(' ', '-')  
                    self.players.append(f"{data.lower()}")
                if data[-1] == '%':    
                    self.is_player_name = 0    

class ValidPlayerURLParser(HTMLParser):
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

if __name__ == '__main__':
    player_url_parser = PlayerUrlParser()
    player_url_parser.feed(get_web_page('https://www.fantasypros.com/nfl/stats/rb.php'))
    
    valid_player_url_parser = ValidPlayerURLParser() 
    output = open('player_urls.out', 'w') 
    for player in player_url_parser.players:
        if player != 'cordarrelle-patterson' and player != 'latavius-murray': # this player has errors in the html
            valid_player_url_parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/rankings/{player}.php'))
            valid_player_url_parser.start_of_data = 0
    output.close()