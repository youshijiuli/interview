from flask import Flask
from .views import myblue


def create_app():

   app = Flask(__name__)
   app.register_blueprint(blueprint=myblue)

   return app
