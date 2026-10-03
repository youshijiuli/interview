# Flask-RESTful

> Flask-RESTful是一个用于构建RESTful API的扩展库，它基于Flask框架，并提供了一组简单易用的工具和功能，帮助开发者更轻松地构建和管理RESTful风格的Web服务。

主要特点和功能：

```css
1.简单易用：Flask-RESTful提供了一组简单易用的工具和约定，可以帮助开发者快速构建RESTful API。

2.支持多种数据格式：Flask-RESTful支持多种常见的数据格式，如JSON、XML、HTML等，可以根据客户端的需求返回相应的数据格式。

3.路由映射：Flask-RESTful支持使用Python装饰器来定义路由映射，可以方便地将API资源和URL路径进行对应。

4.请求解析：Flask-RESTful可以自动解析HTTP请求参数，支持从URL中获取参数、从请求体中获取参数、从查询字符串中获取参数等方式。

5.响应构建：Flask-RESTful可以自动构建HTTP响应，支持自定义响应头、状态码和响应体等。

6.异常处理：Flask-RESTful内置了一些常见的HTTP异常类型（如404、500等），并提供了自定义异常类型的接口，可以方便地处理各种错误情况。

7.安全性：Flask-RESTful提供了一些常用的安全机制，如基本认证、Token认证等，可以保障API的安全性。
```



## 基本使用

#### 安装

> 在使用Flask-RESTful时，需要确保开发环境中已经安装了Flask和Flask-RESTful。

```python
pip install flask

pip install flask-restful
```



#### 定义资源Resources

> 在Flask-RESTful中，资源是API的核心组件，代表了要提供的数据或功能。每个资源都是一个Python类，继承自Flask-RESTful提供的Resource基类。

> 在资源类中，可以定义各种HTTP方法（如GET、POST、PUT、DELETE等），并在每个方法中编写相应的逻辑来处理对应的请求。

```python
# ⾃定义视图类，必须继承⾃Resource
class TestResource(Resource):
	# 定义请求⽅法
	# 处理GET请求的逻辑
    def get(self):
        return {'method': 'get'}

	# 处理POST请求的逻辑
    def post(self):
        return {'method': 'post'}
```



#### 创建API实例

> 使用Flask-RESTful的Api类创建一个API实例，并将其与Flask应用关联起来。

```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
# Api⽤来在Flask中创建接⼝
api = Api(app)
```

#### 添加资源到API

> 使用API实例的add_resource方法将定义的资源添加到API中，并指定其对应的URL路径。当客户端请求`/test`路径时，Flask-RESTful将会调用TestResource类中相应HTTP方法的逻辑。

```python
# 添加路由
api.add_resource(TestResource, '/test')
```



#### 运行Flask应用

> 使用Flask的run方法运行应用。

```python
if __name__ == '__main__':
    app.run(debug=True)
```





## 请求处理

#### 请求解析

> 请求解析是指从客户端的请求中提取和解析参数的过程。Flask-RESTful提供了reqparse模块来帮助进行请求解析。可以使用RequestParser类来定义请求参数，并在资源类中使用它进行解析。

1.定义一个名为name的请求参数，指定参数类型为字符串、必需参数，并提供了一个帮助信息，同时描述参数应该在请求数据中出现的位置。

2.在post方法中，通过`parser.parse_args()`解析请求中的参数，并使用`args['name']`获取name参数的值。

```python
from flask_restful import reqparse

# 创建RequestParser对象
parser = reqparse.RequestParser()
# 向RequestParser对象中添加需要检验或转换的参数声明
parser.add_argument('name', type=int, required=True, help='rate is required', location='args')
parser.add_argument('age')

class MyResource(Resource):
    def post(self):
    	# 使用parse_args()方法检验处理
        args = parser.parse_args()
        # 检验之后从检验结果中获取参数时可按照字典操作或对象属性操作
		print(args.name)
		print(args['name'])
```

