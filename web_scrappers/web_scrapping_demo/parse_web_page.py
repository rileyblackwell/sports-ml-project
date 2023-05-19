from requests_demo import get_web_page

def parse(f, *args):  
    data = ''
    store_data = False
    for i in range(len(f)-3):
        tag = f[i:i+len(args[0])]
        if store_data and '</' not in tag:
            try:
                data += str(int(tag[len(args[0]) - 1:]))
            except ValueError:
                if tag[len(args[0]) - 1:] == '.':
                    data += tag[len(args[0]) - 1:]    
        if tag == args[0] or tag == args[1]:
            store_data = True
        if args[2] in tag:
            store_data = False
            if tag[:len(args[2])] == '</span></td>':    
                data += ', '         
    return data[:-2]

print(parse(get_web_page('https://www.espn.com/nhl/team/stats/_/name/bos/boston-bruins'), 
            '<td class=\"Table__TD\"><span class=\"\">', 'span class=\"Stats__TotalRow fw-bold\">', '</span></td>'))

# f = open('sample_bengals_data.txt', 'r').read() 
# print(parse(f, '<td class=\"Table__TD\"><span class=\"\">', '</span>'))