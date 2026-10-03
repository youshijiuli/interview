from flask import Blueprint


user = Blueprint(
    'user',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/user'
)


from .views import *

