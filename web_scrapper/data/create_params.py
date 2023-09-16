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

            if season != -1:
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

def create_fantasy_points(filename='../weekly_data/weekly_data.out'):
    """
    Creates a list of fantasy points for each player.

    Args:
        filename (str): Path to the file containing weekly data.

    Returns:
        dict: A dictionary with keys as tuples (player_id, season) and values as fantasy points.
    """
    with open(filename) as f:
        data = f.readlines()
        data = [line.strip() for line in data]
        data = [line.split(',') for line in data]

    fantasy_points = {}
    player_fantasy_points = []
    season = 1
    player_id = 1
    for line in data:
        if line[0] == '':
            season += 1
            fantasy_points[(player_id, season - 1)] = player_fantasy_points
            player_fantasy_points = []
            if season == 4:
                season = 1
                player_id += 1
        
        if line[0][:34] == 'Player does not have any game data':         
            num_games = 16
            if season >= 2: # NFL changed schedule to 17 games in 2021
                num_games = 17
            for _  in range(num_games):
                player_fantasy_points.append('0.0')
        else: 
            if line[0] == 'Totals':
                pass
            else:
                try:
                    player_fantasy_points.append(line[17][1:])
                except IndexError: # bye week
                    pass
    return fantasy_points

def create_roster(team_ids):
    """
    Creates a list of players on each team.

    Args:
        team_ids (list): A list of dictionaries, each containing season-wise team IDs.

    Returns: roster (dict): A dictionary with keys as tuples (season, team_id) and values as lists of player_ids.
    """
    player_id = 1
    roster = {}
    season = 1
    for player in team_ids:
        for season in player:
            
            current_roster = roster.get((season, player[season]))  
            if current_roster is None:
                roster[(season, player[season])] = [player_id] # (season, team_id) : [player_id]
            else:
                roster[(season, player[season])].append(player_id)

            season += 1
        player_id += 1

    return roster 

def create_depth_chart(rosters, fantasy_points):
    """
    Creates a weekly depth chart ranking for each player.

    Args:
        rosters (dict): A dictionary with keys as tuples (season, team_id) and values as lists of player_ids.
        fantasy_points (dict): A dictionary with keys as tuples (player_id, season) and values as fantasy points.
    
    Returns:
        dict: A dictionary with keys as tuples (player_id, season, team_id) and values as lists of depth chart rankings.
    """
    def fantasy_points_list_to_string(fantasy_points):
        """
        Converts fantasy points from a list to a string.

        Args:
            fantasy_points (list): A list of fantasy points.

        Returns:
            str: A comma-separated string of fantasy points.
        """
        fantasy_points_str = ''
        for points in fantasy_points:
            if points == '-':
                fantasy_points_str += '0.0, '
            else:
                fantasy_points_str += points + ', '
        return fantasy_points_str  

    def get_games_in_season(team_game_averages):
        """
        Gets the number of games in a season.

        Args: 
            team_game_averages (dict): A dictionary with keys as player_ids and values as game averages.

        Returns:
            int: The number of games in a season.
        """
        for average in team_game_averages.values():
            game_average = average[:-2].split(', ')
            return len(game_average) 
    
    depth_chart = {}
    for team in rosters.items():
        team_id = team[0][1]
        season_id = team[0][0]
        players = team[1]
        
        # calculate the 3 game averages for each player on the team
        team_game_averages = {}
        for player_id in players:
            player_fantasy_points = fantasy_points[(player_id, season_id)]
            fantasy_points_str = fantasy_points_list_to_string(player_fantasy_points)
            team_game_averages[player_id] = create_game_average(fantasy_points_str, 3)
        
        for week in range(get_games_in_season(team_game_averages)):
            game_averages_rankings = []
            for player_game_averages in team_game_averages.items():
                game_averages = player_game_averages[1][:-2].split(', ')
                game_averages_rankings.append((player_game_averages[0], team_id, float(game_averages[week])))

            # rank players on the depth chart by highest to lowest 3 game averages    
            game_averages_rankings.sort(key=lambda x: x[2], reverse=True)
            rank = 1 
            for player in game_averages_rankings:
                if week == 0:
                    depth_chart[(player[0], season_id)] = [0] # intialize depth chart ranking to 0
                else:
                    depth_chart[(player[0], season_id)].append(rank) # (player_id, season, team_id) : [rank]
                rank += 1      

    return depth_chart