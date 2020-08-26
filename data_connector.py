import pymongo
import configparser
from datetime import datetime as dt


db_section = 'DB'
params = configparser.ConfigParser()
params.read('parameters.ini')

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client[params.get(db_section, 'database')]
players_collection = db['players']
matches_collection = db['matches']


def new_player(name):
    players_collection.insert_one({'name': name, 'inserted': dt.now(), 'active': True})


def active_players():
    # TODO filter those players who're currently playing
    return list(players_collection.find({'active': True}, {}))


def clear():
    players_collection.drop()
    matches_collection.drop()


def new_match(team_a, team_b):
    matches_collection.insert_one({'team_a': team_a, 'team_b': team_b, 'inserted': dt.now(), 'active': True})


def match_result(object_id, points_a, points_b):
    matches_collection.update_one(
        {'_id': object_id},
        {'$set': {'result': {'team_a': points_a, 'team_b': points_b}, 'active': False}})


def active_matches():
    return list(matches_collection.find({'active': True}))


def compute_statistics(results):
    statistics = dict()
    statistics['count'] = len(results)
    won_games = 0
    lost_games = 0
    won_points = 0
    lost_points = 0
    for result in results:
        won_points += result[0]
        lost_points += result[1]
        if result[0] > result[1]:
            won_games += 1
        else:
            lost_games += 1
    statistics['won_games'] = won_games
    statistics['lost_games'] = lost_games
    statistics['won_points'] = won_points
    statistics['lost_points'] = lost_points
    if len(results) > 0:
        statistics['point_ratio'] = won_points/(lost_points+won_points)
        statistics['match_ratio'] = won_games/(lost_games+won_games)
    return statistics


def update_statistics():
    players = players_collection.find({}, {})
    for player in players:
        # collect all match results
        results = list()
        for result in matches_collection.find(
            {'active': False, 'team_a': player},
            {'result.team_a': 1, 'result.team_b': 1}):
            results.append((result['result']['team_a'], result['result']['team_b']))
        for result in matches_collection.find(
            {'active': False, 'team_b': player},
            {'result.team_a': 1, 'result.team_b': 1}):
            results.append((result['result']['team_b'], result['result']['team_a']))

        statistics = compute_statistics(results)

        players_collection.update_one(
            {'_id': player},
            {'$set': {'statistics': statistics}})

        print(statistics)
