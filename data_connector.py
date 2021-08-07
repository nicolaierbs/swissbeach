import pymongo
from datetime import datetime as dt
import os


client = pymongo.MongoClient()
db = client.test


# Get environment variables
password = os.getenv('SWISSBEACH_DB_PASSWORD')
database = 'vcor'

connection_string = \
    "mongodb+srv://swissbeach_admin:{}@cluster0.5ozes.mongodb.net/{}?retryWrites=true&w=majority".format(
        password, database)

client = pymongo.MongoClient(connection_string)
db = client[database]

players_collection = db['players']
matches_collection = db['matches']


def new_player(player_name):
    statistics = dict()
    last_player_id=1
    players_collection.insert_one({'name': player_name,
                                   'inserted': dt.now(),
                                   'active': True,
                                   'statistics': statistics,
                                   'markers': {
                                       'child': False,
                                       'female': False,
                                       'male': False
                                   }})


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
    return list(players_collection.find(sort=[("statistics.percentage", -1)]))


def clear():
    players_collection.drop()
    matches_collection.drop()


def new_match(players):
    matches_collection.insert_one(
        {'team_a': players[0:2], 'team_b': players[2:4], 'inserted': dt.now(), 'active': True})


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
    matches_player_names = list()
    for match in matches:
        match['team_a_names'] = player_names(match['team_a'])
        match['team_b_names'] = player_names(match['team_b'])
        match['inserted'] = match['inserted'].strftime("%H:%M")
        matches_player_names.append(match)
    return matches_player_names


def delete_match(match_id):
    matches_collection.delete_one({'_id': match_id})


def toggle_player(player_id):
    active = players_collection.find_one({'_id': player_id})['active']
    players_collection.update_one({'_id': player_id}, {'$set': {'active': not active}})


def change_marker(player_id, marker):
    state = players_collection.find_one({'_id': player_id})['markers'][marker]
    players_collection.update_one({'_id': player_id}, {'$set': {'markers.' + marker: not state}})


def team_count(players):
    return matches_collection.count_documents(
        {'$or': [
            {'$and': [{'team_a': players[0]['_id']}, {'team_a': players[1]['_id']}]},
            {'$and': [{'team_b': players[0]['_id']}, {'team_b': players[1]['_id']}]},
        ]
        }
    )


def match_count(players):
    return matches_collection.count_documents(
        {'$or': [
            {'$and': [
                {'team_a': players[0]['_id']}, {'team_a': players[1]['_id']},
                {'team_b': players[2]['_id']}, {'team_b': players[3]['_id']}
            ]},
            {'$and': [
                {'team_b': players[0]['_id']}, {'team_b': players[1]['_id']},
                {'team_a': players[2]['_id']}, {'team_a': players[3]['_id']},
            ]},
        ]
        }
    )


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
