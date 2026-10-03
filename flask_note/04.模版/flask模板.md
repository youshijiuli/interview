

# flask使用操作指南之模板

>Auth: 王海飞
>
>Data：2018-05-15
>
>Email：779598160@qq.com
>
>github：https://github.com/coco369/knowledge 

### 1. jinja2

Flask中使用jinja2模板引擎

jinja2是由Flask作者开发，模仿Django的模板引擎

优点：
	
	速度快，被广泛使用
	
	HTML设计和后端python分离
	
	非常灵活，快速和安全
	
	提供了控制，继承等高级功能







### 2. 模板语法


#### 2.1 模板语法主要分为两种：变量和标签

模板中的变量：`{{ var }}`

	视图传递给模板的数据
	
	前面定义出来的数据
	
	变量不存在，默认忽略

模板中的标签：`{% tag %}`
	控制逻辑
	
	使用外部表达式
	
	创建变量
	
	宏定义





`example01`

```python
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index20.html',info='Flask模板传参')

@app.route('/index')
def index2():
    return render_template('index20.html',arg='Python中的Flask',info='Flask模板传参')

@app.route('/home')
def home():
    context = {
        'uname':'吕布',
        'age':18,
        'height':180,
        'wu_qi':{'jin':'方天画戟','yuan':'弓箭'}
    }

    return render_template('index20.html',**context)

if __name__ =='__main__':
    app.run(debug=True)
```







模版中使用 `url_for`

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>url_for函数的使用</title>
</head>
<body>
    <h1>url_for 函数</h1>
    <hr>
    {{ url_for('index') }}
    <br>
    {{ url_for('home') }}
    <br>
    {{ url_for('home1',id=1101) }}
    <br>
    {{ url_for('home',id=1101) }}
    <br>
    {{ url_for('home1',id=1101,addr='bj') }}
    <br>
    <a href="/home/">访问home的内容</a>
    <br>
    <a href="{{ url_for('home')}}">访问home的内容</a>

</body>
</html>
```

```python
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home2/')
def home():
    return 'Home!!'

@app.route('/home1/<int:id>')
def home1(id):
    return 'Home!!'

if __name__ =='__main__':
    app.run(debug=True)
```



#### 2.2 结构标签：

block
	
	{% block xxx %}
	
	{% endblock %}
	
	块操作
		父模板挖坑，子模板填坑

extends
	
	{% extends ‘xxx.html’ %}
	
	继承以后保留块中的内容
	{{ super() }}

挖坑继承体现的化整为零的操作


macro
	
	{% macro hello(name) %}
	
		{{ name }}
	
	{% endmacro %}
	
	宏定义，可以在模板中定义函数，在其他地方调用

宏定义可导入

	{% from 'xxx' import xxx %}

例子1：

在index.html中定义macro标签，定义一个方法，然后去调用方法，结果是展示商品的id和商品名称


	{% macro show_goods(id, name) %}
	    商品id：{{ id }}
	    商品名称：{{ name }}
	{% endmacro %}
	
	{{ show_goods('1', '娃哈哈') }}
	<br>
	{{ show_goods('2', '雪碧') }}

例子2：

在index.html页面中定义一个say()方法，然后解析该方法：

	{% macro say() %}
	
	    <h3>今天天气气温回升</h3>
	    <h3>适合去游泳</h3>
	    <h3>适合去郊游</h3>
	
	{% endmacro %}
	
	{{ say() }}


例子3：

定义一个function.html中定义一个方法：

	{% macro create_user(name) %}
	    创建了一个用户:{{ name }}
	{% endmacro %}

在index.html中引入function.html中定义的方法


	{% from 'functions.html' import create_user %}
	
	{{ create_user('小花') }}



#### 2.3 循环

	{% for item in cols %}
	
		aa
	
	{% else %}
	
		bb
	
	{% endfor %}

也可以获取循环信息loop

	loop.first
	
	loop.last
	
	loop.index
	
	loop.revindex

例子:

在视图中定义一个视图函数：

	@stu.route('/scores/')
	def scores():
	
	    scores_list = [21,34,32,67,89,43,22,13]
	
	    content_h2 = '<h2>今天你们真帅</h2>'
	    content_h3 = '   <h3>今天你们真帅</h3>   '
	
	    return render_template('scores.html',
	                           scores=scores_list,
	                           content_h2=content_h2,
	                           content_h3=content_h3)

(该视图函数，在下面讲解的过滤器中任然使用其返回的content_h2等参数)

首先: 在页面中进行解析scores的列表。题目要求：第一个成绩展示为红色，最后一个成绩展示为绿色，其他的不变

   	<ul>
	   {% for score in scores %}
	        {% if loop.first %}
	            <li style="color:red;">{{ loop.revindex }}:{{ loop.index }}:{{ score }}</li>
	        {% elif loop.last %}
	            <li style="color:green;">{{ loop.revindex }}:{{ loop.index }}:{{ score }}</li>
	        {% else %}
	            <li> {{ loop.revindex }}:{{ loop.index }}:{{ score }}</li>
	        {% endif %}
	    {% endfor %}
	</ul>




#### 2.4 过滤器

语法：
	
	{{ 变量|过滤器|过滤器... }}


capitalize 单词首字母大写

lower 单词变为小写

upper 单词变为大写

title

trim 去掉字符串的前后的空格

reverse 单词反转

format

striptags 渲染之前，将值中标签去掉

safe 讲样式渲染到页面中

default

last 最后一个字母

first

length

sum

sort

例子：

	<ul>
	    <li>{{ content_h2 }}</li>
	    <li>{{ content_h2|safe }}</li>
	    <li>{{ content_h2|striptags }}</li>
	
	    <li>{{ content_h3 }}</li>
	    <li>{{ content_h3|length }}</li>
	    <li>{{ content_h3|trim|safe }}</li>
	    <li>{{ content_h3|trim|length }}</li>
	</ul>



```
<body>
    <h1>过滤器的使用</h1>
    过滤前的数据是：{{ param }}
    <br>
    过滤后的数据是：{{ param | int }}
