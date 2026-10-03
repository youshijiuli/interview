from flask import Flask
# 前后端分离架构，要使用flask-restful插件
from flask_restful import Api, Resource


app = Flask(__name__)
# 实例化Api对象
api = Api()


# 创建一个视图类，此时视图和路由已经分离
class HelloResource(Resource):
    """ 视图类必须继承Resource """

    def get(self):
        # 只要是get请求，都会被get方法捕获
        return {"msg": "hello get"}

    def post(self):
        # 只要是post请求，都会被post方法捕获
        return {"msg": "hello post"}


# 路由要单独配置，这里不要将api写错成app了
api.add_resource(HelloResource, '/hello')

# 注册到app上去（这里注意，要先add_resource才能再init_app顺序不能反）
api.init_app(app)

if __name__ == '__main__':
    
    app.run(debug=True)