## 参数校验

1.required：`描述请求是否一定要携带对应参数，默认值为False`

> False不强制要求携带，在客户端请求未携带参数时，取出值为None
>
> True强制要求携带，若未携带，则校验失败，向客户端返回错误信息，状态码400



```python
class TestResource(Resource):
    def get(self):
        rp = RequestParser()
        rp.add_argument('name', required=True)
        rp.add_argument('age', required=False)
        args = rp.parse_args()
        return {'name': args.name, 'age': args.age}
```

发送Json数据

```python
{"name":"Python","age":20}
```

2.help：`参数检验错误时返回的错误描述信息`

```python
rp.add_argument('name', required=True, help='名称不能为空')
```

3.action：`描述对于请求参数中出现多个同名参数时的处理方式`

```ini
ini

代码解读
复制代码action='store' 保留出现的第一个， 默认

action='append' 以列表追加保存所有同名参数的值
python

代码解读
复制代码rp.add_argument('name', required=True, help='名称不能为空', action='append')
python

代码解读
复制代码{
	"name": [
		"Python"
	],
	"age": 20
}
```

4.type：`描述参数应该匹配的类型，可以使用python的标准数据类型string、int，也可使用Flask-RESTful提供的检验方法，还可以自己定义`

**1.标准类型**

```python
python

代码解读
复制代码rp.add_argument('name', type=str, required=True, help='名称不能为空', action='append')
```

**2.Flask-RESTful提供**

检验类型方法在flask_restful.inputs模块中

```python
python

代码解读
复制代码rp.add_argument('url', type=inputs.url)
scss

代码解读
复制代码regex(指定正则表达式)
python

代码解读
复制代码from flask_restful import inputs

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
rp.add_argument('name', type=inputs.regex(email_pattern))
```

natural 自然数0、1、2、3...

```python
python

代码解读
复制代码rp.add_argument('age', type=inputs.natural)
```

positive 正整数 1、2、3...

```python
python

代码解读
复制代码rp.add_argument('age', type=inputs.positive)
```

int_range(low ,high) 整数范围

```python
python

代码解读
复制代码rp.add_argument('age', type=inputs.int_range(0, 120))
```

boolean

```python
python

代码解读
复制代码rp.add_argument('tag', type=inputs.boolean)
```

**3.自定义**

```python
python

代码解读
复制代码def email_check(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    else:
        raise ValueError('邮箱：{} 格式错误'.format(email))

class TestResource(Resource):
    def get(self):
        rp = RequestParser()
        rp.add_argument('email', type=email_check)
        args = rp.parse_args()
        return {'msg': 'OK'}
```

5.location：`描述参数应该在请求数据中出现的位置`

```python
python

代码解读
复制代码# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From json
parser.add_argument('user_id', location='json')

# From file uploads
parser.add_argument('picture', location='files')
```

也可指明多个位置

```python
python

代码解读
复制代码parser.add_argument('text', location=['headers', 'json'])
```

# 响应处理

## 数据序列化

> Flask-RESTful 提供了一个名为`marshal`的工具，用于将 Python 对象序列化为 JSON 格式。使用 Flask-RESTful 中的序列化功能，可以在编写 RESTful API 时方便地将 Python 对象转换为 JSON 格式，并根据需要包含或排除某些字段。

定义一个字典`resource_fields`，用于描述待序列化数据的结构和类型。然后通过调用`marshal `方法或者使用`@marshal_with装饰器`将user 对象序列化为 JSON 格式

```python
python

代码解读
复制代码from flask import Flask
from flask_restful import Api, marshal
from flask_restful import Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

# 数据对象类
class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


resource_fields = {
    'name': fields.String,
    'age': fields.Integer,
}


# 使用装饰器
class TestResource1(Resource):
    @marshal_with(resource_fields, envelope='user')
    def get(self):
        user = User('Python', 22)
        return user


# 不使用装饰器
class TestResource2(Resource):
    def get(self):
        user = User('Java', 22)
        return marshal(user, resource_fields, envelope='user')


api.add_resource(TestResource1, '/test1')
api.add_resource(TestResource2, '/test2')
```

