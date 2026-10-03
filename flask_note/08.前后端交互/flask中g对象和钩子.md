

# flask使用操作指南之应用上下文和钩子函数的使用

>Auth: 王海飞
>
>Data：2018-09-15
>
>Email：779598160@qq.com
>
>github：https://github.com/coco369/knowledge 

### 前言

&nbsp;&nbsp;&nbsp;&nbsp;在Web开发中经常会对所有的请求做一些相同的操作，如果将相同的代码写入每一个视图函数中，那么程序就会变得非常臃肿。为了避免在每个视图函数中定义相同的代码，可以使用钩子函数。如下有三个常见的钩子:

1. before_request: 被装饰的函数会在每个请求被处理之前调用。

2. after_request: 被装饰的函数会在每个请求退出时才被调用。在程序没有抛出异常的情况下，才会被执行。

3. teardown_request: 被装饰的函数会在每个请求退出时才被调用。不论程序是否抛出异常，都会执行。

<b style="color:red;">注意:

	1. 这个异常是指代码本身错误（代码中出现10/0）不执行，如果abort抛出异常了，after_request还是会执行。
	2. 必须配置app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False。该配置表示无论如何都将执行teardown_request装饰的方法。
</b>

#### 1. 钩子函数执行顺序

	@blue.before_request
	def before_request():
	    print('before_request')


​	
	@blue.after_request
	def after_request(response):
	    print('after_request')
	    return response


​	
	@blue.teardown_request
	def teardown_request(exception):
	    print('teardown_request')
	
	@blue.route('index/')
	def index_requst():
	    return 'index_requst'

分析:访问http://127.0.0.1:8080/app/index/后，在控制台可以看到如下输出:

before_request

after_request

teardown_request

从控制台的输出中可以看出各函数的执行顺序，被before_request装饰的函数会在请求处理之前被调用。而after_request和teardown_request会在请求处理完后才被调用。区别就在于after_request只会在请求正常退出的情况下才会被调用，并且atfer_request函数必须接受一个响应对象，并返回一个响应对象。而teardown_request函数在任何情况下都会被调用，并且必须传入一个参数来接收异常对象。







## 钩子函数

- 中间件

```
from flask import Flask, render_template, redirect

app = Flask(__name__)

"""
before_reuqest = [xxxxxxxxxx1,xxxxxxxxxx2]
"""


@app.before_request  # 视图执行之前
def xxxxxxxxxx1():
    print('前1')


@app.before_request
def xxxxxxxxxx2():
    print('前2')


"""
after_request = [oooooooo1,oooooooo2]
[oooooooo2,oooooooo1,] reversed(after_request)
"""


@app.after_request
def oooooooo1(response):
    print('后1')
    return response


@app.after_request
def oooooooo2(response):
    print('后2')
    return response


@app.route('/x1', methods=['GET', 'POST'])
def x1():
    print('视图函数x1')
    return "视图函数x1"


if __name__ == '__main__':
    # app.__call__  # 最先调用call方法
    app.run()

```







- 2.中间件有返回值的话不执行视图

```
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.before_request
def xxxxxxxxxx1():
    print('前1')
    return "不要再来烦我了"


@app.before_request
def xxxxxxxxxx2():
    print('前2')


@app.after_request
def oooooooo1(response):
    print('后1')
    return response


@app.after_request
def oooooooo2(response):
    print('后2')
    return response


@app.route('/x1', methods=['GET', 'POST'])
def x1():
    print('视图函数x1')
    return "视图函数x1"

if __name__ == '__main__':
    """
    前1
    后2
    后1
    """
    app.__call__
    app.run()

```







- 3.用装饰器重写登录认证方式

```
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'asdfasdfasdf'


@app.before_request
def check_login():
    if request.path == '/login':  # 登录不用认证
        return None
    user = session.get('user_info')  # 其他接口需要认证
    if not user:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return "视图函数x1"


@app.route('/index', methods=['GET', 'POST'])
def index():
    print('视图函数x2')
    return "视图函数x2"


if __name__ == '__main__':
    app.run()

```







## 特殊装饰器

```
常见装饰器详细说明：http://www.coolpython.net/flask_tutorial/basic/flask-decorator-hook.html
```

- @app.before_request  执行视图函数之前（从上到下）
- @app.after_request 执行视图函数之后（从下到上）
- **如果before_request有返回值就不执行后面的视图函数**和django类似

