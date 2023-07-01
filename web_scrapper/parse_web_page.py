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
            output.write(f"{data}, ")
            self.start_of_data = True           
               
if __name__ == '__main__':
    parser = MyHTMLParser()
    output = open('parse_web_page.out', 'w')
    
    i = 0
    with open ('players_urls.out', 'r') as f:  
        for player in f:
            player = player.strip()
            # if i == 0:
            #     output.write(f'\n{player}\n\n')
            # else:
            #     output.write(f'\n\n{player}')    
            parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/{player}.php'))
            i += 1
            if i == 5:
                break
    # season = 2020
    # while season <= 2021:
    #     parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/games/dandre-swift.php?season={season}'))
    #     season += 1
     
    
    output.close()
