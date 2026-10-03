## 删除数据 注意事项

ORM层面 删除数据，会无视mysql级别的外键约束

直接会将对应的数据删除，然后将从表中的那个外键设置为NULL，也就是数据库的 SET NULL 

如果想要避免这种行为，应该将从表中的外键的 nullable=False


```python
from sqlalchemy import Column,Integer,String,Text,ForeignKey,create_engine, Table
from sqlalchemy.orm  import relationship, sessionmaker, backref

from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    """用户"""
    
    # 表名
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))


class Article(Base):
    """文章"""
    
    # 表名
    __tablename__ = 't_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    
    uid = Column(Integer, ForeignKey("t_user.id"))
    # uid = Column(Integer, ForeignKey("t_user.id"),nullable = False)
    
    user = relationship('User',backref='articles')


def create_data():
    """创建数据"""
    # 删除已有的表
    Base.metadata.drop_all() 
    
    # 创建映射表
    Base.metadata.create_all() 
    
    # 初始化数据
    user = User(name='SXT')
    art1 = Article(title='Python', uid=1)
    art2 = Article(title='MySQL', uid=1)
    user.articles.append(art1)
    user.articles.append(art2)

    with Session() as ses:
        ses.add(user)
        ses.commit()
        
def delete_data():
    """删除数据"""
    
    # 默认删除主表数据时，会将子表的引用主表数据的外键设置Null
    with Session() as ses:
        user = ses.query(User).first()
        ses.delete(user)
        ses.commit()
        
if __name__ == '__main__':
    create_data()
    delete_data()



```

## relationship方法中的 cascade

在 SQLAlchemy，只要将一个数据添加到 session中，和他相关联的数据都可以一起存入到数据库中了。

这些是怎么设置的呢？其实是通过 relationship 的时候，有一个关键字 参数cascade 可以设置这些属性

**cascade 属性值为：**

**save-update：** 默认选项。在添加一条数据的时候，会把其他和他相关联的数据都添加到数据库中。

**delete：** 表示当删除某一个模型中的数据的时候，是否也删掉使用 relationship 和他关联的数据

**delete-orphan：** 表示当对一个 ORM对象 解除了父表中的关联对象的时候，自己便会被删除掉。当然如果父表中的数据被删除，自己也会被删除。这个选项只能用在一对多上，并且还需要在子模型中的 relationship 中，增加一个 single_parent=True 的参数。

**merge：** 默认选项。当在使用session.merge，合并一个对象的时候，会将使用了relationship相关联的对象也进行merge操作。

**expunge：** 移除操作的时候，会将相关联的对象也进行移除。这个操作只是从session中移除，并不会真正的从数据库中删除。

**all：** 是对save-update, merge, refresh-expire, expunge, delete几种的缩写。


```python
from sqlalchemy import Column,Integer,String,Text,ForeignKey,create_engine, Table
from sqlalchemy.orm  import relationship, sessionmaker, backref

from sqlalchemy.ext.declarative import declarative_base

# 链接数据库
HOST = '127.0.0.1' 
PORT = 3306
DATA_BASE = 'flask_db'
USER = 'root'
PWD = 'zxydsg123'
DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'

engine = create_engine(DB_URI)
Base = declarative_base(engine)
Session = sessionmaker(engine)



class User(Base):
    """用户"""
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))

    # articles = relationship('Article',backref='user',cascade='') 
    
    # 默认cascade的值是save-update
    # articles = relationship('Article',backref='user',cascade='save-update') 
    
    # delete可以帮助删除关联表的数据
    # articles = relationship('Article',backref='user',cascade='save-update,delete') 
    
    # 当关联关系被解除时，子表数据会被清空
    # articles = relationship('Article',backref='user',cascade='save-update,delete,delete-orphan',single_parent=True)  

class Article(Base):
    """文章"""
    __tablename__ = 't_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    uid = Column(Integer, ForeignKey("t_user.id"))
    
    # user = relationship('User',backref='articles',cascade='save-update,delete') # 会把主表的数据删除
    user = relationship('User',backref=backref('articles',cascade='save-update, delete, delete-orphan')) 


def create_data():
    """创建数据"""
    
    # 删除已有的表
    Base.metadata.drop_all() 
    
    # 创建表
    Base.metadata.create_all() 
    
    # 初始化数据
    user = User(name='SXT')
    art1 = Article(title='Python', uid=1)
    art2 = Article(title='MySQL', uid=1)
    user.articles.append(art1)
    user.articles.append(art2)
    
    # 保存数据
    with Session() as ses:
        ses.add(user)
        ses.commit()
        
def delete_data():
    """删除用户数据"""
    with Session() as ses:
        user = ses.query(User).first()
        ses.delete(user)
        ses.commit()

def delete_art():
    """删除文章数据"""
    with Session() as ses:
        art = ses.query(Article).first()
        ses.delete(art)
        ses.commit()

def update_data():
    with Session() as ses:
        user = ses.query(User).first()
        user.articles = []
        ses.commit()

if __name__ == '__main__':
    create_data()
    delete_data()

```











