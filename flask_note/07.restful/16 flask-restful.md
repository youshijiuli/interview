## Flask-Restful笔记：

### 安装：
```python
pip install flask-restful
```



### 基本使用：
1. 从`flask_restful`中导入`Api`，来创建一个`api`对象。
2. 写一个视图函数，让他继承自`Resource`，然后在这个里面，使用你想要的请求方式来定义相应的方法，比如你想要将这个视图只能采用`post`请求，那么就定义一个`post`方法。
3. 使用`api.add_resource`来添加视图与`url`。
示例代码如下：

```python
from flask imo


class LoginView(Resource):
    def post(self,username=None):
        return {"username":"zhiliao"}

api.add_resource(LoginView,'/login/<username>/','/regist/')
```

注意事项：
* 如果你想返回json数据，那么就使用flask_restful，如果你是想渲染模版，那么还是采用之前的方式，就是`app.route`的方式。
* url还是跟之前的一样，可以传递参数。也跟之前的不一样，可以指定多个url。
* endpoint是用来给url_for反转url的时候指定的。如果不写endpoint，那么将会使用视图的名字的小写来作为endpoint。

#### 对类方法添加装饰器
```python
class Home(Resource):

    method_decorator = {'get':['login_required']
    def get(self):
        pass

    def post(self):
        pass
```

### 参数验证：
Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法的包，叫做reqparse。以下是基本用法：
    ```python
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,help='请输入用户名')
    args = parser.parse_args()
    ```
add_argument可以指定这个字段的名字，这个字段的数据类型等。以下将对这个方法的一些参数做详细讲解： 
1. default：默认值，如果这个参数没有值，那么将使用这个参数指定的值。 
2. required：是否必须。默认为False，如果设置为True，那么这个参数就必须提交上来。 3. type：这个参数的数据类型，如果指定，那么将使用指定的数据类型来强制转换提交上来的值。 
4. choices：选项。提交上来的值只有满足这个选项中的值才符合验证通过，否则验证不通过。 
5. help：错误信息。如果验证失败后，将会使用这个参数指定的值作为错误信息。 
6. trim：是否要去掉前后的空格。

其中的type，可以使用python自带的一些数据类型，也可以使用flask_restful.inputs下的一些特定的数据类型来强制转换。比如一些常用的： 
1. url：会判断这个参数的值是否是一个url，如果不是，那么就会抛出异常。 
2. regex：正则表达式。 
3. date：将这个字符串转换为datetime.date数据类型。如果转换不成功，则会抛出一个异常。


#### 对于定义的字段格式：以格式的字段为主
- 当格式与model对应的字段一致时，即返回预期的格式化的数据。
- 当格式比model字段多时，不存在的字段为默认值None
- 当格式比model字段少，多余的字段不会显示。

对于一个视图函数，你可以指定好一些字段用于返回。以后可以使用ORM模型或者自定义的模型的时候，他会自动的获取模型中的相应的字段，生成json数据，然后再返回给客户端。这其中需要导入flask_restful.marshal_with装饰器,如果函数使用marsha(data,fields)。并且需要写一个字典，来指示需要返回的字段，以及该字段的数据类型。示例代码如下：

```python
class ProfileView(Resource):
    resource_fields = {
        'username': fields.String,
        'age': fields.Integer,
        'school': fields.String
    }

    @marshal_with(resource_fields)
    def get(self,user_id):
        user = User.query.get(user_id)
        return user
```

#### ListField
```python
user_fields = {
    "username":fields.String,
    "age":fields.Integer,
    }
    
dest_data = {
    'status':200,
    'message':'ok',
    'data':[{'u1':1,'age':18},{'u2':2,'age':19}]
}

resource_fields = {
    "status": fields.String,
    "message":fields.String,
    "data":fields.List(fields.Nested(user_fields))
    }
```

在get方法中，返回user的时候，flask_restful会自动的读取user模型上的username以及age还有school属性。组装成一个json格式的字符串返回给客户端。

### 重命名属性：

