## 视图函数的路由



### 1.视图函数的路由规则说明

***

```

# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "hello flask"


if __name__ == '__main__':
    # 通过url_map可以查看整个flask中的路由信息
    print(app.url_map)
    # 启动flask程序
    app.run(debug=True)
```



首先我们来说说如何查看视图函数的路由：

```
# 通过url_map可以查看整个flask中的路由信息    print(app.url_map)
```

在pycharm运行查看url_map,在terminal里运行

```
python app.py
```

![](D:\Code\FlaskNote\images\Day03_1.png)

大家可以看到输出了一个Map映射的对象，里面有一个列表，列表里就有着路由的详细信息。这里我给大家详细讲解一下里面的内容

```
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,  <Rule '/python/<filename>' (HEAD, OPTIONS, GET) -> static>])
```



这里面有两个规则，首先看第一个，'/' 是我们绑定的主路径，它所对应的视图函数是hello_world，大家可以在上面的完整代码中查看。

那么中间那一部分到底是干啥的呢？中间括号中所代表的是当前视图函数所对应的路径的网络请求方法。HTTP里面的请求方式有很多，之前也跟大家谈到过。



在这个index视图函数中，我们看到默认有GET请求方式，那么如果我想要POST请求方式那该怎么做呢？  

```

@app.route("/post_only", methods=["POST"])
def post_only():
    return "post"
```

输出结果：![](D:\Code\FlaskNote\images\Day03_2.png)



**不同视图函数但有相同的装饰器**

当装饰器和请求方式完全相同时，那么执行的是第一个，如果装饰器相同但是请求方式不相同，那么它们将是独立的个体。

![](D:\Code\FlaskNote\images\Day03_3.png)



![](D:\Code\FlaskNote\images\Day03_5.png)



![](D:\Code\FlaskNote\images\Day03_4.png)



**相同视图函数不同装饰器**

无论是访问hi1还是hi2都是可以执行这个视图函数的

![](D:\Code\FlaskNote\images\Day03_8.png)

![](D:\Code\FlaskNote\images\Day03_7.png)



![](D:\Code\FlaskNote\images\Day03_6.png)



**Flask重定向**

```

# -*- coding: utf-8 -*-
from flask import Flask, redirect

app = Flask(__name__)


@app.route("/hello")
def hello1():
    return "hello 1"


@app.route("/login")
def login():
    url = '/hello'
    return redirect(url)


if __name__ == '__main__':
    # 启动flask程序
    app.run(debug=True)
```

通过访问login的视图函数跳转到/hello装饰器所对应的视图函数上。



我们可以发现上面的url是写死的，那如果某一天我把hello1视图函数的装饰器修改了，那我岂不是还要一个一个去修改？所以这里还有另外一种方法：

```
@app.route("/login")
def login():
    url = url_for("hello1")
    return redirect(url)
```

可以看到我们又导入了一个叫url_for的方法，通过把视图函数的名称放进参数当中就可以找到视图函数所对应的url路径。



###  2.路由提取参数与自定义路由转换器

***

转换器有下面几种：

| int   | 接受整数                   |
| ----- | -------------------------- |
| float | j接受浮点数                |
| path  | 和默认的相似，但也接受斜线 |

**转换器**

1. 不使用，默认字串

   ```
   #不用转换器，普通字符串类型
   # @app.route('/goods/<goods_id>')
   def goods(goods_id):
       return "goods_id:%s"%goods_id
   ```

   <class str>

2. 使用转换器

   ```
   # @app.route('/goods/<int:goods_id>')
   def goods(goods_id):
       return "goods_id:%s"%goods_id
   ```

   ![](D:\Code\FlaskNote\images\Day03_10.png)

   

### 3.路由转换器的进阶使用

**自定义转换器**

```

# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.routing import BaseConverter
app = Flask(__name__)


# 1.定义自己的转换器
class RegexConverte(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(RegexConverte, self).__init__(url_map)
        # 将正则表达式的参数保存在对象的属性中，flask会去使用这个属性来进行路由的正则匹配
        self.regex = regex

# 2. 将自定义的转换器添加到flask的应用中
app.url_map.converters["re"] = RegexConverte

@app.route("/send/<re(r'1[345678]\d{9}'):moblie>")
def send_sms(moblie):

    return "send_sms: %s" % moblie

if __name__ == '__main__':

    # 启动flask程序
    app.run(debug=True)
```

上面代码提取出路由中的电话号码