# 使用插件有三步
# 第一步：导包
from flask_caching import Cache

# 第二步：实例化
cache = Cache(config={'CACHE_TYPE': 'simple'})

# 第三步：绑定app
def init_exts(app):
    cache.init_app(app=app)



"""
flask-caching支持多种缓存后端，包括但不限于：

- simple: 基于Python字典的简单内存缓存，适用于单进程环境。
- redis: 使用Redis作为缓存后端，适合多进程或多机部署。
- memcached: 利用Memcached服务进行缓存，也是分布式缓存的优秀选择。
- filesystem: 文件系统缓存，将缓存数据存储在文件中。
"""