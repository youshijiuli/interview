# Flask-RESTful风格编程

## 一、什么是RESTful的风格编程

​		在前后端不分离的应用模式中，前端页面看到的效果都是由后端控制，由后端渲染页面或重定向，也就是后端需要控制前端的展示，前端与后端的耦合度很高。

​		这种应用模式比较适合纯网页应用，但是当后端对接App时，App可能并不需要后端返回一个HTML网页，而仅仅是数据本身，所以后端原本返回网页的接口不再适用前端App应用。为了对接App后端还需要开发一套接口。

![前后端不分离模式](E:\PythonLearning\WebPro\FlaskProjectLearing\ThirdLearningFlask\FlaskProject16-Flask的RESTful\前后端不分离模式.png)



​		在前后端分离的应用模式中，后端仅返回前端所需的数据，不再渲染HTML页面，不再控制前端的效果。至于前端用户看到什么效果，从后端请求的数据如何加载到前端中，都由前端自己决定，网页有网页的处理方式，App有App的处理方式，但无论哪种前端，所需的数据基本相同，后端仅需开发一套逻辑对外提供数据即可。



![前后端分离模式](E:\PythonLearning\WebPro\FlaskProjectLearing\ThirdLearningFlask\FlaskProject16-Flask的RESTful\前后端分离模式.png)

RESTful是一种网络应用程序的设计风格和开发方式，基于HTTP，可以使用XML格式定义或JSON格式定义。RESTful适合于移动互联网厂商作为业务使能接口的场景。

**RESTful特点包括：**

1. 每一个URI代表一个资源

2. 客户端使用GET、POST、PUT、DELETE这四种操作方式的动词对服务端资源进行操作

   - GET是用来获取资源（查）

   - POST是用来新建资源（增）
   - PUT用来更新资源（改）
   - DELETE用来删除资源（删）

3. 通过操作资源的表现形式来操作资源

4. 资源的表现形式是**JSON（主流）**或**XML（已经被淘汰了）**

5. 客户端与服务器之间的交互在请求之间是无状态的，从客户端到服务端的每个请求都必须包含理解请求所必需的信息。

比如：（POST/PUT/GET/DELETE）http://127.0.0.1:5000/book/book_content?id=1

## 二、RESTful风格的软件架构

​		RESTful架构是对MVC架构改进后所形成的一种架构。通过使用事先定义好的接口与不同的服务联系起来、在RESTful架构中，客户端使用POST，DELETE，PUT和GET四种请求方式分别对指定的URL资源进行增删改查操作。因此RESTful是通过URI实现对资源的管理及访问，具有扩展性强，结构清晰的特点。

​		RESTful架构将服务器分成前端服务器和后端服务器两个部分。前端服务器为用户提供无模型的视图。后端服务器为前端服务器提供接口，浏览器向前端服务器请求视图，通过视图中包含的Ajax函数发起接口请求获取模型。

​		项目开发引入RESTful架构，利于团队并行开发。在RESTful架构中，将多数HTTP请求转移前端服务器上，降低服务器的负荷，使视图获取后端模型失败也能呈现。但RESTful架构却不适用于所有项目，当项目比较小时无需使用RESTful架构，项目变得更加复杂。





## 三、安装和使用

安装插件：

```bash
pip install flask-restful
```

注册插件的三个步骤：

```python
# 1. 导包
from flask_restful import Api

# 2. 实例化
api = Api()

# 3. 绑定
api.init_app(app)
```

创建Resource实现类视图：

```python
class HelloRESTful(Resource):
    
    def get(self):
        return {"data": "hello GET"}
    def post(self):
        return {"data": "hello POST"}
```

创建类视图后，路由和视图就分离了。所以必须要额外的添加路由。

```python
api.add_resource(HelloRESTful, '/hello')
```

上面是在没有蓝图的情况下的使用示例，接下来在蓝图中使用：

```python
# 从flask模块导入Flask和Blueprint类
from flask import Flask, Blueprint
# 从flask_restful模块导入Api和Resource类
from flask_restful import Api, Resource

# 创建一个Flask应用实例
app = Flask(__name__)

# 创建一个名为'user'的蓝图实例，用于组织用户相关的路由
user_bp = Blueprint('user', __name__)

# 使用蓝图实例创建一个API对象
user_api = Api(user_bp)

# 定义一个资源类HelloWorld，继承自Resource
class HelloWorld(Resource):
    # 定义GET请求的处理函数
    def get(self):
        # 返回一个简单的JSON响应，包含消息'hello get'
        return {'msg': 'hello get'}
    
    # 定义POST请求的处理函数
    def post(self):
        # 返回一个简单的JSON响应，包含消息'post get'
        return {'msg': 'hello post'}
    
# 将HelloWorld资源类添加到API中，并指定其URL路径为根路径'/user/hello'
user_api.add_resource(HelloWorld, '/user/hello')

# 注册'user'蓝图
app.register_blueprint(user_bp)

```

**注意**：如果蓝图里面有`url_prefix`，那么请求`url` = `url_prefix` + `resource_url`