浏览器访问：`http://127.0.0.1:5000/test1`

```python
python

代码解读
复制代码{
    "user": {
        "name": "Python",
        "age": 22
    }
}
```

注意：除了简单的字段类型之外，Flask-RESTful还支持自定义字段、嵌套字段等高级特性，可以满足更加复杂的序列化需求。

## 定制返回格式

> Flask-RESTful的Api对象提供了一个representation的装饰器，允许定制返回数据的呈现格式

源码: `from flask_restful.representations.json import output_json`

```python
python

代码解读
复制代码from __future__ import absolute_import
from flask import make_response, current_app
from flask_restful.utils import PY3
from json import dumps


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
```

使用representation的装饰器，同时进行代码改动即可。

```python
python

代码解读
复制代码from json import dumps

from flask import Flask, current_app, make_response
from flask_restful import Api
from flask_restful import Resource
from flask_restful.utils import PY3

app = Flask(__name__)
api = Api(app)


@api.representation('application/json')
def response_json(data, code, headers=None):
    if 'message' not in data:
        data = {
            'msg': 'OK',
            'data': data
        }

    settings = current_app.config.get('RESTFUL_JSON', {})

    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# 使用装饰器
class TestResource1(Resource):
    def get(self):
        return {"name": "Python"}

api.add_resource(TestResource1, '/')
```