## 图书管理系统

```
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
engine = create_engine('sqlite:///books.db')
Base = declarative_base()

# 定义图书模型
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 添加图书
def add_book(title, author):
    new_book = Book(title=title, author=author)
    session.add(new_book)
    session.commit()
    print(f"图书《{title}》添加成功！")

# 查询所有图书
def get_all_books():
    books = session.query(Book).all()
    for book in books:
        print(f"ID: {book.id}, 书名: {book.title}, 作者: {book.author}")

# 根据 ID 修改图书信息
def update_book(book_id, title=None, author=None):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        if title:
            book.title = title
        if author:
            book.author = author
        session.commit()
        print(f"图书 ID 为 {book_id} 的信息更新成功！")
    else:
        print(f"未找到 ID 为 {book_id} 的图书。")

# 根据 ID 删除图书
def delete_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        session.delete(book)
        session.commit()
        print(f"图书 ID 为 {book_id} 的图书已删除！")
    else:
        print(f"未找到 ID 为 {book_id} 的图书。")

# 示例操作
add_book("Python 编程入门", "张三")
get_all_books()
update_book(1, title="Python 高级编程")
get_all_books()
delete_book(1)
get_all_books()

session.close()
```





学生管理系统

```
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
engine = create_engine('sqlite:///students.db')
Base = declarative_base()

# 定义学生模型
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Float)

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 添加学生信息
def add_student(name, score):
    new_student = Student(name=name, score=score)
    session.add(new_student)
    session.commit()
    print(f"学生 {name} 的信息添加成功！")

# 查询所有学生信息
def get_all_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, 姓名: {student.name}, 成绩: {student.score}")

# 查询平均分
def get_average_score():
    total_score = session.query(func.sum(Student.score)).scalar()
    student_count = session.query(Student).count()
    if student_count > 0:
        average_score = total_score / student_count
        print(f"学生的平均成绩为: {average_score}")
    else:
        print("暂无学生信息。")

# 示例操作
from sqlalchemy import func
add_student("李四", 85)
add_student("王五", 90)
get_all_students()
get_average_score()

session.close()
```







代办事项管理系统

```
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
engine = create_engine('sqlite:///todos.db')
Base = declarative_base()

# 定义待办事项模型
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    completed = Column(Boolean, default=False)

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 添加待办事项
def add_todo(task):
    new_todo = Todo(task=task)
    session.add(new_todo)
    session.commit()
    print(f"待办事项 '{task}' 添加成功！")

# 查看所有待办事项
def get_all_todos():
    todos = session.query(Todo).all()
    for todo in todos:
        status = "已完成" if todo.completed else "未完成"
        print(f"ID: {todo.id}, 事项: {todo.task}, 状态: {status}")

# 标记待办事项为完成
def mark_todo_completed(todo_id):
    todo = session.query(Todo).filter_by(id=todo_id).first()
    if todo:
        todo.completed = True
        session.commit()
        print(f"待办事项 ID 为 {todo_id} 已标记为完成！")
    else:
        print(f"未找到 ID 为 {todo_id} 的待办事项。")

# 示例操作
add_todo("学习 SQLAlchemy")
get_all_todos()
mark_todo_completed(1)
get_all_todos()

session.close()
```

