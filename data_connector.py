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

match_id = 0


def new_player(name):
    players_collection.insert_one({'name': name, 'inserted': dt.now(), 'active': True})


def free_players():
    players = list()
    for player in players_collection.find({'active': True}, {}):
        if not len(list(matches_collection.aggregate([
            {'$match': {'$and': [{'active': True}, {'$or': [
                {'team_a': player['_id']}, {'team_b': player['_id']}
            ]}]}}
        ]))):
            players.append(player['_id'])


    return players


def players():
    return list(players_collection.find())


def clear():
    players_collection.drop()
    matches_collection.drop()


def new_match(team_a, team_b):
    global match_id
    matches_collection.insert_one(
        {'id': match_id, 'team_a': team_a, 'team_b': team_b, 'inserted': dt.now(), 'active': True})
    match_id += 1


def match_result(object_id, points_a, points_b):
    matches_collection.update_one(
        {'_id': object_id},
        {'$set': {'result': {'team_a': points_a, 'team_b': points_b}, 'active': False}})


def active_matches():
    return list(matches_collection.find({'active': True}))


def player_name(object_id):
    return players_collection.find_one({'_id': object_id}, {'name': 1})['name']


def player_names(object_ids):
    player_names = list()
    for object_id in object_ids:
        player_names.append(player_name(object_id))
    return player_names


def matches_with_names():
    matches = list(matches_collection.find())
    matches_with_names = list()
    for match in matches:
        match['team_a_names'] = player_names(match['team_a'])
        match['team_b_names'] = player_names(match['team_b'])
        match['inserted'] = match['inserted'].strftime("%H:%M")
        matches_with_names.append(match)
    return matches_with_names


def compute_statistics(results):
    statistics = dict()
    statistics['count'] = len(results)
    won_matches = 0
    lost_matches = 0
    won_points = 0
    lost_points = 0
    for result in results:
        won_points += result[0]
        lost_points += result[1]
        if result[0] > result[1]:
            won_matches += 1
        else:
            lost_matches += 1
    statistics['matches'] = won_matches + lost_matches
    statistics['won_matches'] = won_matches
    statistics['lost_matches'] = lost_matches
    statistics['won_points'] = won_points
    statistics['lost_points'] = lost_points
    if len(results) > 0:
        statistics['point_ratio'] = won_points / (lost_points + won_points)
        statistics['match_ratio'] = won_matches / (lost_matches + won_matches)
    return statistics


def update_statistics():
    for player in players_collection.find({}, {}):
        # collect all match results
        results = list()
        for result in matches_collection.find(
                {'active': False, 'team_a': player['_id']},
                {'result.team_a': 1, 'result.team_b': 1}):
            results.append((result['result']['team_a'], result['result']['team_b']))
        for result in matches_collection.find(
                {'active': False, 'team_b': player['_id']},
                {'result.team_a': 1, 'result.team_b': 1}):
            results.append((result['result']['team_b'], result['result']['team_a']))

        statistics = compute_statistics(results)

        players_collection.update_one(
            player,
            {'$set': {'statistics': statistics}})

        print(statistics)
