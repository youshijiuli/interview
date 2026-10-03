# 导入Flask库
from flask import Flask
# 从当前目录下的views模块中导入myblue对象
from .views import myblue


# 定义一个创建Flask应用的函数
def create_app():
    # 创建一个Flask应用实例，并将其命名为app
    app = Flask(__name__)
    # 将myblue蓝图注册到app上
    app.register_blueprint(blueprint=myblue)
    # 返回创建好的Flask应用实例
    return app
