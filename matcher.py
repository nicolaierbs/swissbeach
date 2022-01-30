import random
import data_connector
import time

config = dict()
config['weight_match_count'] = 5
config['weight_won_matches_count'] = 3
config['weight_equal_team_strength_matches'] = 1
config['weight_same_match'] = 2
config['weight_same_team'] = 3
config['weight_equal_type'] = 1


def tournament_config(database):
    return config


def match_count(player):
    return player['statistics'].get('matches', 0)


def optimize(players, database):
    start = time.time()
    best_combination = players
    for i in range(6):
        players = switch(best_combination.copy())
        if score(players, database) < score(best_combination, database):
            best_combination = players

    # Debug the final match
    end = time.time()
    print('Duration for computation: ' + str(end - start))

    print(str([player['statistics'].get('won', 0) for player in best_combination[0:4]])
          + ' - '
          + str([match_count(player) for player in best_combination[0:4]]))

    # Select best combination for match
    return [player['_id'] for player in best_combination[0:4]]


def next_match(players, database):
    random.shuffle(players)
    # Select min. 4 players with lowest number of matches
    if len(players) < 4:
        return None
    selected_players = list()
    last_match_count = 0
    for player in sorted(players, key=match_count, reverse=False):
        if last_match_count == match_count(player) or len(selected_players) < 4:
            selected_players.append(player)
            last_match_count = match_count(player)
        else:
            return optimize(selected_players, database)
    return optimize(selected_players, database)


def type_difference(players, marker):
    return abs(
        sum([player['markers'][marker] for player in players[0:2]])
        - sum([player['markers'][marker] for player in players[2:4]]))


def score(players, database):
    value = 0
    value += config['weight_match_count'] * sum([match_count(player) for player in players[0:4]])
    value += config['weight_won_matches_count'] * abs(
        sum([player['statistics'].get('won', 0) for player in players[0:2]])
        - sum([player['statistics'].get('won', 0) for player in players[2:4]]))
    value += config['weight_equal_team_strength_matches'] * (
            abs(players[0]['statistics'].get('won', 0) - players[1]['statistics'].get('won', 0))
            + abs(players[2]['statistics'].get('won', 0) - players[3]['statistics'].get('won', 0))
    )
    value += config['weight_equal_type'] * sum([type_difference(players, marker)
                                                for marker in players[0]['markers'].keys()])

    value += config['weight_same_match'] * data_connector.match_count(players[0:4], database=database)
    value += config['weight_same_team'] * (
            data_connector.team_count(players[0:2], database=database) + data_connector.team_count(players[2:4], database=database))

    return value


def switch(players):
    i = random.randrange(0, len(players))
    j = i
    while i == j:
        j = random.randrange(0, len(players))
    players[i], players[j] = players[j], players[i]
    return players
