from flask import Blueprint, request, render_template, jsonify, make_response, Response
from .models import *


myblue = Blueprint('myblue', __name__)


@myblue.route('/', methods=['get', 'post'])
def index():

    # Respose响应对象
    # 视图函数有四种响应方式

    """
    # 第1种：返回字符串（不推荐）
    return 'hello flask!'

    """
    # 第2种：模版渲染
    # render_template函数在flask包里面导入
    # 第一个参数是模版名称；第二个参数是传入模版的数据
    context = {
        'name': 'xiaodai'
    }

    return render_template('index.html', **context)
    # 渲染到模版的参数可以直接关键字传参
    # return render_template('index.html', name='xiaodai', age=18)
    """

    # 第3种：返回json数据（前后端分离）
    # jsonify函数，可以将字典反序列化为字符串
    # jsonify函数在flask包中导入
    return jsonify(context)

    
    # 第4种：自定义Response响应
    html = render_template('index.html', name='xiaodai')
    print(html, type(html))
    # 1. 用make_response函数创建响应对象
    rep = make_response(html, 200)
    # 2. 用Respose类创建响应对象
    # rep = Respose(html)
    return rep
    """