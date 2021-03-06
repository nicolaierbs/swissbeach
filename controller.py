import data_connector
import matcher
import pprint
import random


pp = pprint.PrettyPrinter(indent=4)

data_connector.clear()

data_connector.new_player('A')
data_connector.new_player('B')
data_connector.new_player('C')
data_connector.new_player('D')


def one_round():
    next_match = matcher.next_match(data_connector.free_players())
    data_connector.new_match(next_match)

    # Get current matches and add some random results
    active_matches = data_connector.active_matches()
    for match in active_matches:
        winner = random.choice([True, False])
        data_connector.match_result(match['_id'], winner, not winner)
        if random.randint(0, 2) % 2:
            break


for i in range(20):
    one_round()

match_list = sorted([str(sorted([sorted(match['team_a_names']), sorted(match['team_b_names'])]))
                     for match in data_connector.matches_with_names()])
for match in match_list:
    print(match)
print(len(list(set(match_list)))/len(match_list))
