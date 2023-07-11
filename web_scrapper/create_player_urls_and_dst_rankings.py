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
                    output.write(f"{data.lower()}\n")
                if data[-1] == '%':    
                    self.is_player_name = 0    

class DstRankingParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
        self.start_of_data = False
        self.dst = 0
    
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
                if self.dst == 0:
                    output.write(f"{data}, ")
                if self.dst == 2:
                    data = data.replace(' (', '')
                    data = data.replace(')', '')
                    output.write(f"{data}\n")    
                self.dst += 1 
                if data[-1] == '%':
                    self.dst = 0

if __name__ == '__main__':
    parser = PlayerUrlParser()
    output = open('players_urls.out', 'w') 
    parser.feed(get_web_page('https://www.fantasypros.com/nfl/stats/rb.php'))
    output.close()

    parser = DstRankingParser()
    output = open('dst_rankings.out', 'w')
    parser.feed(get_web_page('https://www.fantasypros.com/nfl/stats/dst.php'))
    output.close()
    
    with open('players_urls.out', 'r') as f:
        players = f.readlines()
        players = [player.strip() for player in players]
        
    