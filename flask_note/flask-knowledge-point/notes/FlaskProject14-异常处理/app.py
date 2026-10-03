from flask import Flask, render_template, abort, make_response


app = Flask(__name__)


# 异常捕获
# 自定义一个异常捕获处理函数
@app.errorhandler(500)
def internal_server_error(e):
    response = make_response('服务器压力山大！')
    response.status = '500'
    return response


@app.errorhandler(ZeroDivisionError)
def internal_server_error(e):
    response = make_response('除数不能为0哦！')
    response.status = '500'
    return response


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/error1')
def error1():

    abort(500)
    return 'ok'


@app.route('/error2')
def error2():

    1/0
    return 'ok'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
