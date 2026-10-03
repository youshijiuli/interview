# Jinja2模版

## 一、模版是什么？

1、视图函数的主要作用是生成请求的响应，这是最简单的请求，实际上视图函数有两个作用：

- 处理业务逻辑
- 返回响应内容

2、在大型的应用中，把业务逻辑和表现内容放在一起，会增加代码的复杂度和维护成本

- 模版其实是一个包含响应文本内容的html文件，其中用占位符表示动态部分，告诉模版引擎具体的值需要从使用的数据中获取；
- 使用真实值替换变量，再返回最终的到的字符串，这个过程就是“渲染”；
- Flask是使用jinja2这个模版引擎来渲染模版的。

3、使用模版的好处

- 视图函数只负责业务逻辑和数据处理（业务逻辑方面）
- 而模版则取到视图函数的数据结果进行展示（视图展示方法）
- 代码结构清晰，耦合度低

## 二、Jinja2模版

jinja2是Python的Web项目中被广泛应用的模版引擎，是由Python实现的模版语言。jinja2的作者也是Flask的作者。他的设计思想来源于Django的模版引擎，并扩展了其语法和一系列强大的功能，其是Flask内置的模版语言。

jinja2之所以被广泛使用是因为他有一下的优点：

1. 相对template而言，jinja2更加灵活，它提供了控制结构，表达式和继承等。
2. 相对于mako引擎，jinja2仅有控制结构，不允许模版中写太多业务逻辑。
3. 相对于Django模版，jinja2性能更高。
4. jinja2模版的可读性非常棒。

要渲染一个模版，在Flask中使用`render_template`方法实现。

### （1）模版语法

怎么给模版传参？

1. 在使用`render_template`渲染模版的时候，可以传递关键字参数（命名参数）。以后直接在模版中使用就可以了。
2. 如果你的参数过多，那么可以将所有的参数放在一个字典中，或者列表中。一般如果想将字典打散成关键字参数，可以在参数的前面加上`**`

```python
from flask import Flask, render_template, redirect, request


app = Flask(__name__)


STUDENT = {
    'name': 'old',
    'age': 38,
    'gender': '未知'
}

STUDENT_LIST = [
    {'name': 'old', 'age': 38, 'gender': '未知'},
    {'name': 'boy', 'age': 18 , 'gender': '男'},
    {'name': 'edu', 'age': 80, 'gender': '女'}
]


STUDENT_DICT = {
    'a': {'name': 'old', 'age': 38, 'gender': '未知'},
    'b': {'name': 'boy', 'age': 18 , 'gender': '男'},
    'c': {'name': 'edu', 'age': 80, 'gender': '女'}
}


@app.route('/student')
def detail():
    # ** 一般只用在，没有嵌套的字典中
    return render_template('student.html', **STUDENT)


@app.route('/detail_list')
def detail_list():
    
    return render_template('student_list.html', stu_list=STUDENT_LIST)
   

@app.route('/detail_dict')
def detail_dict():
    
    return render_template('student_dict.html', stu_dict=STUDENT_DICT)
    
```

在jinja2中，存在三种语法：

1. 控制结构 {% %}
2. 变量{{ }}
3. 注释{# #}

### （2）表达式

常用的是变量，有Flask渲染模版时传过来，比如name

也可以是任意一种Python的基础数据类型，比如字符串，或者数值，列表，元组，字典，布尔值等等

运算，包括算术运算，如{{ 2+3 }}、比较运算{{ 2 > 1 }}、逻辑运算{{ 1 and True }}

过滤器 |

测试器 is

函数调用，比如{{ current_time() }}

成员运算符 in ，比如{{ 1 in [1, 2, 3] }}

字符串连接符 ~ ，比如 {{ 'hello' ~ argument ~ 'world' }}

None值处理 {{ name or ""}}

### （3）控制语句

jinja2的控制语句主要是条件控制语句if，和循环控制语句for，语法类似python的 if-else和for

```python
# 条件判断语句：单分支
{% if name == 'admin' %}
	<h1>This is admin console</h1>
{% endif %}


# 条件判断语句：双分支
{% if age > 18 %}
	<p>成年人</p>
{% else %}
	<p>未成年人</p>
{% endif %}


# 条件判断语句：多分支
{% if score > 80 %}
	<p>评级A</p>
{% elif score > 60 %}
	<p>评级B</p>
{% else %}
	<p>评级C</p>
{% endif %}
```

比如：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ stu_list }}
    <table border="1px">
        <tr>
            <td>name</td>
            <td>age</td>
            <td>gender</td>
        </tr>
        {% for stu in stu_list %}
            {% if stu.name != "Old" %}
                {% if stu.age != 73 %}
                    <tr>
                        <td>{{ stu.name }}</td>
                        <td>{{ stu.get("age") }}</td>
                        <td>{{ stu["gender"] }}</td>
                    </tr>
                {% endif %}
            {% endif %}
        {% endfor %}
    </table>
