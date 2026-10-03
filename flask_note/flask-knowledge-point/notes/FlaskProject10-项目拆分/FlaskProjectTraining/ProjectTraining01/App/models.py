# models.py：模型，ORM数据库
from .exts import db


# 模型类必须继承 db.Model
class User(db.Model):

    # 表名
    __tablename__ = 't_user'

    # 表字段
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, index=True)
    age = db.Column(db.Integer, default=1)
    gender = db.Column(db.Boolean, default=True)
    salary = db.Column(db.Float, default=3000.3, nullable=False)