很多时候你面向公众的字段名称是不同于内部的属性名。使用 attribute可以配置这种映射。比如现在想要返回user.school中的值，但是在返回给外面的时候，想以education返回回去，那么可以这样写：
```python
resource_fields = {
    'education': fields.String(attribute='school')
}
```

### 默认值：
在返回一些字段的时候，有时候可能没有值，那么这时候可以在指定fields的时候给定一个默认值，示例代码如下：
```python
resource_fields = {
    'age': fields.Integer(default=18)
}
```

### 复杂结构：
有时候想要在返回的数据格式中，形成比较复杂的结构。那么可以使用一些特殊的字段来实现。比如要在一个字段中放置一个列表，那么可以使用fields.List，比如在一个字段下面又是一个字典，那么可以使用fields.Nested。以下将讲解下复杂结构的用法：
```python
class ArticleView(Resource):

    resource_fields = {
        'aritlce_title':fields.String(attribute='title'),
        'content':fields.String,
        'author': fields.Nested({
            'username': fields.String,
            'email': fields.String
        }),
        'tags': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        })),
        'read_count': fields.Integer(default=80)
    }

    @marshal_with(resource_fields)
    def get(self,article_id):
        article = Article.query.get(article_id)
        return article
```


### Flask-restful注意事项：
1. 在蓝图中，如果使用`flask-restful`，那么在创建`Api`对象的时候，就不要再使用`app`了，而是使用蓝图。
2. 如果在`flask-restful`的视图中想要返回`html`代码，或者是模版，那么就应该使用`api.representation`这个装饰器来定义一个函数，在这个函数中，应该对`html`代码进行一个封装，再返回。示例代码如下：

```python
@api.representation('text/html')
def output_html(data,code,headers):
    print(data)
    # 在representation装饰的函数中，必须返回一个Response对象
    resp = make_response(data)
    return resp

class ListView(Resource):
    def get(self):
        return render_template('index.html')
api.add_resource(ListView,'/list/',endpoint='list')
```


### 返回值的规范：
```json
{
    "code":200,
    "message": "",
    "data":{
        "name":'xxx',
        "age":'xxx'
    }
}
```

### 状态码的规范：
1. 200：成功。
2. 401：没有授权。
3. 400：参数错误。
4. 500：服务器错误。









## 12. Flask-Restful插件  



#### 12.1 介绍

Flask-Restful是⼀个专⻔⽤来写restful api的⼀个插件。使⽤他可以快速的集
成restful api功能。在app的后台以及纯api的后台中，这个插件可以帮助我们
节省很多时间。当然，如果在普通的⽹站中，这个插件就显得有些鸡肋了，因
为在普通的⽹⻚开发中，是需要去渲染HTML代码的，⽽Flask-Restful在每个
请求中都是返回json格式的数据  



安装

Flask-Restful需要在Flask 0.8以上的版本，在Python2.6或者Python3.3上运
⾏。通过pip install flask-restful即可安装  





定义Restful的视图

如果使⽤Flask-Restful，那么定义视图函数的时候，就要继承⾃
flask_restful.Resource类，然后再根据当前请求的method来定义相应的⽅法。⽐如期望客户端是使⽤get⽅法发送过来的请求，那么就定义⼀个get⽅
法。类似于MethodView  

```
from flask import Flask,render_template,url_for
from flask_restful import Api,Resource

app = Flask(__name__)
# ⽤Api来绑定app
api = Api(app)

class IndexView(Resource):
    def get(self):
        return {"username":"juran"}

api.add_resource(IndexView,'/',endpoint='index')
```



注意事项：

endpoint是⽤来给url_for反转url的时候指定的。如果不写endpoint，那么将
会使⽤视图的名字的⼩写来作为endpoint。
add_resource的第⼆个参数是访问这个视图函数的url，这个url可以跟之前
的route⼀样，可以传递参数。并且还有⼀点不同的是，这个⽅法可以传递多
个url来指定这个视图函数。



参数解析

Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法的包，叫做reqparse  

```
parser = reqparse.RequestParser()
parser.add_argument('username',type=str,help='请输⼊⽤户名')
args = parser.parse_args()
```



