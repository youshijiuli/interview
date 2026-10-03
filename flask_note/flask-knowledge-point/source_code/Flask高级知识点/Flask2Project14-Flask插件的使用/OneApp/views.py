from flask import Blueprint, request, render_template
from .models import *
from .exts import cache
import time


blue = Blueprint('blue', __name__)


# cache的两种使用方法之一：用装饰器cached来缓存
@cache.cached(timeout=3)  # 使用装饰器cached来缓存index函数的结果，设置缓存超时时间为3秒
@blue.route('/')
def index():
    # 利用延时来判断是否使用了缓存
    # 如果使用了缓存，那么就不会延迟等待，立刻返回响应。
    # 如果没有使用缓存，就会等5秒才会返回响应
    time.sleep(5)

    return render_template('index.html')



# cache的两种使用方法之二：手动set和get来缓存
@blue.route('/test/')
def test():

    # 从缓存中获取数据
    ip = cache.get('ip')  # 如果缓存中存在ip数据，说明请求速度过快，返回提示信息

    if ip:
        return '你的请求速度过快！请稍后再试！'
    else:
        # 存储数据到缓存
        ip = request.remote_addr   # 如果缓存中不存在ip数据，将用户的IP地址存储到缓存中，并设置超时时间为1秒
        cache.set('ip', ip, timeout=1)
        # 渲染并返回index.html模板
        return render_template('index.html')
