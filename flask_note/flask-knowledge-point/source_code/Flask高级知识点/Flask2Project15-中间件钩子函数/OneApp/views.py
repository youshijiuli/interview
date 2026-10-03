from flask import Blueprint, render_template, request, abort
from .exts import cache
from .models import *


blue = Blueprint('blue', __name__)


@blue.route('/')
@cache.cached(timeout=5)
def index():
    return render_template('index.html')


"""
在 Flask 框架中，“钩子”（Hooks）和“中间件”（Middleware）这两个概念在某些方面相似，
但它们并不完全相同，尽管它们都可以在请求的生命周期中插入自定义的逻辑。

Flask 提供了几种类型
- before_first_request：在处理第一个请求前调用，只执行一次。(Blueprint没有这个钩子)
- before_request：在每个请求之前调用。
- after_request：如果未触发异常，则在每个请求之后调用，用于处理响应。
- teardown_request：无论请求是否成功完成，都会在每个请求之后调用，常用于关闭资源，如数据库连接。
- 错误处理函数：用于处理特定类型的错误。
"""


# @blue.before_request
# def before_request_func():
#     print('这个函数会在每一次请求之前调用！')
#     # 可以在这个钩子里面写反爬验证
#     print(request.path)
#     print(request.method)
#     print(request.remote_addr)   # 检查IP
#     print(request.user_agent)    # 检查UA

#     if 'python' in request.user_agent.string:
#         return '爬虫无法访问！'


# 定义一个名为limit_remote_addr的函数，用于限制客户端IP的请求次数
@blue.before_request
def limit_remote_addr():
    # 获取客户端的IP地址
    client_ip = request.remote_addr
    # 生成缓存键值，用于存储客户端IP的请求次数
    cache_key = 'ip_limit_' + client_ip

    # 从缓存中获取客户端IP的请求次数
    request_count = cache.get(cache_key)
    # 如果缓存中没有该客户端IP的请求次数，则初始化为0
    if request_count is None:
        request_count = 0
    print(request_count)
    # 如果客户端IP的请求次数大于等于5次，封禁IP
    if request_count >= 2:
        # 将客户端IP的请求次数重置为0，并设置缓存超时时间为10秒(封禁10秒)
        cache.set(cache_key, request_count + 1, timeout=10)
        abort(429)  # Too Many Requests HTTP状态码
    else:
        # 如果客户端IP的请求次数小于5次，将其请求次数加1，并设置缓存超时时间为1秒
        cache.set(cache_key, request_count + 1, timeout=1)


@blue.after_request
def after_request_func(response):
    print('这个函数会在每一次请求之后调用！\
        但只有在没发生异常的时候！\
        而且这个函数还会需要接受和返回Response对象')
    return response


@blue.teardown_request
def teardown_request_func(exception):
    print('这个函数无论请求是否成功，都会在请求后调用')
