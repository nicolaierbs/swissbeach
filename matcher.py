import random
import data_connector

weight_match_count = 20
weight_won_matches_count = 10
weight_equal_team_strength_matches = 2
weight_same_match = 20
weight_same_team = 5


def match_count(player):
    return player['statistics'].get('matches', 0)


def optimize(players):
    best_combination = players
    for i in range(10):
        players = switch(best_combination.copy())
        if score(players) < score(best_combination):
            best_combination = players

    # Debug the final match
    print(str([player['statistics'].get('won', 0) for player in best_combination[0:4]])
          + ' - '
          + str([match_count(player) for player in best_combination[0:4]]))

    # Select best combination for match
    return [player['_id'] for player in best_combination[0:4]]


def next_match(players):
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
            return optimize(selected_players)
    return optimize(selected_players)


def score(players):
    value = 0
    value += weight_match_count * sum([match_count(player) for player in players[0:4]])
    value += weight_won_matches_count * abs(
        sum([player['statistics'].get('won', 0) for player in players[0:2]])
        - sum([player['statistics'].get('won', 0) for player in players[2:4]]))
    value += weight_equal_team_strength_matches * (
            abs(players[0]['statistics'].get('won', 0) - players[1]['statistics'].get('won', 0))
            + abs(players[2]['statistics'].get('won', 0) - players[3]['statistics'].get('won', 0))
    )

    # print('same match ' + str(data_connector.match_count(players[0:4]))
    #      + ' - same team ' + str((data_connector.team_count(players[0:2]) + data_connector.team_count(players[2:4]))))
    value += weight_same_match * data_connector.match_count(players[0:4])
    value += weight_same_team * (data_connector.team_count(players[0:2]) + data_connector.team_count(players[2:4]))

    return value


def switch(players):
    i = random.randrange(0, len(players))
    j = i
    while i == j:
        j = random.randrange(0, len(players))
    players[i], players[j] = players[j], players[i]
    return players
