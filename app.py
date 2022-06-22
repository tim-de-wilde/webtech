from src import app, db
from src.routes import web
from src.models import *


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
