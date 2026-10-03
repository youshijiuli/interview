from flask import Flask
from .views import blue
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


def create_app():

    # 配置静态文件和模版文件目录到项目路径下
    # static_folder = '../static'
    # template_folder = '../templates'

    static_folder = os.path.join(BASE_DIR, 'static')
    template_folder = os.path.join(BASE_DIR, 'templates')


    app = Flask(
        __name__,
        static_folder=static_folder,
        template_folder=template_folder
    )
    app.register_blueprint(blueprint=blue)

    return app

