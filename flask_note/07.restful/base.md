# flask-restful



```
1. Restful Api
    1.1 restful api是用于在前端与后台进行通信的一套规范。使用这个规范可以让前后端开发变得更加轻松。以下将讨论这套规范的一些设计细节。
    1.2 采用http或者https协议。
    1.3 数据之间传输的格式应该都使用json，而不使用xml。
    1.4 url连接中，不能有动词，只能有名词。并且对于一些名词，如果出现复数，那么应该在后面加s。
2. HTTP请求的方法
    2.1 GET：从服务器上获取资源。
    2.2 POST：在服务器上新创建一个资源。
    2.3 PUT：在服务器上更新资源。（客户端提供所有改变后的数据）
    2.4 PATCH：在服务器上更新资源。（客户端只提供需要改变的属性）
    2.5 DELETE：从服务器上删除资源。
3. 状态码
    3.1 200：OK，服务器成功响应客户端的请求。
    3.2 400：INVALID REQUEST用户发出的请求有错误，服务器没有进行新建或修改数据的操作。
    3.3 401：Unauthorized，用户没有权限访问这个请求
    3.4 403：Forbidden，因为某些原因禁止访问这个请求。
    3.5 404：NOT FOUND，用户发送的请求的url不存在
    3.6 406：NOT Acceptable，用户请求不被服务器接收（比如服务器期望客户端发送某个字段，但是没有发送）。
    3.7 500：Internal server error，服务器内部错误，比如出现了bug。
4. 安装
    4.1 Flask-Restful需要在Flask 0.8以上的版本，在Python2.6或者Python3.3上运行。通过pip install flask-restful即可安装。I
5. 定义Restful的视图
    5.1 如果使用Flask-Restful，那么定义视图函数的时候，就要继承自f1ask_restful.Resource类，然后再根据当前请求的method来定义相应的方法。比如期望客户端是使用get方法发送过来的请求，那么就定义一个get方法。类似于Methodview。
        5.1.1 从flask_restful中导入Api，来创建一个api对象。
        5.1.2 写一个视图函数，让他继承自Resource，然后在这个里面，使用你想要的请求方式来定义相应的方法，比如你想要将这个视图只能采用post请求，那么就定义一个post方法。
        5.1.3 使用api.add_resource来添加视图与url。
    5.2 endpoint是用来给ur1_for反转ur1的时候指定的。如果不写endpoint，那么将会使用视图的名字的小写来作为endpoint。
    5.3 add-resource的第二个参数是访问这个视图函数的url，这个url可以跟之前的route一样，可以传递参数。并且还有一点不同的是，这个方法可以传递多个url来指定这个视图函数。
6. 参数解析
    6.1 Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法的包，叫做reqparse。
    6.2 add_argument可以指定这个字段的名字，这个字段的数据类型等。
        6.2.1 default：默认值，如果这个参数没有值，那么将使用这个参数指定的值。
        6.2.2 required：是否必须。默认为False，如果设置为True，那么这个参数就必须提交上来。
        6.2.3 type：这个参数的数据类型，如果指定，那么将使用指定的数据类型来强制转换提交上来的值。
        6.2.4 choices：选项。提交上来的值只有满足这个选项中的值才符合验证通过，否则验证不通过。
        6.2.5 help：错误信息。如果验证失败后，将会使用这个参数指定的值作为错误信息。
        6.2.6 trim：是否要去掉前后的空格。
        6.2.7 其中的type，可以使用python自带的一些数据类型，也可以使用flask_restful.inputs下的一些特定的数据类型来强制转换。url：会判断这个参数的值是否是一个url，如果不是，那么就会抛出异常；regex：正则表达式；date：将这个字符串转换为datetime.date数据类型。如果转换不成功，则会抛出一个异常。

```





`demo.py`

