## flask_migrate笔记：
在实际的开发环境中，经常会发生数据库修改的行为。一般我们修改数据库不会直接手动的去修改，而是去修改ORM对应的模型，然后再把模型映射到数据库中。这时候如果有一个工具能专门做这种事情，就显得非常有用了，而flask-migrate就是做这个事情的。flask-migrate是基于Alembic进行的一个封装，并集成到Flask中，而所有的迁移操作其实都是Alembic做的，他能跟踪模型的变化，并将变化映射到数据库中。

### 安装：
pip install flask-migrate


### 在manage.py中的代码：
```python
from flask_script import Manager
from zhiliao import app
from exts import db
from flask_migrate import Migrate,MigrateCommand

manager = Manager(app)

# 用来绑定app和db到flask_migrate的
Migrate(app,db)
# 添加Migrate的所有子命令到db下
manager.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

### flask_migrate常用命令：
1. 初始化一个环境：python manage.py db init
2. 自动检测模型，生成迁移脚本：python manage.py db migrate
3. 将迁移脚本映射到数据库中：python manage.py db upgrade
4. 更多命令：python manage.py db --help

### 实例

#### config.py
```python
#encoding: utf-8

DB_USERNAME = 'root'
DB_PASSWORD = 'password'
DB_HOST = '192.168.16.8'
DB_PORT = '3306'
DB_NAME = 'flask_migrate_demo'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
```

#### exts.py
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

#### manage.py
```python
from flask_script import Manager
from demo import app
from exts import db
from flask_migrate import Migrate, MigrateCommand


manager = Manager(app)
Migrate(app,db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

#### models.py
```python

from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=True)


if __name__ == '__main__':
    pass
```

#### demo.py
```python
from flask import Flask
from exts import db
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/index')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
```









#### 7.10 Flask-Migrate  

在实际的开发环境中，经常会发⽣数据库修改的⾏为。⼀般我们修改数据库不
会直接⼿动的去修改，⽽是去修改 ORM 对应的模型，然后再把模型映射到数据
库中。这时候如果有⼀个⼯具能专⻔做这种事情，就显得⾮常有⽤了，⽽
flask-migrate 就是做这个事情的。 flask-migrate 是基于 Alembic 进
⾏的⼀个封装，并集成到 Flask 中，⽽所有的迁移操作其实都是 Alembic 做
的，他能跟踪模型的变化，并将变化映射到数据库中。



使⽤ Flask-Migrate 需要安装  

```
pip install flask-migrate
```

要让 Flask-Migrate 能够管理 app 中的数据库，需要使⽤
Migrate(app,db) 来绑定 app 和数据库  

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from constants import DB_URI
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
#  绑定app和数据库
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))

    addresses = db.relationship('Address',backref='user')

class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email_address = db.Column(db.String(50))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

初始化一个迁移文件夹：

```
flask db init
```

然后再把当前的模型添加到迁移⽂件中  

```
flask db migrate
```

最后再把迁移⽂件中对应的数据库操作，真正的映射到数据库中  

```
flask db upgrade
```



###### manage.py文件

这个⽂件⽤来存放映射数据库的命令，MigrateCommand是flask-migrate集
成的⼀个命令，因此想要添加到脚本命令中，需要采⽤
manager.add_command('db',MigrateCommand)的⽅式，以后运⾏python
manage.py db xxx的命令，其实就是执⾏MigrateCommand。  

```
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_app import app, db, User

# 需要映射那个模型，就把哪个模型导入进来


manage = Manager(app)

Migrate(app, db)

manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()
    
```



#### 百战flask-migrate

介绍
flask-migrate是flask的一个扩展模块，主要是扩展数据库表结构
的。
flask-migrate是基于Alembic进行的一个封装，并集成到Flask中，
所有的迁移操作其实都是Alembic做的，他能跟踪模型的变化，并
将变化映射到数据库中



安装

```
pip install flask-migrate
```



使用方法
模型类

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)

# 数据库的变量
HOST = '192.168.30.151'  # 127.0.0.1/localhost
PORT = 3306
DATA_BASE = 'flask_db'
USER = 'root'
PWD = '123'
DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =  SQLAlchemy(app)

# 创建模型类
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    city = db.Column(db.String(32))

    def __repr__(self):
        return f'<User id={self.id}  name={self.name}>'

# 使用migrate同步表结构
# pip install flask-migrate

from flask_migrate import Migrate

Migrate(app,db)  # KeyError: 'migrate'

# flask db init  1次就可以了
# flask db migrate
# flask db upgrade
```

创建迁移仓库
这个命令会创建migrations文件夹，所有迁移文件都放在里面

```
flask db init
```



生成脚本文件

```
flask db migrate
```



更新数据库

```
flask db upgrade
```



返回以前的版本

```
flask db downgrade version_
```







上下文管理和sqlhelper

```python
import pymysql
from DBUtils.PooledDB import PooledDB

class SqlHelper(object):
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='127.0.0.1',
            port=3306,
            user='root',
            password='222',
            database='cmdb',
            charset='utf8'
        )

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn,cursor

    def close(self,cursor,conn):
        cursor.close()
        conn.close()

    def fetchall(self,sql, *args):
        """ 获取所有数据 """
        conn,cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn,cursor)
        return result

    def fetchone(self,sql, *args):
        """ 获取所有数据 """
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def __enter__(self):
        return self.open()[1]

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)


db = SqlHelper()
```







