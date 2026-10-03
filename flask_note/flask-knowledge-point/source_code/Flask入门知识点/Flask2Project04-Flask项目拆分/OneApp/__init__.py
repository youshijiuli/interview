# 导入flask包
from flask import Flask
from .views import user_blue


def create_app():
    app = Flask(__name__)

    # 注册蓝图（其实就挂载app）
    app.register_blueprint(blueprint=user_blue)

    return app
