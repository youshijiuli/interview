# 深入了解CSRF

CSRF（Cross-site request forgery）跨站请求伪造，是一种常见的网络攻击手段，具体内容和含义请大家自行百度。Django为我们提供了防范CSRF攻击的机制。


## 一、基本使用

默认情况下，使用`django-admin startproject xxx`命令创建工程时，CSRF防御机制就已经开启了。如果没有开启，请在MIDDLEWARE设置中添加'django.middleware.csrf.CsrfViewMiddleware'。

**对于GET请求，一般来说没有这个问题，CSRF通常是针对POST方法的！**


在含有POST表单的模板中，只需要在其`<form>`表单内部添加`csrf_token`标签，如下所示：

```html
<form action="" method="post">
    {% csrf_token %}
    ....
</form>
```

这样，实际上就是生成了一个隐藏的名称为`'csrfmiddlewaretoken'`的input输入框，这个input的值就是Django提供给表单的csrf_token。

当表单数据通过POST方法，发送到后台服务器的时候，除了正常的表单数据外，还会携带这个CSRF令牌随机字符串，用于进行csrf验证。

其实没有多么麻烦和复杂，对么？如果表单中没有携带这个csrf令牌，你将会获得一枚403奖章。

额外提示：对于初学者，要明白一件事情，就是我们上面讲的都是Django项目自己内部的事务，不涉及与外界的关系。例如，你不能把上面那个表单发往百度，百度会懵逼的，你这发的啥？其次，那样也不安全，可能引起CSRF信息泄露而导致自己的站点出现漏洞。

## 二、 AJAX

我们知道，在前端的世界，有一种叫做AJAX的东西，也就是“Asynchronous Javascript And XML”（异步 JavaScript 和 XML），经常被用来在不刷新页面的情况下，提交和请求数据。如果我们的Django服务器接收的是一个通过AJAX发送过来的POST请求的话，那么将很麻烦。

为什么？因为AJAX中，没有办法像form表单中那样通过一个隐藏的input标签携带`{% csrf_token %}`令牌。

那怎么办呢？其实也很好办。

**首先我们要知道CSRF中间件会在cookie中写入CSRF令牌随机字符串。**

我们只需要通过JS代码获取这个字符串，然后随同AJAX发送到后台服务器即可。

这个随同的过程也很简单，很多JS框架都提供修改HTTP头部的钩子，我们可以在header中添加**`X-CSRFToken`**键值对，值就是CSRF令牌。键的名字可以通过 `CSRF_HEADER_NAME`配置项自定义，但一般保持默认值就好。

然后第一步是获取cookie中的CSRF令牌，不过这取决于两个配置项：

- 当`CSRF_USE_SESSIONS` 和`CSRF_COOKIE_HTTPONLY` 都是`False`的时候

> `CSRF_USE_SESSIONS` 为True表示将csrf的令牌储存在会话中。
>
> `CSRF_COOKIE_HTTPONLY` 为True表示客户端的JS代码不能访问cookie。
>
> 一般来说，大多Web服务器都会保持这两个设置为False，因为True没什么实际意义。

此时直接去cookie中读取CSRF令牌即可(将下面的代码抄到你的HTML中)：

```JS
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
```

如果你安装了`js-cookie`前端库，那么上面的代码可以简化为：

```js
const csrftoken = Cookies.get('csrftoken');
```

`'csrftoken'`是默认情况下CSRF令牌储存在cookie中的键，可以通过`CSRF_COOKIE_NAME`设置来自定义名称。

**注意，为了保证在没有表单系统的时候，Django向cookie中写入了CSRF令牌，你需要在视图上使用装饰器`django.views.decorators.csrf.ensure_csrf_cookie`。**

- 当`CSRF_USE_SESSIONS` 和`CSRF_COOKIE_HTTPONLY` 有一个是`True`的时候

这个时候显然，cookie中即使有CSRF令牌也读取不到。

我们需要在Django进行`render（request, 'xxx.html',{}）`的时候，在HTML文件中显式地添加一个csrf_token到DOM中，然后通过JS代码获得它，如下所示:

```js
{% csrf_token %}
<script>
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
</script>
```

现在，我们通过JS手段成功获取到了CSRF令牌，然后就是通过AJAX在发送POST数据的同时一起发送它了：

