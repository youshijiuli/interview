# 路由



从之前的`helloworld.py`⽂件中，我们已经看到，⼀个URL要与执⾏函数进⾏映射，使⽤的是@app.route装饰器。@app.route装饰器中，可以指定URL的规则来进⾏更加详细的映射，⽐如现在要映射⼀个⽂章详情的URL，⽂章详情的URL是/article/id/，id有可能为1、2、3...,那么可以通过以下⽅式  

```python
@app.route('/article/<id>/')
def hello(aid):
    return f'article{aid}'
```



```python
from flask import Flask

app = Flask(__name__)

# @app.route('/article/details/86714886')
# def index1():
#     return '/article/details/86714886'

# @app.route('/article/details/103582822')
# def index2():
#     return '/article/details/103582822'

@app.route('/article/details/<id>')
def index(id):
    
    print(f'接收到的文章ID是：{id}')
    # 获取到ID后，去数据库查询数据

    return f'返回了，{id}的文章'

if __name__ == '__main__':
    app.run()
```

其中，尖括号是固定写法，语法为，variable默认的数据类型是字符串。如果需
要指定类型，则要写成converter:variable，其中converter就是类型名称，可
以有以下⼏种  :

- str：默认的数据类型，接受没有任何斜杠/的字符串。

- int: 整形

- float: 浮点型。

- path： 和string类似，但是可以传递斜杠/。

- uuid： uuid类型的字符串。

- any：可以指定多种路径



```python
@app.route('/<any(article,blog):url_path>/')
def item(url_path):
	return url_path
```



```python
from flask import Flask

app = Flask(__name__)

@app.route('/article/<id>')
def index(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'


@app.route('/int/<int:id>')
def index_int(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'


@app.route('/float/<float:id>')
def index_float(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'


@app.route('/str/<string:id>')
def index_str(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'


@app.route('/path/<path:id>')
def index_path(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'

@app.route('/uuid/<uuid:id>')
def index_uuid(id):
    
    print(f'接收到的文章ID是：{id}')
    print(type(id))
    return f'返回了，{id}的文章'

@app.route('/<any(user,item):tmp>/<int:id>')
def index_any(tmp,id):
    if tmp == 'user':
        return f'返回了一个编号为 {id} 的 用户 信息'
    elif tmp =='item':
        return f'返回了一个编号为 {id} 的 元素 信息'

from werkzeug.routing import BaseConverter

# user/[1,2,3]
# item/[1,2,3]
# vip/[1,2,3]
if __name__ == '__main__':
    app.run(debug=True)
```



限定路由参数的类型，flask系统自带转换器编写在werkzeug/routing.py文件中。底部可以看到以下字典：

```python
DEFAULT_CONVERTERS = {
   "default": UnicodeConverter,
   "string": UnicodeConverter,
   "any": AnyConverter,
   "path": PathConverter,
   "int": IntegerConverter,
   "float": FloatConverter,
   "uuid": UUIDConverter,
}
```

  

系统自带的转换器具体使用方式在每种转换器的注释代码中有写，请留意每种转换器初始化的参数。

| 转换器名称 | 描述                                                   |
| :--------- | :----------------------------------------------------- |
| string     | 默认类型，接受不带斜杠的任何文本                       |
| int        | 接受正整数                                             |
| float      | 接受正浮点值                                           |
| path       | 接收`string`但也接受斜线                               |
| uuid       | 接受UUID（通用唯一识别码）字符串 xxxx-xxxx-xxxxx-xxxxx |

  



```python
# 限定类型传递路由参数
# flask内置的所有路由转换器是由werkzeug.routing的DEFAULT_CONVERTERS字典进行配置的。
# flask的所有路由转换器,本质上就是路由经过正则来进行匹配获取参数值的。所有的路由转换器都必须直接或间接继承于BaseConverter路由转换器基类

from flask import Flask

# 应用实例对象
app = Flask(__name__)

# 路由
@app.route(rule='/demo1')
def demo1():
    return 'demo1'

# 路由参数[不限定数据类型]
@app.route('/user/<user_id>')
def user(user_id): # 必须在视图方法中，通过变量名来接受参数
    return f'hello {user_id}'

# 路由参数[限定数据类型]
@app.route("/sms1/<int:num>")
def sms1(num):
    return f"发送短信{num}条"

@app.route("/sms2/<int(min=1, max=100):num>")
def sms2(num):
    return f"发送短信{num}条"

@app.route("/sms3/<string(minlength=11, maxlength=11):mobile>")
def sms3(mobile):
    return f"发送短信给手机号：{mobile}"


if __name__ == '__main__':
    # 启动项目的web应用程序
    app.run(host="0.0.0.0", port=5000, debug=True)
```





如果不想定制⼦路径来传递参数，也可以通过传统的?=的形式来传递参数，例如：/article?id=xxx，这种情况下，可以通过request.args.get('id')来获取id的值。如果是post⽅法，则可以通过request.form.get('id')来进⾏获取。







#### 正则路由

``` python
from flask import Flask,render_template

app = Flask(__name__)
from werkzeug.routing import BaseConverter


class RegConverter(BaseConverter):
    def __init__(self, map, regex):
        super().__init__(map)
        self.regex = regex
app.url_map.converters['regex'] = RegConverter

@app.route('/index/<regex("\d+"):x1>')
def index(x1):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```







### 自定义URL转换器



1. 实现一个类，继承自`BaseConverter`。

2. 在自定义的类中，重写`regex`，也就是这个变量的正则表达式。

3. 将自定义的类，映射到`app.url_map.converters`上。比如：

	```python
	app.url_map.converters['tel'] = TelephoneConverter
	```

	实例：

```python
from flask import Flask,url_for
from werkzeug.routing import BaseConverter

app = Flask(__name__)

#一个url中，含有手机号码的变量，必须限定这个变量的字符串格式满足手机号码的格式
class TelephoneConveter(BaseConverter):
    regex = r'1[85734]\d{9}'

app.url_map.converters['tel'] = TelephoneConveter

@app.route('/telephone/<tel:my_tel>/')
def my_tel(my_tel):
    return '您的手机号码是：%s' % my_tel

if __name__ == '__main__':
    app.run(debug=True)
```

