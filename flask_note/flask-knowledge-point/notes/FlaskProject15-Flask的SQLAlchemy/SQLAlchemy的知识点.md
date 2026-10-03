# SQLAlchemy介绍

## 一、SQLAlchemy是什么

SQLAlchemy 是一个 Python 的 SQL 工具包和 ORM（对象关系映射）框架。

SQLAlchemy对象关系映射器提供了一种方法，用于将用户定义的Python类与数据库表相关联，并将这些类（对象）的实例与其对应表中的行，相关联。它包括一个透明地同步对象及相关行之间状态的所有变化的系统，称之为工作单元，以及根据用户定义的类及其定义的彼此之间的关系表达数据库查询的系统。

可以让我么使用类和对象的方式操作数据库，从繁琐的SQL语句中解脱出来。

ORM就是Object Relational Mapper的简写，就是关系对象映射器的意思。



## 二、基本使用

### （1）下载安装

首先要确保你已经安装了以下软件：

- `mysql`
  - 如果是在windows上，到官网下载。如果是ubuntu，通过命令`sudo apt-get install mysql-serverlibmysqlclient-dev -yq`进行下载安装。
- `pymysql`
  - pymysql是用Python来操作mysql的包，因此通过pip来安装，命令如下：`pip install pymysql`。如果。你用的是Python 3，请安装pymysql。
- `SQLAlchemy`
  - SQLAlchemy是一个数据库的ORM框架，我们在后面会用到。安装命令为：`pip install
    SQLAlchemy`

### （2）创建数据库引擎，并连接数据库

```python
from sqlalchemy import create_engine


# 使用 postgresql 驱动
engine_postgresql = create_engine("postgresql+psycopg2://user:password@localhost/dbname")

# 使用 mysqlclient 驱动
engine_mysql = create_engine("mysql+mysqlconnector://user:password@localhost/dbname")

# 使用 pymysql 驱动
engine_mysql = create_engine("mysql+pymysql://user:password@localhost/dbname")
```

也可以把关键数据库连接配置变量写在config文件中

```
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test'
USERNAME = 'root'
PASSWORD = '123123'

DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)
```

### （3）定义模型类

```python
# 从sqlalchemy.ext.declarative模块导入declarative_base函数，用于创建基类
from sqlalchemy.ext.declarative import declarative_base
# 从sqlalchemy模块导入Column, Integer和String，用于定义数据库表的列
from sqlalchemy import Column, Integer, String

# 创建一个基类Base，所有映射类都将继承这个基类
Base = declarative_base()

# 定义一个User类，继承自Base，表示数据库中的一个表
class User(Base):
    # 指定表名为't_users'
    __tablename__ = 't_users'

    # 定义id列，类型为Integer，并且是主键
    id = Column(Integer, primary_key=True)
    # 定义name列，类型为String
    name = Column(String)
    # 定义fullname列，类型为String
    fullname = Column(String)
    # 定义password列，类型为String
    password = Column(String)

    # 定义__repr__方法，用于返回对象的字符串表示形式
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


```

### （4）创建数据库表

```python
# 使用Base.metadata.create_all()来将模型映射到数据库中。
Base.metadata.create_all(engine_sqlite)
```

注意：一旦使用`Base.metadata.create_all()`将模型映射到数据库中后，即使改变了模型的字段，也不会重新映射了。

### 三、常用参数

### （1）SQLAlchemy常用数据类型

​		SQLAlchemy 提供了一系列的数据类型，这些数据类型可以映射到不同的 SQL 数据库列类型。下面是一些常见的数据类型及其用途：

- **Integer**：整数类型。
  ```python
  from sqlalchemy import Column, Integer
  
  class User(Base):
      id = Column(Integer, primary_key=True)
  ```

- **String**：字符类型，通常用于存储文本。
  ```python
  name = Column(String(50))
  ```

- **Text**：长文本类型。
  ```python
  description = Column(Text)
  ```

- **Float**：浮点数类型。
  ```python
  price = Column(Float)
  ```

- **Numeric**：数值类型，可以指定精度和小数位数。
  ```python
  amount = Column(Numeric(precision=10, scale=2))
  ```

- **Boolean**：布尔类型。
  ```python
  active = Column(Boolean)
  ```

- **Date**：日期类型。
  ```python
  birth_date = Column(Date)
  ```

- **DateTime**：日期时间类型。
  ```python
  created_at = Column(DateTime)
  ```

- **Time**：时间类型。
  ```python
  start_time = Column(Time)
  ```

- **Enum**：枚举类型，用于存储有限的预定义值。
  ```python
  status = Column(Enum('pending', 'completed', 'cancelled', name='order_status'))
  ```

- **PickledType**：用于存储 Python 对象的序列化形式。
  ```python
  settings = Column(PickledType)
  ```

- **LargeBinary**：二进制大对象类型。
  ```python
  image_data = Column(LargeBinary)
  ```

