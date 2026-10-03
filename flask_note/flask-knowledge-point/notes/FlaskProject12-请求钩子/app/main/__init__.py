from flask import Blueprint


main = Blueprint(
    'main',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/main'
)


# 一定要在__init__.py中导入views视图
from .views import *
