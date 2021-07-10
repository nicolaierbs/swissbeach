from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from bson import ObjectId

import data_connector, matcher

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')

# data_connector.clear()


@app.route('/register', methods=['POST'])
def registration():
    data_connector.new_player(request.form.get('name'))
    return redirect(url_for('show_players'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('welcome.html')


@app.route('/players')
def show_players():
    players = data_connector.all_players()
    return render_template('players.html', players=players)


@app.route('/matches')
def show_matches():
    matches = data_connector.matches_with_names()
    return render_template('matches.html', matches=matches)


@app.route('/deletematch/<string:match_id>')
def delete_match(match_id):
    data_connector.delete_match(ObjectId(match_id))
    matches = data_connector.matches_with_names()
    return redirect(url_for('show_matches'))


@app.route('/config')
def show_config():
    config = matcher.tournament_config()
    return render_template('config.html', config=config)


@app.route('/cleardata')
def clear_data():
    data_connector.clear()
    return show_players()


@app.route('/playertoggle/<string:player_id>')
def toggle_player(player_id):
    data_connector.toggle_player(ObjectId(player_id))
    return redirect(url_for('show_players'))


@app.route('/result/<string:match_id>/<string:winner>')
def result(match_id, winner):
    if winner == 'a':
        data_connector.match_result(ObjectId(match_id), True, False)
    else:
        data_connector.match_result(ObjectId(match_id), False, True)
    # show the post with the given id, the id is an integer
    return redirect(url_for('show_matches'))


@app.route('/nextgame')
def next_game():
    next_match = matcher.next_match(data_connector.free_players())
    if next_match:
        data_connector.new_match(next_match)
    return redirect(url_for('show_matches'))


if __name__ == '__main__':
    app.run()
