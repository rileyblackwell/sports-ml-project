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
            try: # data starts recording when a number is encountered
                int(data)
                self.start_of_data = True        
            except ValueError:
                pass
            if self.start_of_data:
                if data[-1] == '%':
                    output.write(f"{data}")       
                    output.write('\n')
                else:
                    output.write(f"{data}, ")    

parser = MyHTMLParser()

output = open('parse_web_page.out', 'w') 
parser.feed(get_web_page('https://www.fantasypros.com/nfl/stats/wr.php?year=2022&week=3&range=week'))
output.close()