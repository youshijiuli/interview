from flask import Flask
from werkzeug.routing import BaseConverter  # 自定义转换器要导入这个父类


app = Flask(__name__)


@app.route('/')
def index():

    return 'hello'


@app.route('/string_converter/<user_id>')
def string_converter(user_id):
    # 当默认不写转换器的时候，就是字符串转换器
    # 或者写成 <str:user_id>
    print(user_id)
    print(type(user_id))
    return 'hello ' + user_id


@app.route('/int_converter/<int:user_id>')
def int_converter(user_id):
    # int转换器
    print(user_id)
    print(type(user_id))
    return f'hello {user_id}'


@app.route('/int_converter_min/<int(min=1):user_id>')
def int_converter_min(user_id):
    # int转换器还能设置边界, min=1指的是包括1不小于1
    print(user_id)
    print(type(user_id))
    return f'hello {user_id}'


@app.route('/float_converter/<float:user_id>')
def float_converter(user_id):
    # float浮点数转换器
    print(user_id)
    print(type(user_id))
    return f'hello {user_id}'


@app.route('/any_converter/<any(jack, bob, lee):user_name>')
def any_converter(user_name):
    # any转换器，只允许你设定的值出现
    # 比如：http://127.0.0.1:5000/any_converter/lee
    print(user_name)
    print(type(user_name))
    return f'hello {user_name}'


# 自定义转换器
class RegexConverter(BaseConverter):
    regex = r'[A-Z]{3}'  # 自定义一个正则规则的转换器


# 注册转换器
app.url_map.converters['regex'] = RegexConverter


@app.route('/regex_converter/<regex:username>')
def regex_converter(username):
    print(username)
    print(type(username))
    return f'hello {username}'


if __name__ == '__main__':
    app.run(debug=True)
