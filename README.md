# Swiss Beach Tournament
This web app is the extension of a [swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament) for beach-volleyball.
Usually, the swiss-system is applied in chess or other sports when the number of players can be large.
This implementation of the swiss-system is developed for beach-volleyball tournaments where a team consists of two players and teams are mixed after each match.
This allows for having 'open' tournaments with no limit of rounds and how many people one meets.

## How does a swiss-system beach-volleyball tournament work?
All active players of the tournament are registered. It will still be possible to join later, leave the tournament earlier or just have a break.
The tournament consists of a sequenced list of matches which are computed based on the previous matches and results.
For the first round, the first four players are randomly selected as there is no combination with a better score.
All the other rounds are selected using the following steps automatically:
1. Select all players who are not playing and are considered as active.
2. Select the players with the least number of matches (at least four)
3. Create a random match with four of those players
4. Compute the score of this match based on factors like the level of the players in a team and the balance of the match.
5. Switch a pair of players (from both teams or the bench)
6. Compute the score of the changed match and keep it if the score is lower (better)
7. Iteratively optimize the next match for a predefined number of times (go back to step 5)
8. Register the best match as the next match and wait for the next match

The role of tournament organization is to keep track of whether the players are active and start the match generation process when a court is ready.
When a match is registered the players in the current match are not free to play in another match but as soon as the result for their match is entered, they can be selected to play in the next match.
Players joining later are likely to play several rounds after each other and it is avoided that the same two players are in a team repeatedly.

## Advantages and disadvantages of this system
This system is suitable for tournaments in a colloquial atmosphere with players open to play with anyone else.

It has the following advantages:
* No fixed deadline for registration: Players can join later and leave earlier as matches are generated based only on available players
* The balance of teams and matches increases over time: Stronger (in terms of won games) players are more likely to play with other strong players as their match has a better score
* No need to wait for opponent: If there are four players available, there will always be a suggested match and no need to wait for results of other matches
* Meet everyone: The score of a proposed match is better if the teams have not played before as team which leads to everyone playing with almost everyone
* No predefined end: The players or the organizer can decide when to stop the tournament as there is always a high score with a winner

The system will most likely not work if the team need a long preparation before being able to play (warm up).
It is also not recommended to use with more than 50 players and few rounds because it will essentially be the same as a random selection of matches.

## Installation
To run it locally, you need to have Python and a MongoDB installed.