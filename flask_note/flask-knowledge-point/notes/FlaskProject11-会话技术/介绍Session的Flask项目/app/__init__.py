from flask import Flask
from .user import user as user_bp
import datetime


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('../config.py')

    # 设置 session 的有效期为 7 天
    app.permaent_session_lifetime = datetime.timedelta(days=7)

    app.register_blueprint(user_bp)


    return app