```js
const request = new Request(
    /* URL */,
    {headers: {'X-CSRFToken': csrftoken}}
);
fetch(request, {
    method: 'POST',
    mode: 'same-origin'  // Do not send CSRF token to another domain.
}).then(function(response) {
    // ...
});
```

以上是ES6新语法（不再使用JQuery了），如果不熟悉的可以自行学习或者观看我的Vue视频。


## 三、装饰器

### 1. 单独指定csrf验证需要

有时候，我们在全站上关闭了CSRF功能，但是希望某些视图还有CSRF防御，那怎么办呢？

Django为我们提供了一个`csrf_protect(view)`装饰器，使用起来非常方便，如下所示：

```python
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def my_view(request):
    c = {}
    # ...
    return render(request, "a_template.html", c)
```

现在，虽然全站关掉了csrf，但是my_view视图依然需要进行csrf验证。

另外，当你缓存某个视图的时候，由于缓存的机制，你必须显式的为需要csrf保护的视图添加此装饰器：

```python
from django.views.decorators.csrf import csrf_protect

@cache_page(60 * 15)
@csrf_protect
def my_view(request):
    ...
```

### 2. 单独指定忽略csrf验证

有正就有反。在全站开启CSRF机制的时候，有些视图我们并不想开启这个功能。比如，有另外一台机器通过requests库，模拟HTTP通信，以POST请求向我们的Django主机服务器发送过来了一段保密数据。它无法携带CSRF令牌，必然会被403。

这怎么办呢？

在接收这个POST请求的视图上为CSRF开道口子，不进行验证。这就需要使用Django为我们提供的`csrf_exempt(view)`装饰器了，下面是使用范例：

```python
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def my_view(request):
    
    return HttpResponse('Hello world')
```

这下POST数据是没问题了，但是又带来了新的安全问题，需要你自己处理。

最常见的用法如下：

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt  # 外面忽略csrf
def my_view(request):

    @csrf_protect  # 里面需要csrf
    def protected_path(request):
        do_something()

    if some_condition():
       return protected_path(request)
    else:
       do_something_else()
```

### 3. 确保csrf令牌被设置

Django还提供了一个装饰器，确保被装饰的视图在返回HTML页面给前端用户时同时将csrf令牌写入Cookie。

这个装饰器是：`ensure_csrf_cookie(view)`，其使用方法和上面的一样：

```python
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse

@ensure_csrf_cookie
def my_view(request):
    return HttpResponse('Hello world')
```

### 4. requires_csrf_token(view)

这个装饰器类似csrf_protect，一样要进行csrf验证，但是它不会拒绝发送过来的请求。

```python
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

@requires_csrf_token
def my_view(request):
    c = {}
    # ...
    return render(request, "a_template.html", c)
```

## 四、配置项

下面是Django中可配置的关于CSRF的settings：

- `CSRF_COOKIE_AGE`： cookie的有效期
- `CSRF_COOKIE_DOMAIN`： 允许访问的域名
- `CSRF_COOKIE_HTTPONLY`：是否允许JS读取cookie
- `CSRF_COOKIE_NAME`： cookie的键
- `CSRF_COOKIE_PATH`:cookie的位置
- `CSRF_COOKIE_SAMESITE`
- `CSRF_COOKIE_SECURE`：将此设置为 `True`，避免不小心使用 HTTP 传输 CSRF cookie。
- `CSRF_FAILURE_VIEW`：csrf拒绝后跳转的视图
- `CSRF_HEADER_NAME`：csrf在header中的键
- `CSRF_TRUSTED_ORIGINS` ：信任源
- `CSRF_USE_SESSIONS`：是否使用基于session的csrf令牌

大多情况下，以上都不需要配置，保持Django默认即可。







csrftoken

详述CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。攻击者通过HTTP请求江数据传送到服务器，从而盗取回话的cookie。盗取回话cookie之后，攻击者不仅可以获取用户的信息，还可以修改该cookie关联的账户信息。

　　![img](https://img2018.cnblogs.com/blog/988061/201908/988061-20190804210821110-1699988322.png)

　　所以解决csrf攻击的最直接的办法就是生成一个随机的csrftoken值，保存在用户的页面上，每次请求都带着这个值过来完成校验。





### form表单

```python
<form action="" method="post">
    {% csrf_token %}  // form表单里面加上这个标签,模板渲染之后就是一个input标签,type=hidden  name=csrfmiddlewaretoken  value='asdfasdfasdf'
    用户名: <input type="text" name="username">
    密码: <input type="password" name="password">
    <input type="submit">