![在这里插入图片描述](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5501eed1fe7d4518b6634b29838a2a33~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

# 其他功能

## 蓝图

> 蓝图是一种将路由放入可重用模块的方法。蓝图允许您将路由和视图功能组织到单独的模块中，以便于管理和维护。使用蓝图可以更好地组织代码，并使其更易于扩展和重用。

创建一个名为`user_bp`的蓝图。然后定义一个`/users`资源，使用`app.register_blueprint()` 方法将 `user_bp`蓝图注册到应用程序中，并指定 URL 前缀为` /api`。这意味着` /users` 路由现在将成为` /api/users`。

```python
python

代码解读
复制代码from flask import Flask, Blueprint
from flask_restful import Api, Resource

app = Flask(__name__)

# 创建一个蓝图对象
user_bp = Blueprint('user', __name__)

# 把蓝图对象添加的api接⼝中
user_api = Api(user_bp)

# ⾃定义视图类，必须继承⾃Resource
class TestResource(Resource):
	# 定义请求⽅法
    def get(self):
        return {'name': 'Python'}

# 添加蓝图路由
user_api.add_resource(TestResource, '/users')

# 在应用对象上注册这个蓝图对象
app.register_blueprint(user_bp, url_prefix='/api')
```

## 装饰器集合

> 在Flask-RESTful 中，method_decorators是一个装饰器集合，用于添加到资源方法上。这些装饰器将在调用资源方法之前执行，可以用来实现各种功能，例如身份验证、权限检查或者日志记录等。

> 具体来说，当使用`@method_decorators`修饰一个资源类中的方法时，这些装饰器将会被应用到该方法上。每个装饰器都可以对请求进行处理，在所有的装饰器都执行完毕后，才会真正地调用方法并返回响应结果。

1.为类视图中的所有方法添加装饰器

> 当在类中使用 method_decorators 时，所有方法都将使用该属性中指定的装饰器进行装饰。

定义两个装饰器 test1和 test2，然后创建了一个 TestResource类，并将两个装饰器添加到 method_decorators 列表中。这意味着在调用 TestResource类的任何方法时，都会先调用 test1装饰器，然后再调用 test2装饰器。

```python
python

代码解读
复制代码from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def test1(fun):
    def wrapper(*args, **kwargs):
     	# 在这里添加第一个装饰器逻辑
        print('test1')
        return fun(*args, **kwargs)
    return wrapper


def test2(fun):
    def wrapper(*args, **kwargs):
    	# 在这里添加第二个装饰器逻辑
        print('test2')
        return fun(*args, **kwargs)
    return wrapper


class TestResource(Resource):
    method_decorators = [test1, test2]

    def get(self):
        return {'method': 'get'}

    def post(self):
        return {'method': 'post'}


api.add_resource(TestResource, '/')
python

代码解读
复制代码test2
test1
```

> 如果需要在特定方法上覆盖默认的装饰器，可以使用 decorators 属性。

例如，以下代码只对 get() 方法应用 test1装饰器：

```python
python

代码解读
复制代码class TestResource(Resource):
    method_decorators = [test1, test2]

    @decorators=[test1]
    def get(self):
        # 处理 GET 方法，并使用 test1装饰器
```

2.为类视图中不同的方法添加不同的装饰器

```python
python

代码解读
复制代码from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def test1(fun):
    def wrapper(*args, **kwargs):
        print('test1')
        return fun(*args, **kwargs)
    return wrapper


def test2(fun):
    def wrapper(*args, **kwargs):
        print('test2')
        return fun(*args, **kwargs)
    return wrapper


class TestResource(Resource):
    method_decorators = {
        'get': [test1, test2],
        'post': [test2]
    }

    # 使用test1 test2两个装饰器
    def get(self):
        return {'method': 'get'}

    # 使用test2装饰器
    def post(self):
        return {'method': 'post'}

    # 未使用装饰器
    def put(self):
        return {'method': 'put'}
```

## 路由命名规范

在 Flask-RESTful 中，路由命名应该遵循 RESTful API 设计规范。通常情况下，可以将资源名称作为路由的一部分

```python
python

代码解读
复制代码from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, user_id):
        # 获取用户信息
        pass

    def post(self):
        # 创建新用户
        pass

    def put(self, user_id):
        # 更新用户信息
        pass

    def delete(self, user_id):
        # 删除用户
        pass

api.add_resource(User, '/users', '/users/<int:user_id>')
```

`/users`代表所有的用户列表，`/users/<int:user_id> `则代表单个用户的详细信息。这样的设计符合 RESTful API 的理念。

此外，为了更好地区分 HTTP 方法，还可以使用以下常用的命名方式：

```perl
perl

代码解读
复制代码list_ + 资源名称：获取资源列表
create_ + 资源名称：创建新资源
read_ + 资源名称：读取单个资源
update_ + 资源名称：更新单个资源
delete_ + 资源名称：删除单个资源
python

代码解读
复制代码class UserList(Resource):
    def get(self):
        # 获取用户列表
        pass
    
    def post(self):
        # 创建新用户
        pass

class User(Resource):
    def get(self, user_id):
        # 获取单个用户信息
        pass

    def put(self, user_id):
        # 更新单个用户信息
        pass

    def delete(self, user_id):
        # 删除单个用户
        pass

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')
```

## 路由名称

> 在 Flask 中，`endpoint`是一个字符串，用于唯一标识一个视图函数。当我们定义路由时，可以通过 `endpoint `参数为这个路由指定一个名称，以便在其他地方引用它。

```python
python

代码解读
复制代码from flask import Flask, url_for

app = Flask(__name__)

@app.route('/home', endpoint='home')
def index():
    return 'Hello, World!'

with app.test_request_context():
    print(url_for('home'))  # 输出：/home
```

注意：

> 如果没有指定 endpoint 参数，Flask会根据视图函数的名称自动生成一个默认的endpoint名称。但是，如果有多个视图函数的名称相同，那么它们的默认endpoint名称也会相同，可能会导致混淆。因此，在实际开发中，最好始终使用 endpoint 参数为路由起一个明确的名称，以避免出现问题。