add_argument可以指定这个字段的名字，这个字段的数据类型等。

- default：默认值，如果这个参数没有值，那么将使⽤这个参数指定的值。
- required：是否必须。默认为False，如果设置为True，那么这个参数就必须提交上来。
- type：这个参数的数据类型，如果指定，那么将使⽤指定的数据类型来强制转换提交上来的值。
- choices：选项。提交上来的值只有满⾜这个选项中的值才符合验证通过，否则验证不通过。
- help：错误信息。如果验证失败后，将会使⽤这个参数指定的值作为错误信息。
- trim：是否要去掉前后的空格。



输出字段

对于⼀个视图函数，你可以指定好⼀些字段⽤于返回。以后可以使⽤ORM模型
或者⾃定义的模型的时候，他会⾃动的获取模型中的相应的字段，⽣成json数
据，然后再返回给客户端。这其中需要导⼊flask_restful.marshal_with装饰
器。并且需要写⼀个字典，来指示需要返回的字段，以及该字段的数据类型。  

```
class ProfileView(Resource):
    resource_fields = {
        "username": fields.String,
        "age": fields.Integer,
        "school": fields.String,
    }

    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        return user
```

在get⽅法中，返回user的时候，flask_restful会⾃动的读取user模型上的
username以及age还有school属性。组装成⼀个json格式的字符串返回给客户
端。



重命名属性

很多时候你⾯向公众的字段名称是不同于内部的属性名。使⽤ attribute可以配
置这种映射。⽐如现在想要返回user.school中的值，但是在返回给外⾯的时
候，想以education返回回去，那么可以这样写  

```
resource_fields = {
	'education': fields.String(attribute='school')
}
```



默认值

在返回⼀些字段的时候，有时候可能没有值，那么这时候可以在指定fields的时
候给定⼀个默认值  

```
resource_fields = {
	'age': fields.Integer(default=18)
}
```



复杂结构：

有时候想要在返回的数据格式中，形成⽐较复杂的结构。那么可以使⽤⼀些特
殊的字段来实现。⽐如要在⼀个字段中放置⼀个列表，那么可以使⽤
fields.List，⽐如在⼀个字段下⾯⼜是⼀个字典，那么可以使⽤
fields.Nested  

```
class ProfileView(Resource):
    resource_fields = {
        "username": fields.String,
        "age": fields.Integer,
        "school": fields.String,
        "tags": fields.List(fields.String),
        "more": fields.Nested({"signature": fields.String}),
    }
```







#### Restful

1.Restful接口规范
REST 指的是一组架构约束条件和原则。满足这些约束条件和原则的
应用程序或设计就是 RESTful。
RESTful是一种软件架构风格、设计风格，而不是标准，只是提供了
一组设计原则和约束条件。
它主要用于客户端和服务器交互类的软件。基于这个风格设计的软
件可以更简洁，更有层次。
RESTful接口规范是用于在前端与后台进行通信的一套规范。使用这
个规范可以让前后端开发变得更加轻松。



2.适用场景：一个系统的数据库数据，展现的平台有PC端、移动端、app端、ios端。
前端工程师：都遵循RESTful编程规范
后端工程师：都遵循RESTful编程规范
最终结果：开发效率高，便于管理

3.协议：用http或者https协议。



4.数据传输格式：
数据传输的格式应该都用json格式。



5.url链接规则：

url链接中，不能有动词，只能有名词。
并且对于一些名词，如果出现复数，那么应该在后面加s。
比如：获取新闻列表，应该使用 /news/ ，而不应该使用/get_news/



6.HTTP请求方式：
GET：从服务器上获取资源。
POST：在服务器上新增或者修改一个资源。
PUT：在服务器上更新资源。（客户端提供所有改变后的数据）
PATCH：在服务器上更新资源。（客户端只提供需要改变的属性）
DELETE：从服务器上删除资源。



