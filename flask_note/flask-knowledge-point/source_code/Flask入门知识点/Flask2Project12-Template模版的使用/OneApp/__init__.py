from flask import Flask
from .views import blue
import datetime


def create_app():

    app = Flask(__name__)


    app.config['SECRET_KEY'] = 'xiaodai'

    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)

    app.register_blueprint(blueprint=blue)

    return app
