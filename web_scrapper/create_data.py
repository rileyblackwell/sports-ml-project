def create_dst_rankings_dictionary():
    with open('dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_rankings = {}
    week = 0
    for line in data:
        if line[0] == '':
            week += 1
        else:
            dst_rankings[(week, line[1][1:])] = line[0]    
    return dst_rankings

def create_dst_encodings_dictionary():
    with open('dst_encodings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]
    dst_encodings = {}
    for line in data:
        dst_encodings[line[1][1:]] = line[0]
    return dst_encodings

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
            try:
                skill_score += float(line[1]) / float(line[0])        
            except ZeroDivisionError:
                if float(line[0]) != 0 and float(line[1]) != 0: # Error occurs when dividing 0 points scored / 0 games played.
                    raise ZeroDivisionError
            seasons += 1      
    return skill_scores        

def create_player_data(dst_rankings, dst_encodings, skill_scores):
    with open('weekly_data.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    player_dst_rankings = ''
    player_dst_encodings = ''
    player_fantasy_points = '' 
    player_skill_score = ''  
    player_data = []
    player = 0
    week = 0
    for line in data:
        if line[0] == '':    
            player_data.append(f'{player_dst_rankings[:-2]}\n')
            player_data.append(f'{player_dst_encodings[:-2]}\n')
            player_data.append(f'{player_fantasy_points[:-2]}\n')
            player_data.append(f'{player_skill_score[:-2]}\n')
            player_dst_rankings = ''
            player_fantasy_points = ''
            player_skill_score = ''
            player_dst_encodings = ''
            player += 1
            week = 0
        try: 
            dst = line[1][1:]
            dst = dst.replace('@ ', '')
            dst = dst.replace('vs. ', '')
            try:
                dst_rank = dst_rankings[(week, dst)]
                dst_encode = dst_encodings[dst]
                week += 1  
                fantasy_points = line[17][1:]
                skill_score = skill_scores[player]   
                if fantasy_points != '-':              
                    player_dst_rankings += dst_rank + ', '
                    player_dst_encodings += dst_encode + ', '
                    player_fantasy_points += fantasy_points + ', '
                    player_skill_score += skill_score + ', '                          
            except KeyError:
                pass             
        except IndexError:
            pass
    return player_data

def create_data_txt(player_data):
    output = open('data.txt', 'w')
    player_data = [line.split() for line in player_data]     
    for line in player_data:
        if len(line) >= 15:
            for i in range(14):
                output.write(line[i] + ' ')      
            if line[14][-1] == ',':
                line[14] = line[14][:-1]
            output.write(line[14] + '\n')
    output.close()

if __name__ == '__main__':   
    player_data = create_player_data(create_dst_rankings_dictionary(), create_dst_encodings_dictionary(),
                                     create_skill_score())
    create_data_txt(player_data)
      