</body>
</html>
```

或者：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{ stu_dict }}
    <table border="1px">
        <tr>
            <td>id</td>
            <td>name</td>
            <td>age</td>
        <td>gender</td>
        </tr>
        {% for stu_key,stu_value in stu_dict.items() %}
            <tr>
                <td>{{ stu_key }}</td>
                <td>{{ stu_value.get("name") }}</td>
                <td>{{ stu_value.age }}</td>
                <td>{{ stu_value.gender }}</td>
            </tr>
        {% endfor %}
    </table>
</body>
</html>
```

for循环语句中的loop对象：

| 属性/方法             | 描述                                            |
| --------------------- | ----------------------------------------------- |
| `loop.index`          | 当前迭代的索引（从 1 开始）。                   |
| `loop.index0`         | 当前迭代的索引（从 0 开始）。                   |
| `loop.revindex`       | 逆向索引（从 1 开始），即 `len(loop)-index+1`。 |
| `loop.revindex0`      | 逆向索引（从 0 开始），即 `len(loop)-index`。   |
| `loop.first`          | 如果是第一次迭代则为 `True`。                   |
| `loop.last`           | 如果是最后一次迭代则为 `True`。                 |
| `loop.length`         | 迭代对象的长度。                                |
| `loop.cycle(*values)` | 在提供的值之间循环，每次迭代返回下一个值。      |
| `loop.iterable`       | 正在迭代的对象。                                |
| `loop.depth`          | 当前循环的深度（嵌套循环时有用）。              |

### （4）过滤器

什么是过滤器？实际上就是一个转换函数。变量可以通过“过滤器”进行修改，过滤器可以理解成jinja2里面的内置函数和字符串处理函数。

常用的过滤器有：

| 过滤器名称   | 描述                                 |
| ------------ | ------------------------------------ |
| `safe`       | 标记文本为安全的，不需要转义。       |
| `upper`      | 将文本全部转换为大写。               |
| `lower`      | 将文本全部转换为小写。               |
| `capitalize` | 将文本首字母大写。                   |
| `title`      | 将每个单词的首字母大写。             |
| `trim`       | 删除字符串尾部的空白字符。           |
| `striptags`  | 删除所有 HTML/XML 标签。             |
| `reverse`    | 将字符串反转。                       |
| `length`     | 获取变量的长度。                     |
| `slice`      | 截取列表的一部分。                   |
| `sort`       | 排序列表。                           |
| `groupby`    | 根据给定的键对序列中的元素进行分组。 |
| `map`        | 应用一个函数到序列上的每一个元素上。 |
| `default`    | 如果变量未定义，则返回默认值。       |
| `random`     | 从序列中随机选择一个元素。           |
| `join`       | 使用指定的字符串连接列表中的元素。   |

前端模版中的用法：

1、字符串过滤器

```html
<body>
    {# 当变量未定义的时候，显示默认字符串，可以缩写为d #}
    <p>{{ name | default("No name") }}</p>

	{# 单词首字母大写 #}
    <p>{{ 'hello world' | capitalize }}</p>
    
    {# 单词全小写 #}
    <p>{{ 'XML' | lower }}</p>
    
    {# 去除字符串前后的空格 #}
    <p>{{ '  hello  ' | trim }}</p>
    
    {# 字符串翻转 #}
    <p>{{ 'hello' | reverse }}</p>

    {# 格式化输出 #}
    <p>{{ '%s id %d' | format('Number', 99) }}</p>
    
    {# 关闭HTML自动转义 #}
    <p>{{ '<em>name</em>' | safe }}</p>
</body>
```

2、数值过滤器

```html
<body>
	{# 四舍五入取值 #}
    <p>{{ 3.1415 | round }}</p>
    
	{# 保留N位小数 #}
    <p>{{ 3.1415 | round(3) }}</p>   
    
	{# 取绝对值 #}
    <p>{{ -12 | abs }}</p>
</body>
```

3、列表相关的过滤器

