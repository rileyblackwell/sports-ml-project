import random

with open('player_urls.out', 'r') as f:
    players = f.readlines()
    random.shuffle(players)
    with open('player_urls.out', 'w') as out:
        for player in players:
            out.write(player)