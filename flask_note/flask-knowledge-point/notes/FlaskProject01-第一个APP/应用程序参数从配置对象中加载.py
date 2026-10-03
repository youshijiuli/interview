from flask import Flask


# 从配置对象中加载应用程序的配置
class DefaultConfig(object):
    """ 默认Web项目的配置 """
    USER = '小呆'
    PWD = '000'


app = Flask(__name__)

# 将配置对象中的配置导入应用程序
app.config.from_object(DefaultConfig)


@app.route('/')
def index():

    # 使用配置对象中的配置，类似字典的方式
    user = app.config['USER']
    pwd = app.config['PWD']
    print(user, pwd)

    return "hello!"



if __name__ == '__main__':
    app.run()
