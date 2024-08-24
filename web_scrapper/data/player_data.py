from web_scrapper.data.create_params import create_game_average

from web_scrapper.data.database import (
    read_player_urls_from_db,
    read_player_weekly_data_from_db,
)
from web_scrapper.data.player_data_utils import (
    initialize_params,
    add_player_data,
    player_missed_season,
    process_player_data,
    shuffle_player_urls,
)


def initialize_player_data(num_params):
    player_urls = read_player_urls_from_db()
    player_urls = shuffle_player_urls(player_urls)
    params = initialize_params(num_params)
    player_data = []
    return player_urls, params, player_data

def process_player_season_data(data, player, season, params, dst_rankings, dst_ids, skill_scores, seasons_played, teams_ids, depth_chart):
    week = 1
    for row in data[1:]:
        if row[0] == '':
            week = 1
            season += 1
            if season == 4:
                params = update_game_averages(params)
                return params
            continue

        if row[0][:34] == 'Player does not have any game data':
            params = player_missed_season(params, season)
        else:
            dst = row[1][1:].replace('@ ', '').replace('vs. ', '')
            try:
                dst_rank = dst_rankings[(season, week, dst)]
                dst_id = dst_ids[dst]
            except KeyError:
                continue

            params = update_params(params, row, week, season, player, dst_rank, dst_id, skill_scores, seasons_played, teams_ids, depth_chart)
            week += 1
    return params

def update_params(params, row, week, season, player, dst_rank, dst_id, skill_scores, seasons_played, teams_ids, depth_chart):
    params[2] += f'{week}, '
    params[1] += f'{season}, '
    fantasy_points = get_fantasy_points(row)
    params[5] += f'{get_skill_score(skill_scores, player)}, '
    params[6] += f'{get_seasons_played(seasons_played, player, season)}, '
    params[7] += f'{player + 1}, '
    params[15] += f'{get_team_id(teams_ids, player, season)}, '

    if fantasy_points == '-':
        params = handle_missing_fantasy_points(params)
    else:
        params[0] += fantasy_points + ', '
        params[3] += dst_rank + ', '
        params[4] += dst_id + ', '
        params[16] += f'{get_depth_chart(depth_chart, player, season, week)}, '
    return params

def update_game_averages(params):
    for i in range(3, 10):
        params[i + 5] = create_game_average(params[0], i)
    return params

def get_fantasy_points(row):
    if len(row) == 20:
        return row[17][1:]
    else:
        return '-'

def get_skill_score(skill_scores, player):
    try:
        return skill_scores[player]
    except IndexError:
        return 0

def get_seasons_played(seasons_played, player, season):
    try:
        return seasons_played[player][season - 1]
    except IndexError:
        return 0

def get_team_id(teams_ids, player, season):
    try:
        return teams_ids[player][season]
    except (KeyError, IndexError):
        return 0

def get_depth_chart(depth_chart, player, season, week):
    try:
        return depth_chart[(player + 1, season)][week - 1]
    except KeyError:
        return 0

def handle_missing_fantasy_points(params):
    for i in (0, 3, 4, 16):
        params[i] += '0, '
    return params

def create_player_data(dst_rankings, dst_ids, skill_scores, seasons_played, teams_ids, depth_chart, num_params):
    player_urls, params, player_data = initialize_player_data(num_params)
    player = 0
    season = 1
    for player_url in player_urls:
        rows = read_player_weekly_data_from_db(player_url[0])
        data = process_player_data(rows)
        params = process_player_season_data(data, player, season, params, dst_rankings, dst_ids, skill_scores, seasons_played, teams_ids, depth_chart)
        player_data = add_player_data(player_data, params)
        params = initialize_params(num_params)
        player += 1
        season = 1
    return player_data