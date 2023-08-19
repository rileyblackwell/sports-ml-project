import requests
from html.parser import HTMLParser

def get_web_page(url):
    return requests.get(url).content.decode('utf-8')

class WeeklyDataParser(HTMLParser):
    def __init__(self, output):
        super().__init__()     
        self.in_td_tag = False
        self.first_td = True
        self.output = output
         
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:                   
            if self.first_td:
                self.output.write(f'{data}\n')
                self.first_td = False

def main(input_file = '../player_urls/player_urls.out', output_file = 'rookie_seasons_data.out'):
    with open(output_file, 'w') as output:
        parser = WeeklyDataParser(output)
        with open(input_file, 'r') as f: 
            for player in f:
                player = player.strip() 
                parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/stats/{player}.php'))             
                parser.first_td = True                    

if __name__ == '__main__':
   main()
                    