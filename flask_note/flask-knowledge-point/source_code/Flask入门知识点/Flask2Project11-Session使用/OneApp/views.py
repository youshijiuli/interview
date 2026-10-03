# 导入Flask相关模块
from flask import Blueprint, request, render_template, redirect, session
# 导入自定义的模型类
from .models import *

# 创建一个蓝图对象，用于定义路由
blue = Blueprint('blue', __name__)

# 定义根路径和/home/路径的路由，并关联到index函数
@blue.route('/')
@blue.route('/home/')
def index():
    """
    Flask中的session是全局对象（request也是全局对象）
    常用操作：
    - 1. 设置session
        session['key'] = 'value'
        使用的时候要配置加密秘钥'SECRET_KEY'
    - 2. 获取session
        session.get(key, default=None)
    - 3. 删除session
        session.pop(key) 删除某个值
        session.clear()  清除所有值
    """

    # 获取session中的用户名
    username = session.get('user')
    # 渲染模板并传递用户名参数
    return render_template('index.html', username=username)

# 定义/login/路径的路由，支持GET和POST方法，并关联到login函数
@blue.route('/login/', methods=['GET', 'POST'])
def login():

    # 如果是GET请求，渲染登录页面
    if request.method == 'GET':
        return render_template('login.html')

    # 如果是POST请求，处理登录逻辑
    if request.method == 'POST':
        # 获取表单中的用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')
        # 如果用户名和密码正确，则将用户名存入session，并重定向到首页
        if  username == 'xiaodai' and password == '123':
            username = request.form.get('username')
            print('username =', username)

            session['user'] = username
            session.permanent = True

            return redirect('/home/')
        else:
            # 如果用户名或密码错误，返回错误提示
            return '账号密码错误！'

    # 如果请求方法不是GET或POST，返回非法请求提示
    return '非法请求！'

# 定义/logout/路径的路由，并关联到logout函数
@blue.route('/logout/')
def logout():

    # 创建一个重定向到首页的响应对象
    response = redirect('/home/')

    # 从session中删除用户名
    session.pop('user')  # 删除指定1个key
    # session.clear()  # 清除所有服务器里面的session值

    # 返回响应对象
    return response
