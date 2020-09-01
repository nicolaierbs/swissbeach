import random


def random_match_players(players):
    selected_players = random.sample(players, 4)
    return selected_players


def next_round(players):
    matches = random_round(players)


def score(players):


def switch(players):
    i = random.randrange(0, len(players))
    j = i
    while i==j:
        j = random.randrange(0, len(players))
    players[i], players[j] = players[j], players[i]
    return players


def random_round(players):
    matches = list()

    # Stupid matcher by random selection
    while len(players) >= 4:
        match_players = random_match_players(players)
        match = (match_players[0:2], match_players[2:4])
        matches.append(match)
        for player in match_players:
            players.remove(player)

    return matches
