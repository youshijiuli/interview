from flask import Blueprint, redirect, url_for, render_template, request


myblue = Blueprint('myblue', __name__)


@myblue.route('/', methods=['get', 'post'])
def index():

    # 重定向
    # 意思是当一个请求过来的时候，我这个视图函数不做处理，
    # 原封不动的将请求重新定向到另一个视图函数去

    # 重定向的几种方式
    # 1. redirect函数里面传入url
    # return redirect('https://www.qq.com')

    # 2. redirect函数里面传入path
    # return redirect('/make_redirect/')

    # 3. url_for函数功能：反向解析出路径
    # url_for('蓝图名称.视图名称')
    # url_for函数里面还能传参，这里传递的参数是get请求参数，在args中获取
    ret = url_for('myblue.make_redirect', name='xiaopidan')
    print('显示ret:', ret)
    return redirect(ret)


@myblue.route('/make_redirect/')
def make_redirect():

    return render_template('index.html', name=request.args.get('name'))
