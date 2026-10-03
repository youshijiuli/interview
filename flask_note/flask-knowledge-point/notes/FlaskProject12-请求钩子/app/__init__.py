from flask import Flask
from .main import main as main_bp


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('../config.py')

    app.register_blueprint(main_bp)

    return app
