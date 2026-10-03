# 模版中使用url_for

​		模版中的url_for跟我们后台视图函数中的url_for使用起来基本上是一样的，也是传递视图函数的名字。也可以传递参数。使用的时候，需要在url_for左右两边加上`{{ url_for('func') }}`

## 一、动态URL

​		`url_for()` 函数的主要用途是从视图函数的名字生成 URL，这对于构建动态 URL 非常有用，因为它可以避免硬编码 URL 地址，并且在 URL 结构发生变化时能够自动更新链接。

### （1）不带参数

```html
<a href="{{ url_for('index') }}">Home</a>
```

### （2）带参数

**动态路由**

Hmtl页面中使用：

```python
<a href="{% url_for('login', p1='abc', p2='ddd', name='momo') %}"></a>
```

本质上就是动态路由，点击就会变成http://127.0.0.1:5000/accounts/login/momo/?p1=abc&p2=ddd

对应的视图函数为：

```python
@app.route('accounts/login/<name>')
def login(name):
    print(name)
    return render_template('login.html')
```

**查询字符串参数**

```html
<a href="{% url_for('login', p1='abc', p2='ddd') %}"></a>
```

## 二、加载静态文件

静态文件：css、js、图片、字体等等

记在静态文件使用的是`url_for`函数，然后第一个参数需要为`static`，第二个参数需要为一个关键字参数`filename=路径`

语法：

```html
<link herf="{{ url_for('static', filename='css/main.css') }}" rel="stylesheet"/>

<script src="{{ url_for('static', filename='js/main.js') }}"></script>

<img src="{{ url_for('static', filename='img/img.jpg') }}"/>
```

注意事项：

1. **端点名称**：确保你使用的端点名称（通常是视图函数的名称）是正确的，否则可能会导致找不到路由。
2. **URL 规则**：确保你的 URL 规则与视图函数的定义相匹配。
3. **静态文件夹**：默认情况下，Flask 会寻找名为 `static` 的文件夹来存放静态文件。如果你更改了这个设置，请确保在 `url_for()` 中使用正确的端点名称。