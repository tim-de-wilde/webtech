from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from src.models import User
from src import app
from src.api.RoleApi import RoleApi


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Wachtwoord bevestigen', validators=[DataRequired(), EqualTo('password', message='Wachtwoorden komen niet overeen.')])


class ActorForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])


class DirectorForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])


class RoleForm(FlaskForm):
    character_name = StringField('Character name', validators=[DataRequired()])
    actor_id = StringField('Actor id', validators=[DataRequired()])
    film_id = StringField('Film id', validators=[DataRequired()])


class FilmForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = StringField('Title', validators=[DataRequired()])
    director_id = StringField('Title', validators=[DataRequired()])


class CommentForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired()])


class DeleteForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
