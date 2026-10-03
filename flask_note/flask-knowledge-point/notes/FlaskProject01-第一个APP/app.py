# 导入Flask
from flask import Flask

# 实例化主应用app
# Flask的常用参数
"""
    name: 应用的导入名称，默认为传入的参数。这个名称用来确定应用相关的路径。
    import_name: 指定一个导入名，这通常用于更复杂的设置场景。
    static_folder: 静态文件（如CSS, JavaScript, 图片等）所在的目录，默认是 'static'。
    static_url_path: 访问静态文件的 URL 前缀，默认与 static_folder 相同。
    template_folder: 模板文件所在的目录，默认是 'templates'。
    root_path: 应用根路径，如果未设置，则默认为模块所在的文件夹。
"""
# app = Flask(__name__)
app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)



# 创建视图函数
@app.route('/')
def hello_world():

    return 'Hello World!'


# 主程序
if __name__ == '__main__':
    # run() 方法的常用参数
    # 1. host 配置访问主机IP
    # 2. port 端口号默认5000
    # 3. debug 启用debug模式

    app.run(host='0.0.0.0', port=8000, debug=True)
    # app.run()
