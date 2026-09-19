# Flask 框架从入门到精通

## 目录

1. [Flask 介绍与安装](#1-flask-介绍与安装)
2. [第一个 Flask 应用](#2-第一个-flask-应用)
3. [路由系统](#3-路由系统)
4. [请求与响应](#4-请求与响应)
5. [Jinja2 模板引擎](#5-jinja2-模板引擎)
6. [Flask 配置管理](#6-flask-配置管理)
7. [蓝图（Blueprint）](#7-蓝图blueprint)
8. [数据库操作（Flask-SQLAlchemy）](#8-数据库操作flask-sqlalchemy)
9. [表单验证（Flask-WTF）](#9-表单验证flask-wtf)
10. [Cookie 与 Session](#10-cookie-与-session)
11. [Flask 中间件与钩子函数](#11-flask-中间件与钩子函数)
12. [错误处理](#12-错误处理)
13. [RESTful API 开发](#13-restful-api-开发)
14. [项目部署](#14-项目部署)

---

## 1. Flask 介绍与安装

### 1.1 Flask 简介

Flask 是一个使用 Python 编写的轻量级 Web 应用框架。它基于 Werkzeug WSGI 工具包和 Jinja2 模板引擎，核心简洁而易于扩展，被称为"微框架"（microframework）。

**Flask 的核心依赖：**

| 组件 | 说明 |
|------|------|
| Werkzeug | Web 工具包，包含 WSGI 服务器和路由、请求/响应处理 |
| Jinja2 | 模板引擎，用于渲染 HTML 模板 |
| MarkupSafe | 模板渲染时的 XSS 攻击防护 |
| ItsDangerous | 加密模块，对 Cookie 进行签名保护 |
| Click | 命令行工具，用于定制命令 |
| Blinker | 信号机制的支持库 |

**与 Django 的对比：**

| 特性 | Django | Flask |
|------|--------|-------|
| 定位 | 全栈框架（大而全） | 微框架（轻量灵活） |
| ORM | 自带 Django ORM | 需要集成 SQLAlchemy 等 |
| 表单 | 自带 Forms 组件 | 需要集成 WTForms |
| 后台管理 | 自带 Admin | 需要集成 Flask-Admin |
| 项目结构 | 约定式（startproject） | 自由组织 |
| 学习曲线 | 较陡 | 较平缓 |

### 1.2 环境准备与安装

#### 创建虚拟环境（推荐）

在开发 Flask 项目前，建议使用虚拟环境来隔离项目依赖。

**Mac / Linux：**
```bash
mkdir myproject
cd myproject
python3 -m venv .venv
source .venv/bin/activate
```

**Windows：**
```bash
mkdir myproject
cd myproject
py -3 -m venv .venv
.venv\Scripts\activate
```

#### 安装 Flask

```bash
pip install Flask
```

安装 Flask 时会自动安装以下依赖：
- Werkzeug（Web 工具包）
- Jinja2（模板引擎）
- MarkupSafe（XSS 防护）
- ItsDangerous（加密签名）
- Click（命令行工具）
- Blinker（信号机制）

可选依赖：
```bash
pip install python-dotenv    # 管理 .env 配置文件
pip install watchdog          # 监控文件变动，开发时热重载
```

---

## 2. 第一个 Flask 应用

### 2.1 最小应用

```python
from flask import Flask

# 创建 Flask 应用实例
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=8888)
```

### 2.2 运行 Flask 项目的几种方式

```python
# 方式一：通过 python -m flask 命令
# python -m flask --app app.py run

# 方式二：通过 flask 命令
# flask --app app.py run

# 方式三：文件名为 app.py 时可省略文件名
# flask run --host=0.0.0.0 --port=5000

# 方式四：在 PyCharm 中配置 Flask Server 运行

# 方式五：直接在代码中添加 main 入口，右键运行
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
```

**常用命令行参数：**
```bash
flask --app app.py run --debug --host=0.0.0.0 --port=8080
```

### 2.3 "新手四件套"返回值

Flask 视图函数支持四种常见返回类型：

```python
from flask import Flask, render_template, redirect, jsonify

app = Flask(__name__)


@app.route('/str')
def return_string():
    """返回字符串"""
    return '直接返回字符串'


@app.route('/template')
def return_template():
    """返回模板页面"""
    return render_template('index.html', name='Flask')


@app.route('/redirect')
def return_redirect():
    """返回重定向"""
    return redirect('/str')


@app.route('/json')
def return_json():
    """返回 JSON 数据"""
    return jsonify({'code': 100, 'msg': '成功', 'data': {'id': 1, 'name': 'Flask'}})


if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. 路由系统

### 3.1 路由注册

Flask 的路由基于装饰器实现：

```python
from flask import Flask

app = Flask(__name__)


# 方式一：使用 @app.route()
@app.route('/index', methods=['GET', 'POST'])
def index():
    return 'Index Page'


# 方式二：使用简写装饰器
@app.get('/get')
def get_method():
    return 'GET 请求'


@app.post('/post')
def post_method():
    return 'POST 请求'


@app.put('/put')
def put_method():
    return 'PUT 请求'


@app.delete('/delete')
def delete_method():
    return 'DELETE 请求'
```

### 3.2 路由的本质

`@app.route()` 本质上调用的是 `app.add_url_rule()`：

```python
# 以下两种写法等价

# 写法一：装饰器方式
@app.route('/hello', methods=['GET'], endpoint='hello')
def hello():
    return 'Hello'


# 写法二：直接调用 add_url_rule
def hello():
    return 'Hello'

app.add_url_rule('/hello', endpoint='hello', view_func=hello, methods=['GET'])
```

**add_url_rule 的常用参数：**

| 参数 | 说明 |
|------|------|
| `rule` | URL 规则 |
| `endpoint` | 路由别名，用于 `url_for` 反向解析。不指定则默认为函数名 |
| `view_func` | 视图函数 |
| `methods` | 允许的请求方法列表 |
| `defaults` | 默认参数，为视图函数提供默认值 |
| `strict_slashes` | 是否严格要求 URL 末尾的 `/` |
| `redirect_to` | 重定向到指定地址 |

```python
# defaults 参数使用
@app.route('/user', defaults={'page': 1})
@app.route('/user/page/<int:page>')
def user_list(page):
    return f'用户列表第 {page} 页'


# strict_slashes 参数使用
@app.route('/about', strict_slashes=False)
# 访问 /about 和 /about/ 均可

@app.route('/contact', strict_slashes=True)
# 仅能访问 /contact，/contact/ 会 404


# redirect_to 参数使用
@app.route('/old/<int:nid>', redirect_to='/new/<nid>')
```

### 3.3 路由参数（转换器）

Flask 内置了多种路由转换器，用于对 URL 中的变量进行类型校验和转换：

```python
# Flask 内置转换器
DEFAULT_CONVERTERS = {
    'default': UnicodeConverter,    # 默认，字符串（不含 /）
    'string':  UnicodeConverter,    # 字符串（不含 /）
    'any':     AnyConverter,        # 多种路径中的一种
    'path':    PathConverter,       # 字符串（含 /）
    'int':     IntegerConverter,    # 整数
    'float':   FloatConverter,      # 浮点数
    'uuid':    UUIDConverter,       # UUID 格式
}
```

**路由参数使用示例：**

```python
from flask import Flask

app = Flask(__name__)


# 整数参数
@app.route('/user/<int:user_id>')
def user_detail(user_id):
    return f'用户ID: {user_id}'


# 字符串参数
@app.route('/post/<string:slug>')
def post_detail(slug):
    return f'文章标识: {slug}'


# 浮点数参数
@app.route('/price/<float:amount>')
def show_price(amount):
    return f'价格: {amount}'


# 路径参数（可包含斜杠）
@app.route('/files/<path:file_path>')
def read_file(file_path):
    return f'文件路径: {file_path}'


# UUID 参数
@app.route('/order/<uuid:order_id>')
def order_detail(order_id):
    return f'订单ID: {order_id}'


# any 转换器：限制参数可选值
@app.route('/<any(blog, news, wiki):section>/')
def section_page(section):
    return f'当前栏目: {section}'
```

### 3.4 url_for 反向解析

通过 `url_for()` 函数可以根据端点名称生成 URL：

```python
from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '首页'


@app.route('/user/<int:uid>', endpoint='user_detail')
def user(uid):
    return f'用户 {uid} 的详情'


@app.route('/test')
def test():
    # 生成 /user/5
    url1 = url_for('user_detail', uid=5)

    # 生成 /
    url2 = url_for('index')

    # 生成静态文件 URL
    url3 = url_for('static', filename='css/style.css')

    return f'url1: {url1}, url2: {url2}, url3: {url3}'
```

### 3.5 类视图（CBV）

Flask 支持基于类的视图，有两种基类可供选择：

```python
from flask import Flask
from flask.views import MethodView, View

app = Flask(__name__)


# 方式一：继承 MethodView（推荐）
# 自动根据请求方法分发到对应的类方法
class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None:
            return {'users': ['user1', 'user2']}
        return {'user': user_id}

    def post(self):
        return {'msg': '用户创建成功'}

    def put(self, user_id):
        return {'msg': f'用户 {user_id} 更新成功'}

    def delete(self, user_id):
        return {'msg': f'用户 {user_id} 删除成功'}


# 注册类视图
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET'])
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])


# 方式二：继承 View，手动重写 dispatch_request
class CustomView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            return 'GET 请求'
        return 'POST 请求'


app.add_url_rule('/custom', view_func=CustomView.as_view('custom'))
```

**MethodView 源码解析（核心流程）：**

```python
# 1. as_view 返回 view 函数
# 2. 请求到来时执行 view() -> self.dispatch_request()
# 3. dispatch_request 通过反射找到与请求方法同名的方法并执行

def dispatch_request(self, **kwargs):
    meth = getattr(self, request.method.lower(), None)
    if meth is None and request.method == "HEAD":
        meth = getattr(self, "get", None)
    assert meth is not None
    return meth(**kwargs)
```

### 3.6 CBV 加装饰器

```python
from functools import wraps
from flask import session, redirect
from flask.views import MethodView


def login_required(func):
    """登录认证装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        return redirect('/login')
    return wrapper


class UserView(MethodView):
    # 通过 decorators 属性添加装饰器
    # 多个装饰器时，最左侧的装饰器最先执行
    decorators = [login_required]

    def get(self):
        return '用户信息'

    def post(self):
        return '创建用户'
```

---

## 4. 请求与响应

### 4.1 Request 对象

Flask 的 `request` 对象是全局可访问的，包含当前请求的所有信息：

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # --- 请求方法 ---
    print(f'请求方法: {request.method}')

    # --- URL 相关 ---
    print(f'路径 (无域名):    {request.path}')
    print(f'路径+参数:        {request.full_path}')
    print(f'完整URL:          {request.url}')
    print(f'基础URL:          {request.base_url}')
    print(f'域名根:           {request.url_root}')
    print(f'主机地址:         {request.host}')

    # --- 请求参数 ---
    # GET 请求参数（URL 中 ? 后的部分）
    print(f'查询参数:         {request.args}')
    print(f'获取单个参数:     {request.args.get("page", 1)}')

    # POST 请求体数据（form-urlencoded 格式）
    print(f'表单数据:         {request.form}')
    print(f'获取单个字段:     {request.form.get("username")}')

    # GET 和 POST 数据的总和
    print(f'所有参数:         {request.values}')

    # --- 请求头 ---
    print(f'请求头:           {request.headers}')
    print(f'User-Agent:       {request.headers.get("User-Agent")}')
    print(f'Content-Type:     {request.headers.get("Content-Type")}')

    # --- Cookie ---
    print(f'Cookie:           {request.cookies}')
    print(f'获取单个Cookie:   {request.cookies.get("session_id")}')

    # --- 文件上传 ---
    if 'file' in request.files:
        file = request.files['file']
        file.save(f'./uploads/{file.filename}')

    # --- JSON 数据 ---
    json_data = request.get_json()
    print(f'JSON数据:         {json_data}')

    return 'Request 对象演示完成'
```

**request 对象常用属性速查表：**

| 属性/方法 | 说明 |
|-----------|------|
| `request.method` | 请求方法（GET/POST/PUT/DELETE 等） |
| `request.path` | 请求路径（不含域名） |
| `request.full_path` | 请求路径 + 查询参数 |
| `request.url` | 完整 URL |
| `request.args` | URL 查询参数字典 |
| `request.form` | POST 表单数据字典 |
| `request.values` | args + form 合并 |
| `request.json` / `request.get_json()` | JSON 请求体 |
| `request.files` | 上传的文件 |
| `request.headers` | 请求头字典 |
| `request.cookies` | Cookie 字典 |
| `request.data` | 原始请求体（字符串） |

### 4.2 Response 对象

使用 `make_response()` 可以构造响应对象，进行更精细的控制：

```python
from flask import Flask, make_response, jsonify

app = Flask(__name__)


@app.route('/custom-response')
def custom_response():
    # 构造响应对象
    resp = make_response('自定义响应内容')

    # 设置状态码
    resp.status_code = 201

    # 设置响应头
    resp.headers['X-Custom-Header'] = 'my-value'
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'

    # 设置 Cookie
    resp.set_cookie('username', 'Alice', max_age=3600, httponly=True)
    resp.set_cookie('theme', 'dark', path='/')

    return resp


@app.route('/cors-demo')
def cors_demo():
    """设置 CORS 响应头"""
    resp = jsonify({'msg': '跨域请求成功'})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp


@app.route('/delete-cookie')
def delete_cookie():
    """删除 Cookie"""
    resp = make_response('Cookie 已删除')
    resp.delete_cookie('username')
    return resp
```

**直接返回的四种响应类型（无需 make_response）：**
1. `return '字符串'` -- 返回 HTML 文本
2. `return render_template('index.html')` -- 返回渲染后的模板
3. `return redirect('/url')` -- 返回重定向响应
4. `return jsonify({'key': 'value'})` -- 返回 JSON 响应

---

## 5. Jinja2 模板引擎

Jinja2 是 Flask 默认的模板引擎，语法与 Django 模板（DTL）非常相似，但功能更强大。

### 5.1 变量与表达式

```html
<!-- templates/demo.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <!-- 变量渲染 -->
    <p>用户名: {{ user.name }}</p>
    <p>年龄: {{ user['age'] }}</p>
    <p>爱好: {{ user.get('hobby', '未知') }}</p>

    <!-- Jinja2 支持函数调用（带括号），这比 Django 模板更灵活 -->
    <p>{{ add(3, 4) }}</p>

    <!-- 字符串拼接 -->
    <p>{{ 'Hello ' + user.name }}</p>
</body>
</html>
```

```python
from flask import Flask, render_template

app = Flask(__name__)


def add(a, b):
    return a + b + 100


@app.route('/')
def index():
    user = {'name': '小明', 'age': 25, 'hobby': '篮球'}
    return render_template('demo.html',
                           title='Jinja2 演示',
                           user=user,
                           add=add)
```

### 5.2 过滤器

过滤器用于对变量进行格式化处理：

```html
<!-- 常用过滤器 -->
<p>{{ name|capitalize }}</p>       <!-- 首字母大写 -->
<p>{{ name|upper }}</p>            <!-- 全大写 -->
<p>{{ name|lower }}</p>            <!-- 全小写 -->
<p>{{ name|title }}</p>            <!-- 每个单词首字母大写 -->
<p>{{ name|trim }}</p>             <!-- 去除首尾空格 -->
<p>{{ name|length }}</p>           <!-- 序列长度 -->
<p>{{ name|default('默认值') }}</p> <!-- 默认值 -->
<p>{{ price|round(2) }}</p>        <!-- 四舍五入保留两位小数 -->

<!-- 安全输出（不转义 HTML） -->
<p>{{ html_content|safe }}</p>

<!-- 日期格式化 -->
<p>{{ created_time|datetimeformat('%Y-%m-%d %H:%M:%S') }}</p>

<!-- 截断文本 -->
<p>{{ long_text|truncate(50) }}</p>

<!-- 转 JSON -->
<script>
    var data = {{ user_dict|tojson }};
</script>

<!-- 自定义过滤器 -->
<!-- Python 代码中注册 -->
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

<!-- 模板中使用 -->
<p>{{ 'hello'|reverse }}</p>  <!-- 输出: olleh -->
```

### 5.3 控制结构

```html
<!-- if 条件判断 -->
{% if user.is_vip %}
    <span class="badge">VIP 会员</span>
{% elif user.level > 5 %}
    <span class="badge">高级用户</span>
{% else %}
    <span class="badge">普通用户</span>
{% endif %}

<!-- for 循环 -->
<ul>
{% for item in items %}
    <li>{{ loop.index }}. {{ item.name }}</li>
{% else %}
    <li>列表为空</li>
{% endfor %}
</ul>

<!-- loop 对象常用属性 -->
<!-- loop.index     当前迭代索引（从1开始） -->
<!-- loop.index0    当前迭代索引（从0开始） -->
<!-- loop.first     是否为第一次迭代 -->
<!-- loop.last      是否为最后一次迭代 -->
<!-- loop.length    序列长度 -->

<!-- 循环字典 -->
{% for key, value in user.items() %}
    <p>{{ key }}: {{ value }}</p>
{% endfor %}
```

### 5.4 模板继承

**基础模板：** `templates/base.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block head_extra %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav>
        {% block navbar %}
        <a href="/">首页</a>
        <a href="/about">关于</a>
        {% endblock %}
    </nav>

    <!-- 主体内容区域 -->
    <main>
        {% block content %}
        <p>默认内容</p>
        {% endblock %}
    </main>

    <!-- 侧边栏 -->
    <aside>
        {% block sidebar %}{% endblock %}
    </aside>

    <!-- 页脚 -->
    <footer>
        {% block footer %}
        <p>&copy; 2026 My Flask App</p>
        {% endblock %}
    </footer>

    {% block scripts %}{% endblock %}
</body>
</html>
```

**子模板：** `templates/page.html`

```html
{% extends "base.html" %}

{% block title %}自定义页面标题{% endblock %}

{% block content %}
    <h1>我是子模板的内容</h1>
    <p>这段内容会替换父模板中 content 块的内容。</p>

    <!-- 引用父模板内容 -->
    {{ super() }}
    <p>上面是父模板中 content 块的原始内容。</p>
{% endblock %}

{% block sidebar %}
    <h3>侧边栏</h3>
    <ul>
        <li>链接1</li>
        <li>链接2</li>
    </ul>
{% endblock %}
```

### 5.5 include 与宏

```html
<!-- 包含其他模板 -->
{% include 'header.html' %}

<!-- 带参数的 include -->
{% include 'card.html' with context %}

<!-- 宏（类似函数） -->
{% macro input(name, value='', type='text', placeholder='') %}
    <input type="{{ type }}"
           name="{{ name }}"
           value="{{ value }}"
           placeholder="{{ placeholder }}"
           class="form-control">
{% endmacro %}

<!-- 使用宏 -->
{{ input('username', placeholder='请输入用户名') }}
{{ input('password', type='password', placeholder='请输入密码') }}

<!-- 从其他文件导入宏 -->
{% from 'forms.html' import input, textarea %}
```

---

## 6. Flask 配置管理

### 6.1 默认配置项

Flask 应用有一个 `config` 属性（类字典对象），包含以下默认配置：

```python
app.config = {
    'DEBUG':              False,        # 调试模式
    'TESTING':            False,        # 测试模式
    'SECRET_KEY':         None,         # 密钥（Session 等加密需要）
    'PERMANENT_SESSION_LIFETIME': timedelta(days=31),  # Session 持久化时间
    'SESSION_COOKIE_NAME': 'session',   # Session Cookie 名称
    'SESSION_COOKIE_HTTPONLY': True,    # Cookie 仅 HTTP 可访问
    'SESSION_COOKIE_SECURE': False,     # Cookie 仅 HTTPS 传输
    'SESSION_COOKIE_SAMESITE': None,    # SameSite 策略
    'MAX_CONTENT_LENGTH': None,         # 最大请求体大小
    'JSON_AS_ASCII': True,             # JSON 响应是否 ASCII 编码
    'TEMPLATES_AUTO_RELOAD': None,     # 模板自动重载
    'SERVER_NAME': None,               # 服务器名称和端口
    'APPLICATION_ROOT': None,          # 应用根路径
    'PREFERRED_URL_SCHEME': 'http',    # URL 生成时的默认协议
}
```

### 6.2 配置方式

```python
from flask import Flask

app = Flask(__name__)


# ============ 方式一：直接修改 app.config 字典 ============
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DATABASE_URL'] = 'mysql://root:123456@localhost/mydb'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'


# ============ 方式二：通过 app 属性设置（仅限部分属性） ============
app.debug = True
app.secret_key = 'your-secret-key-here'


# ============ 方式三：从 Python 文件加载 ============
# settings.py 文件内容：
# DEBUG = True
# SECRET_KEY = 'my-secret-key'
# DATABASE_URL = 'mysql://...'

app.config.from_pyfile('settings.py')


# ============ 方式四：从对象加载（支持类继承，推荐） ============
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'base-secret-key'
    DATABASE_URL = 'mysql://localhost/mydb'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'mysql://localhost/dev_db'


class ProductionConfig(Config):
    DATABASE_URL = 'mysql://prod-server/prod_db'


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'


# 使用时根据环境变量选择
import os
env = os.environ.get('FLASK_ENV', 'development')
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
app.config.from_object(config_map[env])


# ============ 方式五：从 JSON 文件加载 ============
# config.json:
# {
#   "DEBUG": true,
#   "SECRET_KEY": "json-secret-key"
# }
# ⚠️ Flask 2.0 起 from_json 已被移除，统一改用 from_file 配合 load 函数
import json
app.config.from_file('config.json', load=json.load)


# ============ 方式六：使用字典批量设置 ============
app.config.from_mapping({
    'DEBUG': True,
    'SECRET_KEY': 'mapped-secret-key',
    'CACHE_TYPE': 'redis',
})
```

### 6.3 python-dotenv 配置方式

`.env` 文件（放在项目根目录）：

```bash
# .env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=mysql://root:password@localhost:3306/mydb
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=my-super-secret-key
```

```python
# 安装: pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件到环境变量

# 使用环境变量
database_url = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

---

## 7. 蓝图（Blueprint）

蓝图用于将应用模块化，实现大型项目的目录划分。每个蓝图可以拥有自己的路由、模板、静态文件和请求扩展。

### 7.1 蓝图基本使用

```python
# ============ admin/views.py ============
from flask import Blueprint

# 创建蓝图对象
admin_bp = Blueprint('admin',           # 蓝图名称
                     __name__,           # 模块名
                     url_prefix='/admin',  # URL 前缀
                     template_folder='templates',  # 模板目录
                     static_folder='static')       # 静态文件目录


@admin_bp.route('/')
def admin_index():
    return '管理后台首页'


@admin_bp.route('/users')
def admin_users():
    return '用户管理页面'


# 蓝图也可以使用请求扩展
@admin_bp.before_request
def admin_before_request():
    """进入管理后台前的权限校验"""
    print('管理后台请求来了')


# ============ app.py ============
from flask import Flask
from admin.views import admin_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)
```

### 7.2 小项目目录结构（使用蓝图）

```
myproject/
├── app.py                  # 主入口
├── settings.py             # 配置文件
├── apps/
│   ├── __init__.py
│   ├── home/
│   │   ├── __init__.py
│   │   ├── views.py        # 视图函数
│   │   └── models.py       # 数据模型
│   ├── user/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── models.py
│   └── order/
│       ├── __init__.py
│       ├── views.py
│       └── models.py
├── templates/              # 公共模板
│   └── base.html
├── static/                 # 公共静态文件
│   ├── css/
│   ├── js/
│   └── images/
└── utils/                  # 工具函数
    ├── __init__.py
    └── common.py
```

### 7.3 大项目目录结构

```
myproject/
├── manage.py               # 管理入口
├── config/
│   ├── __init__.py
│   └── settings.py         # 配置
├── app/
│   ├── __init__.py         # 创建 app 的工厂函数
│   ├── models/
│   │   └── base.py         # 基础模型类
│   ├── home/
│   │   ├── __init__.py
│   │   └── views.py
│   ├── user/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── models.py
│   └── templates/          # 应用级模板
├── extensions/
│   └── __init__.py         # 扩展初始化
├── templates/              # 项目级模板
└── static/                 # 项目级静态文件
```

**应用工厂函数：**

```python
# app/__init__.py
from flask import Flask
from config.settings import config_map


def create_app(env='development'):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config_map[env])

    # 注册蓝图
    from app.home.views import home_bp
    from app.user.views import user_bp
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')

    # 初始化扩展
    from extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    return app
```

```python
# manage.py
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run()
```

---

## 8. 数据库操作（Flask-SQLAlchemy）

### 8.1 SQLAlchemy 简介

SQLAlchemy 是 Python 界最强大的企业级 ORM 框架，支持多种数据库。它提供两层 API：

- **Core 层**：SQL 表达式语言，接近原生 SQL
- **ORM 层**：对象关系映射，操作 Python 对象即操作数据库

```bash
pip install sqlalchemy pymysql
```

### 8.2 数据库连接

```python
from sqlalchemy import create_engine

# 创建引擎（内置连接池）
engine = create_engine(
    "mysql+pymysql://root:password@127.0.0.1:3306/mydb?charset=utf8mb4",
    max_overflow=0,   # 超过连接池大小外最多创建的连接
    pool_size=5,      # 连接池大小
    pool_timeout=30,  # 池中没有连接最多等待时间（秒）
    pool_recycle=-1   # 自动回收连接的时间间隔（秒）
)
```

**不同数据库的连接字符串：**

```python
# MySQL
"mysql+pymysql://user:password@host:port/dbname"

# PostgreSQL
"postgresql://user:password@host:port/dbname"
"postgresql+psycopg2://user:password@host:port/dbname"

# SQLite
"sqlite:///path/to/database.db"

# Oracle
"oracle+cx_oracle://user:password@host:port/sid"
```

### 8.3 定义模型

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
import datetime


# 创建基类（新版本推荐方式）
class Base(DeclarativeBase):
    pass


# 定义模型类
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    age = Column(Integer, default=0)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    def __repr__(self):
        return f'<User {self.name}>'


# 创建所有表
Base.metadata.create_all(engine)

# 删除所有表
# Base.metadata.drop_all(engine)
```

### 8.4 基本 CRUD 操作

```python
from sqlalchemy.orm import Session
from models import User

# 创建 Session
session = Session(engine)


# ============ 查询操作 ============

# 查询所有
users = session.query(User).all()

# 条件过滤
user = session.query(User).filter_by(name='Alice').first()
users = session.query(User).filter(User.age >= 18).all()

# 复杂条件（AND / OR）
from sqlalchemy import and_, or_
users = session.query(User).where(
    or_(
        User.age < 18,
        and_(User.name.like('%张%'), User.age > 30)
    )
).all()

# IN 查询
users = session.query(User).where(User.id.in_([1, 2, 3])).all()

# BETWEEN 查询
users = session.query(User).where(User.age.between(20, 30)).all()

# LIKE 模糊查询
users = session.query(User).where(User.name.like('%张%')).all()

# 排序
users = session.query(User).order_by(User.age.desc()).all()

# 分页
users = session.query(User).offset(0).limit(10).all()

# 聚合函数
from sqlalchemy import func
result = session.query(
    func.count(User.id),
    func.avg(User.age),
    func.max(User.age)
).first()


# ============ 新增操作 ============

# 新增单条
user = User(name='Alice', email='alice@example.com', age=25)
session.add(user)
session.commit()

# 批量新增
users = [
    User(name='Bob', email='bob@example.com', age=30),
    User(name='Charlie', email='charlie@example.com', age=22),
]
session.add_all(users)
session.commit()


# ============ 更新操作 ============

# 方式一：查询后修改属性
user = session.query(User).filter_by(id=1).first()
user.age = 26
session.commit()

# 方式二：批量更新
session.query(User).filter_by(age=25).update({'age': 26})
session.commit()


# ============ 删除操作 ============

# 删除单条
user = session.query(User).filter_by(id=1).first()
session.delete(user)
session.commit()

# 批量删除
session.query(User).filter(User.age < 18).delete()
session.commit()


# 关闭 session
session.close()
```

### 8.5 一对多关系

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), default='篮球')

    # 反向引用：hobby.persons 获取所有关联的 Person
    def __repr__(self):
        return f'<Hobby {self.name}>'


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    hobby_id = Column(Integer, ForeignKey('hobby.id'))

    # relationship 用于对象级联查询，不创建数据库字段
    hobby = relationship('Hobby', backref='persons')

    def __repr__(self):
        return f'<Person {self.name}>'


# ============ 操作示例 ============

# 新增（级联）
person = Person(name='张三', hobby=Hobby(name='游泳'))
session.add(person)
session.commit()

# 正向查询：Person -> Hobby
person = session.query(Person).first()
print(person.hobby.name)  # 输出: 游泳

# 反向查询：Hobby -> Persons
hobby = session.query(Hobby).first()
print(hobby.persons)  # 输出: [<Person 张三>, ...]
```

### 8.6 多对多关系

```python
# 中间表
class Boy2Girl(Base):
    __tablename__ = 'boy2girl'
    id = Column(Integer, primary_key=True, autoincrement=True)
    boy_id = Column(Integer, ForeignKey('boy.id'))
    girl_id = Column(Integer, ForeignKey('girl.id'))
    created_at = Column(DateTime, default=datetime.datetime.now)


class Girl(Base):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<Girl {self.name}>'


class Boy(Base):
    __tablename__ = 'boy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)

    # secondary 指定中间表名
    girls = relationship('Girl', secondary='boy2girl', backref='boys')

    def __repr__(self):
        return f'<Boy {self.name}>'


# ============ 操作示例 ============

# 关联新增
boy = session.query(Boy).filter_by(name='古天乐').first()
girl1 = session.query(Girl).filter_by(name='刘亦菲').first()
girl2 = session.query(Girl).filter_by(name='迪丽热巴').first()
boy.girls = [girl1, girl2]
session.add(boy)
session.commit()

# 正向查询
print(boy.girls)  # Person -> 所有关联的 Girl

# 反向查询
print(girl1.boys)  # Girl -> 所有关联的 Boy
```

### 8.7 Session 线程安全（scoped_session）

在多线程 Web 应用中，需要使用 `scoped_session` 保证每个线程拥有独立的 session：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("mysql+pymysql://root:password@127.0.0.1:3306/mydb")

# 创建 Session 工厂
SessionFactory = sessionmaker(bind=engine)

# 创建线程安全的 session对象（全局单例，每个线程独立）
session = scoped_session(SessionFactory)

# 在视图函数中直接使用（内部通过线程 ID 隔离）
@app.route('/')
def index():
    users = session.query(User).all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])
```

### 8.8 Flask-SQLAlchemy 集成

Flask-SQLAlchemy 是对 SQLAlchemy 的 Flask 封装，提供了更方便的集成方式：

```bash
pip install flask-sqlalchemy
```

```python
# extensions.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# app.py
from flask import Flask
from extensions import db

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/mydb?charset=utf8mb4'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化
db.init_app(app)


# models.py
from extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'


# views.py - 在视图函数中使用
@app.route('/users')
def user_list():
    # Flask-SQLAlchemy 的 session 是线程安全的
    users = db.session.execute(db.select(User)).scalars().all()
    # 或使用老式写法
    users = User.query.all()
    return jsonify([u.username for u in users])


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'msg': '创建成功'}), 201
```

### 8.9 数据库迁移（Flask-Migrate）

```bash
pip install flask-migrate
```

```python
from flask import Flask
from flask_migrate import Migrate
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://...'
db.init_app(app)

# 初始化迁移
migrate = Migrate(app, db)


# 迁移命令：
# flask db init          # 初始化迁移目录（仅首次）
# flask db migrate -m "描述"  # 生成迁移文件（类似 makemigrations）
# flask db upgrade       # 应用迁移（类似 migrate）
# flask db downgrade     # 回滚迁移
# flask db history       # 查看迁移历史
```

---

## 9. 表单验证（Flask-WTF）

### 9.1 WTForms 基本使用

```bash
pip install wtforms
```

```python
from flask import Flask, render_template, request
from wtforms import Form
from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms import validators
from wtforms import widgets

app = Flask(__name__)


class LoginForm(Form):
    """登录表单"""
    username = StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空'),
            validators.Length(min=3, max=20, message='用户名长度3-20个字符'),
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control', 'placeholder': '请输入用户名'}
    )

    password = PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空'),
            validators.Length(min=6, max=30, message='密码长度6-30个字符'),
            validators.Regexp(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}',
                message='密码至少含1个大写字母、1个小写字母、1个数字和1个特殊字符'
            ),
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control', 'placeholder': '请输入密码'}
    )

    age = IntegerField(
        label='年龄',
        validators=[
            validators.NumberRange(min=0, max=150, message='年龄范围0-150'),
        ],
        default=18
    )


class RegistrationForm(Form):
    """注册表单（更多校验器示例）"""
    email = StringField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空'),
            validators.Email(message='邮箱格式不正确'),
        ]
    )

    phone = StringField(
        label='手机号',
        validators=[
            validators.DataRequired(message='手机号不能为空'),
            validators.Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确'),
        ]
    )

    confirm_password = PasswordField(
        label='确认密码',
        validators=[
            validators.DataRequired(message='请确认密码'),
            validators.EqualTo('password', message='两次密码不一致'),
        ]
    )
```

**视图函数中使用：**

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        # 将提交的数据绑定到表单
        form = LoginForm(formdata=request.form)

        if form.validate():
            # 验证通过，获取清洗后的数据
            username = form.username.data
            password = form.password.data
            print(f'用户 {username} 登录成功')
            return redirect('/')
        else:
            # 验证失败，form.errors 包含所有错误信息
            print('验证失败:', form.errors)
            return render_template('login.html', form=form)
```

**模板渲染：**

```html
<!-- templates/login.html -->
<form method="post">
    <div class="form-group">
        {{ form.username.label }}
        {{ form.username(class='form-control') }}
        {% if form.username.errors %}
            <span class="text-danger">{{ form.username.errors[0] }}</span>
        {% endif %}
    </div>

    <div class="form-group">
        {{ form.password.label }}
        {{ form.password }}
        {% if form.password.errors %}
            <span class="text-danger">{{ form.password.errors[0] }}</span>
        {% endif %}
    </div>

    <button type="submit" class="btn btn-primary">登录</button>
</form>
```

### 9.2 WTForms 常用字段和校验器

**常用字段：**

| 字段 | 说明 |
|------|------|
| `StringField` | 文本输入 |
| `PasswordField` | 密码输入 |
| `IntegerField` | 整数输入 |
| `FloatField` | 浮点数输入 |
| `BooleanField` | 复选框 |
| `DateField` | 日期选择 |
| `DateTimeField` | 日期时间选择 |
| `RadioField` | 单选按钮 |
| `SelectField` | 下拉选择 |
| `SelectMultipleField` | 多选下拉 |
| `FileField` | 文件上传 |
| `TextAreaField` | 多行文本 |
| `HiddenField` | 隐藏字段 |

**常用校验器：**

| 校验器 | 说明 |
|--------|------|
| `DataRequired()` | 必填校验 |
| `Email()` | 邮箱格式 |
| `Length(min, max)` | 长度限制 |
| `NumberRange(min, max)` | 数值范围 |
| `EqualTo(fieldname)` | 等于某字段 |
| `Regexp(regex)` | 正则匹配 |
| `URL()` | URL 格式 |
| `IPAddress()` | IP 地址格式 |
| `Optional()` | 可选（无值时不校验） |
| `AnyOf(values)` | 必须是集合中的某个值 |
| `NoneOf(values)` | 不能是集合中的某个值 |

---

## 10. Cookie 与 Session

### 10.1 Cookie 操作

```python
from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/set-cookie')
def set_cookie():
    resp = make_response('Cookie 已设置')

    # 设置 Cookie
    resp.set_cookie('username', 'Alice',
                    max_age=86400,      # 有效期（秒），None 表示浏览器关闭即失效
                    expires=None,        # 过期日期（datetime 对象）
                    path='/',            # Cookie 生效路径
                    domain=None,         # Cookie 生效域名
                    secure=False,        # 是否仅 HTTPS 传输
                    httponly=True,       # 是否仅 HTTP 可访问（禁止 JS 读取）
                    samesite='Lax')      # SameSite 策略: Strict/Lax/None

    # 设置多个 Cookie
    resp.set_cookie('theme', 'dark', max_age=2592000)
    resp.set_cookie('lang', 'zh-CN')

    return resp


@app.route('/get-cookie')
def get_cookie():
    # 读取 Cookie
    username = request.cookies.get('username', 'Guest')
    theme = request.cookies.get('theme', 'light')
    return f'用户名: {username}, 主题: {theme}'


@app.route('/delete-cookie')
def delete_cookie():
    resp = make_response('Cookie 已删除')
    resp.delete_cookie('username')
    return resp
```

### 10.2 Session 使用

Flask 默认的 Session 将数据经过 `secret_key` 签名后存储在客户端的 Cookie 中：

```python
from flask import Flask, session

app = Flask(__name__)

# 必须设置 secret_key，否则 session 无法使用
app.secret_key = 'your-secret-key-here-change-in-production'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录成功后，将用户信息写入 session
        session['user_id'] = 123
        session['username'] = request.form['username']
        session['is_admin'] = True
        return redirect('/dashboard')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # 读取 session
    if 'username' in session:
        return f'欢迎回来，{session["username"]}'
    return redirect('/login')


@app.route('/logout')
def logout():
    # 清除单个 key
    session.pop('username', None)

    # 清除所有 session 数据
    session.clear()

    return redirect('/')


@app.route('/profile')
def profile():
    # 使用 get 安全读取
    username = session.get('username', '未登录')
    return f'当前用户: {username}'
```

**Session 配置项：**

```python
app.config.update(
    SECRET_KEY='your-secret-key',
    SESSION_COOKIE_NAME='my_session',           # Cookie 名称，默认 'session'
    SESSION_COOKIE_DOMAIN=None,                 # Cookie 域名
    SESSION_COOKIE_PATH='/',                    # Cookie 路径
    SESSION_COOKIE_HTTPONLY=True,               # 禁止 JS 访问
    SESSION_COOKIE_SECURE=False,                # 是否仅 HTTPS
    SESSION_COOKIE_SAMESITE='Lax',              # SameSite 策略
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),  # 持久化 session 生存时间
    SESSION_REFRESH_EACH_REQUEST=True,          # 每次请求刷新过期时间
)
```

### 10.3 Session 存储到 Redis（flask-session）

默认的 Session 存储在客户端 Cookie 中有大小限制（约 4KB）。生产环境中建议使用 `flask-session` 将 Session 存储到 Redis 等服务端：

```bash
pip install flask-session redis
```

```python
from flask import Flask, session
from flask_session import Session
import redis

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# ============ 配置方式一：通过 app.config ============
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379, db=0)
app.config['SESSION_KEY_PREFIX'] = 'myapp_session:'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_USE_SIGNER'] = True

Session(app)


# ============ 配置方式二：直接替换 session_interface ============
from flask_session.redis import RedisSessionInterface

conn = redis.Redis(host='127.0.0.1', port=6379)
app.session_interface = RedisSessionInterface(
    app,
    client=conn,
    key_prefix='session:',
    use_signer=True,
    permanent=True,
    sid_length=32
)
```

**Session 支持的后端存储：**
- `redis` -- Redis 存储（推荐）
- `memcached` -- Memcached 存储
- `filesystem` -- 文件系统存储
- `mongodb` -- MongoDB 存储
- `sqlalchemy` -- 数据库存储

### 10.4 闪现消息（flash）

flash 用于跨请求传递一次性消息（常用于表单提交后的提示）：

```python
from flask import Flask, flash, get_flashed_messages, render_template

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123456':
            flash('登录成功', category='success')
            return redirect('/')
        else:
            flash('用户名或密码错误', category='error')
            return redirect('/login')

    # GET 请求：获取并显示 flash 消息
    messages = get_flashed_messages(with_categories=True)
    return render_template('login.html', messages=messages)


# 模板中使用
# {% with messages = get_flashed_messages(with_categories=true) %}
#   {% if messages %}
#     {% for category, message in messages %}
#       <div class="alert alert-{{ category }}">{{ message }}</div>
#     {% endfor %}
#   {% endif %}
# {% endwith %}
```

---

## 11. Flask 中间件与钩子函数

### 11.1 请求扩展（钩子函数）

Flask 的请求扩展类似于 Django 的中间件，用于在请求处理的生命周期中插入自定义逻辑：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)


# ============ before_request ============
# 请求进入视图函数之前执行
# 多个 before_request 从上到下依次执行
# 返回 None 继续执行后续，返回响应对象则终止请求
@app.before_request
def check_auth():
    """认证检查"""
    # 排除登录和静态文件路由
    if request.path in ('/login', '/register'):
        return None  # 继续执行

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'code': 401, 'msg': '未登录'}), 401


@app.before_request
def log_request():
    """请求日志"""
    print(f'[Request] {request.method} {request.path}')


# ============ after_request ============
# 视图函数执行完后执行
# 多个 after_request 从下到上依次执行（倒序）
# 必须接收并返回 response 对象
@app.after_request
def add_security_headers(response):
    """添加安全响应头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


@app.after_request
def add_cors_headers(response):
    """添加 CORS 跨域头"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# ============ teardown_request ============
# 无论视图函数是否执行成功，请求结束时都会执行
# 常用于资源清理和异常日志记录
@app.teardown_request
def teardown_request(exception):
    """请求清理（即使异常也会执行）"""
    if exception:
        print(f'[Error] 请求异常: {exception}')
    print(f'[Teardown] 请求结束: {request.path}')
```

**请求扩展的执行顺序：**

```
before_request 1  -->  before_request 2  -->  视图函数
                                               |
                                               v
                                          after_request 2  (倒序)
                                               |
                                               v
                                          after_request 1  (倒序)
                                               |
                                               v
                                          teardown_request (始终执行)
```

### 11.2 Flask 中间件（WSGI Middleware）

Flask 也支持原生的 WSGI 中间件。请求扩展更适合大多数场景，中间件则适用于更底层、更全局的操作：

```python
from flask import Flask

app = Flask(__name__)


class SimpleMiddleware:
    """简单的 WSGI 中间件"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 请求到达时执行的代码
        print(f'[Middleware] 请求路径: {environ.get("PATH_INFO")}')

        # 调用下一个中间件或 Flask 应用
        return self.app(environ, start_response)


class AuthMiddleware:
    """认证中间件 -- 检查请求头中的 Token"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 从 WSGI 环境变量中获取请求头
        # environ 是 WSGI 标准的请求环境字典
        path = environ.get('PATH_INFO', '')

        # 跳过不需要认证的路径
        if path in ('/login', '/static/'):
            return self.app(environ, start_response)

        # 获取 Authorization 头
        auth = environ.get('HTTP_AUTHORIZATION', '')
        if not auth:
            start_response('401 Unauthorized', [('Content-Type', 'application/json')])
            return [b'{"code": 401, "msg": "Unauthorized"}']

        return self.app(environ, start_response)


# 注册中间件（注意注册顺序：先注册的后执行）
app.wsgi_app = AuthMiddleware(app.wsgi_app)
app.wsgi_app = SimpleMiddleware(app.wsgi_app)
```

### 11.3 信号（Signals）

信号基于 Blinker 库实现观察者模式，允许在框架的特定时机执行自定义代码：

```python
from flask import Flask, render_template
from flask import template_rendered, before_render_template, got_request_exception
from blinker import Namespace

app = Flask(__name__)


# ============ 内置信号列表 ============
# request_started             请求开始时
# request_finished            请求结束时
# before_render_template      模板渲染前
# template_rendered           模板渲染后
# got_request_exception       请求异常时
# request_tearing_down        请求结束时（无论成功与否）
# appcontext_tearing_down     应用上下文结束时
# message_flashed             调用 flash 时


# ============ 使用内置信号 ============
def on_template_before_render(sender, **kwargs):
    """模板渲染前记录日志"""
    template = kwargs.get('template')
    context = kwargs.get('context')
    print(f'[Signal] 准备渲染模板: {template.name}')


def on_template_rendered(sender, **kwargs):
    """模板渲染后"""
    template = kwargs.get('template')
    print(f'[Signal] 模板渲染完成: {template.name}')


# 绑定信号
before_render_template.connect(on_template_before_render)
template_rendered.connect(on_template_rendered)


# ============ 自定义信号 ============
# Flask 自身的 _signals 为私有 API，自定义信号推荐直接使用 blinker.Namespace
my_signals = Namespace()

# 定义信号
user_registered = my_signals.signal('user-registered')


def send_welcome_email(sender, **kwargs):
    """发送欢迎邮件"""
    user = kwargs.get('user')
    print(f'[Signal] 向 {user["email"]} 发送欢迎邮件')


def create_default_profile(sender, **kwargs):
    """创建默认用户配置"""
    user_id = kwargs.get('user_id')
    print(f'[Signal] 为用户 {user_id} 创建默认配置')


# 绑定自定义信号
user_registered.connect(send_welcome_email)
user_registered.connect(create_default_profile)


# 在业务代码中触发信号
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # ... 创建用户的业务逻辑 ...

    # 触发自定义信号
    user_registered.send(app, user=data, user_id=999)

    return jsonify({'msg': '注册成功'})
```

### 11.4 g 对象

`g` 是一个请求级别的全局对象，用于在单次请求中跨函数传递数据：

```python
from flask import Flask, g

app = Flask(__name__)


@app.before_request
def load_current_user():
    """在请求开始前加载当前用户信息到 g 对象"""
    token = request.headers.get('Authorization')
    if token:
        # 模拟从 token 解析用户信息
        g.current_user = {'id': 1, 'name': 'Alice', 'role': 'admin'}
        g.request_id = str(uuid.uuid4())
    else:
        g.current_user = None


def check_permission(required_role):
    """权限检查辅助函数（可直接使用 g 对象）"""
    if not g.current_user:
        return False
    return g.current_user.get('role') == required_role


@app.route('/admin')
def admin_page():
    if not check_permission('admin'):
        return jsonify({'msg': '权限不足'}), 403
    return f'欢迎管理员 {g.current_user["name"]}'


# g 与 session 的区别:
# - g: 仅在当前请求中有效，请求结束即释放
# - session: 可以跨请求持久化（存储在 Cookie 或 Redis 中）
# - flash: 跨请求传递一次性消息，本质基于 session
```

---

## 12. 错误处理

### 12.1 HTTP 错误处理

```python
from flask import Flask, jsonify, render_template

app = Flask(__name__)


# ============ 注册错误处理器 ============

@app.errorhandler(404)
def handle_404(error):
    """处理 404 页面未找到"""
    # 返回 JSON（API 模式）
    if request.path.startswith('/api/'):
        return jsonify({'code': 404, 'msg': '请求的资源不存在'}), 404
    # 返回 HTML 页面
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def handle_403(error):
    return jsonify({'code': 403, 'msg': '没有权限访问'}), 403


@app.errorhandler(405)
def handle_405(error):
    return jsonify({'code': 405, 'msg': '不支持的请求方法'}), 405


@app.errorhandler(500)
def handle_500(error):
    """处理服务器内部错误"""
    # 记录错误日志
    app.logger.error(f'服务器错误: {error}')
    return jsonify({'code': 500, 'msg': '服务器内部错误'}), 500


# ============ 全局异常捕获 ============

@app.errorhandler(Exception)
def handle_exception(error):
    """捕获所有未处理的异常"""
    app.logger.error(f'未捕获异常: {str(error)}', exc_info=True)
    return jsonify({
        'code': 500,
        'msg': '服务器内部错误',
        'error': str(error) if app.debug else '请联系管理员'
    }), 500
```

### 12.2 自定义异常类

```python
from flask import Flask, jsonify


class APIError(Exception):
    """自定义 API 异常"""
    def __init__(self, message, status_code=400, data=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.data = data


class AuthenticationError(APIError):
    """认证异常"""
    def __init__(self, message='认证失败'):
        super().__init__(message, status_code=401)


class PermissionDeniedError(APIError):
    """权限异常"""
    def __init__(self, message='权限不足'):
        super().__init__(message, status_code=403)


class NotFoundError(APIError):
    """资源未找到"""
    def __init__(self, message='资源不存在'):
        super().__init__(message, status_code=404)


class ValidationError(APIError):
    """数据校验异常"""
    def __init__(self, message='数据校验失败', errors=None):
        super().__init__(message, status_code=422, data={'errors': errors})


# 统一处理自定义异常
@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'code': error.status_code,
        'msg': error.message,
    }
    if error.data:
        response['data'] = error.data
    return jsonify(response), error.status_code


# 在视图函数中使用
@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = find_user_by_id(user_id)
    if not user:
        raise NotFoundError(f'用户 {user_id} 不存在')
    if not has_permission(user):
        raise PermissionDeniedError()
    return jsonify(user)
```

---

## 13. RESTful API 开发

### 13.1 使用 Flask-RESTful

```bash
pip install flask-restful
```

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)


# ============ 简单示例 ============
class HelloResource(Resource):
    def get(self):
        return {'code': 200, 'msg': 'Hello RESTful API'}

    def post(self):
        return {'code': 201, 'msg': '创建成功'}


api.add_resource(HelloResource, '/hello')


# ============ 参数解析 ============
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='姓名不能为空')
parser.add_argument('age', type=int, required=True, help='年龄不能为空')
parser.add_argument('email', type=str)


# 模拟数据存储
users = {}
user_counter = 0


# 响应格式化
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'email': fields.String,
}


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id=None):
        """获取单个用户或用户列表"""
        if user_id is not None:
            user = users.get(user_id)
            if not user:
                return {'msg': '用户不存在'}, 404
            return user
        return list(users.values())

    def post(self):
        """创建用户"""
        global user_counter
        args = parser.parse_args()

        user_counter += 1
        user = {
            'id': user_counter,
            'name': args['name'],
            'age': args['age'],
            'email': args.get('email', ''),
        }
        users[user_counter] = user
        return {'code': 201, 'msg': '创建成功', 'data': user}, 201

    @marshal_with(user_fields)
    def put(self, user_id):
        """更新用户"""
        if user_id not in users:
            return {'msg': '用户不存在'}, 404

        args = parser.parse_args()
        users[user_id].update({
            'name': args['name'],
            'age': args['age'],
            'email': args.get('email', ''),
        })
        return users[user_id]

    def delete(self, user_id):
        """删除用户"""
        if user_id not in users:
            return {'msg': '用户不存在'}, 404
        del users[user_id]
        return {'code': 200, 'msg': '删除成功'}


api.add_resource(UserResource,
                 '/users',
                 '/users/<int:user_id>',
                 endpoint='user')

if __name__ == '__main__':
    app.run(debug=True)
```

### 13.2 使用蓝图构建 RESTful API

```python
# apps/api/__init__.py
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


# apps/api/user.py
from flask_restful import Resource, reqparse
from . import api

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)


class UserLogin(Resource):
    def post(self):
        args = user_parser.parse_args()
        # 验证逻辑...
        return {'token': 'xxx', 'user': args['username']}


class UserProfile(Resource):
    def get(self):
        return {'username': 'Alice', 'email': 'alice@example.com'}


api.add_resource(UserLogin, '/login')
api.add_resource(UserProfile, '/profile')
```

### 13.3 手动实现 RESTful API

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据库
tasks = [
    {'id': 1, 'title': '学习 Flask', 'done': False},
    {'id': 2, 'title': '学习 SQLAlchemy', 'done': True},
]
next_id = 3


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表，支持状态过滤"""
    status = request.args.get('status')
    if status == 'done':
        result = [t for t in tasks if t['done']]
    elif status == 'pending':
        result = [t for t in tasks if not t['done']]
    else:
        result = tasks
    return jsonify({'code': 200, 'data': result})


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'code': 404, 'msg': '任务不存在'}), 404
    return jsonify({'code': 200, 'data': task})


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建任务"""
    global next_id
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'code': 400, 'msg': '请提供任务标题'}), 400

    task = {
        'id': next_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'done': False,
    }
    next_id += 1
    tasks.append(task)
    return jsonify({'code': 201, 'data': task}), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'code': 404, 'msg': '任务不存在'}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task.get('description', ''))
    task['done'] = data.get('done', task['done'])
    return jsonify({'code': 200, 'data': task})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'code': 404, 'msg': '任务不存在'}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'code': 200, 'msg': '删除成功'})


# 统一的 JSON 响应
def success_response(data=None, msg='成功'):
    return jsonify({'code': 200, 'msg': msg, 'data': data})

def error_response(msg='失败', code=400):
    return jsonify({'code': code, 'msg': msg}), code
```

---

## 14. 项目部署

### 14.1 使用 Gunicorn 部署（Linux）

```bash
# 安装
pip install gunicorn

# 运行（默认 127.0.0.1:8000）
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 参数说明：
# -w 4         启动 4 个 worker 进程
# -b 0.0.0.0:8000  绑定监听地址和端口
# --timeout 120     请求超时时间
# --access-logfile -  访问日志输出到控制台
# --error-logfile -   错误日志输出到控制台
# --reload           代码变更时自动重启（仅开发环境）
# -k gevent          使用 gevent worker（异步）
```

### 14.2 使用 uWSGI 部署

```bash
# 安装
pip install uwsgi

# 运行
uwsgi --http 0.0.0.0:8000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

**uwsgi.ini 配置文件：**

```ini
[uwsgi]
# 项目配置
chdir = /path/to/your/project
wsgi-file = app.py
callable = app

# 进程和线程
processes = 4
threads = 2

# Socket 配置（配合 Nginx 使用）
socket = 127.0.0.1:8001
# 如果直接对外提供服务则使用 http
# http = 0.0.0.0:8000

# 其他配置
master = true
vacuum = true
pidfile = /tmp/uwsgi.pid
daemonize = /var/log/uwsgi/app.log
stats = 127.0.0.1:9191

# 虚拟环境
# home = /path/to/venv

# 缓冲
buffer-size = 32768
harakiri = 120
max-requests = 5000
```

### 14.3 Nginx 配置

```nginx
server {
    listen 80;
    server_name example.com;

    # 前端静态文件
    location / {
        root /var/www/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    # 静态文件直接由 Nginx 服务
    location /static/ {
        alias /path/to/project/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 上传文件
    location /media/ {
        alias /path/to/project/media/;
    }
}
```

### 14.4 Docker 部署

**Dockerfile：**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

**docker-compose.yml（多容器部署）：**

```yaml
version: "3.8"

services:
  web:
    build: .
    container_name: flask_app
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql://user:password@mysql:3306/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    volumes:
      - ./logs:/app/logs
      - ./media:/app/media
    restart: always

  mysql:
    image: mysql:8.0
    container_name: flask_mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  redis:
    image: redis:7-alpine
    container_name: flask_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

  nginx:
    image: nginx:alpine
    container_name: flask_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/var/www/static
    depends_on:
      - web
    restart: always

volumes:
  mysql_data:
  redis_data:
```

### 14.5 生产环境 Checklist

```python
# 生产环境配置
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # 从环境变量获取，不要硬编码

    # 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_RECYCLE = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_COOKIE_SECURE = True   # 仅 HTTPS
    SESSION_COOKIE_HTTPONLY = True  # 禁止 JS 访问
    SESSION_COOKIE_SAMESITE = 'Lax'

    # 日志
    LOG_LEVEL = 'INFO'

    # 限制上传大小
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

**部署检查清单：**

1. 关闭 DEBUG 模式
2. 使用强随机 SECRET_KEY（从环境变量读取）
3. 启用 HTTPS，配置 SSL 证书
4. 配置合理的日志级别和日志轮转
5. 使用连接池管理数据库连接
6. 设置合理的请求体大小限制
7. 配置 Session Cookie 安全选项
8. 使用 Nginx 反向代理，服务静态文件
9. 添加健康检查接口
10. 配置进程监控（supervisor/systemd）
11. 使用环境变量管理敏感配置，不提交到代码仓库

---

## 附录：Flask 常用第三方扩展

| 扩展 | 说明 | 安装命令 |
|------|------|----------|
| Flask-SQLAlchemy | ORM 数据库操作 | `pip install flask-sqlalchemy` |
| Flask-Migrate | 数据库迁移 | `pip install flask-migrate` |
| Flask-WTF | 表单验证 | `pip install flask-wtf` |
| Flask-Login | 用户认证管理 | `pip install flask-login` |
| Flask-CORS | 跨域支持 | `pip install flask-cors` |
| Flask-Caching | 缓存支持 | `pip install flask-caching` |
| Flask-RESTful | RESTful API | `pip install flask-restful` |
| Flask-Session | 服务端 Session | `pip install flask-session` |
| Flask-Admin | 后台管理界面 | `pip install flask-admin` |
| Flask-Mail | 邮件发送 | `pip install flask-mail` |
| Flask-JWT-Extended | JWT 认证 | `pip install flask-jwt-extended` |
| Flask-SocketIO | WebSocket 支持 | `pip install flask-socketio` |
