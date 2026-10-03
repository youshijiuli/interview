# 导入Flask库
from flask import Flask
# 从当前目录下的views模块中导入blue对象
from .views import blue
# 从当前目录下面的exts模块中导入初始化插件函数
from .exts import init_exts


# 定义一个创建应用的函数
def create_app():
    # 创建一个Flask应用实例
    app = Flask(__name__)
    
    # 注册蓝图，将blue对象注册到app上
    app.register_blueprint(blueprint=blue)

    # 设置数据库连接URI
    DB_URI = 'sqlite:///sqlite3.db'  # 这是连接sqlite数据的设置
    
    # DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    #     USERNAME,
    #     PASSWORD,
    #     HOSTNAME,
    #     PORT,
    #     DATABASE
    # )  # 这是连接MySQL数据库的设置


    # 将数据库连接URI配置到app的配置中
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    # 关闭SQLAlchemy的事件系统，提高性能
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化插件
    init_exts(app)

    # 返回创建好的Flask应用实例
    return app
