import data_connector
import matcher
import pprint
import random


pp = pprint.PrettyPrinter(indent=4)

data_connector.clear()

data_connector.new_player('Nicolai')
data_connector.new_player('Ari')
data_connector.new_player('Sven')
data_connector.new_player('Carsten')
data_connector.new_player('Mark')
data_connector.new_player('Valle')
data_connector.new_player('Stefan')
data_connector.new_player('Mario')
data_connector.new_player('Flo')

players = data_connector.active_players()
print('Players')
pp.pprint(players)

next_matches = matcher.next_round(players)
print('Matches')
pp.pprint(next_matches)
for match in next_matches:
    data_connector.new_match(match[0], match[1])


# Get current matches and add some random results
active_matches = data_connector.active_matches()
for match in active_matches:
    data_connector.match_result(match['_id'], 21, random.randint(5, 19))

data_connector.update_statistics()