</body>
```





- default过滤器

```
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index23.html',nick_name=None)


if __name__ =='__main__':
    app.run(debug=True)
```



```
<body>
    <h1>default过滤器</h1>
    过滤前的昵称数据是：{{nick_name}}<br>
    过滤后的昵称数据是：{{nick_name | default('用户1',boolean=true)}}<br>
    过滤后的昵称数据是：{{nick_name or '用户2'}}<br>
</body>
```





- 转义字符过滤器

```
def index():
    info = '<script>alert("Hello!!")</script>'
    return render_template('index24.html',info=info)
```



```
<body>
    <h1>转义字符过滤器</h1>
    <!-- 模板中默认 做了转义字符的效果 -->
    转义前的数据是：{{ info | safe }}  <!-- 不转义：不将特殊字符转换成 &lt;类似的数据 -->

    {% autoescape true %} <!-- false代表不再转义特殊字符 / true 转义特殊字符  &lt;-->
    {{info }}  <!-- 转义：将特殊字符转换成 &lt;类似的数据 -->
    {% endautoescape %}

</body>
```





- 其它过滤器的使用

```
<body>
    <h1>其它过滤器</h1>
    绝对值：{{ -6 | abs }}<br>
    小数: {{ 6 | float }}<br>
    字符串：{{ 6 | string }}<br>

    格式化:{{'%s--%s' | format('我','你')}}<br> 
    长度：{{'我是九，你是三，除了你，还是你' |length}}<br>
    最后一个：{{'我是九，你是三，除了你，还是你' |last}}<br>
    第一个：{{'我是九，你是三，除了你，还是你' |first}}<br>
    统计次数： {{'我是九，你是三，除了你，还是你' | wordcount }}<br>
    替换：{{'===我是九，你是三，除了你，还是你====' |replace('我是九，你是三，除了你，还是你','拿着,这个无限额度的黑卡，随便刷')}}
</body>
```







- 自定义过滤器的使用

```
from flask import Flask,render_template

app = Flask(__name__)


@app.template_filter('cut')
def cut(value):
    value = value.replace('我是九，你是三，除了你，还是我','你不用好，我喜欢就好')
    return value

@app.route('/')
def index():
    info = '============= 我是九，你是三，除了你，还是我=============='
    return render_template('index26.html',info = info)

if __name__ =='__main__':
    app.run(debug=True)
```

```
<body>
    <h1>自定义过滤器</h1>
    过滤前的数据是：{{info}}<br>
    过滤后的数据是：{{info|cut}}
</body>
```



- 自定义时间过滤器

```
from flask import Flask,render_template
from datetime import datetime

app = Flask(__name__)


# 年 月 日  时 分 秒
# 数据库中存放的数据是 2030/01/01 00:00:00
# 现在时间是          2030/01/01 01:30:00


@app.template_filter('handler_time')
def handler_time(time):
    '''
        time距离现在的时间间隔
       1. 如果时间间隔小于1分钟以内，那么就显示“刚刚”
       2. 如果是大于1分钟小于1小时，那么就显示“xx分钟前”
       3. 如果是大于1小时小于24小时，那么就显示“xx小时前”
       4. 如果是大于24小时小于30天以内，那么就显示“xx天前”
       5. 否则就是显示具体的时间 2030/10/20 16:15
    '''
    # 获取当前时间
    now = datetime.now()
    # 将相差的时间转为秒
    temp_stamp = (now-time).total_seconds()
    if temp_stamp <60:
        return '1分钟之前'
    elif temp_stamp >=60 and temp_stamp <60*60:
        return '1小时之前'
    elif temp_stamp >= 60*60 and temp_stamp < 60*60*24:
        hours = int(temp_stamp/(60*60))
        return f'{hours}小时之前'
    elif temp_stamp >= 60*60*24 and temp_stamp< 60*60*24*30:
        day = int(temp_stamp/(60*60*24))
        return f'{day}天之前'
    else:
        return '很久以前'