7.状态码：
状态
码 原因描述 描述
200 OK 服务器成功响应客户端的请求。
400 INVALID
REQUEST 用户发出的请求有错误，服务器没有进行新建或修改数据的操作
401 Unauthorized 用户没有权限访问这个请求
403 Forbidden 因为某些原因禁止访问这个请求
404 NOT FOUND 用户请求的url不存在
406 NOT
Acceptable
用户请求不被服务器接收（比如服务器期望客户端发送某个字段，
但是没有发送）。
500 Internal server
error 服务器内部错误，比如遇到bug





#### 基本使用

1.介绍：
优势：
Flask-Restful是一个专门用来写restful api的一个插件。
使用它可以快速的集成restful api接口功能。
在系统的纯api的后台中，这个插件可以帮助我们节省很多时间。
缺点：
如果在普通的网站中，这个插件就没有优势了，因为在普通的网站
开发中，是需要去渲染HTML代码的，
而Flask-Restful在每个请求中都是返回json格式的数据。
2.安装：
3.基本使用：

定义Restful的类视图：

1. 从 flask_restful 中导入 Api ，来创建一个 api 对象。
2. 写一个类视图，让他继承自 Resource 类，然后在这个里面，使用
	你想要的请求方式来定义相应的方法，比如你想要将这个类视图只
	能采用 post 请求，那么就定义一个 post 方法。
3. 使用 api.add_resource 来添加类视图与 url

```
from flask import Flask,url_for
# pip install flask-restful
from flask_restful import Resource,Api


app = Flask(__name__)
# 建立Api对象，并绑定应用APP
api = Api(app)

class LoginView(Resource):
    def get(self):
        return {"flag":True}
    def post(self):
        return {"flag":False}

# 建立路由映射
# api.add_resource(LoginView,'/login/')
api.add_resource(LoginView,'/login/','/login2/',endpoint='login')

with app.test_request_context():
    # werkzeug.routing.BuildError: Could not build url for endpoint 'LoginView'.
    # Did you mean 'loginview' instead?
    # 默认没有写endpoint反向url_for函数通过小写函数名
    # 如果有多个url，会返回第1个URL
    # print(url_for('loginview'))
    print(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```





注意：

如果你想返回json数据，那么就使用flask_restful，如果你是想渲染模版，那么还是采用之前
的方式，就是 app.route 的方式。

url还是跟之前的一样，可以传递参数。也跟之前的不一样，可以指定多个url。2

endpoint是用来给url_for反转url的时候指定的。如果不写endpoint，那么将会使用视图的
名字的小写来作为endpoint。

add_resource的第二个参数是访问这个视图函数的url，这个url可以跟之前的route一样，可
以传递参数，并且还有一点不同的是，这个方法可以传递多个url来指定这个视图函数







#### Flask_RESTful参数验证



参数验证
参数验证也叫参数解析
Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法
的包，叫做reqparse。
基本用法
1 通过 flask_restful.reqparse 中 RequestParser 建立解析器
2 通过 RequestParser 中的 add_argument 方法定义字段与解析规则
3 通过 RequestParser 中的 parse_args 来解析参数
解析正确，返回正确参数1
解析错误，返回错误信息给前端



```
from flask import Flask
from flask_restful import Api,Resource
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
api = Api(app)

class RegisterView(Resource):
    def post(self):
        # 建立解析器
        parser = RequestParser()
        # 定义数据的解析规则
        parser.add_argument('uname',type=str,required=True,help='用户名验证错误',trim=True)
        # 解析数据
        args = parser.parse_args()
            # 正确，直接获取参数
        print(args)
            # 错误，回馈到前端
        
        # 响应数据
        return {'msg':'注册成功！！'}
# 建立映射关系
api.add_resource(RegisterView,'/register/')

if __name__ == '__main__':
    app.run(debug=True)
```





add_argument方法参数详解