- **Unicode** 和 **UnicodeText**：Unicode 字符串类型，支持非 ASCII 字符。
  ```python
  name = Column(Unicode(50))
  description = Column(UnicodeText)
  ```

- **SmallInteger**：小型整数类型。
  ```python
  quantity = Column(SmallInteger)
  ```

- **BigInteger**：大整数类型。
  ```python
  large_number = Column(BigInteger)
  ```

- **Interval**：间隔类型，用于存储时间间隔。
  ```python
  duration = Column(Interval)
  ```

- **CLOB**：字符大对象类型。
  ```python
  text_data = Column(CLOB)
  ```

- **BLOB**：二进制大对象类型。
  ```python
  binary_data = Column(BLOB)
  ```

- **JSON** 和 **JSONB**：JSON 数据类型，支持存储结构化的 JSON 数据。
  ```python
  settings = Column(JSON)
  ```

- **ARRAY**：数组类型，用于存储列表或数组。
  ```python
  tags = Column(ARRAY(String))
  ```

- **UniqueIdentifier (UUID)**：唯一标识符类型。
  ```python
  uuid = Column(UniqueIdentifier)
  ```

- **Binary**：固定长度的二进制数据类型。
  ```python
  hash = Column(Binary(32))
  ```

下面是一个使用 SQLAlchemy 数据类型的简单示例：

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///example.db")
Base = declarative_base()

class Product(Base):
    __tablename__ = 't_products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    is_available = Column(Boolean)
    status = Column(Enum('available', 'unavailable', name='product_status'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 插入数据
product = Product(name="Laptop", price=1000.0, stock=50, is_available=True, status='available')
session.add(product)
session.commit()

# 查询数据
products = session.query(Product).filter_by(is_available=True).all()
for product in products:
    print(product.name, product.price)
```



### （2）Column常用参数

在 SQLAlchemy 中，`Column` 类是定义数据库表列的基本单元。`Column` 类有许多可选参数，这些参数可以用来详细地配置列的行为和属性。下面是 `Column` 类的一些常用参数及其说明：

**type_**（必须）

这是 `Column` 的第一个参数，指定了列的数据类型。例如 `Integer`、`String` 等。

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    id = Column(Integer)
    name = Column(String)
```

**nullable**（默认为 `True`）

指定列是否可以接受 `NULL` 值。如果设置为 `False`，则表示该列不允许为空。

```python
age = Column(Integer, nullable=False)
```

**default**（默认为 `None`）

指定列的默认值。可以是一个值或者是一个可调用的对象，如果是可调用的，则每次插入新行时都会调用该函数来获取默认值。

```python
from datetime import datetime

created_at = Column(DateTime, default=datetime.utcnow)
```

**server_default**（默认为 `None`）

指定在数据库级别设置的默认值。通常用于设置默认值，该值在插入时由数据库服务器计算。

```python
created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
```

**primary_key**（默认为 `False`）

指定该列为表的主键。如果设置为 `True`，则该列为表的唯一标识符。

```python
id = Column(Integer, primary_key=True)
```

**unique**（默认为 `False`）

指定该列是否具有唯一性约束。如果设置为 `True`，则该列的值在整个表中必须是唯一的。

```python
email = Column(String, unique=True)
```

 **index**（默认为 `False`）

指定是否为该列创建索引。如果设置为 `True`，则会为该列创建索引。

```python
email = Column(String, index=True)
```

**autoincrement**（默认为 `None`）

指定主键是否自动递增。如果设置为 `True`，则主键会自动递增。通常用于主键列。

```python
id = Column(Integer, primary_key=True, autoincrement=True)
```

**info**（默认为 `{}`）

用于存储任意的元数据，可以是字典形式的任何数据。

```python
extra_info = Column(String, info={'my_info': 'This is extra info'})
```

**comment**（默认为 `None`）

在某些数据库中（如 MySQL），可以为列添加注释。

```python
description = Column(String, comment='This is the description column.')
```

**foreign_keys**（默认为 `None`）

指定该列为外键，关联其他表的主键。

```python
from sqlalchemy import ForeignKey

class Order(Base):
    user_id = Column(Integer, ForeignKey('users.id'))
```

**onupdate**（默认为 `None`）

指定列在更新时的默认值。可以是一个值或者是一个可调用的对象。

```python
last_updated = Column(DateTime, onupdate=datetime.utcnow)
```

下面是一个使用多个 `Column` 参数的示例：

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
```

在这个示例中：

- `User` 表包含了 `id`（主键，自动递增）、`name`（不可为空）、`email`（唯一，有索引）、`password`（不可为空）、`created_at`（默认值为当前时间）、`last_login`（在更新时设置为当前时间）和 `is_active`（默认为 `True`）等字段。
- `Post` 表包含了 `id`（主键，自动递增）、`title`（不可为空）、`content`（不可为空）、`author_id`（外键，引用 `users` 表的 `id` 列）、`created_at`（服务器默认值为当前时间戳）等字段。

