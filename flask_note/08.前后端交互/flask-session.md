# flask-session插件

#### 7、flask中的session

```
更多操作示例：https://www.cnblogs.com/wupeiqi/articles/7552008.html
```

除请求对象之外，还有一个 session 对象。它允许你在不同请求间存储特定用户的信息。它是在 Cookies 的基础上实现的，并且对 Cookies 进行密钥签名要使用会话，你需要设置一个密钥。

- 设置：session['username'] ＝ 'xxx'
- 删除：session.pop('username', None)

flask中的session继承了字典，所以字典有的方法session都有，flask是把session存入cookies中，本地不存。

a.设置一把盐，和django一样 app.secret_key = 'sadfasdfasdf'

b.对session进行添加获取删除等操作

```python
"""
1. 请求刚刚达到
    ctx = RequestContext(...)
          - request
          - session=None
    ctx.push()
        ctx.session = SecureCookieSessionInterface.open_session

2. 视图函数

3. 请求结束
    SecureCookieSessionInterface.save_session()
"""
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'sadfasdfasdf'


@app.route('/x1')
def index():
    # 去ctx中获取session
    session['k1'] = 123
    session['k2'] = 123
    del session['k2']
    return "Index"


@app.route('/x2')
def order():
    print(session['k1'])
    return "Order"


if __name__ == '__main__':
    app.run()

    # 1. 请求一旦到来显
    # app.__call__
    # app.wsgi_app
    # app.open_session

```



## 简介

作用：将默认保存的签名cookie中的值 保存到 redis/memcached/file/Mongodb/SQLAlchemy

作用：将默认保存的签名cookie中的值 保存到 redis/memcached/file/Mongodb/SQLAlchemy

应用：

a. 配置
        

```python
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='192.168.0.94',port='6379')
```



b. 替换
    

```python
from flask_session import Session
Session(app)
```

注意：session中存储的是字典，修改字典内部元素时，会造成数据不更新。
```python
motified = True
SESSION_REFRESH_EACH_REQUEST = True and  session.permanent = True(redis中默认)
```



```python
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = 'abasd'

# 默认的session存储方式
from flask.sessions import SecureCookieSessionInterface
app.session_interface = SecureCookieSessionInterface()

# 其他
# 方式一：保存到redis中
from redis import Redis
from flask_session import RedisSessionInterface

app.session_interface = RedisSessionInterface(
    redis=Redis(host='127.0.0.1', port=6379),
    key_prefix='rediszz'  # session的前缀
)
# 方式二 保存在redis中
from flask_session import Session
from redis import Redis

app.config['SESSION_TYPE'] = 'REDIS'
app.config['SESSION_REDIS'] = Redis(host='', db='', port='', password='', encoding='')
Session(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'login'
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    session['user_info'] = {'user': user, 'pwd': pwd}

    return 'login'


@app.route('/index', methods=['GET'])
def index():
    user_info = session.get('user_info')
    return 'index'


if __name__ == '__main__':
    app.run()

```





#### 1、flask_session

```
详细：https://blog.csdn.net/weixin_43976393/article/details/87983656?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-87983656-blog-83781020.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-87983656-blog-83781020.pc_relevant_antiscanv2&utm_relevant_index=1
```

作用：将默认保存的签名cookie中的值，保存到redis/memcached/file/mangodb/SQLAlchemy中

**注意：session中存储的是字典，修改字典内部元素时，会造成数据不更新，解决方法：**

- motified = True
- SESSION_REFRESH_EACH_REQUEST = True and  session.permanent = True(redis中默认)

**存入session的方式，将session存入数据库中，不使用默认的了**

```python
"""
1. flask-session
    作用：将默认保存的签名cookie中的值 保存到 redis/memcached/file/Mongodb/SQLAlchemy
"""
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = 'abasd'

# 默认的session存储方式
from flask.sessions import SecureCookieSessionInterface
app.session_interface = SecureCookieSessionInterface()

# 其他
# 方式一：保存到redis中
from redis import Redis
from flask_session import RedisSessionInterface

app.session_interface = RedisSessionInterface(
    redis=Redis(host='127.0.0.1', port=6379),
    key_prefix='rediszz'  # session的前缀
)
# 方式二 保存在redis中
from flask_session import Session
from redis import Redis

app.config['SESSION_TYPE'] = 'REDIS'
app.config['SESSION_REDIS'] = Redis(host='', db='', port='', password='', encoding='')
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'login'
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    session['user_info'] = {'user': user, 'pwd': pwd}
    return 'login'

@app.route('/index', methods=['GET'])
def index():
    user_info = session.get('user_info')
    return 'index'

if __name__ == '__main__':
    app.run()
```









## flask-session

flask-session，允许设置session到指定的存储空间中，例如：redis/mongoDB/mysql。

文档: https://flask-session.readthedocs.io/en/latest/

