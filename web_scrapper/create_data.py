def create_dst_rankings_dictionary():
    with open('dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_rankings = {}
    for line in data:
        dst_rankings[line[1][1:]] = line[0]
    return dst_rankings

def create_skill_score():
    with open('skill_scores.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    skill_scores = []
    skill_score = 0
    seasons = 0
    for line in data:
        if line[0] == '':
            skill_scores.append(str(round(skill_score / seasons, 2)))
            skill_score = 0
            seasons = 0
        else:     
            skill_score += float(line[1]) / float(line[0])
            seasons += 1
    return skill_scores        
     
dst_rankings = create_dst_rankings_dictionary()
skill_scores = create_skill_score()

with open('parse_web_page.out') as f:
    data = f.readlines()
    data = [line.strip() for line in data]
    data = [line.split(',') for line in data]

player_dst = ''
player_fantasy_points = '' 
player_skill_score = ''  
output = open('data.out', 'w')
player = 0
for line in data:
    if line[0] == '':    
        output.write(f'{player_dst[:-2]}\n{player_fantasy_points[:-2]}\n{player_skill_score[:-2]}\n')
        player_dst = ''
        player_fantasy_points = ''
        player_skill_score = ''
        player += 1
    try: 
        dst = line[1][1:]
        dst = dst.replace('@ ', '')
        dst = dst.replace('vs. ', '')
        try:
            dst = dst_rankings[dst]  
            fantasy_points = line[17][1:]
            skill_score = skill_scores[player]   
            if fantasy_points != '-':              
                player_dst += dst + ', '
                player_fantasy_points += fantasy_points + ', '
                player_skill_score += skill_score + ', '                          
        except KeyError:
            pass             
    except IndexError:
        pass
output.close()   