import pymongo
import configparser
from datetime import datetime as dt

config_section = 'DB'
params = configparser.ConfigParser()
params.read('parameters.ini')

client = pymongo.MongoClient(params.get(config_section, 'connection_string'))
db = client[params.get(config_section, 'database')]

players_collection = db['players']
matches_collection = db['matches']

match_id = 0


def new_player(name):
    statistics = dict()
    players_collection.insert_one({'name': name, 'inserted': dt.now(), 'active': True, 'statistics': statistics})


def free_players():
    players = list()
    for player in players_collection.find({'active': True}):
        if not len(list(matches_collection.aggregate([
            {'$match': {'$and': [{'active': True}, {'$or': [
                {'team_a': player['_id']}, {'team_b': player['_id']}
            ]}]}}
        ]))):
            players.append(player)
    return players


def all_players():
    return list(players_collection.find())


def clear():
    players_collection.drop()
    matches_collection.drop()


def new_match(players):
    global match_id
    matches_collection.insert_one(
        {'id': match_id, 'team_a': players[0:2], 'team_b': players[2:4], 'inserted': dt.now(), 'active': True})
    match_id += 1


def match_result(object_id, team_a_won, team_b_won):
    matches_collection.update_one(
        {'_id': object_id},
        {'$set': {'result': {'team_a_won': team_a_won, 'team_b_won': team_b_won}, 'active': False}})
    update_statistics()


def active_matches():
    return list(matches_collection.find({'active': True}))


def name(object_id):
    return players_collection.find_one({'_id': object_id}, {'name': 1})['name']


def player_names(object_ids):
    names = list()
    for object_id in object_ids:
        names.append(name(object_id))
    return names


def matches_with_names():
    matches = list(matches_collection.find())
    matches_with_names = list()
    for match in matches:
        match['team_a_names'] = player_names(match['team_a'])
        match['team_b_names'] = player_names(match['team_b'])
        match['inserted'] = match['inserted'].strftime("%H:%M")
        matches_with_names.append(match)
    return matches_with_names


def update_statistics():
    for player in players_collection.find({}, {}):
        # collect all match results
        results = list()
        won = 0
        lost = 0
        won += matches_collection.count_documents({'active': False, 'team_a': player['_id'], 'result.team_a_won': True})
        won += matches_collection.count_documents({'active': False, 'team_b': player['_id'], 'result.team_b_won': True})
        lost += matches_collection.count_documents({'active': False, 'team_a': player['_id'], 'result.team_a_won': False})
        lost += matches_collection.count_documents({'active': False, 'team_b': player['_id'], 'result.team_b_won': False})

        statistics = dict()
        statistics['matches'] = won + lost
        statistics['won'] = won
        statistics['lost'] = lost
        if won > 0:
            statistics['percentage'] = won / (won + lost)
        else:
            statistics['percentage'] = 0

        players_collection.update_one(
            player,
            {'$set': {'statistics': statistics}})
