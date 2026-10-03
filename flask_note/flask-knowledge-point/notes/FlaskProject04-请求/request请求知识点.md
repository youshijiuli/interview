# request参数

## 一、请求方式

在Flask中，可以定义路由默认的请求方式：

利用`methods`参数可以自己指定一个接口的请求方式

`get`方式：把请求参数放到url的`?`问号后面，每个请求参数格式为：参数名=参数值。

参数之间采用`&`符号隔开。采用的字符数据传输，所以也叫明文的请求。

`post`方式：表单提交，并采用字节流的方式传递数据。

```python
@app.route("/func1", methods=['POST'])
def view_func1():
    
    return 'hello'

@app.route("/fun2", methods=['GET', 'POST'])
def view_func2():
    
    return 'hello'
```



## 二、请求参数

如果想要其他地方传递的参数，可以通过Flask提供的全局对象request来读取。

不同位置的参数都存放在request的不同属性中：

| 属性    | 说明                           | 类型           |
| ------- | ------------------------------ | -------------- |
| data    | 记录请求的数据，并转换为字符串 | *              |
| form    | 记录请求中的表单数据           | MultiDict      |
| args    | 记录请求中的查询参数           | MultiDict      |
| cookies | 记录请求中的cookie信息         | Dict           |
| headers | 记录请求中的报文头             | EnvironHeaders |
| method  | 记录请求的URL地址              | GET/POST       |
| url     | 记录请求的URL地址              | string         |
| files   | 记录请求上传的文件             | *              |

例如：想要获取`/find?user_id=1`中的`user_id`的参数，可以按如下方式使用：

```python
from flask import Flask, request

@app.route('/find')
def get_articles():
    
    channel_id = request.args.get('user_id')
    return '你传入的用户ID是：{}'.format(channel_id)
```

例如：上传文件

客户端上文件到服务器，并保存到服务器中

```python
from flask import request

@app.route('/upload', method=["POST"])  # 必须是大写，上传文件必须是POST
def upload_file():
    f = request.files['pic']
    # 有两种方式保存
    # 第一种：
    with open('./static/demo.png', 'wb') as new_file:
        new_file.write(f.read())
    # 第二种：
    f.save('./static/demo.png')
    return '保存成功！'
```

