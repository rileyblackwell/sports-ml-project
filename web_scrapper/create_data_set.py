with open('parse_web_page.out') as f:
    data = f.readlines()
    data = [line.strip() for line in data]
    data = [line.split(',') for line in data]
   
players = {}
for line in data:
    players[(line[1], line[2][1:])] = line[16]

players    