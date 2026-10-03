from flask import Blueprint
from .models import *


# 使用蓝图来创建应用
# 第一个参数：应用的名字
# 第二个参数是项目主路径
user_blue = Blueprint('user', __name__)  


# views.py: 路由 + 视图函数
@user_blue.route('/')
def index():

    return '使用蓝图创建app'
