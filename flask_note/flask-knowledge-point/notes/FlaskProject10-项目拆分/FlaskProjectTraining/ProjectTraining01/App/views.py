# views.py：里面存放蓝图的路由和视图
from flask import Blueprint
from .models import *
from .exts import *


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
def index():

    return 'user blueprint hello'
