from flask_caching import Cache


cache = Cache(config={'CACHE_TYPE': 'simple'})


def init_exts(app):

    cache.init_app(app=app)
