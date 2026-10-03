# 会话技术

## 一、Cookie介绍

Cookie是一段不超过4KB的小型文本数据，保存在客户端浏览器中，由一个名称name、一个值value和其他几个用于控制Cookie有效期、安全性、使用范围的可选属性组成。其中：

1. `name/value`：设置Cookie的名称及对应的值，对于认证Cookie，value值包括Web服务器所提供的访问令牌。
2. `expires`：设置cookie的过期时间，有两种存储类型的cookie，会话型和持久型。expire属性缺失的时候，是会话型cookie，仅报错在客户端内存中，并在用户关闭浏览器时失效；持久型cookie会保存在用户的硬盘中，直到生命期结束或用户直接在网页中注销删除才会失效。
3. `path`：定义了Web站点上可以访问该Cooike的目录
4. `domain`：指定了可以访问该cookie的Web站点或域

## 二、Flask中操作cookie

### （1）设置cookie

```python
from flask import Flask
from flask import make_response

app = Flask(__name__)

@app.route('/set_cookie')
def set_cookie():
    
    # 需要在返回的响应中去设置cookie
    resp = make_response('set cookie success!')
    resp.set_cookie('user_id', '1')  # 不设置有效期，默认是关闭游览器后失效
    resp.set_cookie('user_name', 'xiaodai', max_age=3600)  # 设置有效期，单位秒
    
    return resp
```

**设置 Cookie 的其他属性**

除了有效期之外，你还可以设置其他属性，如 `path`、`domain`、`secure` 和 `httponly`。

```python
response.set_cookie(
    'name',
    'value',
    max_age=60*60*24*365*2,
    path='/',
    domain=None,
    secure=False,
    httponly=True
)
```

- `path`：指定 cookie 的适用路径，默认为当前路径。
- `domain`：指定 cookie 的域，默认为空（当前域）。
- `secure`：如果设置为 `True`，则只有在 HTTPS 连接下才会发送 cookie。
- `httponly`：如果设置为 `True`，则 JavaScript 无法访问此 cookie，增加安全性。

### （2）读取cookie

```python
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/get_cookie')
def get_cookie():
    # 需要在传入的请求对象中获取cookie
    user_id = request.cookies.get('user_id')
    user_name = request.cookies.get('username', '游客')
    return f"现在登录用户是：{user_id}={user_name}"
```

### （3）删除cookie

```python
from flask import Flask 
from flask import make_response

app = Flask(__name__)

@app.route('/delete_cookie')
def delete_cookie():
    
    # 在响应中去删除cookie
    resp = make_response('delete cookie success!')
    resp.delete_cookie('user_id')
    resp.set_cookie('user_name', expires=0)  # 还可以使用set_cookie设置过期时间为0来删除
    # resp.set_cookie('user_id', max_age=-3600) # 还可以使用 max_age 属性来设置 cookie 的有效期为过去的某个时间来删除
    
    return resp
```

### （4）总结cookie操作

设置 cookie 通常是在响应对象中进行的。可以通过 `response.set_cookie` 方法来设置 cookie。

读取 cookie 可以通过 `request.cookies` 属性来完成。这个属性是一个字典，包含了客户端发送过来的所有 cookie。

删除cookie 可以通过 `response.set_cookie` 方法来设置 cookie 的 `expires` 属性设置为0，还可以设置 cookie 的 `max_age` 属性设置为过去的时间。这样浏览器会认为 cookie 已经过期并自动删除它。



## 三、Session介绍

Session与cookie功能效果相同。Session与cookie的区别在于Session是记录在服务端的。而cookie是记录在客户端的。当访问服务器整个网页的时候，会在服务器端开辟一块内存，这块内存就叫做Session。而这个内存是跟浏览器关联在一起的。

**问题**：如何直到浏览器和这个服务器中的Session是一一对应的呢？如何保证不会去访问其他的Session？

**解答**：当用户访问网站时，服务器会在用户设备上设置一个唯一的Session ID 通常是通过cookie存储起来。服务器会将用户的Session数据存储在服务器端。并使用Session ID来标识和检索这些数据。

在flask中Session的签名算法是HMAC和SHA1算法

## 四、Flask中操作Session

### （1）先设置SECRET_KEY和SESSION_TYPE

```python
import uuid

class DefaultConfig(object):
    SECRET_KEY = 'your-secret-key'  # 可以用uuid.uuid4()来随机生成
    SESSION_TYPE = 'filesystem'  # 默认使用文件存储
    
app.config.from_object(DefaultConfig)
```

**常见的 Session 存储方式**

1. **文件系统存储 (`filesystem`)**： 将 session 数据存储在服务器的文件系统中。这是默认的存储方式。
2. **数据库存储 (`sqlalchemy`)**： 将 session 数据存储在数据库中，适合需要跨服务器共享 session 的场景。
3. **Redis 存储 (`redis`)**： 将 session 数据存储在 Redis 缓存服务器中，适合需要高性能存储的场景。
4. **Memcached 存储 (`memcached`)**： 将 session 数据存储在 Memcached 缓存服务器中，适合需要高性能存储的场景。

### （2）设置Session

flask自带一个session对象，这个对象是一个类字典，可以通过字典的添加元素的形式来设置Session

```python
from flask import session

@app.route('/set_session')
def set_session():
    
    session['user_name'] = 'xiaodai'  # 类似字典一样来设置键值对
    
    return 'set session success!'
```

**设置session的过期时间**

通过app对象中的`permanent_session_lifetime`来设置

```python
app.permanent_session_lifetime = datetime.timedelta(days=7)  # 设置 session 的有效期为 7 天
```

上面你设置的过期时间要在设置session的时候开启

```python
# 默认是设置 session 为永久 session
session.permanent = True  # 但如果你设置了app.permaent_session_lifetime，那么True能让其生效，变成你设置的时长。
```

### （3）读取Session

```python
@app.route('/get_session')
def get_session():
    user_name = session.get('user_name', '游客')
    return f'get session user name={user_name}'
```

### （4）删除Session

```python
@app.route('/delete_session')
def delete_session():
    session.pop('user_name')
    return f'delete session success'
```

### （5）总结session操作



使用 `pop` 方法删除特定的 session 数据。`pop` 方法的第一个参数是要删除的 key，第二个参数是默认值，如果 key 不存在，则返回默认值。





