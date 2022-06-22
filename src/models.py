from flask_login import UserMixin
from src import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id} : {self.username} heeft het emailadres: {self.email}."


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    films = db.relationship(
        'Film', back_populates='actor', cascade='all, delete-orphan'
    )

    roles = db.relationship(
        'Role', back_populates='actor', cascade='all, delete-orphan'
    )

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    films = db.relationship(
        'Film', back_populates='director', cascade='all, delete-orphan'
    )

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)

    actors = db.relationship(
        'Actor', back_populates='film'
    )

    roles = db.relationship(
        'Role', back_populates='film'
    )

    def __init__(self, title, year, director_id):
        self.title = title
        self.year = year
        self.director_id = director_id


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(64), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)

    actor = db.relationship(
        'Actor', back_populates='role'
    )

    director = db.relationship(
        'Director', back_populates='role'
    )

    def __init__(self, character_name, actor_id, director_id):
        self.character_name = character_name
        self.actor_id = actor_id
        self.director_id = director_id


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=False)

    user = db.relationship(
        'User', back_populates='comment'
    )

    film = db.relationship(
        'Film', back_populates='comment'
    )

    def __init__(self, body, user_id, film_id):
        self.body = body
        self.user_id = user_id
        self.film_id = film_id
