# 导入Flask框架的Blueprint模块，用于创建蓝图对象
from flask import Blueprint, request
# 从当前目录下的models模块中导入所有内容
from .models import *


# 创建一个名为user_blue的蓝图对象，并将其关联到当前模块
user_blue = Blueprint('user_blue', __name__)


# 定义一个路由，当访问'/'时，执行下面的index函数
@user_blue.route('/')
def index():
    # 返回字符串'hello flask'
    return 'hello flask'


# /method 必须要有前面的斜杠，可以没有后面的斜杠
@user_blue.route('/method', methods=['GET', 'POST'])
def user_get():

    if request.method == 'GET':
        return '请求方式为GET'

    elif request.method == 'POST':
        return '请求方式为POST'


