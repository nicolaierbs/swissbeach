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


def one_round():
    next_match = matcher.next_match(data_connector.free_players())
    data_connector.new_match(next_match)

    # Get current matches and add some random results
    active_matches = data_connector.active_matches()
    for match in active_matches:
        data_connector.match_result(match['_id'], 21, random.randint(10, 19))
        if random.randint(0, 2) % 2:
            break


for i in range(20):
    one_round()

match_list = sorted([str(sorted([sorted(match['team_a_names']), sorted(match['team_b_names'])])) for match in data_connector.matches_with_names()])
for match in match_list:
    print(match)
print(len(list(set(match_list)))/len(match_list))
