## flask-sqlachemy数据库

先给出一个整体代码

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1314@localhost:3306/flask_test?charset=utf8'

#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s'%self.name
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    ro1 = Role(name='admin')
    ro2 = Role(name='user')
    db.session.add_all([ro1,ro2])
    db.session.commit()
    us1 = User(name='wang',email='wang@163.com',pswd='123456',role_id=ro1.id)
    us2 = User(name='zhang',email='zhang@189.com',pswd='201512',role_id=ro2.id)
    us3 = User(name='chen',email='chen@126.com',pswd='987654',role_id=ro2.id)
    us4 = User(name='zhou',email='zhou@163.com',pswd='456789',role_id=ro1.id)
    db.session.add_all([us1,us2,us3,us4])
    db.session.commit()
    app.run(debug=True)
```



### 1.数据库的设置

***

`SQLAlchemy`是一个关系型数据库框架，它提供了高层的ORM和底层的原生数据库的操作。`flask-sqlalchemy`是一个简化了SQLAlchemy操作的flask扩展。

这里使用mysql数据库

安装扩展

```
pip install flask-sqlalchemy
```

但是，除了这一个当然是不够的，因为我们需要链接到mysql数据库，所以还得安装下面的库：

```
pip install flask-mysqldb
```

使用Flask-SQLAlchemy扩展操作数据库，首先需要建立数据库连接。数据库连接通过URL指定，而且程序使用的数据库必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中，就例如下面这样

![](./images/Day10_1.png)

配置数据库，需要先创建一个数据库

```python
#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1314@localhost:3306/flask_test?charset=utf8'

#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
```



### 2.定义模型

***

模型是表示应用使用的持久化实体，在ORM中，模型一般是一个Python类，类中的属性就是数据库表中的列。

在这里我们来创建两个模型，分别是Role和User

```python
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s'%self.name
```

__tablename__代表着数据库表的名称

下面的代码就是创建来一个整型的列id，以及一个字符串类的列name，并且id设置为主键

```
 # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
```

db.Column类构造函数的第一个参数是数据库列和模型属性的类型。这里为给大家准备了一份常用的SQLAlchemy列类型：

| 类型名       | python中类型      | 说明                                                |
| ------------ | ----------------- | --------------------------------------------------- |
| Integer      | int               | 普通整数，一般是32位                                |
| SmallInteger | int               | 取值范围小的整数，一般是16位                        |
| BigInteger   | int或long         | 不限制精度的整数                                    |
| Float        | float             | 浮点数                                              |
| Numeric      | decimal.Decimal   | 普通整数，一般是32位                                |
| String       | str               | 变长字符串                                          |
| Text         | str               | 变长字符串，对较长或不限长度的字符串做了优化        |
| Unicode      | unicode           | 变长Unicode字符串                                   |
| UnicodeText  | unicode           | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool              | 布尔值                                              |
| Date         | datetime.date     | 时间                                                |
| Time         | datetime.datetime | 日期和时间                                          |
| LargeBinary  | str               | 二进制文件                                          |

同时也给出SQLAlchemy常用的列选项：



| 选项名      | 说明                                              |
| ----------- | ------------------------------------------------- |
| primary_key | 如果为True，代表表的主键                          |
| unique      | 如果为True，代表这列不允许出现重复的值            |
| index       | 如果为True，为这列创建索引，提高查询效率          |
| nullable    | 如果为True，允许有空值，如果为False，不允许有空值 |
| default     | 为这列定义默认值                                  |



### 3.关系

***

![](D:\Code\FlaskNote\images\Day10_2.png)

上图是一个一对多的关系

那么如何通过代码来实现这种关系呢？

```

class Role(db.Model):
   #...
   users = db.relationship('User', backref='role')
   
class User(db.Model):
   # ...
   role_id = db.Column(db.Integer, db.ForeignKey('role_id'))
