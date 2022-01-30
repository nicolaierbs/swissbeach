from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from bson import ObjectId

import data_connector, matcher

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')

# data_connector.clear()


@app.route('/<string:database>/register', methods=['POST'])
def registration(database):
    data_connector.new_player(request.form.get('name'), database)
    return redirect(url_for('show_players', database=database))


@app.route('/')
@app.route('/home')
@app.route('/<string:database>/home')
def home(database = None):
    return render_template('welcome.html', database=database)


@app.route('/<string:database>/players')
def show_players(database):
    players = data_connector.all_players(database)
    return render_template('players.html', database=database, players=players)


@app.route('/<string:database>/markertoggle/<string:player_id>/<string:marker>')
def change_marker(database, player_id, marker):
    data_connector.change_marker(ObjectId(player_id), marker, database)
    return redirect(url_for('show_players', database=database))


@app.route('/<string:database>/matches')
def show_matches(database):
    matches = data_connector.matches_with_names(database)
    return render_template('matches.html', database=database, matches=matches)


@app.route('/<string:database>/deletematch/<string:match_id>')
def delete_match(database, match_id):
    data_connector.delete_match(ObjectId(match_id), database)
    matches = data_connector.matches_with_names(database)
    return redirect(url_for('show_matches', database=database))


@app.route('/<string:database>/config')
def show_config(database):
    config = matcher.tournament_config(database)
    return render_template('config.html', database=database, config=config)


@app.route('/datausage')
@app.route('/<string:database>/datausage')
def show_datausage(database=None):
    return render_template('datausage.html', database=database)


@app.route('/contact')
@app.route('/<string:database>/contact')
def show_contact(database=None):
    return render_template('contact.html', database=database)


@app.route('/<string:database>/cleardata')
def clear_data(database):
    data_connector.clear(database)
    return show_players(database)


@app.route('/<string:database>/playertoggle/<string:player_id>')
def toggle_player(database, player_id):
    data_connector.toggle_player(ObjectId(player_id), database)
    return redirect(url_for('show_players'), database=database)


@app.route('/<string:database>/result/<string:match_id>/<string:winner>')
def result(database, match_id, winner):
    if winner == 'a':
        data_connector.match_result(ObjectId(match_id), True, False, database)
    else:
        data_connector.match_result(ObjectId(match_id), False, True, database)
    # show the post with the given id, the id is an integer
    return redirect(url_for('show_matches', database=database))


@app.route('/<string:database>/nextgame')
def next_game(database):
    next_match = matcher.next_match(data_connector.free_players(database), database)
    if next_match:
        data_connector.new_match(next_match, database)
    return redirect(url_for('show_matches', database=database))


if __name__ == '__main__':
    app.run()
