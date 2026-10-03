from flask import Blueprint, make_response, render_template, request
from .models import *

user = Blueprint('user', __name__, static_folder='static', template_folder='templates', url_prefix='/user')


@user.route('/set_cookie')
def set_cookie():

    # 设置cookie是在响应里面
    html = render_template('index.html')
    response = make_response(html)
    response.set_cookie('user_name', 'wx', max_age=300)  # 设置过期时间
    response.set_cookie('user_id', '1')  # 不能是数值

    return response



@user.route('/get_cookie')
def get_cookie():

    # 获取cookie是在请求中
    print(request.cookies)
    user_name = request.cookies.get('user_name', '游客')
    user_id = request.cookies.get('user_id')

    return render_template('index.html', user_name=user_name, user_id=user_id)


@user.route('/delete_cookie')
def delete_cookie():

    html = render_template('index.html')
    response = make_response(html)
    response.delete_cookie('user_name')  # 直接调用delete_cookie方法可以删掉
    response.set_cookie('user_id', expires=0)  # 也可以设置过期时间为0，表示立马过期，来删除cookie

    return response

