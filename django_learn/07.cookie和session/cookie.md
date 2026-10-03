# Cookie和Session



**Cookie规范 **

-  Cookie大小上限为4KB； 
-  一个服务器最多在客户端浏览器上保存20个Cookie； 
-  一个浏览器最多保存300个Cookie，因为一个浏览器可以访问多个服务器。



上面的数据只是HTTP的Cookie规范，但在浏览器大战的今天，一些浏览器为了打败对手，为了展现自己的能力起见，可能对Cookie规范“扩展”了一些，例如每个Cookie的大小为8KB，最多可保存500个Cookie等！但也不会出现把你硬盘占满的可能！ 

注意，不同浏览器之间是不共享Cookie的。也就是说在你使用IE访问服务器时，服务器会把Cookie发给IE，然后由IE保存起来，当你在使用FireFox访问服务器时，不可能把IE保存的Cookie发送给服务器。





**Cookie与HTTP头  **

Cookie是通过HTTP请求和响应头在客户端和服务器端传递的： 

- Cookie：请求头，客户端发送给服务器端； 
- 格式：Cookie: a=A; b=B; c=C。即多个Cookie用分号离开；  Set-Cookie：响应头，服务器端发送给客户端； 
- 一个Cookie对象一个Set-Cookie： Set-Cookie: a=A Set-Cookie: b=B Set-Cookie: c=C  

**Cookie的覆盖 **

如果服务器端发送重复的Cookie那么会覆盖原有的Cookie，例如客户端的第一个请求服务器端发送的Cookie是：Set-Cookie: a=A；第二请求服务器端发送的是：Set-Cookie: a=AA，那么客户端只留下一个Cookie，即：a=AA。 



## 1. Cookie的使用

在 Django 中，对于请求上的 Cookie，通常会进行以下常见操作：

1. **获取 Cookie 值**：从请求对象中获取 Cookie 的值，可以通过 `request.COOKIES` 字典来获取，其中键是 Cookie 名称，值是 Cookie 值。

   ```python
   cookie_value = request.COOKIES.get('cookie_name', default_value)
   ```

2. **设置 Cookie 值**：在响应中设置 Cookie，使其在客户端保存。可以使用响应对象的 `set_cookie` 方法来设置 Cookie。

   ```python
   response = HttpResponse()
   response.set_cookie('cookie_name', 'cookie_value', max_age=3600, path='/', domain='example.com', secure=True, httponly=True)
   ```

3. **删除 Cookie**：从响应中删除 Cookie，使其在客户端被移除。可以使用响应对象的 `delete_cookie` 方法来删除 Cookie。

   ```python
   response.delete_cookie('cookie_name')
   ```

4. **获取带签名的 Cookie 值**：获取带签名的 Cookie 值，可以使用请求对象的 `get_signed_cookie` 方法。

   ```python
   cookie_value = request.get_signed_cookie('cookie_name', default=None, salt='some_salt')
   ```

5. **设置带签名的 Cookie 值**：在响应中设置带签名的 Cookie。可以使用响应对象的 `set_signed_cookie` 方法来设置带签名的 Cookie。

   ```python
   response.set_signed_cookie('cookie_name', 'cookie_value', salt='some_salt')
   ```

6. **清除所有 Cookie**：从响应中清除所有 Cookie。可以使用响应对象的 `delete_cookie` 方法并指定 Cookie 的名称为 None 来清除所有 Cookie。

   ```python
   response.delete_cookie('cookie_name', path='/', domain='example.com')
   ```

通过以上操作，你可以在 Django 中对请求上的 Cookie 进行常见的操作，包括获取、设置、删除以及对带签名的 Cookie 进行安全的处理。





#### 1.1 cookie的基本使用

**案例一：登录[无cookie]**

```html
<body>
    <h1>登录页面</h1>
    <form action="" method="post">
        {% csrf_token %}
        用户名：<input type="text" name="username">
        密 码：<input type="password" name="password">
        <input type="submit" value="提交">
        <span>{{error}}</span>
    </form>
</body>
```

