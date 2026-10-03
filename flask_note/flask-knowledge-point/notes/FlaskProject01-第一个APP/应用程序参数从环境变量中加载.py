from flask import Flask


def create_flask_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    # silent参数的意思是如果没有找到环境变量也不报错
    app.config.from_envvar("PROJECT_SETTING", silent=True)

    return app


class DefaultConfig():
    """ 默认配置 """
    USER = "ROOT"


class DevelopemntConfig(DefaultConfig):
    """ 开发配置 """
    DEBUG = True


app = create_flask_app(DevelopemntConfig)


@app.route('/')
def index():

    return 'hello ' + app.config['USER']


if __name__ == '__main__':
    app.run()
