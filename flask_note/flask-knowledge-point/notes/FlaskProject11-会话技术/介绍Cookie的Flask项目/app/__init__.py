from flask import Flask
from .views import user as user_bp


def create_app():


    app = Flask(__name__)

    app.config.from_pyfile('../config.py')

    app.register_blueprint(user_bp)

    return app

