from src.models import Film
from src import db


class FilmApi:
    @staticmethod
    def index():
        return Film.query.all()