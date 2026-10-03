from flask import Blueprint
from .models import *


# 创建蓝图
user_blue = Blueprint('user_blue', __name__)


# 视图函数
@user_blue.route('/')
def index():

    return 'hello flask!'


# 路由通过装饰器对应视图函数，并且可以接受参数，
# 所以我们只需要在视图函数上使用装饰器即可
@user_blue.route('/string/<string:username>/')
def get_string(username):
    # 路由参数可以是 string 类型，这是默认类型
    print(type(username))
    return f'路由参数默认传递string类型:{username}'


@user_blue.route('/int/<int:age>/')
def get_int(age):
    # 路由参数可以直接传入int类型
    print(type(age))
    return f'路由参数可以传入int类型：{age}'


@user_blue.route('/float/<float:money>/')
def get_float(money):
    # 路由参数可以传入float类型，而且不能是int类型，要带小数点
    print(type(money))
    return f'路由参数可以传入float类型：{money}'


@user_blue.route('/path/<path:url>/')
def get_path(url):
    # 路由参数可以传入路径字符串，这种字符串可以带"/"
    print(type(url))
    return f'路由参数可以传入路径字符串:{url}'


@user_blue.route('/uuid/<uuid:getuuid>/')
def get_uuid(getuuid):
    # eb11ec05-70bb-41a4-9cba-41cfe7ef5ae2
    print(type(getuuid))
    return f'路由参数可以传入UUID:{getuuid}'


@user_blue.route('/any/<any(apple, orange, banana):fruit>/')
def get_any(fruit):
    # 只能在路径中输入any里面的
    print(type(fruit))
    return f'从any列出的项目中选择一个：{fruit}'
    