视图函数：

```python
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    # post请求获取数据，校验
    print(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'lisa' and password == '123':
        return render(request, 'index.html', {'username': username})

    error_msg = '用户名或者密码错误'

    return render(request, 'login.html', {'error': error_msg})
```

登录成功，跳转到首页；没有问题；



下面就是问题来了，如果直接访问首页我们发现也能行得通，那为什么还需要登录呢？所以就需要保存用户信息用于鉴权；不能谁来了都能看到首页；



**案例二：结合cookie的用户登录**

Cookie:本质上就是保存到浏览器的键值对

用户到浏览器接受存储到cookie里面，当下次再次发起请求的时候，就会把这个以前存储到浏览器中的cookie再次携带过去，发送到django后台，我们是不是可以在请求中读取cookie

```python
from django.shortcuts import render, HttpResponse,redirect


def index(request):

    # 判断是否登录成功
    res = request.COOKIES.get('is_login')

    if res:
        username = request.COOKIES.get('user')
        return render(request, 'index.html', {'username': username})
    

    return redirect('/login/')


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    # post请求获取数据，校验
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'lisa' and password == '123':

        res = HttpResponse('登录成功')
        res.set_cookie('is_login', True)
        res.set_cookie('user', username)

        return res

    error_msg = '用户名或者密码错误'

    return render(request, 'login.html', {'error': error_msg})

```



**案例三：加盐和设置有效期**

`set_signed_cookie` 是 Django 中用于设置带签名的 cookie 的方法。与普通的 cookie 不同，带签名的 cookie 包含了一个签名，用于验证其内容在传输过程中是否被篡改。【每次请求都会携带cookie，我可以在获取cookie，修改之后再去发起请求】

普通的 cookie 可能会存在安全风险，因为其内容可以被用户篡改。为了确保 cookie 的完整性和安全性，Django 提供了带签名的 cookie。带签名的 cookie 会在内容末尾追加一个签名值，该签名值是通过对 cookie 内容进行哈希计算而生成的，使用了一个密钥作为盐值。当服务器接收到带签名的 cookie 时，会验证签名是否有效，以确定内容是否被篡改。



- 加盐：

防止Cookie被伪造，例如A用户的Cookie存储了一对值，就是别的爬虫可以伪装这样的Cookie，假装是A用户进行登录，篡改窃取A用户的个人信息等一些违法操作，所以需要加盐，那么Cookie就伪造不了，因为盐和用户是绑定的。



使用 `set_signed_cookie` 方法可以方便地设置带签名的 cookie。它的基本用法如下：

```python
response.set_signed_cookie(key, value, salt='some_salt')
```

源码：

```python
def set_signed_cookie(self, key, value, salt='', **kwargs):
  	value = signing.get_cookie_signer(salt=key + salt).sign(value)
    return self.set_cookie(key, value, **kwargs)
```

其中：

- `key` 是要设置的 cookie 的键名；
- `value` 是要设置的 cookie 的值；
- `salt` 是用于生成签名的盐值，默认为 `django.utils.crypto.get_default_md5_salt()`，你也可以自定义盐值。

这个方法会将带签名的 cookie 设置到响应对象中，发送给客户端。然后客户端在下次请求时会将这个带签名的 cookie 发送给服务器，服务器会验证签名，以确保其完整性和安全性。

带签名的 cookie 是通过 Django 的请求对象 `request` 中的 `get_signed_cookie` 方法来获取的，而不是直接从 `request.COOKIES` 中获取。这是因为带签名的 cookie 包含了签名信息，需要使用密钥和盐值来验证签名。

你可以使用以下方式来获取带签名的 cookie：

```python
value = request.get_signed_cookie(key, default=None, salt='some_salt')
```

其中：

- `key` 是要获取的 cookie 的键名；
- `default` 是可选参数，表示如果找不到指定的 cookie 时返回的默认值；
- `salt` 是用于生成签名的盐值，需要和设置 cookie 时使用的盐值一致。

