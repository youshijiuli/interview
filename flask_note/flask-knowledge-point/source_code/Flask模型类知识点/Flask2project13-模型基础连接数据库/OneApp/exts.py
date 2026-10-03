# 连接数据库要安装一些插件
"""
用于ORM：pip install flask-sqlalchemy

用于数据迁移：pip install flask-migrate

用于MySQL驱动：pip install pymysql
"""

# 插件的使用方法可以总结成三步：

# 1. 导入第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 2. 实例化插件对象
db = SQLAlchemy()
migrate = Migrate()

# 3. 绑定app
def init_exts(app):

    db.init_app(app=app)  # 初始化数据库插件
    migrate.init_app(app=app, db=db)  # 初始化迁移插件，并关联数据库插件

