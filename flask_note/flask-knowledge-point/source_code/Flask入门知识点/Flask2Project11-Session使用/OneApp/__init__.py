from flask import Flask  # 导入Flask模块
from .views import blue  # 从当前目录下的views模块中导入blue对象
import datetime  # 导入datetime模块

def create_app():  # 定义一个创建应用的函数

    app = Flask(__name__)  # 创建一个Flask应用实例

    # 配置session秘钥
    app.config['SECRET_KEY'] = 'xiaodai'  # 设置Flask应用的秘钥为'xiaodai'
    # 设置session过期时间
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)  # 设置session的过期时间为31天
    
    app.register_blueprint(blueprint=blue)  # 注册蓝图，将blue对象注册到Flask应用中

    return app  # 返回创建好的Flask应用实例
