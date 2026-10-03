from flask import Flask, url_for, redirect


# 复习一下Flask的配置
# 第一种：使用类的方式
class MyConfig(object):

    USER = '小呆'


# 实例化主应用
app = Flask(__name__)

# 要将配置类注册到app里面
app.config.from_object(MyConfig)


@app.route('/')
def index():
    # 1. 反向解析
    # url_for函数可以反向解析出路由地址
    # path = url_for('demo1')  # 如果视图有参数，你不传就会报错
    path = url_for('demo1', page=2, num=100)
    print(path, type(path))  # /demo1/2?num=100 <class 'str'>

    return 'hello'


@app.route('/demo1/<int:page>')
def demo1(page):

    print(app.config.get('USER') + str(page))

    return f"page={page}"


@app.route('/demo2')
def demo2():
    # 2.重定向
    # redirect函数可以做重定向
    # 传入一个代表路由路径的字符串就行
    # 可以配合url_for来使用
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
