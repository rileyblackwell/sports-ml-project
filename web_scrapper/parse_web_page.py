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
    
    def handle_starttag(self, tag, attrs):         
        if tag == 'td':
            self.in_td_tag = True
         
        
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_td_tag:        
            print(f"{data}")

parser = MyHTMLParser()

html_code = get_web_page('https://www.fantasypros.com/nfl/games/dalvin-cook.php')
parser.feed(html_code)
