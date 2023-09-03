def create_dst_rankings_dictionary():
    """
    Creates a dictionary of DST (Defense/Special Teams) rankings for each season and week.

    Returns:
        dict: A dictionary with keys as tuples (season, week, team_name) and values as rankings.
    """
    with open('../dst_id_and_rankings/dst_rankings.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    dst_rankings = {}
    week, season = 1, 1
    for line in data:
        if line[0] == '':
            week += 1
        elif line[0] == 'end of season':
            season += 1
            week = 1
        else:
            dst_rankings[(season, week, line[1][1:])] = line[0]
    return dst_rankings


def create_dst_id_dictionary():
    """
    Creates a dictionary of DST (Defense/Special Teams) names their corresponding IDs.

    Returns:
        dict: A dictionary with keys as DST names and values as IDs.
    """
    with open('../dst_id_and_rankings/dst_id.out') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    dst_ids = {}
    for line in data:
        dst_ids[line[1][1:]] = line[0]
    return dst_ids


def create_team_ids(dst_ids, filename='../team_id/team_id.out'):
    """
    Creates a list of dictionaries containing team IDs for each season.

    Args:
        dst_ids (dict): Dictionary of DST IDs.
        filename (str): Path to the file containing team IDs data.

    Returns:
        list: A list of dictionaries, each containing season-wise team IDs.
    """
    dst_ids['ALL'] = '33'  # ID if player played for multiple teams in a season
    with open(filename) as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    team_ids = []
    for line in data:
        i, j = 0, 1
        teams = {}
        while j < len(line):
            season = -1
            if line[i].strip() == '2020':
                season = 1
            elif line[i].strip() == '2021':
                season = 2
            elif line[i].strip() == '2022':
                season = 3

            teams[season] = dst_ids[line[j].strip()]
            i += 2
            j += 2
        team_ids.append(teams)
    return team_ids


def create_skill_score(filename='../skill_scores/skill_scores.out'):
    """
    Creates a list of skill scores.

    Args:
        filename (str): Path to the file containing skill scores data.

    Returns:
        list: A list of skill scores.
    """
    with open(filename) as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    skill_scores = []
    skill_score, seasons = 0, 0
    for line in data:
        if line[0] == '':
            skill_scores.append(str(round(skill_score / seasons, 2)))
            skill_score, seasons = 0, 0
        else:
            try:
                skill_score += float(line[1]) / float(line[0])
            except ZeroDivisionError:
                if float(line[0]) != 0 and float(line[1]) != 0:  # Error occurs when dividing 0 points scored / 0 games played
                    raise ZeroDivisionError
            seasons += 1
    return skill_scores


def create_seasons_played(filename='../rookie_seasons/rookie_seasons_data.out'):
    """
    Creates a list of number of seasons played for each player.

    Args:
        filename (str): Path to the file containing rookie seasons data.

    Returns:
        list: A list of number of seasons played for each player.
    """
    def create_rookie_season():
        with open(filename) as f:
            data = f.readlines()
            data = [line.strip() for line in data]
            data = [line.split(',') for line in data]
        rookie_seasons = []
        for line in data:
            rookie_seasons.append(line[0][2:])
        return rookie_seasons

    rookie_seasons = create_rookie_season()
    seasons_played = []
    for rookie_season in rookie_seasons:
        seasons = []
        for i in range(2, -1, -1):
            current_season = max(23 - int(rookie_season) - i, 0)
            seasons.append(str(current_season))
        seasons_played.append(seasons)
    return seasons_played


# NOTE: Game average will also include games from the previous season
def create_game_average(fantasy_points, num_games):
    """
    Creates a string containing game averages for fantasy points.

    Args:
        fantasy_points (str): Comma-separated string of fantasy points.
        num_games (int): Number of games to calculate the average over.

    Returns:
        str: A comma-separated string of game averages.
    """
    games = fantasy_points[:-2].split(', ')
    games = [float(game) for game in games]
    game_data = ''
    for i in range(len(games)):
        games_played = 0
        game_average = 0.0
        for j in range(i - num_games, i):
            if j >= 0:
                game_average += games[j]
                if games[j] != 0.0:
                    games_played += 1
        if games_played != 0:
            game_data += str(round(game_average / games_played, 2)) + ', '
        else:
            game_data += '0.0' + ', '
    return game_data
