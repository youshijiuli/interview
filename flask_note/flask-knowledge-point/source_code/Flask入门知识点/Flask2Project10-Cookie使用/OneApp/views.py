from flask import Blueprint, render_template, request, redirect
from .models import *
import datetime


blue = Blueprint('blue', __name__)


# 首页
@blue.route('/')
@blue.route('/home/')  # 可以将两个路由都绑在一个视图函数上
def index():
    # 4. 获取cookie
    username = request.cookies.get('user')
    return render_template('index.html', username=username)


# 登录
@blue.route('/login/', methods=['get', 'post'])  # 可以小写，为了统一以后都大写
def login():
    # GET请求，访问登录界面
    if request.method == 'GET':  # 必须大写

        return render_template('login.html')

    # POST请求，实现登录功能
    if request.method == 'POST':  # 必须大写
        # 1. 获取前端提交过来的数据
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        # 2. 模拟登录，用户名和密码验证
        if username == 'xiaodai' and password == '000':
            # 登录成功
            response = redirect('/home/')
            # 设置cookie
            # cookie不能用中文
            # set_cookie方法主要有四个参数：key、value、max_age、expires
            response.set_cookie('user', username)  # 如果不设置的话会，cookie默认在退出浏览器后失效
            response.set_cookie('user', username, max_age=3600)  # 单位是秒
            response.set_cookie('user', username, expires=datetime.datetime(2024, 7, 1))  # 单位是秒

            return response
 
        else:
            return '用户密码错误！'
    else:
        return render_template('login.html')


# 注销
@blue.route('/logout/')
def logout():

    response = redirect('/home/')

    # 5. 删除cookie
    response.delete_cookie('user')

    return response


