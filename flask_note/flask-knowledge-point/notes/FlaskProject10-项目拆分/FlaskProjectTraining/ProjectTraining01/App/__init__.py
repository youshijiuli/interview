# __init__.py：初始化蓝图
from flask import Flask
from .views import user
from .exts import init_exts


def create_app():

    app = Flask(__name__)

    app.register_blueprint(user)


    DB_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        USERNAME,
        PASSWORD,
        HOSTNAME,
        PORT,
        DATABASE
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_exts(app)

    return app
