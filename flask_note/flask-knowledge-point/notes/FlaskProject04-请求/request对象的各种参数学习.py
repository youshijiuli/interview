from flask import Flask, request  # request必须要导入
from flask import render_template, redirect, url_for


app = Flask(__name__)


# 请求方式：默认请求方式如果不写的话，那么默认的请求方法是 GET
@app.route('/')
def index():

    return render_template('form-data.html')


# 通过methods指定请求方式，必须是全大写
@app.route('/home', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        return 'handling POST request'
    else:
        return 'handling GET request'

"""
在 Flask 中，`request` 对象提供了一组丰富的属性和方法，用于获取客户端请求的各种信息。以下是一些常用的属性：

1. **request.method**: 返回请求的方法（如 `'GET'`, `'POST'`, `'PUT'`, `'DELETE'` 等）。

2. **request.path**: 返回请求的路径（不包含查询字符串或片段标识符）。

3. **request.args**: 返回一个 MultiDict 对象，包含了所有通过 URL 传递的查询参数。

4. **request.form**: 返回一个 MultiDict 对象，包含了通过表单提交的数据（通常用于 `POST` 请求）。

5. **request.data**: 返回原始请求数据作为字符串，通常用于读取非表单数据（如 JSON 数据）。

6. **request.json**: 如果请求的 Content-Type 是 `application/json`，则返回解析后的 JSON 数据为 Python 字典。

7. **request.files**: 返回一个 MultiDict 对象，包含了上传的文件（通常用于 `POST` 请求）。

8. **request.cookies**: 返回一个字典，包含了客户端发送的所有 Cookie。

9. **request.headers**: 返回一个类字典对象，包含了所有的请求头信息。

10. **request.environ**: 返回 WSGI 环境字典，包含了所有底层 WSGI 服务器的信息。

11. **request.remote_addr**: 返回客户端的 IP 地址。

12. **request.user_agent**: 返回一个 UserAgent 对象，提供了有关客户端浏览器的信息。

13. **request.scheme**: 返回请求使用的协议（如 `'http'` 或 `'https'`）。

14. **request.host**: 返回请求的主机名和端口号。

15. **request.base_url**: 返回请求的基本 URL（包含主机名和路径，但不包含查询字符串或片段标识符）。

16. **request.url**: 返回完整的请求 URL（包含路径、查询字符串和片段标识符）。

17. **request.full_path**: 返回带有查询字符串的完整路径。

18. **request.url_rule**: 返回当前匹配的 URL 规则对象（如果可用的话）。

19. **request.is_xhr**: 判断请求是否来自 XMLHttpRequest（即 AJAX 请求）。

20. **request.mimetype**: 返回 MIME 类型（如 `'text/html'`）。

这些属性可以帮助你处理客户端的请求，并从中提取有用的信息。在实际开发中，你可能会根据具体的业务需求选择使用其中的部分或全部属性。

"""

# 上面的是比较全的，下面我们领出比较重要的几个讲解
# request参数的学习：args、full_path
@app.route('/args', methods=['GET'])
def args_param():

    # **request.args**: 返回一个 MultiDict 对象，包含了所有通过 URL 传递的查询参数。
    name = request.args['name']  # 获取不到就会报错BadRequestKeyError
    age = request.args.get('age')

    # /args?name=wangxin&age=10
    # 可以通过full_path来获取带查询字符串的路径
    print("full_path: ", request.full_path)
    return f"name={name}, age={age}"


# request参数的学习：form、files
@app.route('/form', methods=['GET', 'POST'])
def from_param():

    # **request.form**: 返回一个 MultiDict 对象，包含了通过表单提交的数据（通常用于 `POST` 请求）。
    name = request.form['name']
    age = request.form.get('age')
    print(type(name), type(age))  # 都是str类型
    print(f'name={name}, age={age}')

    # **request.files**: 返回一个 MultiDict 对象，包含了上传的文件（通常用于 `POST` 请求）。
    # 必须要在前端form表单中加入enctype="mutipart/form-data"属性
    f = request.files['pic']
    f.save('./static/1.jpg')

    return redirect(url_for('index'))  # 重定向到首页视图



if __name__ == '__main__':
    app.run(debug=True)
