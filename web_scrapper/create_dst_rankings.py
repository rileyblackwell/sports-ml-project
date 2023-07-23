import requests
from html.parser import HTMLParser

def get_web_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

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
    parser = DstRankingParser()
    output = open('dst_rankings.out', 'w')
    parser.feed(get_web_page('https://www.fantasypros.com/nfl/stats/dst.php?year=2021&range=full'))
    output.write('\n')
    for week in range(1, 18):
        parser.feed(get_web_page(f'https://www.fantasypros.com/nfl/stats/dst.php?year=2022&range=custom&start_week=1&end_week={week}'))
        output.write('\n')
    output.close()  
    