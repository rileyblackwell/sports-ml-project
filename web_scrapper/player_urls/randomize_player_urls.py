import random
import sys

def shuffle_player_urls():
    with open(f'player_urls_{sys.argv[1]}.out', 'r') as f:
        players = f.readlines()
        for _ in range(500000):
            random.shuffle(players)
        with open(f'player_urls_{sys.argv[1]}.out', 'w') as out:
            for player in players:
                out.write(player)

    
if __name__ == '__main__':
    shuffle_player_urls()