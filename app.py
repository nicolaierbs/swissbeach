from flask import Flask, render_template
import data_connector

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/players')
def show_players():
    players = data_connector.all_players()
    return render_template('players.html', players=players)


@app.route('/matches')
def show_matches():
    matches = data_connector.matches_with_names()
    return render_template('matches.html', matches=matches)


@app.route('/match/<int:match_id>')
def show_post(match_id):
    # show the post with the given id, the id is an integer
    return 'Match %d' % match_id


if __name__ == '__main__':
    app.run()
