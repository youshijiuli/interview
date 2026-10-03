# 路由和URL

## 一、路由

flask中的路由是用装饰器来和视图函数映射在一起的

```python
@app.route("/index")
def view_func():
    """ 视图函数 """
    return 'hello'
```

在程序中获取路由信息的方法：

在应用中的url_map属性中保存着整个Flask应用的路由映射信息，可以通过读取这个属性获取路由信息

```python
print(app.url_map)
```

如果想在程序中遍历路由信息，可以采用如下方式：

```python
for rule in app.url_map.iter_rules():
	print('name={} path={}'.format(rule.endpoint, rule.rule))
```

需求

​	通过访问 / 地址，以json的方式返回应用内的所有路由信息

实现

```python
@app.route("/")
def route_list():
	""" 主视图，返回所有视图网址 """
	rules_iterator = app.url_map.iter_rules()
	return json.dumps(
		{rule.endpoint: rule.rule for rule in rules_iterator}
	)
```

## 二、动态路由（URL路径参数）

如果，有一个请求访问的接口地址为 `/users/123` ,其中123实际以上为具体的请求参数，表明请求123号用户的信息。此时如何从url中提取出123的数据？

Flask不同于Django直接在定义路由时编写正则表达式的方式，而是采用转换器语法：

```python
@app.route('/users/<user_id>')
def user_info(user_id):
	print(type(user_id))
	return f"hello user {user_id}"
```

此处的`<>`即是一个转换器，默认为字符串类型，即将位置数据以字符串的格式进行匹配、并以字符串为数据类型、`user_id`为参数名传入视图。

### ① Flask提供的转换器

```python
DEFAULT_CONVERTERS = {
    'default': UnicodeConverter,
    'string': UnicodeConverter,
    'any': AnyConverter,
    'path': PathConverter,
    'uuid': UUIDConverter,
}
```

将上面的例子以整型匹配数据，可以如下使用：

```python
@app.route('/users/<int:user_id>')
def user_info(user_id):
    print(type(user_id))
    return 'hello user {}'.format(user_id)

@app.route('/users/<int(min=1):user_id>')
def user_info(user_id):
    print(type(user_id))
    return "hello user {}".format(user_id)
```

### ② 自定义转换器

如果遇到需要匹配提取`/sms_codes/13011112222`中的手机号数据，Flask内置的转换器就无法满足需求，此时需要自定义转换器。

自定义转换器的主要三个步骤：

1. 创建转换器类，保存匹配时的正则表达式

```python
from werkzeug.routing import BaseConverter

class MobileConverter(BaseConverter):
    """ 手机号格式 """
    regex = r'1[3-9]\d{9}'
```

2. 将自定义的转换器告知Flask应用

```python
app = Flask(__name__)

# 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为：mobile
app.url_map.converters['mobile'] = MobileConverter
```

3. 在使用转换器的地方定义使用

```python
@app.route('/sms_codes/<mobile:mob_num>')
def send_sms_code(mob_num):
    return 'send sms code to {}'.format(mob_num)
```