@app.route('/')
def index():
    tmp_time = datetime(2021, 10, 20,10,10,10)
    return render_template('index27.html',tmp_time = tmp_time)

if __name__ =='__main__':
    app.run(debug=True)
```

```
<body>
    <h1>自定义时间过滤器</h1>
    数据过滤后的：{{tmp_time|handler_time}}
</body>
```





#### 宏的使用

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏的使用</title>
</head>

{% macro inp(type,name="",value="") %}
    <input type="{{type}}" name="{{name}}" value="{{value}}">
{% endmacro %}
<body>
    <h1>宏的使用</h1>

    <table>
        <tr>
            <td>用户名：</td><td><input type="text" name="" value=""></td>
        </tr>
        <tr>
            <td>密码：</td><td><input type="password" name="" value=""></td>
        </tr>
        <tr>
            <td><input type="submit" value="登录"></td>
        </tr>
    </table>

    <hr>

    <table>
        <tr>
            <td>用户名：</td><td>{{inp('text','uname')}}</td>
        </tr>
        <tr>
            <td>密码：</td><td>{{inp('password','pwd')}}</td>
        </tr>
        <tr>
            <td>{{inp('submit',value='登录')}}</td>
        </tr>
    </table>

</body>
</html>
```





- 宏的引入

目录结构如下：

```
templates
	|--macros
	|----|--common.html
	|--indexx.html
```



```
{% macro inp(type='text',name='',value='')%}
    <input type="{{type}}" name="{{name}}" value="{{nick}}">
{% endmacro %}
```

```
index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏的引入</title>
</head>

{% import 'macros/common.html' as mc with context %}
<!-- {% from 'macros/common.html' import inp with context %} -->
{% from 'macros/common.html' import inp%}
<body>
    <h1>宏的引入</h1>
    <table>
        <tr>
            <td>用户名：</td><td><input type="text" name="" value="{{nick}}"></td>
        </tr>
        <tr>
            <td>密码：</td><td><input type="password" name="" value=""></td>
        </tr>
        <tr>
            <td><input type="submit" value="登录"></td>
        </tr>
    </table>

    <hr>
    <table>
        <tr>
            <td>用户名：</td><td>{{ mc.inp(name='uname')}}</td>
        </tr>
        <tr>
            <td>密码：</td><td>{{mc.inp('password','pwd')}}</td>
        </tr>
        <tr>
            <td>{{ mc.inp('submit',value='登录')}}</td>
        </tr>
    </table>


    <hr>
    <table>
        <tr>
            <td>用户名：</td><td>{{ inp(name='uname')}}</td>
        </tr>
        <tr>
            <td>密码：</td><td>{{inp('password','pwd')}}</td>
        </tr>
        <tr>
            <td>{{ inp('submit',value='登录')}}</td>
        </tr>
    </table>
</body>
</html>
```





#### include的使用

```
<body>
    <h1>include的使用</h1>
    <hr>

        {% include 'common/header.html' %}
        <main>主要内容</main>
        {% include 'common/footer.html' %}
</body>
</html>
```



```
<nav>头部信息 </nav>
```

```
<footer>底部信息</footer>
{{uname}}
```







### 3. 定义模板

#### 3.1 定义基础模板base.html

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>
	        {% block title %}
	        {% endblock %}
	    </title>
	    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
	
	    {% block extCSS %}
	    {% endblock %}
	</head>
	<body>
	
	{% block header %}
	{% endblock %}
	
	{% block content%}
	{% endblock %}
	
	{% block footer%}
	{% endblock %}
	
	{% block extJS %}
	{% endblock %}
	
	</body>
	</html>


#### 3.2 定义基础模板base_main.html


	{% extends 'base.html' %}
	
	{% block extCSS %}
	    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
	{% endblock %}



#### 3.3 模版继承

```
{% extends 'base.html' %}

{% block footer %}
    这个是底部内容 Python!!!!
{% endblock %}

{% block content %}
    {{ super() }}
    <p>这个是子模板的内容</p>
    {{ self.footer() }}
{% endblock%}

{% block info%}

这个内容出不来的！！
{% endblock %}
```



### 4. 静态文件信息配置

<b>django</b>：

第一种方式：

	{% load static %}
	<link rel="stylesheet" href="{% static 'css/index.css' %}">

第二种方式：

	<link rel="stylesheet" href="/static/css/index.css">


<b>flask</b>：

第一种方式：

	<link rel="stylesheet" href="/static/css/index.css">

第二种方式：

	<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">



- 静态文件的引入

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>静态文件引入</title>
    <script src="{{url_for('static',filename='js/test.js')}}"></script>
    <link href="{{url_for('static',filename='css/test.css')}}"  rel="stylesheet"></link>
</head>
<body>
    <h1>静态文件引入</h1>
    <img src="/static/imgs/img1.jpg" alt="">
    <img src="{{url_for('static',filename='imgs/img1.jpg')}}" alt="" srcset="">
</body>
</html>
```