这个方法会从请求中获取指定的带签名的 cookie，并返回其值。如果找不到指定的 cookie，则返回默认值（如果提供了）或者 `None`。

通过使用 `get_signed_cookie` 方法，你可以安全地获取带签名的 cookie 的值，并确保其完整性和安全性。

带签名的 cookie 可以增加 cookie 的安全性，防止内容被篡改，从而提高了应用的安全性。





下面来看一下代码示例，如下所示：

```python

salt = '56d4b275-1f3d-4196-925e-c04bb0788ef7' # uuid


def index(request):

    # 判断是否登录成功
    print(request.get_signed_cookie,'--------')
    # <bound method HttpRequest.get_signed_cookie of <WSGIRequest: GET '/index/'>> --------
    # res = request.get_signed_cookie('is_login',None)
    # print(res) # None
    res = request.get_signed_cookie('is_login',salt=salt)

    if res:
        username = request.get_signed_cookie('user',salt=salt)
        return render(request, 'index.html', {'username': username})

    return redirect('/login/')


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    # post请求获取数据，校验
    print(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'lisa' and password == '123':

        res = HttpResponse('登录成功')
        res.set_signed_cookie('is_login', True, salt=salt,max_age=10)
        res.set_signed_cookie('user', username, salt=salt,max_age=10)

        return res

    error_msg = '用户名或者密码错误'

    return render(request, 'login.html', {'error': error_msg})
```





**案例四：注销**



- 清除指定的`Cookie`

```python
def logout(request):
    rep = redirect("/login/")
    rep.delete_cookie("user")  # 删除用户浏览器上之前设置的usercookie值
    return rep
```



- 清空所有的`Cookie`

```python
def logout(request):
    response = redirect('/login/')
    response.cookies.clear()

    return response
```





#### 1.2 cookie设置中文时的编码问题



cookie在设置时不允许出现中文。非要设置中文的怎么办，看下面的解决方案：

- 方式一

```python
def login(request):

    ret = HttpResponse('ok')
    
    ret.set_cookie('k1','你好'.encode('utf-8').decode('iso-8859-1'))
    
    #取值：request.COOKIES['k1'].encode('utf-8').decode('iso-8859-1').encode('iso-8859-1').decode('utf-8')
```



- 方式2 `json`

```python
import json

def login(request):
    ret = HttpResponse('ok')
    ret.set_cookie('k1',json.dumps('你好'))
    #取值 json.loads(request.COOKIES['k1'])
    return ret
```

 所以尽量不要出现中文。



## jquery之cookie操作

这种技术叫做“Cookie”。Cookie 是网站服务器存储在用户本地计算机上的小块数据。它们用于跟踪和存储有关用户的信息，比如登录状态、个人设置、会话信息等，以便在用户再次访问网站时能够识别用户并恢复之前的会话状态。

`Cookie`定义：让网站服务器把少量数据储存到客户端的硬盘或内存，从客户端的硬盘读取数据的一种技术；

下载与引入:jquery.cookie.js基于jquery；先引入jquery，再引入：jquery.cookie.js；

下载：http://plugins.jquery.com/cookie/

或者boot CDN：https://www.bootcdn.cn/jquery-cookie/

```
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
```

 1.添加一个"会话cookie"

```js
$.cookie('the_cookie', 'the_value');
```

这里没有指明 cookie有效时间，所创建的cookie有效期默认到用户关闭浏览器为止，所以被称为 `会话cookie（session cookie）`。

2.创建一个cookie并设置有效时间为 7天

```js
$.cookie('the_cookie', 'the_value', { expires: 7 });
```

这里指明了cookie有效时间，所创建的cookie被称为“持久 cookie （persistent cookie）”。注意单位是：天；



3.创建一个cookie并设置 cookie的有效路径

```js
$.cookie('the_cookie', 'the_value', { expires: 7, path: '/' });
```

在默认情况下，只有设置 cookie的网页才能读取该  cookie。如果想让一个页面读取另一个页面设置的cookie，必须设置cookie的路径。cookie的路径用于设置能够读取  cookie的顶级目录。将这个路径设置为网站的根目录，可以让所有网页都能互相读取 cookie （一般不要这样设置，防止出现冲突）。

