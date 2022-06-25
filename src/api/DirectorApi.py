from src.models import Director
from src import db


class DirectorApi:
    @staticmethod
    def index():
        return Director.query.all()

    @staticmethod
    def index_one(director_id):
        return Director.query.filter_by(id=director_id).first()

    @staticmethod
    def create(form):
        director = Director(
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )

        db.session.add(director)
        db.session.commit()

    @staticmethod
    def update(director_id, form):
        director = DirectorApi.index_one(director_id)

        director.first_name = form.first_name.data
        director.last_name = form.last_name.data

        db.session.commit()

    @staticmethod
    def delete(director_id):
        director = DirectorApi.index_one(director_id)

        if director is not None:
            db.session.delete(director)
            db.session.commit()
