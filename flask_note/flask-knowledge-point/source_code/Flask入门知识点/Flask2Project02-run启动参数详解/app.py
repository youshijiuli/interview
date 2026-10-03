# 导入flask
from flask import Flask


# 实例化app对象
app = Flask(__name__)


# 创建视图函数并绑定路由
@app.route('/')
def index():
    return 'hello flask'


if __name__ == '__main__':
    """
    run()方法的三个重要参数：
    # debug:  是否开启调试模式，开启后修改Python代码后会自动重启
    # port :  启动指定服务器的端口号，默认是5000
    # host :  主机，默认是127.0.0.1，指定为0.0.0.0代表任何人可访问
    """
    app.run(debug=True, host='0.0.0.0', port=5001)
