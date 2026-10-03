# 导入flask包和render_template模版渲染函数
from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.route('/index/')
def index():

    # 视图函数可以返回三种Response对象
    # 第一种：返回字符串
    # return 'hello flask!'

    # 第二种：返回JSON
    json_dict = {
        'name': 'xiaodai',
        'age': 18,
        'comment': 'render_template函数可以渲染模版；jsonify可以反序列化成字符串。'
    }
    # return jsonify(json_dict)

    # 第三种：渲染模版
    # return render_template('index.html')  # 函数会自动找到templates文件
    return render_template('index.html', **json_dict)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
