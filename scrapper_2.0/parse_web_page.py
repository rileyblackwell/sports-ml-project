from requests_demo import get_web_page

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()     
        self.in_td_tag = False
        self.in_span_tag = False
    
    def handle_starttag(self, tag, attrs):         
        if tag == 'td' and attrs == [('class', 'Table__TD')]:
            self.in_td_tag = True
        elif tag == 'span' and self.in_td_tag:
            self.in_span_tag = True
        
    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_span_tag = False
            self.in_td_tag = False    

    def handle_data(self, data):
        if self.in_span_tag and data != ' ':        
            print(f"{data}")

parser = MyHTMLParser()

# html_code = open('sample_data.txt', 'r').read()
html_code = get_web_page('https://www.espn.com/nfl/team/stats/_/name/dal/dallas-cowboys')
parser.feed(html_code)