```html
<body>
    {# 在模版中定义一个变量 #}
    {% set lst = [1, 2, 3, 4, 5] %}
    
	{# 取出第一个元素 #}
    <p>{{ lst | first }}</p>
    
	{# 返回列表长度，可以写作count #}
    <p>{{ lst | length }}</p>

	{# 列表求和 #}
    <p>{{ lst | sum }}</p>
    
    {# 列表排序 #}
    <p>{{ lst | sort }}</p>
    
    {# 合并为字符串 #}
    <p>{{ lst | join(,) }}</p>
    
</body>
```

4、字典相关的过滤器

```html
<body>
    {# 在模版中定义一个变量 #}
    {% 
    	set users = [
            {'name':'Tom','gender':'M','age':20},
            {'name':'John','gender':'M','age':18}, 
            {'name':'Mary','gender':'F','age':24},
            {'name':'Bob','gender':'M','age':31},
            {'name':'Lisa','gender':'F','age':19}
    	]
    %}
    
    
    {# 指定字段排序，这里设reverse为true让其降序排 #}
    <ul>
    	{% if for user in users | sort(attribute='age', reverse=true) %}
        	<li>{{ user.name }}, {{ user['age'] }}</li>
    	{% endif %}
    </ul>
    
    
    {# 列表分组，每组是一个子列表，组名就是分组项的值 #}
    <ul>
    	{% for group in users | groupby('gender') %}
        	<li>{{ group.grouper }}</li>
        	{% for user in group.list %}
        		<li>{{ user.name }}</li>
        	{% endfor %}
    	{% endfor %}
    </ul>
    
    {# 取字典中的某一项组成列表，再将其连接起来 #}
    <p>{{ users | map(attribute='name') | join(',') }}</p>
    
</body>
```

5、自定义过滤器

第一种方式：使用`app.jinja_env.filters`添加属性的方式来注册

```python
def get_even_list(lst):
    """定义一个获取偶数的函数，过滤器实际上就是一个函数"""
    return lst[::2]

# 函数的第一个参数就是过滤器函数，第二个参数是过滤器的名称
app.jinja_env.filters['even_filter'] = get_even_list
```

第二种方式：在函数上方加上`template_filter`装饰器的方式来注册

```python
@app.template_filter()  # 加了装饰器，普通函数就变成了过滤器函数
def is_even(num):
    if num % 2 == 0:
        return 'even number'
    else:
        return 'odd number'
```

在模版中：

```html
<p>{{ [1, 2, 3, 4, 5] | even_filter }}</p>

<p>{{ 2 | is_even }}</p>
```

### （5）测试器

测试器总是返回一个布尔值，它可以用来测试一个变量或者表达式，使用`is`关键字来进行测试。

```html
{% set name = 'ab' %}

{% if name is lower %}
	<h2>"{{ name }}" are all lower case.</h2>
{% endif %}
```

jinja2中内置的测试器

```html
{# 检查变量是否被定义，也可以用undefined检查是否未被定义 #}
{% if name is defined %}
	<p>Name is: {{ name }}</p>
{% endif %}


{# 检查是否所有字符都是大写 #}
{% if name is upper %}
	<h2>"{{ name }}" are all upper case.</h2>
{% endif %}


{# 检查变量是否为空 #}
{% if name is none %}
	<h2>Variable is none.</h2>
{% endif %}


{# 检查变量是否为字符串，也可以用number检查是否为数值 #}
{% if name is string %}
	<h2>{{ name }} is a string.</h2>
{% endif %}


{# 检查数值是否是偶数，也可以用odd检查是否为奇数 #}
{% if 2 is even %}
	<h2>Variable is an even number.</h2>
{% endif %}


{# 检查变量是否可被迭代循环，也可以用sequence检查是否是序列 #}
{% if [1,2,3] is iterable %}
	<h2>Variable is iterable.</h2>
{% endif %}


{# 检查变量是否是字典 #}
{% if {'name':'test'} is mapping %}
	<h2>Variable is dict.</h2>
{% endif %}
```

自定义测试器：

第一种方法：通过`app.jinja_env.tests`的来注册

```python
import re


def test_tel(tel_num):
    pattren = r'\d{11}'
    return re.match(pattren, tel_num)

app.jinja_env.tests['is_tel'] = test_tel
```

第二种方式：通过`template_test`装饰器来注册

```python
@app.template_test('start_with')  # 里面传入的参数是指定测试器的名字
def start_with(string, suffix):
    return string.lower().startswith(suffix.lower())
```

在模版中使用：

```html
{% set tel = '13011112222' %}

{% if tel is is_tel %}
	<p>{{ tel }} is mobile phone</p>
{% endif %}

{% set name = 'Hello world' %}
{% if name is start_with 'hello' %}
	<p>'{{name}}' start with 'hello'</p>
{% endif %}
```