```python
#这是关于flask框架下快速实现restful_api的python方法


# _*_ coding: utf-8 _*_

"""
python_restful_api.py by xianhu
"""

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from flask import Flask, g
from flask_restful import reqparse, Api, Resource
from flask_httpauth import HTTPTokenAuth


# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

# 认证相关
auth = HTTPTokenAuth(scheme="token")
TOKENS = {
    "fejiasdfhu",
    "fejiuufjeh"
}


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        g.current_user = token
        return True
    return False


# 数据库相关变量声明
engine = sqlalchemy.create_engine("mysql+pymysql://username:password@ip/db_name", encoding="utf8", echo=False)
BaseModel = sqlalchemy.ext.declarative.declarative_base()


# 构建数据模型User
class User(BaseModel):
    __tablename__ = "Users"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
    }

    # 表结构,具体更多的数据类型自行百度
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False)
    age = sqlalchemy.Column("age", sqlalchemy.Integer, nullable=False)


# 构建数据模型的json格式
def get_json(user):
    return {"id": user.id, "name": user.name, "age": user.age}


# 利用Session对象连接数据库
DBSessinon = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSessinon()
BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)

# RESTfulAPI的参数解析 -- put / post参数解析
parser_put = reqparse.RequestParser()
parser_put.add_argument("name", type=str, required=True, help="need name data")
parser_put.add_argument("age", type=int, required=True, help="need age data")

# RESTfulAPI的参数解析 -- get参数解析
parser_get = reqparse.RequestParser()
parser_get.add_argument("limit", type=int, required=False)
parser_get.add_argument("offset", type=int, required=False)
parser_get.add_argument("sortby", type=str, required=False)


# 操作（put / get / delete）单一资源
class Todo(Resource):
    # 添加认证
    decorators = [auth.login_required]

    def put(self, user_id):
        """
        更新用户数据: curl http://127.0.0.1:5000/users/1 -X PUT -d "name=Allen&age=20" -H "Authorization: token fejiasdfhu"
        """
        args = parser_put.parse_args()
        user_ids_set = set([user.id for user in session.query(User.id)])
        print(user_ids_set)

        # 用户不存在，返回404
        if user_id not in user_ids_set:
            return None, 404

        # 更新用户数据
        user = session.query(User).filter(User.id == user_id)[0]
        user.name = args["name"]
        user.age = args["age"]
        session.merge(user)
        session.commit()

        # 更新成功，返回201
        return get_json(user), 201

    def get(self, user_id):
        """
        获取用户数据: curl http://127.0.0.1:5000/users/1 -X GET -H "Authorization: token fejiasdfhu"
        """
        users = session.query(User).filter(User.id == user_id)

        # 用户不存在，返回404
        if users.count() == 0:
            return None, 404

        # 返回用户数据
        return get_json(users[0]), 200

    def delete(self, user_id):
        """
        删除用户数据: curl http://127.0.0.1:5000/users/1 -X DELETE -H "Authorization: token fejiasdfhu"
        """
        session.query(User).filter(User.id == user_id).delete()
        return None, 204


# 操作（post / get）资源列表
class TodoList(Resource):
    # 添加认证
    decorators = [auth.login_required]

    def get(self):
        """
        获取全部用户数据: curl http://127.0.0.1:5000/users -X GET -d "limit=2&offset=0&sortby=name" -H "Authorization: token fejiasdfhu"
        """
        args = parser_get.parse_args()
        users = session.query(User)

        # 根据条件查询
        if "sortby" in args:
            users = users.order_by(User.name if args["sortby"] == "name" else User.age)
        if "offset" in args:
            users = users.offset(args["offset"])
        if "limit" in args:
            users = users.limit(args["limit"])

        # 返回结果
        return [get_json(user) for user in users], 200

    def post(self):
        """
        添加一个新用户: curl http://127.0.0.1:5000/users -X POST -d "name=Brown&age=20" -H "Authorization: token fejiasdfhu"
        """
        args = parser_put.parse_args()

        # 构建新用户
        user = User(name=args["name"], age=args["age"])
        session.add(user)
        session.commit()

        # 资源添加成功，返回201
        return get_json(user), 201


# 设置路由
api.add_resource(TodoList, "/users")
api.add_resource(Todo, "/users/<int:user_id>")


if __name__ == "__main__":
    app.run(debug=True)


""" 常见返回代码
200 OK - [GET]：服务器成功返回用户请求的数据
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作
406 Not Acceptable - [GET]：用户请求的格式不可得
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功
"""
```

