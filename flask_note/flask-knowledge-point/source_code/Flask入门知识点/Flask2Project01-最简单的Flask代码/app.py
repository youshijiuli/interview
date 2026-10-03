# 导入flask包
from flask import Flask


# 创建app，它是一个Flask应用对象
app = Flask(__name__)


# 定义视图函数并绑定路由
@app.route('/')  # 这里和Django不一样，Django是前面不能有斜杠，Flask是前面必须有斜杠
def index():
	return 'hello flask!'


if __name__ == '__main__':
	app.run()