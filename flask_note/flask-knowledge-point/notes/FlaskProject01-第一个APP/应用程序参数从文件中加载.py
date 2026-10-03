from flask import Flask


app = Flask(__name__)

# 从一个叫做settings.py的文件中导入应用程序的配置
app.config.from_pyfile('settings.py')


@app.route('/')
def index():

    # 类似字典取值一样获取配置参数
    user = app.config['USER']
    pwd = app.config.get('PWD')  # 可以使用get
    print(user, pwd)

    return 'hello ' + user


if __name__ == "__main__":

    app.run()
