import random

if __name__ == '__main__':
    with open('player_urls.out', 'r') as f:
        players = f.readlines()
        for _ in range(100000):
            random.shuffle(players)
        with open('player_urls.out', 'w') as out:
            for player in players:
                out.write(player)