```
pip install Flask-Session
```

使用session之前,必须配置一下配置项:

```
# session秘钥
app.config["SECRET_KEY"] = "*(%#4sxcz(^(#$#8423"
```





#### Sqlalchemy存储Session的基本配置

需要手动创建session表，在项目第一次启动的时候，使用`db.create_all()`来完成创建。

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 引入session存储驱动类
from flask_session import Session
# 引入sessio操作类，注意：引入路径不同，大小写不同的。
from flask import session

app = Flask(__name__)
# 务必要先创建模块的实例对象
db = SQLAlchemy()
session_store = Session()

class Config(object):
    DEBUG = True
    # 数据库连接配置
    # SQLALCHEMY_DATABASE_URI = "数据库类型://数据库账号:密码@数据库地址:端口/数据库名称?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = "mysql://root:123@127.0.0.1:3306/flaskdemo?charset=utf8mb4"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 秘钥
    SECRET_KEY = "*(%#4sxcz(^(#$#8423"  # session秘钥
    # 把session通过SQLAlchmey保存到mysql中
    SESSION_TYPE = "sqlalchemy" # session类型为sqlalchemy
    SESSION_SQLALCHEMY = db     # SQLAlchemy的数据库连接对象
    SESSION_SQLALCHEMY_TABLE = 'db_session' # session要保存的表名称
    SESSION_PERMANENT = True    # 如果设置为True，则关闭浏览器session就失效
    SESSION_USE_SIGNER =  True  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = "session:" # session数据表中sessionID的前缀，默认就是 session:

app.config.from_object(Config)
# 在app加载配置以后，注册app对象
db.init_app(app)
session_store.init_app(app)


@app.route("/set")
def set_session():
    session["uname"] = "xiaoming"
    session["age"]   = 18
    return "ok"

@app.route("/get")
def get_session():
    print(session.get("uname"))
    print(session.get("age"))
    return "ok"

@app.route("/del")
def del_session():
    # 此处的删除，不是删除用户对应的session表记录，而是删除session值而已。
    print(session.pop("uname"))
    print(session.pop("age"))
    return "ok"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # 使用Session存储库必须要调用db.create_all()或者数据迁移生成session表
    app.run()
```





#### redis保存session的基本配置

这个功能必须确保，服务器必须已经安装了redis而且当前项目虚拟环境中已经安装了redis扩展库

```
pip install flask-redis 
```

flask-redis是第三方开发者为了方便我们在flask框架中集成redis数据库操作所封装一个redis操作库、

在flask中要基于flask-redis进行数据库则可以完成以下3个步骤即可：

```python
from flask import Flask
from flask_redis import FlaskRedis

# 实例化
app = Flask(__name__)
session_redis = FlaskRedis(config_prefix="SESSION")
user_redis = FlaskRedis(config_prefix="USER")
order_redis = FlaskRedis(config_prefix="ORDER")

# 初始化 flask_redis
session_redis.init_app(app)
user_redis.init_app(app)
order_redis.init_app(app)

@app.route("/")
def q2():
    user_redis.setnx("doing", 100)
    return "ok"

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)
```

在redis中保存session,代码：

```python
from flask import Flask
from flask_redis import FlaskRedis
# 引入session存储驱动类
from flask_session import Session
# 引入sessio操作类，注意：引入路径不同，大小写不同的。
from flask import session

app = Flask(__name__)
# 要先创建模块的实例对象
session_store = Session()
redis = FlaskRedis() # config_prefix 用于指定redis的URL配置项前缀，默认值是REDIS，对应的配置项：REDIS_URL

class Config(object):
    DEBUG = True
    # 数据库连接配置
    # 2. 在config配置中使用 REDIS_URL配置redis的url地址
    REDIS_URL = "redis://@127.0.0.1:6379/0"

    # 把session保存到redis
    SESSION_TYPE = "redis"     # session存储方式为redis
    SESSION_PERMANENT = False  # 如果设置session的生命周期是否是会话期, 为True，则关闭浏览器session就失效
    SESSION_USE_SIGNER = False # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = "session:" # 保存到redis的session数的名称前缀
    # session保存数据到redis时启用的链接对象
    SESSION_REDIS = redis      # 用于连接redis的配置

app.config.from_object(Config)

# 在app加载配置以后，注册app对象
redis.init_app(app)
session_store.init_app(app)

@app.route("/set")
def set_session():
    session["uname"] = "xiaoming"
    session["age"]   = 18
    return "ok"

@app.route("/get")
def get_session():
    print(session.get("uname"))
    print(session.get("age"))
    return "ok"

@app.route("/del")
def del_session():
    # 此处的删除，是直接删除保存在redis中的数据，当所有session被删除，则key也会消失了。
    print(session.pop("uname"))
    print(session.pop("age"))
    return "ok"

if __name__ == '__main__':
    app.run()
```