**其实就是把装饰的函数放入列表中，after_request就列表反转了一下**

示例一：

```python
from flask import Flask, render_template, redirect

app = Flask(__name__)

"""
before_reuqest = [xxxxxxxxxx1,xxxxxxxxxx2]
"""

@app.before_request  # 视图执行之前
def xxxxxxxxxx1():
    print('前1')

@app.before_request
def xxxxxxxxxx2():
    print('前2')

"""
after_request = [oooooooo1,oooooooo2]
[oooooooo2,oooooooo1,] reversed(after_request)
"""

@app.after_request
def oooooooo1(response):
    print('后1')
    return response

@app.after_request
def oooooooo2(response):
    print('后2')
    return response

@app.route('/x1', methods=['GET', 'POST'])
def x1():
    print('视图函数x1')
    return "视图函数x1"

if __name__ == '__main__':
    # app.__call__  # 最先调用call方法
    app.run()

# 前1 前2  视图函数x1 后2 后1
```

示例二：

```python
from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.before_request
def xxxxxxxxxx1():
    print('前1')
    return "不要再来烦我了"

@app.before_request
def xxxxxxxxxx2():
    print('前2')

@app.after_request
def oooooooo1(response):
    print('后1')
    return response

@app.after_request
def oooooooo2(response):
    print('后2')
    return response

@app.route('/x1', methods=['GET', 'POST'])
def x1():
    print('视图函数x1')
    return "视图函数x1"

if __name__ == '__main__':
    app.__call__
    app.run()
# 前1 后2 后1
```

示例三：接口校验是否登录

```python
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'asdfasdfasdf'


@app.before_request
def check_login():
    if request.path == '/login':  # 登录不用认证
        return None
    user = session.get('user_info')  # 其他接口需要认证
    if not user:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return "视图函数x1"


@app.route('/index', methods=['GET', 'POST'])
def index():
    print('视图函数x2')
    return "视图函数x2"


if __name__ == '__main__':
    app.run()
```

##### 其他常见的装饰器

```python
@app.before_first_request  # 第一次请求
def before_first_request1():
    print('before_first_request1')

@app.before_request   # 执行视图之前执行从上到下
def before_request1():
    Request.nnn = 123
    print('before_request1')

@app.after_request  # 执行视图之后执行从下到上
def after_request1(response):
    print('before_request1', response)
    return response

@app.errorhandler(404)  # 错误页面装饰器，有错误的时候执行
def page_not_found(error):
    return 'This page does not exist', 404

@app.template_global()  # 模板装饰器，可以在所有的模板中使用
def sb(a1, a2):
    return a1 + a2

@app.template_filter()  # 过滤装饰器
def db(a1, a2, a3):
    return a1 + a2 + a3
```








#### 2. 应用上下文G对象

&nbsp;&nbsp;&nbsp;&nbsp;应用全局对象（g）是Flask为每一个请求自动建立的一个对象。g的作用范围只是在一个请求（也就是一个线程）里，它不能在多个请求中共享数据，故此应用全局变量（g）确保了线程安全。


##### 案例: 连接pymysql，并实现表的创建和数据的插入

	@blue.before_request
	def get_mysql_connect():
	    # 建立mysql数据库的连接
	    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='f_db')
	    cursor = conn.cursor()
	    # 设置当前请求上下文中的应用全局对象
	    g.conn = conn
	    g.cursor = cursor


​	
	@blue.before_request
	def create_student_table():
	    # 创建student表
	    sql = 'drop table if exists student;'
	    sql1 = 'create table student(id int auto_increment, s_name varchar(10) not null, s_age int not null, primary key(id)) engine=InnoDB default charset=utf8;'
	    # 执行删除表，如果student表存在则删除
	    g.cursor.execute(sql)
	    # 执行创建student表
	    g.cursor.execute(sql1)


​	
	@blue.route('excute_sql/')
	def excute_sql():
	    # 定义插入sql语句
	    sql = 'insert into student (name, age) values ("%s", "%s")' % ('xiaoming', '18')
	    # 执行插入语句
	    g.cursor.execute(sql)
	    # 提交事务
	    g.conn.commit()
	    return '创建数据'


​	
	@blue.teardown_request
	def close_mysql_connect(exception):
	    # 关闭mysql数据库的连接
	    g.conn.close()

