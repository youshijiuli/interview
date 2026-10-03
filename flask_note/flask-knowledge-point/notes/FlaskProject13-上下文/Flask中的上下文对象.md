# Flask上下文

上下文是指在程序中可以理解为在代码执行到某一时刻时，根据之前代码所做的操作以及上下文即将要执行的逻辑，可以决定在当前时刻下可以使用到的变量，或者可以完成的事情。

Flask中有两种上下文，请求上下文和应用上下文。

Flask中上下文对象：相当于一个容器，保存了Flask程序运行过程中的一些信息

## 一、请求上下文

思考：在视图函数中，如何取到当前请求的相关数据？比如：请求地址、请求方式、cookie等

在Flask中，可以直接在视图函数中使用request这个对象进行获取相关数据，而request就是请求上下文的对象，报错了当前本次请求的相关数据，请求上下文对象有：request、session

- `request`封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')获取的是get请求的参数
- `session`用来记录请求会话中的信息，针对的是用户信息。举例：session['name'] = user.name，可以记录用户信息，还可以通过session.get('name')获取用户信息。



## 二、应用上下文

它的字面意思是应用上下文，但它不是一直存在的，它只是request context中的一个对app的代理人，所谓local proxy。它的作用主要是帮助request获取当前的应用，它是伴request而生，随request而灭。

应用上下文对象有两个：current_app、g

### `current_app`

应用程序上下文，用于存储应用程序中的变量。可以通过current_app.name打印当前app的名称，也可以在current_app中存储变量，例如：

1. 应用程序脚本是哪个文件，启动时指定了哪些参数
2. 加载了哪些配置文件，导入了哪些配置
3. 连了哪个数据库
4. 有哪些public的工具类、常量
5. 应用跑在哪个机器上、IP多少、内存多大

```python
from flask import Flask, current_app

# 以redis客户端对象为例
# 用字符串表示创建的redis客户端
# 为了方便在各个视图中使用，将创建的redis客户端对象保存到flask app中，
# 后续可以在视图中使用current_app.redis_cli获取
app1.redis_cli = 'app1 redis client'
app2.redis_cli = 'app2 redis client'


@app1.route('/route11')
def route11():
	return current_app.redis_cli


@app1.route('/route12')
def route12():
	return current_app.redis_cli


@app2.route('/route21')
def route21():
	return current_app.redis_cli


@app2.route('/route22')
def route22():
	return current_app.redis_cli


```

**注意：current_app就是当前运行的flask app，在代码不方便直接操作Flask app对象的时候，可以操作current_app就等价于操作Flask app对象**

### `g`

g作为Flask程序全局的一个临时变量，充当中间媒介的作用，我们可以通过它在一次请求调用的多个函数间传递一些数据。每次请求都会重置这个变量。

```python
from flask import Flask, g

app = Flask(__name__)


def db_query():
    # 从g对象中获取数据
    user_id = g.user_id
    user_name = g.user_name
    print("user_id={}  user_name={}".format(user_id, user_name))
    
@app.route('/')
def get_user_profile():
    g.user_id = 1
    g.user_name = 'xiaodai'
    
    db_query()  # g可以在不同函数间传递数据
    
    return 'hello world'
    
```

g对象与请求钩子配合

案例需求：

- 构建认证机制
- 对特定视图可以提供强制要求用户登录的限制
- 对所有视图，无论是否强制要求用户登录，都可以在视图中尝试获取用户认证后的身份信息

代码实现：

```python
from flask import Flask, abort, g, request, render_template, redirect, url_for, make_response

# 创建Flask应用实例
app = Flask(__name__)

@app.before_request
def authentication():
    """ 利用before_request请求钩子，在进入所有视图前先尝试判断用户身份 """
    # 使用cookie来鉴别用户身份信息
    user_id = request.cookies.get('user_id', None)
    
    # 如果用户已经登录了，用户有身份
    g.user_id = user_id

def login_required(func):
    """ 自定义一个装饰器来认证用户 """
    
    def wrapper(*args, **kwargs):
        # 如果用户已登录（即g.user_id存在），则允许访问被装饰的视图函数
        if g.user_id:
            return func(*args, **kwargs)
        else:
            # 否则返回401未授权错误
            abort(401)
            
    return wrapper

@app.route('/')
def index():
    """ 首页，无论你是否登录，都可以访问 """
    # 返回首页内容，并显示当前用户的user_id（如果有）
    return "home page user_id={}".format(g.user_id)

@app.route('/profile')
@login_required
def get_user_profile():
    """ 这里必须认证用户才能访问 """
    # 返回用户个人资料页面，并显示当前用户的user_id
    return "user profile page user_id={}".format(g.user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ 处理用户登录请求 """
    if request.method == 'GET':
        # 如果是GET请求，返回登录页面
        return render_template('login.html')
    elif request.method == 'POST':
        # 如果是POST请求，处理登录逻辑
        user_id = request.form.get('user_id', None)
        html = redirect(url_for('index'))
        if user_id:
            # 如果提供了user_id，设置cookie并重定向到首页
            resp = make_response(html)
            resp.set_cookie('user_id', user_id)
            return resp
        else:
            # 如果没有提供user_id，直接重定向到首页
            return html
    else:
        # 其他HTTP方法，重定向到登录页面
        return redirect(url_for('login'))

```

