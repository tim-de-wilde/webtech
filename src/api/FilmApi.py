from src.models import Film, Comment
from src import db
from src.api.RoleApi import RoleApi


class FilmApi:
    @staticmethod
    def index():
        return Film.query.all()

    @staticmethod
    def index_one(film_id):
        return Film.query.filter_by(id=film_id).first()

    @staticmethod
    def create(form):
        film = Film(
            title=form.title.data,
            year=form.year.data,
            director_id=form.director_id.data
        )

        db.session.add(film)
        db.session.commit()

    @staticmethod
    def create_comment(film_id, user_id, form):
        comment = Comment(
            form.body.data,
            user_id,
            film_id
        )

        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def update(film_id, form):
        film = FilmApi.index_one(film_id)

        film.title = form.title.data
        film.year = form.year.data
        film.director_id = form.director_id.data

        db.session.commit()

    @staticmethod
    def delete(film_id):
        film = FilmApi.index_one(film_id)

        if film is not None:
            # Delete roles associated with film
            for role in film.roles:
                db.session.delete(role)

            db.session.delete(film)
            db.session.commit()
