# 导入Flask相关模块
from flask import Blueprint, render_template, request, redirect, session, url_for
# 导入自定义的模型类
from .models import *

# 创建一个蓝图对象，用于定义路由
blue = Blueprint('blue', __name__)

# 定义根路由的处理函数
@blue.route('/')
def index():
    """
    模版处理分两个过程
    1. 加载HTML
    2. 模版渲染（模版语言）

    模版代码也同样包含两个部分
    1. 静态HTML
    2. 动态插入的代码段（模版语法）
    """
    # 从session中获取用户名
    username = session.get('user')
    # 定义一个列表，用于存储模版中的循环变量
    items = [
        'loop.first 判断是否是第一个元素',
        'loop.last 判断是否是最后一个元素',
        'loop.index 从1开始的下标',
        'loop.index0 从0开始的下标',
        'loop.revindex 反向下标，不包括0',
        'loop.revindex0 反向下标，包括0',
    ]

    # 定义一个字典，用于存储模版中的变量
    context = {
        'username': username,
        'items': items
    }
    # 渲染模版并返回结果
    return render_template('index.html', **context)

# 定义登录路由的处理函数
@blue.route('/login/', methods=['GET', 'POST'])
def login():

    # 如果是GET请求，渲染登录页面
    if request.method == 'GET':
        """
        模版中的变量 {{ var }}
        模版中的标签 {% tag %}
        """
        return render_template('login.html')

    # 如果是POST请求，处理登录逻辑
    if request.method == 'POST':
        
        # 从表单中获取用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')

        # 如果用户名和密码正确，将用户名存入session并重定向到首页
        if username == 'xiaodai' and password == '123':
            session['user'] = username
            return redirect('/')

        # 如果用户名或密码错误，返回错误信息
        else:
            return '账号密码错误！'

    # 如果请求方法不是GET或POST，返回非法请求信息
    return '非法请求！'

# 定义登出路由的处理函数
@blue.route('/logout/')
def logout():

    # 获取首页的URL
    ret_url = url_for('blue.index')

    # 从session中移除用户名
    session.pop('user')

    # 重定向到首页
    return redirect(ret_url)


# 定义一个路由，当访问'/show_base/'时，执行下面的函数
@blue.route('/show_base/')
def show_base():
    # 渲染并返回'base.html'模板
    return render_template('base.html')

# 定义一个路由，当访问'/show_child/'时，执行下面的函数
@blue.route('/show_child/')
def show_child():
    # 渲染并返回'child.html'模板
    return render_template('child.html')
