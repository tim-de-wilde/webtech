from src.models import Actor
from src import db


class ActorApi:
    @staticmethod
    def index():
        return Actor.query.all()

    @staticmethod
    def index_one(actor_id):
        return Actor.query.filter_by(id=actor_id).first()

    @staticmethod
    def create(form):
        actor = Actor(
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )

        db.session.add(actor)
        db.session.commit()

    @staticmethod
    def update(actor_id, form):
        Actor.query \
            .filter_by(id=actor_id) \
            .update(first_name=form.first_name.data, last_name=form.last_name.data)

        db.session.commit()

    @staticmethod
    def delete(actor_id):
        actor = ActorApi.index_one(actor_id)

        if actor is not None:
            db.session.delete(actor)
            db.session.commit()
