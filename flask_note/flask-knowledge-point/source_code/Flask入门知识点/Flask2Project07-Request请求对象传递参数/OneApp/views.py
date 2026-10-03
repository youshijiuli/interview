# 导入蓝图和请求模块
from flask import Blueprint, request
# 导入渲染模板模块
from flask import render_template
# 导入模型模块
from .models import *

# 创建一个蓝图对象，命名为myblue
myblue = Blueprint('myblue', __name__)

# 定义路由和视图函数
@myblue.route('/', methods=['get', 'post'])
def index():
    """
    Request对象，从flask包里面导入
    属性
    - url   完整请求地址
    - base_url  去掉请求参数的url
    - host_url  只有主机号和端口号的url
    - path      路由中的路径
    - method    请求方式
    - remote_addr   请求的客户端地址
    - args      get请求参数
    - form      post请求参数
    - files     文件上传
    - headers   请求头
    - cookies   请求头中的cookie
    - user_agent    用户代理，包括浏览器和操作系统的信息
    """
    # 创建一个字典，用于存储请求相关的信息
    context = {
        'url': request.url,
        'base_url': request.base_url,
        'host_url': request.host_url,
        'path': request.path,
        'method': request.method,
        'remote_addr': request.remote_addr,
        'headers': request.headers,
        'user_agent': request.user_agent
    }
    # 用args属性取出get请求参数的三种方法
    # args返回的是一个类字典对象ImmutableMultiDict([])
    # print(request.args['name'])  # 取不到，会报错
    print(request.args.get('name'))  # 取不到，不会报错
    print(request.args.getlist('name'))

    # 取出post请求参数的方法
    # form返回一个类字典对象ImmutableMultiDict([])
    print(request.form)
    # print(request.form['name'])  # 取不到，会报错
    print(request.form.get('name'))  # 取不到，不会报错

    # 取出cookie
    # cookies属性返回的也是一个类字典对象ImmutableMultiDict([])
    print(request.cookies)
    print(request.cookies['name'])
    print(request.cookies.get('name'))

    # 取出请求过来的文件files
    # files属性返回的是一个类字典对象ImmutableMultiDict([])
    print(request.files)
    print(request.headers)
    
    # 使用render_template渲染模板，并将context传递给模板
    return render_template('index.html', **context)