</form>
```

### ajax过csrf认证

```javascript
方式1
    $.ajax({
      url: "/cookie_ajax/",
      type: "POST",
      data: {
        "username": "chao",
        "password": 123456,
        "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()  // 使用jQuery取出csrfmiddlewaretoken的值，拼接到data中
      },
      success: function (data) {
        console.log(data);
      }
    })

方式2
	$.ajax({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
    });
方式3
	$.ajax({
 
		headers:{"X-CSRFToken":$.cookie('csrftoken')}, #其实在ajax里面还有一个参数是headers，自定制请求头，可以将csrf_token加在这里，我们发contenttype类型数据的时候，csrf_token就可以这样加
 
})

jquery操作cookie: https://www.cnblogs.com/clschao/articles/10480029.html
```

### form表单上传文件

```javascript
<form action="" method="post" enctype="multipart/form-data">  别忘了enctype
    {% csrf_token %}
    用户名: <input type="text" name="username">
    密码: <input type="password" name="password">
    头像: <input type="file" name="file"> 

    <input type="submit">

</form>


views.py
def upload(request):

    if request.method == 'GET':
        print(settings.BASE_DIR) #/static/

        return render(request,'upload.html')

    else:
        print(request.POST)
        print(request.FILES)
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        file_obj = request.FILES.get('file')  #文件对象

        print(file_obj.name) #开班典礼.pptx,文件名称
		
        with open(file_obj.name,'wb') as f:
            # for i in file_obj:
            #     f.write(i)
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse('ok')
```

### ajax上传文件

```javascript
  $('#sub').click(function () {
  
        var formdata = new FormData();
	    
        var uname = $('#username').val();
        var pwd = $('#password').val();

        var file_obj = $('[type=file]')[0].files[0]; // js获取文件对象

        formdata.append('username',uname);
        formdata.append('password',pwd);
        formdata.append('file',file_obj);

        $.ajax({
            url:'{% url "upload" %}',
            type:'post',
            // data:{username:uname,password:pwd,csrfmiddlewaretoken:csrf},
            //data:{username:uname,password:pwd},
            data:formdata,
            
            processData:false,  // 必须写
            contentType:false,  // 必须写

            headers:{
                "X-CSRFToken":$.cookie('csrftoken'),
            },
            success:function (res) {
                console.log(res);
                if (res === '1'){
                    // $('.error').text('登录成功');
                    location.href = '/home/'; // http://127.0.0.1:8000/home/

                }else{
                    $('.error').text('用户名密码错误!');
                }

            }

        })

    })
```

jsonresponse

```javascript
from django.http import JsonResponse


        username = request.POST.get('username')
        pwd = request.POST.get('password')
        ret_data = {'status':None,'msg':None}
        print('>>>>>',request.POST)
        #<QueryDict: {'{"username":"123","password":"123"}': ['']}>
        if username == 'chao' and pwd == '123':
            ret_data['status'] = 1000  # 状态码
            ret_data['msg'] = '登录成功'


        else:
            ret_data['status'] = 1001  # 状态码
            ret_data['msg'] = '登录失败'

        # ret_data_json = json.dumps(ret_data,ensure_ascii=False)
        # return HttpResponse(ret_data_json,content_type='application/json')
        
        
        return JsonResponse(ret_data) # 如果是费字典类型数据,在括号里面加safe=false
	    
 $.ajax({
            url:'{% url "jsontest" %}',
            type:'post',
            // data:{username:uname,password:pwd,csrfmiddlewaretoken:csrf},
            //data:JSON.stringify({username:uname,password:pwd}),

            data:{username:uname,password:pwd},
            headers:{
                // contentType:'application/json',
                "X-CSRFToken":$.cookie('csrftoken'),
            },
            success:function (res) {
                console.log(res,typeof res); // statusmsg {"status": 1001, "msg": "登录失败"}
                var res = JSON.parse(res);  //-- json.loads()
                console.log(res,typeof res);  //直接就是反序列化之后的了
                //JSON.stringify()  -- json.dumps
                if (res.status === 1000){
                    // $('.error').text('登录成功');
                    location.href = '/home/'; // http://127.0.0.1:8000/home/

                }else{
                    $('.error').text(res.msg);
                }

            }

        })
```

