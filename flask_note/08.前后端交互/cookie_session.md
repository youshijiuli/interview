# Cookies对象

> Request对象包含Cookie对象属性，它是所有cookie变量及其对应值的字典对象

## 设置cookie

> 设置cookie,默认有效期是临时cookie,浏览器关闭就失效

```python
@app.route('/set')
def set():
    resp = make_response('Hello World')
    resp.set_cookie('Token', 'Python' , max_age=3600)
    return resp
```

在设置 cookie 时，可以指定其过期时间、域名、路径等信息。在 Flask 中，可以通过设置 max_age、expires、domain、path 等参数来实现这些功能。

```python
resp.set_cookie('user', 'Tom', max_age=3600, expires=None, domain=None, path='/')


max_age ：参数表示 cookie 的最大存活时间（单位为秒）

expires  ：参数表示 cookie 的过期时间（可以是一个 datetime 对象或时间戳）

domain  ：参数表示 cookie 可以被发送到哪些域名

path ： 参数表示 cookie 在哪些路径下可用
```

## 获取cookie

> 获取cookie，通过request.cookies的方式， 返回的是一个字典，可以获取字典里的相应的值

```python
@app.route('/get')
def get():
    resp = request.cookies.get('Token')
    return resp
```

## 删除cookie

> 删除只是让cookie过期，并不是直接删除cookie，通过delete_cookie()的方式

```python
@app.route('/delete')
def delete():
    response = make_response('Successfully')
    response.delete_cookie('Token')
    return response
```







小案例

```python
from flask import Flask, request, Response
import time


app = Flask(__name__)

@app.route('/add')
def login():
    res = Response('add cookies')
    res.set_cookie(key='name', value='wuyve', expires=time.time()+6*60)
    return res

@app.route('/show')
def show():
    return request.cookies.__str__()

@app.route('/del')
def del_cookie():
    res = Response('delete cookies')
    res.set_cookie('name', '', expires=0)
    return res

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```





# Session会话对象

> 与Cookie不同，Session（会话）数据存储在服务器上。会话是客户端登录到服务器并注销服务器的时间间隔。需要在该会话中保存的数据会存储在服务器上的临时目录中

> Session对象也是一个字典对象，包含会话变量和关联值的键值对。

## 设置SECRET_KEY

> 为每个客户端的会话分配会话ID。会话数据存储在cookie的顶部，服务器以加密方式对其进行签名。对于此加密，Flask应用程序需要一个定义的SECRET_KEY。

```python
class DefaultConfig(object):
    SECRET_KEY = '6512bd43d9caa6e02c990b0a82652dca'


app.config.from_object(DefaultConfig)
```

直接设置

```python
app.secret_key='6512bd43d9caa6e02c990b0a82652dca'
```

## 设置会话

```python
from flask import session


@app.route('/set')
def set():
    session['Token'] = 'Python'
    return 'Successfully'
```

## 获取会话

> 可以在 Flask 应用程序中的任何地方访问这个Session变量

```python
@app.route('/get')
def get():
    Token = session.get('Token')
    return 'session : {}'.format(Token)
```

## 释放会话

```python
@app.route('/pop')
def pop():
    session.pop('Token', None)
    return 'OK'
```