```

添加到user模型中的role_id列被定义成外键，就是这个外键建立起列关系。传给db.ForeignKey()的参数‘role.id'表明，这列的值是roles表中的相应行的id值。



从“一”那一端可知，添加到Role模型中的users属性代表这个关系的面向对象吃的视角。对于一个Role实例，其users属性将返回和角色相关联的用户组成的列表（也就是“多“那一端）。



db.relationship()的第一个参数表明这个关系的另一端是哪个模型。backref参数向User模型中添加一个role属性，从而定义反向关系。通过User实例的这个属性可以获得对应的Role模型对象，而不用再通过role_id外键获取。

这里给出常用的SQLAlchemy关系选项：

| 选项名         | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| backref        | 在关系的另一模型中添加反向引用                               |
| primary join   | 明确指定两个模型之间使用的联结条件                           |
| uselist        | 如果为False，不使用列表，而使用标量值                        |
| order_by       | 指定关系中记录的排序方式                                     |
| secondary      | 指定多对多中记录的排序方式                                   |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件 |



### 4.数据库的基本操作

***

**1.创建表**

```
db.create_all()
```

**2.删除表**

```
   db.drop_all()
   db.create_all()
```

为什么我要写两行代码呢？因为删除表这种操作只能在你第一次创建表时使用，不然随意使用删除表，你就等着被炒鱿鱼吧。



如果想要更新现有数据库表的结构，可以先删除旧表再重新创建。

**3.插入一条数据**

```
ro1 = Role(name='admin')
db.session.add(ro1)
db.session.commit()
#再次插入一条数据
ro2 = Role(name='user')
db.session.add(ro2)
db.session.commit()
```



可以看到想要插入一条数据，只需要去创建一个模型类的实例，然后通过db.session.add(实例名称)来进行插入即可，非常的形象简单。



当然，如果我们有一百万条数据，一条一条的插入，那岂不是得插到猴年马月？所以这里也有多条数据同时插入的方法。



**4.一次插入多条数据**

```
us1 = User(name='wang',email='wang@163.com',pswd='123456',role_id=ro1.id)
us2 = User(name='zhang',email='zhang@189.com',pswd='201512',role_id=ro2.id)
us3 = User(name='chen',email='chen@126.com',pswd='987654',role_id=ro2.id)
us4 = User(name='zhou',email='zhou@163.com',pswd='456789',role_id=ro1.id)
db.session.add_all([us1,us2,us3,us4])
db.session.commit()
```

通过把模型类实例放入到list当中，然后用add_all函数插入。



**5.更新数据**

```
user = User.query.first()
user.name = 'dong'
db.session.commit()
User.query.first()
```



**6.删除数据**

```
user = User.query.first()
db.session.delete(user)
db.session.commit()
```



**7.精准查询**

返回名字等于wang的所有人：

```
User.query.filter_by(name='wang').all()
```

返回查询到的第一个对象：

```
User.query.first()
```

返回查询到的所有对象：

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiaBYicCQealGrZuHWOiaR1tqqOrpDKDn1Ru2bgl6ThRjW89lW9zokoYS3A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
User.query.all()
```

**filter模糊查询，返回名字结尾字符为g的所有数据：**

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiaECd4j8UmfjEq5w3DZyTOQmanVvyUPVskibFcic0sbpheLJ6icP1WqEmtQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
User.query.filter(User.name.endswith('g')).all()
```

get()，参数为主键，如果主键不存在没有返回内容：

```
User.query.get()
```

逻辑非，返回名字不等于wang的所有数据：

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiacxDu6qgre9Z2UHE8J3SrdPttkicQcwRdEJQvQhtiaT6C7VFdM0gK291g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
User.query.filter(User.name!='wang').all()
```

逻辑与，需要导入and，返回and()条件满足的所有数据：

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiaqMQg68mGJibfsBAgXtu3hcMjV7eNyg8d0HFd5tUln66kEqHbUIhQryw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
from sqlalchemy import and_
User.query.filter(and_(User.name!='wang',User.email.endswith('163.com'))).all()
```

逻辑或，需要导入or_：

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiajJW93dhtSYuUoa39vuW2R0WEtvqaP12aeVnweHkpePhAzj8Bx84ebg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
from sqlalchemy import or_
User.query.filter(or_(User.name!='wang',User.email.endswith('163.com'))).all()
```

### not_ 相当于取反：

![图片](https://mmbiz.qpic.cn/mmbiz_png/MsfpRUYbUlo3rch73QzTbmT4YbvZ0RjiaSrMibDwzU3amZd04OdxvQmvVmjy8cwjKXZIiaVFSj1lammS8XzuJOXuw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```
from sqlalchemy import not_
User.query.filter(not_(User.name=='chen')).all()
```