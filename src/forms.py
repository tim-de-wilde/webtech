from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from src.models import User
from src import app


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Wachtwoord bevestigen', validators=[DataRequired(), EqualTo('password', message='Wachtwoorden komen niet overeen.')])