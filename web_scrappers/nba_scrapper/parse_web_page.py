from gather_data import get_web_page

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
    
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

# html_code = open('sample_data.txt', 'r').read()
print(get_web_page('https://www.nba.com/stats/teams/traditional?SeasonType=Regular+Season'))
# parser.feed(html_code)


