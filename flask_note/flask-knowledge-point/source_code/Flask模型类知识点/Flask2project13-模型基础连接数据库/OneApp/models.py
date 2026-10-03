# models.py : 模型，数据库
from .exts import db


# ORM对象关系映射
"""
模型    ==>   数据库
类      ==>   表结构
类属性  ==>    表字段
一个对象 ==>   表中一行数据
"""

# 模型类必须继承 db.model
class User(db.Model):

    # 表名
    __tablename__ = 'tb_user'

    # 定义表字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, index=True)
    age = db.Column(db.Integer, default=1)
    sex = db.Column(db.Boolean, default=True)
    salary = db.Column(db.Float, default=10000, nullable=False)



"""
执行数据迁移命令：
1. 在CMD或者Terminal中进入项目路径（app.py所在路径）
2. 输入以下命令执行迁移：
    - flask db init         创建迁移文件夹migrates，只调用一次
    - flask db migrate      生成迁移文件
    - flask db upgrade      如果有模型改动则需要升级迁移（执行迁移）
    - flask db downgrade    如果想回到之前的模型版本则需要降级迁移


"""
