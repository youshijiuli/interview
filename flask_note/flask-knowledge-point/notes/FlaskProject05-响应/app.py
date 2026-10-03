from flask import Flask
from flask import jsonify, make_response, render_template



app = Flask(__name__)


@app.route('/index1')
def index1():
    """ 响应：字符串响应 """
    return 'ok'


@app.route('/index2')
def index2():
    """ 响应：json响应 """
    data = {
        'name': 'xiaodai',
        'age': 18
    }
    return jsonify(data)


@app.route('/index3')
def index3():
    """ 响应：元组响应 """
    
    return ("tuple response", 200, {'User-Agent': 'python flask'})


@app.route('/index4')
def index4():
    """ 响应：make_response响应 """
    resp = make_response('make response')
    resp.headers['User-Agent'] = 'python flask'.title()
    resp.status = 200
    return resp


@app.route('/index5/<int:user_id>')
def index5(user_id):
    """ 响应：render_template响应 """
    username = 'xiaodai'
    return render_template("index.html", user_id=user_id, username=username)


if __name__ == '__main__':
    app.run(debug=True)
