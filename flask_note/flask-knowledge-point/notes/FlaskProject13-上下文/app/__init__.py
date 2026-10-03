from flask import Flask
from .views import user as user_bp


def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'XIAODAI'

    app.register_blueprint(user_bp)

    return app

