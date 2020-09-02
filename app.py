from flask import Flask, render_template, request, redirect, url_for
from forms import RegistrationForm
from flask_bootstrap import Bootstrap

import data_connector, matcher

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        data_connector.new_player(request.form.get('name'))
        players = data_connector.all_players()
        return redirect(url_for('show_players'))
    return render_template('registration.html', form=form)


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
def show_match(match_id):
    # show the post with the given id, the id is an integer
    return 'Match %d' % match_id


@app.route('/nextgame')
def next_game():
    next_match = matcher.next_match(data_connector.free_players())
    if next_match:
        data_connector.new_match(next_match)
    return redirect(url_for('show_matches'))


if __name__ == '__main__':
    app.run()
