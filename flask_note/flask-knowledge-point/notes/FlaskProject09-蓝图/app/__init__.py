from flask import Flask
from .main import main as main_bp
from .exts import init_exts

def create_app():

    app = Flask(__name__)

    app.register_blueprint(main_bp)

    app.config.from_pyfile('../config.py')

    init_exts(app)

    return app