add_argument方法可以指定这个字段的名字，这个字段的数据类
型等，验证错误提示信息等，具体如下：
1 default：默认值，如果这个参数没有值，那么将使用这个参数
指定的默认值。
2 required：是否必须。默认为False，如果设置为True，那么这
个参数就必须提交上来。
3 type：这个参数的数据类型，如果指定，那么将使用指定的数
据类型来强制转换提交上来的值。可以使用python自带的一些
数据类型(如str或者int)，也可以使用flask_restful.inputs下的一
些特定的数据类型来强制转换。
url：会判断这个参数的值是否是一个url，如果不是，那么就会抛出异常。
regex：正则表达式。
date：将这个字符串转换为datetime.date数据类型。如果转换不成功，则会抛出一个异常.
4 choices：固定选项。提交上来的值只有满足这个选项中的值才
符合验证通过，否则验证不通过。
5 help：错误信息。如果验证失败后，将会使用这个参数指定的
值作为错误信息。
6 trim：是否要去掉前后的空格。
代码案例

```
from flask import Flask
from flask_restful import Api,Resource,inputs
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
api = Api(app)

class RegisterView(Resource):
    def post(self):
        # 建立解析器
        parser = RequestParser()
        # 定义解析规则
        parser.add_argument('uname',type=str,required=True,trim=True,help='用户名不符合规范')
        parser.add_argument('pwd',type=str,help='密码错误',default='123456')
        parser.add_argument('age',type=int,help='年龄验证错误！')
        parser.add_argument('gender',type=str,choices=['男', '女','保密'],help='性别验证错误')
        parser.add_argument('birthday',type=inputs.date,help='生日验证错误')
        parser.add_argument('phone',type=inputs.regex('^1[356789]\d{9}$'),help='电话验证错误')
        parser.add_argument('homepage',type=inputs.url,help='个人主页验证错误')
        # 解析数据
        args = parser.parse_args()
        print(args)
        return {'msg':'注册成功！'}
    
api.add_resource(RegisterView,'/register/')

if __name__ == '__main__':
    app.run(debug=True)
```







#### Flask_RESTful规范返回值



对于一个类视图，可以指定好一些字段做标准化用于返回。
以后使用ORM模型或者自定义模型的时候，他会自动的获取模型中
的相应的字段，
生成json格式数据，然后再返回给客户端。

使用方法

- 导入 flask_restful.marshal_with 装饰器
- 定义一个字典变量来指定需要返回的标准化字段，以及该字段的数据类型

在请求方法中，返回自定义对象的时候，flask_restful会自动的读
取对象模型上的所有属性。
组装成一个符合标准化参数的json格式字符串返回给客户端



```
from flask import Flask
from flask_restful import Api,Resource,fields,marshal_with


app = Flask(__name__)
api = Api(app)

class News:
    def __init__(self,code,msg,state,content):
        self.code = code
        self.msg = msg
        self.state1 =state
        self.content = content

class NewsView(Resource):
    resouce_fields ={
        'code':fields.Integer,
        'msg':fields.String,
        'state':fields.String
    }

    @marshal_with(resouce_fields)
    def get(self):
        return {'code':200,'msg':'访问成功！','state':'移动'}

    @marshal_with(resouce_fields)
    def post(self):
        return {'msg':'注册成功！'}
    @marshal_with(resouce_fields)
    def put(self):
        # 在返回对象时，会自动在对象中获取与约定好的字段，并获取封装成json。
        news = News(404, 'OK', '电脑端','尚学堂')
        return news
    
api.add_resource(NewsView,'/news/')

if __name__ == '__main__':
    app.run(debug=True)
```







#### Flask_RESTful规范返回值-参数设置



设置重命名属性和默认值

```
问题
规范给出的属性名和模型内部的属性名不相同
解决方案
使用 attribute 配置这种映射,比如： fields.String(attribute='username')

问题
某些字段，没有值，但想给一个值做为默认值
解决方案
使用 default 指定默认值，比如： fields.String(default='sxt')

```



```
from flask import Flask
from flask_restful import Api,Resource,fields,marshal_with


app = Flask(__name__)
api = Api(app)

class News:
    def __init__(self,code,msg,info):
        self.code = code
        self.msg = msg
        self.info = info
        self.state = 1000
class NewsView(Resource):
    resouce_fields ={
        'code':fields.Integer(default=200),# 通过参数default来设置默认值
        'msg':fields.String, 
        'content':fields.String(attribute='info'),  # 通过参数attribute来设置提取数据的字段
        'state':fields.Integer(default=2000) # 优先级不如真实数据里面的高
    }

    @marshal_with(resouce_fields)
    def get(self):
        news = News(200,'访问成功！','移动')
        return news

    @marshal_with(resouce_fields)
    def post(self):
        return {'msg':'增加数据成功！','info':'联通'}


    
    @marshal_with(resouce_fields)
    def put(self):
        news = News(200,'访问成功！','移动')
        return news
api.add_resource(NewsView,'/news/')

if __name__ == '__main__':
    app.run(debug=True)
```





