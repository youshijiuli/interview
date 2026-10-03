# 使用插件有三步
# 第一步：导包
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# 第二步：实例化
cache = Cache(
    config={
        "CACHE_TYPE": "simple"
    }
)

db = SQLAlchemy()
migrate = Migrate()


# 第三步：绑定app
def init_exts(app):

    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db=db)
