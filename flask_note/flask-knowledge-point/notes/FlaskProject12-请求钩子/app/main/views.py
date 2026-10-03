from . import main
from flask import render_template
from flask import current_app



@main.route('/')
def index():
    # 1/0
    return render_template('index.html')


"""
@app.before_first_request
def before_first_request():
    # 只会在第一次请求的时候执行，后续请求就不会执行了
    print('before_app_first_request')
"""

@main.before_app_request
def before_app_request():
    # 在每次请求之前都会执行
    print('before_app_request')
    # 如果提前返回响应了，那么视图函数就无法进入了
    # return render_template('404.html')


@main.before_request
def before_request():
    # 在每次请求之前都会执行
    print('before_request')
    # 如果提前返回响应了，那么视图函数就无法进入了
    # return render_template('404.html')


@main.after_request
def after_request(response):
    # 每次请求结束，返回响应的时候执行
    print('after_request')
    # 当视图函数抛出异常后，这个钩子函数就不会被执行了
    # 必须要有返回值，返回值必须是传入的response
    return response


@main.teardown_request
def teardown_request(exception=None):
    # 无论视图函数是否出错，都会执行这个钩子函数
    # 它可以捕获异常
    print('捕获异常:', exception)



@main.context_processor
def context_processor():

    return {'global_variable': 'Global Value'}
