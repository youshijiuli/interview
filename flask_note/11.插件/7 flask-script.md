# flask-script



## 笔记

flask_scipt 已经快10年没有维护了，新版本migrate也已经不支持了，所以这里转换到使用click,下面是一个相对稍高级的用法，将命令直接注册到蓝图上，对于app
同理（理解blueprint和app的关系）

```python

@user_bp.cli.command('create_user')
@click.argument('nick_name')
@click.argument('password')
def create_user(nick_name, password):
    """
    Func: 在蓝图上注册命令：命令行添加user
    Args: user必须的参数:nick_name, password
    Example: flask user create_user 'andy' '123456'
    Return: None
    :Author:  Andy
    :Version: 1.0
    :Created:  2022/3/26 下午9:08
    :Modified: 2022/3/26 下午9:08
    """
    user = User()
    user.nick_name = nick_name
    user.password = password
    with db.auto_commit():
        db.session.add(user)

#对应蓝图
# 因为指定了cli_group所以在命令行时要使用flask user,指定 cli_group=None 会删除嵌套并把命令直接合并到应用级别
user_bp = Blueprint('user', __name__, url_prefix='/user', cli_group='user')

```

Flask-Script的作用是可以通过命令行的形式来操作Flask。例如通过命令跑一个开发版本的服务器、设置数据库，定时任务等。要使用Flask-Script，可以通过`pip install flask-script`安装最新版本。

### 命令的添加方式：

### 示例代码

新建文件manage.py,文件中的代码如下

```
 代码解读
复制代码from flask_script import Manager
from app.app import app

manager = Manager(app)

# 定义自己要执行的command
@manager.command
def test():
    print(u'test run')
    
if __name__ == '__main__':
    manager.run()
```

### 执行命令行

执行格式：`python manage.py [commond]`

```
 代码解读
复制代码# 执行示例中的test中的内容
python manage.py test

# 启动flask项目的命令
python manage.py runserver
```

### 引用其它文件或第三方的flask-script命令

实际使用中，我们往往可能会遇到需要引用第三方的flask-script，如flask-migrate。或者期望将一种类型的命令放置同一个文件中统一管理，这时就涉及到如何引入这些flask-script命令的问题

#### 1. 引用其它文件中的flask-script

假设我们需要创建的是一个数据库统一处理的命令集文件db_script.py,示例代码如下：

```
 代码解读
复制代码from flask_script import Manager
# 注意命名，不能命名成Manager，否则会有冲突
DBManager = Manager()

@DBManager.command
def init():
    print('数据库初始化完成')

@DBManager.command
def migrate():
    print '数据表迁移成功'
```

这是原来的manage.py文件中变更如下：

```
 代码解读
复制代码from flask_script import Manager
# 变更一：引入定义的命令集对象
from db_scripts import DBManager
from app.app import app

manager = Manager(app)

# 变更二：将名利集添加到manager中
manager.add_command('db', DBManager)

# 定义自己要执行的command
@manager.command
def test():
    print(u'test run')
    
if __name__ == '__main__':
    manager.run()
```

执行命令的方式有所不同：

```
 代码解读
复制代码python manage.py db init
python manage.py db migrate
```











1. 使用`manage.commad`：这个方法是用来添加那些不需要传递参数的命令。示例代码如下：
    ```python
    manager = Manager(app)
    manager.add_command("db",db_manager)

    @manager.command
    def greet():
        print('你好')
    ```
2. `使用manage.option`：这个方法是用来添加那些需要传递参数的命令。有几个参数就需要写几个`option`。示例代码如下：
    ```python
    @manager.option("-u","--username",dest="username")
    @manager.option("-e","--email",dest="email")
    def add_user(username,email):
        user = BackendUser(username=username,email=email)
        db.session.add(user)
        db.session.commit()
    ```

3. 如果有一些命令是针对某个功能的。比如有一堆命令是针对ORM与表映射的，那么可以将这些命令单独放在一个文件中方便管理。也是使用`Manager`的对象来添加。然后到主manage文件中，通过`manager.add_command`来添加。示例代码如下：
db_script.py

```python
from flask_script import Manager

db_manager = Manager()

@db_manager.command
def init():
    print('迁移仓库创建完毕！')

@db_manager.command
def revision():
    print('迁移脚本生成成功！')

@db_manager.command
def upgrade():
    print('脚本映射到数据库成功！')
```

manage.py
```python
from db_script import db_manager

manager = Manager(app)
manager.add_command("db",db_manager)
```
### 实例
```python
from flask_script import Manager
from models import app
from models import NewUser,db

manager = Manager(app)

@manager.command
def greet():
    print('hello')

@manager.option("-n", "--name", dest="name")
@manager.option('-a', '--age', dest='age')
def add_user(name,age):
    print("你要输入的用户名是：%s 年龄是 %s" %(name, age))
    user = NewUser(name=name,age=age)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
```
然后在shell中运行：`python manage.py add_user -n "andy" -a "18"`



















#### 7.9 Flask-Script  

Flask-Script的作⽤是可以通过命令⾏的形式来操作Flask。例如通过命令跑⼀
个开发版本的服务器、设置数据库，定时任务等。要使⽤Flask-Script，可以
通过pip install flask-script安装最新版本  

```
from flask_script import Manager
from your_app import app

manager = Manager(app)

@manager.command
def hello():
    print('hello')

if __name__ == '__main__':
    manager.run()
```

我们把脚本命令代码放在⼀个叫做manage.py⽂件中，然后在终端运⾏python
manage.py hello命令，就可以看到输出hello了  





###### 定义命令的三种方法

\1. 使⽤@command装饰器
\2. 使⽤类继承⾃Command类  

```
from flask_script import Command,Manager
from your_app import app

manager = Manager(app)

class Hello(Command):
    # "prints hello world"
    def run(self):
        print("hello world")

manager.add_command('hello',Hello())
```





使⽤类的⽅式，有三点需要注意
必须继承⾃Command基类。
必须实现run⽅法。
必须通过add_command⽅法添加命令。



\3. 使⽤option装饰器：如果想要在使⽤命令的时候还传递参数进去，那么使⽤
@option装饰器更加的⽅便  

```
@manager.option('-n','--name',dest='name')
def hello(name):
	print('hello ',name)
```

这样，调⽤hello命令  

```
python manage.py -n juran
python manage.py --name juran
```



###### 添加参数到命令中：

option装饰器：以上三种创建命令的⽅式都可以添加参数，@option装饰
器，已经介绍过了  

```

```

command装饰器：command装饰器也可以添加参数，但是不能那么的灵活  

```

```

类继承：类继承也可以添加参数  

```

```

如果要在指定参数的时候，动态的做⼀些事情，可以使⽤get_options⽅法  

```

```