4.读取cookie

```js
$.cookie('the_cookie');
```

 5.删除cookie

```js
$.cookie('the_cookie', null);   //通过传递null作为cookie的值即可
```

6.可选参数

```js
$.cookie('the_cookie','the_value',{
    expires:7, 
    path:'/',
    domain:'jquery.com',
    secure:true
})　
```



参数

```js
expires：（Number|Date）有效期；设置一个整数时，单位是天；也可以设置一个日期对象作为Cookie的过期日期；
path：（String）创建该Cookie的页面路径；
domain：（String）创建该Cookie的页面域名；
secure：（Booblean）如果设为true，那么此Cookie的传输会要求一个安全协议，例如：HTTPS；
```

 



## 3. Cookie源码

#### 3.1 请求源码分析

- HttpResponse，包裹

	```python
	# 包含：响应体、响应头、状态码等信息
	obj = HttpResponse("x1", status=201, reason="OK")
	
	# 设置响应头
	obj['name'] = "wupeiqi"
	
	# 设置cookie
	# import datetime
	# ctime = datetime.datetime.now() + datetime.timedelta(seconds=10)
	
	obj.set_cookie("v3", "root", max_age=10, path="/")
	obj.set_cookie("v2", "hello")
	
	obj.set_signed_cookie("info", "xiaoguang")  # 签名
	return obj
	```

- WSGIRequest

	```python
	class WSGIHandler(base.BaseHandler):
	    request_class = WSGIRequest
	
	    def __init__(self, *args, **kwargs):
	        super().__init__(*args, **kwargs)
	        self.load_middleware()
	
	    def __call__(self, environ, start_response):
	        set_script_prefix(get_script_name(environ))
	        signals.request_started.send(sender=self.__class__, environ=environ)
	
	        request = self.request_class(environ)
	```

	```python
	class HttpRequest:
	    def get_signed_cookie(self, key, default=RAISE_ERROR, salt="", max_age=None):
	        cookie_value = self.COOKIES[key]
	        value = signing.get_cookie_signer(salt=key + salt).unsign(cookie_value, max_age=max_age)
			return value
	
	class WSGIRequest(HttpRequest):
	    def __init__(self, environ):
	        self.environ = environ
	        ...
	        
	    @cached_property
	    def COOKIES(self):
	        raw_cookie = get_str_from_wsgi(self.environ, "HTTP_COOKIE", "")
	        return parse_cookie(raw_cookie)
	```

	





#### 3.2 Cookie响应源码

HttpResponse，包裹

```python
# 包含：响应体、响应头、状态码等信息
obj = HttpResponse("x1", status=201, reason="OK")

# 设置响应头
obj['name'] = "wupeiqi"

# 设置cookie
# import datetime
# ctime = datetime.datetime.now() + datetime.timedelta(seconds=10)

obj.set_cookie("v3", "root", max_age=10, path="/")
obj.set_cookie("v2", "hello")

obj.set_signed_cookie("info", "xiaoguang")  # 签名
return obj
```

WSGIRequest

```python
class WSGIHandler(base.BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()

    def __call__(self, environ, start_response):
        set_script_prefix(get_script_name(environ))
        signals.request_started.send(sender=self.__class__, environ=environ)

        request = self.request_class(environ)
```

```python
class HttpRequest:
    def get_signed_cookie(self, key, default=RAISE_ERROR, salt="", max_age=None):
        cookie_value = self.COOKIES[key]
        value = signing.get_cookie_signer(salt=key + salt).unsign(cookie_value, max_age=max_age)
		return value

class WSGIRequest(HttpRequest):
    def __init__(self, environ):
        self.environ = environ
        ...
        
    @cached_property
    def COOKIES(self):
        raw_cookie = get_str_from_wsgi(self.environ, "HTTP_COOKIE", "")
        return parse_cookie(raw_cookie)
```














