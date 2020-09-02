from wtforms import SubmitField, StringField, validators
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    submit = SubmitField('Register')
