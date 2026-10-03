# Flask-SQLAlchemy使用指南

# 一、Flask-SQLAlchemy是什么

Flask-SQLAlchemy是一个Flask扩展，他为Flask应用程序提供了一个简化版本的SQLAlchemy封装。

- Flask的一个插件
- 对SQLAlchenmy进行了简单的封装
- 使我们在使用Flask操作ORM更加简单

安装`pip install flask-sqlchemy`用于ORM

安装`pip install flask-migrate`用于数据迁移

安装`pip install pymysql`用于MySQL驱动

# 二、Flask-SQLAlchemy如何使用

### （1）连接数据库

1. **定义好数据库连接字符串DB_URI**

```python
from flask import Flask

app = Flask(__name__)

# MySQL的连接方式
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(
	USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DATABASE
)

# postgresql的连接方式 "postgresql+psycopg2://user:password@localhost/dbname"
# sqlite的连接方式 'sqlite:///sqlite3.db'
```

2. **配置`app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI`**

```python
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

这里配置了数据库 URI 和关闭了 `SQLALCHEMY_TRACK_MODIFICATIONS`，因为跟踪修改的默认行为会消耗额外的内存。

3. **注册插件**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


db.init_app(app)
migrate.init_app(app=app, db=db)

```

### （2）定义模型类

之间都是通过`Base = declarative_base()`来初始化一个基类，然后再继承这个基类。在Flask-SQLAlchemy中不需要这样了。

1. 还是跟sqlalchemy一样，定义模型。但使用db.model来作为基类
2. 在模型类中`Column`、`String`、`Integer`以及`relationship`等都不用单独导入，直接使用`db`下面相应的属性名就可以了。
3. 在定义模型的时候，可以不写`__tablename__`，如果你不写默认会使用当前的模型名字转换成小写来作为表的名字。并且如果这个模型的名字用到了多个单词使用了驼峰命令，那么会在多个单词之间使用下划线来连接。虽然有这个默认功能，但一般还是自己定义表名，不推荐使用这种方式。

```python
class User(db.Model):
    
    __tablename__ = 't_user'
	
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    gender = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
```

### （3）执行迁移

执行数据迁移的命令：

- 首先cmd必须在app.py所在的路径下
- 然后再输入命令，常用命令有4个

```bash
flask db init  // 创建迁移文件夹migrates，只需要调用一次
flask db migrate  // 生成迁移文件
flask db upgrade  // 执行迁移文件中的升级
flask db downgrage  // 执行迁移文件中的降级
```

以上这些命令都是需要你先安装`flask-migrate`才能使用的。

如果你不安装这个插件也可以生成数据库表，只需要在代码中写上：

```python 
# 创建数据库表
db.create_all()

# 删除数据库表
db.drop_all()
```

### （4）增删改查

flask-sqlalchemy中的CRUD是通过实例化的`db`数据库引擎对象中的`session`操作对象来实现的。

1. **增加**

向数据库表中插入数据

```python
from .models improt User


@app.route('/add_user')
def add_user():
    new_user = User(username='xiaodai', gender=False)
    db.session.add()     # 添加
    db.session.commit()  # 提交
    
    return 'User added.'
```

2. **删除**

向数据库表中删除数据，先查找再删除。

```python
@app.route('/delete_user/<username>')
def delete_user(username):
    user = User.query.filter(User.username==username).first()
    db.session.delete(user)   # 删除
    db.session.commit()       # 提交
```

3. **修改**

向数据库表中修改数据，先查找到再修改。

```python
@app.route('/update_user/<int:uid>')
def update_user(uid):
	user = User.query.get(uid)
    user.username = 'pidan'  # 修改
    db.session.commit()      # 提交
```

4. **查询**

- `get()` 方法的基本用法是传入一个主键值作为参数，然后返回对应的模型实例。如果找不到对应的记录，则返回 `None`。如果你的模型中有多个主键，`get()` 方法将不起作用，因为它只能处理单一的主键。

- `filter()` 方法提供了更大的灵活性，允许你使用原始的 SQL 表达式来构建查询条件。这对于更复杂的查询条件特别有用。如果你需要根据其他字段来获取记录可以使用这种方法。

- `filter_by()` 方法允许你通过指定模型的字段值来过滤查询结果。这是一个非常方便的方法，可以用来根据多个字段的值来筛选记录。

- `filter()` 和 `filter_by()` 方法都是用于构建查询条件的，它们返回的结果都是一个查询对象 (`Query` 对象)，而不是直接返回查询结果。你可以进一步调用 `.all()`, `.first()`, `.count()` 等方法来获取具体的查询结果。

```python
# 获取 id 为 1 的用户
user = User.query.get(1)

# 查询所有user
all_user = User.query.all()
#在query属性之后 可以用 order_by、filter、filter_by、group_by、having等方法进行更复杂的单表查询

# 获取名字包含'john'的所有用户
# 使用 filter_by()
users = User.query.filter_by(username='john').all()

# 使用 filter()
users = User.query.filter(User.username == 'john').all()

# 获取名字包含'john'的第一个用户
# 使用 filter_by()
user = User.query.filter_by(username='john').first()

# 使用 filter()
user = User.query.filter(User.username == 'john').first()

# 获取第一条记录，如果没找到则抛出 404 错误
# 使用 filter_by()
user = User.query.filter_by(username='john').first_or_404()

# 使用 filter()
user = User.query.filter(User.username == 'john').first_or_404()

# 获取记录数量
# 使用 filter_by()
count = User.query.filter_by(username='john').count()

# 使用 filter()
count = User.query.filter(User.username == 'john').count()
```

