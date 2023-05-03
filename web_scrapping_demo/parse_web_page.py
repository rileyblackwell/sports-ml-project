from requests_demo import get_web_page

def parse(f, *args):  
    data = ''
    store_data = False
    for i in range(len(f)-3):
        tag = f[i:i+15]
        if store_data and '<' not in tag and '/' not in tag:
            try:
                data += str(int(tag[14:]))
            except ValueError:
                if tag[14:] == '.':
                    data += tag[14:]    
        if tag == args[0]:
            store_data = True
        if args[1] in tag:
            store_data = False
            if tag[:2] == '</':    
                data += ', '         
    return data

print(parse(get_web_page('https://www.espn.com/nfl/team/stats/_/name/dal/dallas-cowboys'), '<span class=\"\">', '</span>'))
 
