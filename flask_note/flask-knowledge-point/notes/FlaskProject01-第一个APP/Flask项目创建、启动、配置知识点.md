# 一、第一个Flask

## （1）安装环境

```
创建虚拟环境
mkvirturalenv flask

安装Flask
pip install flask
```

## （2）创建项目

方法一：直接创建个文件夹，里面写上app.py文件就可以了

方法二：在PyCharm中创建。

## （3）启动程序

如何启动Flask应用？

```
在命令行中有两种方式启动Flask的Web应用
1. python app.py

2. 配置环境变量后使用flask run启动
	- 先配置环境变量，Windows系统下输入 set FLASK_APP=app.py  若是Linux系统下则改成 exprot FLASK_APP=app.py
	- 然后输入 flask run 来启动，还能指定参数 flask run --host 0.0.0.0
```

## （4）访问项目

访问项目，在浏览器输入你配置的路由即可。

```
# 默认
http://127.0.0.1:5000
# 配置后
http://0.0.0.0:80
```

## （5）参数说明

接下来就来详细查看一下Flask应用程序在创建的时候一些需要我们关注的

### ① Flask参数

```
import_name
	Flask程序所在的模块（包），传__name__就可以
	其可以决定Flask在访问静态文件的查找的路径

static_url_path
	静态文件访问路径，可不传，默认为 / + static_folder

static_folder
	静态文件存储的文件，可以不传，默认为static

template_folder
	模版文件存储的文件夹，可以不传，默认为templates
```

默认参数情况下

```
app = Flask(__name__)

|---static
|    |--- 1.png
|---templates
|    |--- index.html
|---app.py

访问 127.0.0.1:80/static/1.png 就可以访问到图片
```

修改参数的情况下

```
app = Flask(__name__, static_url_path='/url_path_param', static_folder='folder_param')


|---folder_param # 此处目录名变化
|    |--- 1.png
|---app.py

访问127.0.0.1:80/url_path_param/1.png 才可以访问到图片
```

### ② app.run参数

可以指定运行的主机IP地址，端口，是否开启Flask框架的调试模式

```
app.run(host="0.0.0.0", port=8080, debug=True)

注：IP代表0.0.0.0代表当前计算机的所有IP地址
```

关于DEBUG调试模式

1. 程序代码修改后可以自动重启服务器
2. 在服务器出现相关错误的时候，可以直接将错误信息返回到前端进行展示。

## （6）应用程序配置参数

应用程序配置参数设置的是一个Web应用工程的相关信息，比如：

- 数据库的连接信息
- 日志的配置信息
- 自定义的配置信息
- ...

注意：这样可以集中管理项目的所有配置信息



Flask将配置信息保存了app.config属性中，该属性可以按照字典类型进行操作。

### ① 从配置对象中加载

```python
# app.config.from_object(配置对象)

class DefaultConfig(object):
    """ 默认配置 """
    USER = 'ROOT'

app = Flask(__name__)

app.config.from_object(DefaultConfig)

@app.route('/')
def index():
    print(app.config['USER'])
    return "hello"
```

这样的好处是可以在项目开发中来继承：

```python
class MyDevelopmentConfig(DefaultConfig):
    DEBUG=True
```

### ② 从配置文件中加载

新建一个配置文件setting.py，这个文件中的内容是：参数名=参数值，比如USER='root'

```python
# app.config.from_pyfile(配置文件)
app = Flask(__name__)

app.config.from_pyfile('setting.py')

@app.route('/')
def index():
    print(app.config['USER'])
    return 'hello'
```

### ③ 从环境变量中加载

Flask使用环境变量加载配置的本质是通过环境变量的值来找到配置文件，再读取配置文件的信息，其使用方式为：

```python
app.config.from_envvar('环境变量名')
```

环境变量的值为配置文件的绝对路径，

先在终端执行如下命令：

```python
export PROJECT_SETTING="~/setting.py"
```

```python
app = Flask(__name__)

app.config.from_envvar('PROJECT_SETTING', silent=True)

@app.route("/")
def index():
    print(app.config['USER'])
    return "hello"
```

silent参数：

- False表示不安静的处理，没有值时报错通知，默认为False
- True表示安静的处理，即使没有值也让Flask正常的运行下去

注：设置了环境变量后pycharm可能找不到，需要重启一下pycharm

### ④ 从PyCharm中的运行时设置环境变量的方式加载

使用非常少，在运行按钮的右上角，Edit Configurations配置Enviroment variables



### ⑤ 企业项目开发常用的方式

使用工厂模式创建Flask app，并结合使用配置对象与环境变量加载配置。

- 使用配置对象加载默认配置
- 使用环境变量加载不想出现在代码中的敏感配置信息

```python
def create_flask_app(config):
    """
    创建Flask应用
    :param config: 配置对象
    :return Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(config)
    # 从环境变量指向的配置文件中读取的配置信息会覆盖掉从配置对象中加载的同名参数
    app.config.from_envvar("PROJECT_SETTING", silent=True)
    return app

class DefaultConfig(object):
    """ 默认配置 """
    USER = 'ROOT'

    
class DevelopmentConfig(DefaultConfig):
    """ 开发配置 """
    DEBUG=True


# app = create_flask_app(DefaultConfig)
app = create_flask_app(DevelopmentConfig)

@app.route('/')
def index():
    print(app.config['USER'])
    return 'hello'
```
