from flask import url_for, request, render_template, session,\
redirect
from . import user
from .models import *


@user.route('/')
def index():
    # 获取session
    username = session.get('username', '游客')

    return f'hello {username} session'


@user.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # 设置session
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        # 设置session过期时间
        session.permanent = True  # 只有设置了True才能让app.permaent_session_lifetime生效
        # 加了蓝图后，url_for里面不是只传视图函数名，还得在前面带上蓝图名点上视图函数名
        return redirect(url_for('user.index'))  


@user.route('/delete_session')
def delete_session():
    # 删除session
    session.pop('username', None)  # 删除session中某一个键值对

    # 清空所有session
    session.clear()  # 把整个session全部删了，连客户端的cookie中的session id都没有了
    return redirect(url_for('user.index'))
    