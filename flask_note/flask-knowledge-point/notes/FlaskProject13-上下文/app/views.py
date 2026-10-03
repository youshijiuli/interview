from flask import Blueprint
from flask import make_response, redirect, g, request, abort, render_template, url_for



user = Blueprint('user', __name__, static_folder='static', template_folder='template')


@user.route('/')
def index():

    return f"欢迎{g.user_id}来到首页！"


@user.before_app_request
def authentication():
    """ 利用before_request请求钩子，在进入所有视图前先尝试判断用户身份 """
    g.user_id = request.cookies.get('user_id', None)


def login_required(func):
    """ 自定义一个装饰器来认证用户 """
    def wrapper(*args, **kwargs):

        if g.user_id:
            # 如果用户已登录（即g.user_id存在），则允许访问被装饰的视图函数
            return func(*args, **kwargs)
        else:
            # 否则返回401未授权错误
            return abort(401)
    return wrapper



@user.route('/profile')
@login_required
def get_user_profile():

    return  "当前登录用户为：{}".format(g.user_id)


@user.route('/login', methods=['GET', 'POST'])
def login():

    if request.method=='GET':

        return render_template('login.html')

    elif request.method=='POST':
        user_id = request.form.get('user_id')

        html = redirect(url_for('user.index'))
        if user_id:
            response = make_response(html)
            response.set_cookie('user_id', user_id)
            return response
        else:
            return html
    else:
        return render_template('login.html')
        