#### Flask_RESTFul规范返回值-类型设置

大型的互联网项目中，返回的数据格式，有时是比较复杂的结构。
如：豆瓣电影
https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=20&limit=20
返回的值里有json或者列表数据，这时可以通过以字段来实现
fields.List 放置一个列表
fields.Nested放置一个字典

```python
from flask import Flask
from flask_restful import Api,Resource,fields,marshal_with

app = Flask(__name__)
api = Api(app)

class User:
    def __init__(self,uname):
        self.uname = uname
   
    def __repr__(self):
        return f'<User uname:{self.uname}>'

class NewsType:
    def __init__(self,_type):
        self._type = _type

    def __repr__(self):
        return f'<User type:{self._type}>'
class News:
    def __init__(self,code,msg):
        self.code = code
        self.msg = msg
        self.user = None
        self._type = []

    def __repr__(self):
        return f'<News code:{self.code} msg:{self.msg} user:{self.user} type:{self._type}>'

def create_data():
    user = User('尚学堂')
    _type1 = NewsType('IT')
    _type2 = NewsType('Python')
    news = News(200,'Python又双叕更新了！')
    news.user = user
    news._type.append(_type1)
    news._type.append(_type2)

    return news
class NewsView(Resource):
    resouce_fields ={
        'code':fields.Integer,
        'msg':fields.String,
        'user':fields.Nested({
            'uname':fields.String
        }),
        '_type':fields.List(fields.Nested({
            '_type':fields.String
        }))
    }

    @marshal_with(resouce_fields)
    def get(self):
        news = create_data()
        return news

api.add_resource(NewsView,'/news/')

if __name__ == '__main__':
    app.run(debug=True)
    # print(create_data())

```





#### Flask_RESTful结合蓝图使用

Flask_RESTful结合蓝图使用
在蓝图中，如果使用Flask_RESTful，
创建Api对象的时候，传入蓝图对象即可，不再是传入 app 对象



user/

```
init.py

from flask.blueprints import Blueprint

user_bp = Blueprint('user',__name__)

from user import views


views.py

from flask import Flask


app = Flask(__name__)

from user import user_bp
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
```



app.py

```
from flask import Flask


app = Flask(__name__)

from user import user_bp
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
```









Flask_RESTful渲染模版



渲染模版就是在Flask_RESTful的类视图中要返回html片段代码，或
者是整个html文件代码。
如何需要浏览器渲染模板内容应该使用 api.representation 这个装饰器来定
义一个函数，
在这个函数中，应该对 html 代码进行一个封装，再返回。

```
注意
api.representation装饰器修饰的函数必须返回一个Response
对象


```





```
from flask import Flask,render_template,Response
from flask_restful import Api,Resource
import json

app = Flask(__name__)
# 如果想要前端的中文不再是\u这样的编码，可以加如下参数配置
app.config['RESTFUL_JSON'] = dict(ensure_ascii=False)
api = Api(app)

class HomeView(Resource):
    def get(self):
        return {"msg":"这个是个人主页"}


class IndexView(Resource):
    def get(self):
        return render_template('index.html')

api.add_resource(IndexView,'/index/')
api.add_resource(HomeView,'/home/')

@api.representation('text/html')
def out_html(data,code,headers):
    # 必须返回一个response对象
    if isinstance(data, str):
        resp = Response(data)
        return resp
    else:
        return Response(json.dumps(data,ensure_ascii=False).encode('gbk'))

if __name__ == '__main__':
    app.run(debug=True)
```



```
<body>
    <h1>这个是模板的内容</h1>
</body>
```

