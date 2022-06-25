from src.models import Role
from src import db


class RoleApi:
    @staticmethod
    def index():
        return Role.query.all()

    @staticmethod
    def index_one(role_id):
        return Role.query.filter_by(id=role_id).first()

    @staticmethod
    def create(form):
        role = Role(
            character_name=form.character_name.data,
            actor_id=form.actor_id.data,
            film_id=form.film_id.data
        )

        db.session.add(role)
        db.session.commit()

    @staticmethod
    def update(role_id, form):
        role = RoleApi.index_one(role_id)

        role.character_name = form.character_name.data
        role.actor_id = form.actor_id.data
        role.film_id = form.film_id.data

        db.session.commit()

    @staticmethod
    def delete(role_id):
        role = RoleApi.index_one(role_id)

        if role is not None:
            db.session.delete(role)
            db.session.commit()
