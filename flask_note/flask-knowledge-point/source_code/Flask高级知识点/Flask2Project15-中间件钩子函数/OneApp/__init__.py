from flask import Flask
from .views import blue
from .exts import init_exts


def create_app():

    app = Flask(__name__)
    app.register_blueprint(blueprint=blue)
    init_exts(app)

    return app
