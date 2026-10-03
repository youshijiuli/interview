from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    在 Flask 框架中，渲染模板通常使用 render_template 函数。
    这个函数位于 Flask 的 flask 模块中，你需要从这个模块导入它以便使用。
    """
    name = 'wangxin'
    hobby= ['runing', 'gaming', 'reading']
    # 第一个参数是渲染的模版路径。后续是参数
    # 默认如果没设置模版路径的话，就会去templates文件夹里面找
    return render_template('index.html', name=name, hobby=hobby)


if __name__ == '__main__':
    app.run(debug=True)
