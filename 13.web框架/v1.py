
##### DNS域名解析过程
1. 浏览器检查缓存中有没有这个域名对应的解析后的IP地址，如果缓存中有，解析过程结束。缓存大小、时间都有限制，时间由TTL属性决定；
2. 如果浏览器缓存中么有，浏览器会查找操作系统缓存中有无这个域名DNS解析后的结果。操作系统也有一个域名解析的过程，windows通过C:\Windows\System32\drivers\etc\hosts，浏览器会优先使用这个解析结果（Win7已将hosts设置为只读），linux系统中/etc/named.conf。目前为止都是在本机完成，如果未完成，才会真正请求域名服务器解析域名。
3. “网络配置”中都会有“DNX服务器地址”，操作系统会把域名发送给这个LDNS，本地区的域名服务器，通常都会提供一个本地互联网接入的DNS解析服务。就在你所在城市的某个角落，通过ipconfig可以看到。
4. 如果LDNS仍然没有命中，则向RootServer域名服务器请求解析。
5. 根域名服务器向本地域名服务器返回一个所查询域的主域名服务器（gTLD Server）。国际顶级域名服务器（.com、.cn、.org等），全球13台。
6. 本地域名服务器（Local DNS Server）再向上一步返回的gTLD发送请求。
7. gTLD返回域名对应NameServer域名服务器地址，通常由你购买域名的服务商提供。
8. NameServer服务器查询域名与IP映射关系表，返回目标IP记录和TTL值给DNS Server域名服务器。
9. Local DNS Server根据TTL缓存该IP解析。
10. 缓存结果返回给用户，用户根据TTL缓存到本地操作系统中，域名解析过程结束。

##### 了解过Hbase，DB2，SQLServer，Access吗
* Hbase：HBase是一个分布式的、面向列的开源数据库
* DB2：一套关系型数据库管理系统，
* SQLServer：SQL Server是由Microsoft开发和推广的关系数据库管理系统
* Sccess：Access是由微软发布的关系数据库管理系统。


##### JavaScript(或者jQuery)如何选择一个id为main的容器

> jquery：$('#id')
> JavaScript：document.getElementById("id"))


##### css如何隐藏一个元素
* display：none

##### 前后端分离的基本原理
[参考链接](https://www.cnblogs.com/Kevin-ZhangCG/p/9501635.html)

* 前后端分离并非仅仅只是一种开发模式，而是一种架构模式（前后端分离架构）。前端项目与后端项目是两个项目，放在两个不同的服务器，需要独立部署，两个不同的工程，两个不同的代码库，不同的开发人员。前后端工程师需要约定交互接口，实现并行开发，开发结束后需要进行独立部署，前端通过Ajax来调用HTTP请求调用后端的restful api。前端只需要关注页面的样式与动态数据的解析&渲染，而后端专注于具体业务逻辑。

##### 如何保证api调用时数据的安全性
1. 通信使用https
2. 请求签名，防止参数被篡改
3. 身份确认机制，每次请求都要验证是否合法
4. app中使用ssl pinning防止抓包操作
5. 对所有的请求和响应都进行加解密操作

##### 如何实现响应式布局
1. 流体布局
    * 其实就是度量单位的改变。在响应式设计的布局中，不在把像素(px)作为唯一的单位，而是采用%或者是混合%、px为单位，设计出自己想要的布局方式。
2. 媒体查询
    * 媒体查询可以在你根据特定的环境下查询到各种属性---------比如设备类型，分辨率、屏幕物理尺寸以及色彩等。通过使用媒体查询，可以获得设备的一些特性，以及响应式的布局方案。
3. 弹性图片
    * 其实在做响应式布局时，大多用到的是弹性盒子进行布局，那么在设置图片的地方也应该具有一些变化以适应布局的变化。出了图片外，像图标啦！视频啦也应做一些调整用以适应布局的变化。

##### 曾经使用过哪些前端框架
* react，vue，bootstrap，elementUI，Echarts

##### 什么是ajax请求？手写一个ajax请求
* ajax（异步JavaScript和XML）是指一种创建交付式网页应用的网页开发技术。可以在不重新加载整个网页的情况下，对网页的某部分进行更新。
```javascript
// 不使用第三方
var xhr = new XMLHttpRequest();
xhr.open("GET", url, false);
xhr.onreadtstatechange = function () {
    if (xhr.readystate == 4) {
        //响应内容解析完成，可以在客户端调用了
        if (xhr.status == 200) {
            //客户端的请求成功了
            alert(xhr.responseText);
        }
    }
}
xhr.send(null);

// 使用ajax

$.ajax({
            type:"GET",
            url:"",
            dataType:"json",
            success:function(data){
            },
            error:function(jqXHR){
            }
        });

```

##### 什么是轮询和长轮询
* 轮询是在特定的的时间间隔（如每1秒），由浏览器对服务器发出HTTP request，然后由服务器返回最新的数据给客户端的浏览器。这种传统的HTTP request 的模式带来很明显的缺点 – 浏览器需要不断的向服务器发出请求，然而HTTP request 的header是非常长的，里面包含的有用数据可能只是一个很小的值，这样会占用很多的带宽。
```javascript
var xhr = new XMLHttpRequest();         
    setInterval(function(){
        xhr.open('GET','/user'); 
        xhr.onreadystatechange = function(){ }; 
        xhr.send();
    },1000)
```

* 长轮询是ajax实现:在发送ajax后,服务器端会阻塞请求直到有数据传递或超时才返回。 客户端JavaScript响应处理函数会在处理完服务器返回的信息后，再次发出请求，重新建立连接。

```javascript
 function ajax(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','/user');
        xhr.onreadystatechange = function(){
              ajax();
        };
        xhr.send();
    }
```

##### vuex的作用

1. 组件之间的数据通信
2. 使用单向数据流的方式进行数据的去中心化管理

##### vue中的路由拦截器的作用

* 当某些页面需要访问权限时，可以使用路由拦截器对用户权限进行判断

##### axios的作用

* axios是基于promise的用于浏览器和nodejs的HTTP客户端，本身有以下特征：
  1. 从浏览器中创建XMLHttpRequest；
  2. 从nodejs发出http请求
  3. 支持promiseAPI
  4. 拦截 请求和响应
  5. 转换请求和响应数据
  6. 取消请求
  7. 自动转换JSON数据
  8. 客户端支持防止CSRF/XSRF攻击

##### 简述jsonp及其原理

* JSONP是JSON with Padding的略称。它是一个非官方的协议，它允许在服务器端集成Script tags返回至客户端，通过javascript callback的形式实现跨域访问（这仅仅是JSONP简单的实现形式）

* 原理：<script>标签的src属性并不被同源策略所约束，所以可以获取任何服务器上脚本并执行。

  ```javascript
  <script type="text/javascript" src="http://localhost:20002/test.js"></script>
  ```

  

##### 简述http协议以及常用请求头

* HTTP(超文本传输协议)是一个应用层协议，由请求和相应构成，是一个标准的客户端服务器模型。HTTP通常承载于TCP协议之上，有时也承载于TLS或SSL协议层之上，这个时候，就成了常说的HTTPS。默认HTTP的端口号为80，HTTPS的端口号为443。
* 常用请求头
  * Accept：向服务器申明客户端（浏览器）可以接受的媒体类型（MIME）的资源
  * Accept-encoding：向服务器申明客户端（浏览器）接收的编码方法，通常为压缩方法
  * Accept-Language：向服务器申明客户端（浏览器）接收的语言
  * Cookie：告诉服务器关于 Session 的信息，存储让服务器辨识用户身份的信息。
  * Refer：告诉服务器该页面从哪个页面链接的。
  * User-agent：向服务器发送浏览器的版本、系统、应用程序的信息。

##### 列举常用的http请求方法

1. GET    请求指定的页面信息，并返回实体主体。
2. HEAD    类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头
3. POST    向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。
4. PUT    从客户端向服务器传送的数据取代指定的文档的内容。
5. DELETE    请求服务器删除指定的页面。
6. CONNECT    HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。
7. OPTIONS    允许客户端查看服务器的性能。
8. TRACE    回显服务器收到的请求，主要用于测试或诊断。

##### 列举常用的状态码

> 1xx：指示信息–表示请求已接收，继续处理 
> 2xx：成功–表示请求已被成功接收、理解、接受 
> 3xx：重定向–要完成请求必须进行更进一步的操作
>  4xx：客户端错误–请求有语法错误或请求无法实现
>  5xx：服务器端错误–服务器未能实现合法的请求 
> 常见状态代码、状态描述、说明： 
> 200 OK     //客户端请求成功 
> 400 Bad Request  //客户端请求有语法错误，不能被服务器所理解 
> 401 Unauthorized //请求未经授权，这个状态代码必须和 WWW-Authenticate 报头域一起使用
>  403 Forbidden  //服务器收到请求，但是拒绝提供服务 
> 404 Not Found  //请求资源不存在，eg：输入了错误的 URL 
> 500 Internal Server Error //服务器发生不可预期的错误 
> 503 Server Unavailable  //服务器当前不能处理客户端的请求，一段时间后可能恢复正常 

##### http和https的区别

> 1、https协议需要到ca申请证书，一般免费证书较少，因而需要一定费用。
> 2、http是超文本传输协议，信息是明文传输，https则是具有安全性的ssl加密传输协议。
> 3、http和https使用的是完全不同的连接方式，用的端口也不一样，前者是80，后者是443。
> 4、http的连接很简单，是无状态的；HTTPS协议是由SSL+HTTP协议构建的可进行加密传输、身份认证的网络协议，比http协议安全。

##### 简述websocket协议及实现原理
[参考链接](https://www.cnblogs.com/nnngu/p/9347635.html)

* WebSocket用于在Web浏览器和服务器之间进行任意的双向数据传输的一种技术。WebSocket协议基于TCP协议实现，包含初始的握手过程，以及后续的多次数据帧双向传输过程。其目的是在WebSocket应用和WebSocket服务器进行频繁双向通信时，可以使服务器避免打开多个HTTP连接进行工作来节约资源，提高了工作效率和资源利用率。

##### django中如何实现websocket

* 通过使用channels模块来实现

##### python web开发中跨域问题的解决思路

[参考链接](https://blog.csdn.net/a961634066/article/details/82765554)

1. 使用django-cors-headers模块，给跨域增加忽略
2. 使用jsonp
3. 修改对应的api实现函数views.py，允许其他域通过ajax请求数据。

##### 简述http缓存机制

[参考链接](http://www.cnblogs.com/chenqf/p/6386163.html)

* 对于强制缓存，服务器通知浏览器一个缓存时间，在缓存时间内，下次请求，直接用缓存，不在时间内，执行比较缓存策略。对于比较缓存，将缓存信息中的Etag和Last-Modified通过请求发送给服务器，由服务器校验，返回304状态码时，浏览器直接使用缓存。

##### 什么是wsgi

* WSGI是Python在处理HTTP请求时，规定的一种处理方式。如一个HTTP Request过来了，那么就有一个相应的处理函数来进行处理和返回结果。WSGI就是规定这个处理函数的参数长啥样的，它的返回结果是长啥样的？至于该处理函数的名子和处理逻辑是啥样的，那无所谓。简单而言，WSGI就是规定了处理函数的输入和输出格式。

##### 列举django的内置组件

- .Admin是对model中对应的数据表进行增删改查提供的组件
- .model组件：负责操作数据库
- .form组件：1.生成HTML代码2.数据有效性校验3校验信息返回并展示
- .ModelForm组件即用于数据库操作,也可用于用户请求的验证

##### django请求的生命周期

* 当用户在浏览器中输入url时,浏览器会生成请求头和请求体发给服务端
   请求头和请求体中会包含浏览器的动作(action),这个动作通常为get或者post,体现在url之中.
* url经过Django中的wsgi,再经过Django的中间件,最后url到过路由映射表,在路由中一条一条进行匹配,
   一旦其中一条匹配成功就执行对应的视图函数,后面的路由就不再继续匹配了.
* 视图函数根据客户端的请求查询相应的数据.返回给Django,然后Django把客户端想要的数据做为一个字符串返回给客户端.
* 客户端浏览器接收到返回的数据,经过渲染后显示给用户.

##### 列举django中间件的5个方法

* process_request : 请求进来时,权限认证
* process_view : 路由匹配之后,能够得到视图函数
* process_exception : 异常时执行
* process_template_responseprocess : 模板渲染时执行
* process_response : 请求有响应时执行

##### 简述什么是FBV和CBV

FBV和CBV本质是一样的，基于函数的视图叫做FBV，基于类的视图叫做CBV
在python中使用CBV的优点：
- .提高了代码的复用性，可以使用面向对象的技术，比如Mixin（多继承）
- .可以用不同的函数针对不同的HTTP方法处理，而不是通过很多if判断，提高代码可读性

##### 如何给CBV的程序添加装饰器

```python
from django.utils.decorators import method_decorator
# 1、给方法加：
@method_decorator(check_login)
def post(self, request):
	...
# 2、给dispatch加：
@method_decorator(check_login)
def dispatch(self, request, *args, **kwargs):
	...
# 3、给类加：
@method_decorator(check_login, name="get")
@method_decorator(check_login, name="post")
class HomeView(View):
	...
```



##### 列举django orm中的所有方法

```
  <1> all():                  查询所有结果 
  <2> filter(**kwargs):       它包含了与所给筛选条件相匹配的对象。获取不到返回None
  <3> get(**kwargs):          返回与所给筛选条件相匹配的对象，返回结果有且只有一个。
                              如果符合筛选条件的对象超过一个或者没有都会抛出错误。
  <4> exclude(**kwargs):      它包含了与所给筛选条件不匹配的对象
  <5> order_by(*field):       对查询结果排序
  <6> reverse():              对查询结果反向排序 
  <8> count():                返回数据库中匹配查询(QuerySet)的对象数量。 
  <9> first():                返回第一条记录 
  <10> last():                返回最后一条记录 
  <11> exists():              如果QuerySet包含数据，就返回True，否则返回False
  <12> values(*field):        返回一个ValueQuerySet——一个特殊的QuerySet，运行后得到的
                              并不是一系 model的实例化对象，而是一个可迭代的字典序列
  <13> values_list(*field):   它与values()非常相似，它返回的是一个元组序列，values返回的是一个字典序列
  <14> distinct():            从返回结果中剔除重复纪录
```



##### select_related和prefetch_related的区别

> 前提：有外键存在时，可以很好的减少数据库请求的次数,提高性能
> select_related通过多表join关联查询,一次性获得所有数据,只执行一次SQL查询
> prefetch_related分别查询每个表,然后根据它们之间的关系进行处理,执行两次查询

##### filter和exclude的区别？

> 两者取到的值都是QuerySet对象,filter选择满足条件的,exclude:排除满足条件的.



##### 列举django orm中三种能写sql语句的方法

```
1.使用execute执行自定义的SQL
     直接执行SQL语句（类似于pymysql的用法）
        # 更高灵活度的方式执行原生SQL语句
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT DATE_FORMAT(create_time, '%Y-%m') FROM blog_article;")
        ret = cursor.fetchall()
        print(ret)
2.使用extra方法 ：queryset.extra(select={"key": "原生的SQL语句"})
3.使用raw方法
    1.执行原始sql并返回模型
    2.依赖model多用于查询
```



##### values和values_list的区别

- values : queryset类型的列表中是字典
- values_list : queryset类型的列表中是元组

##### cookie和session的区别

* cookie:
 cookie是保存在浏览器端的键值对,可以用来做用户认证
* session：
 将用户的会话信息保存在服务端,key值是随机产生的字符串,value值是session的内容
 依赖于cookie将每个用户的随机字符串保存到用户浏览器上
* Django中session默认保存在数据库中：django_session表
* flask,session默认将加密的数据写在用户的cookie中

##### 如何使用django orm批量创建数据

```python
objs=[models.Book(title="图书{}".format(i+15)) for i in range(100)]
models.Book.objects.bulk_create(objs)
```



##### django的Form组件中，如果字段中包含choices参数，使用两种方式实现数据源实时更新

```python
# 1. 重写构造函数
def__init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     self.fields["city"].widget.choices = models.City.objects.all().values_list("id", "name")

# 2. 利用ModelChoiceField字段，参数为queryset对象
authors = form_model.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())//多选
```



##### django的Model中的ForeignKey字段中的on_delete参数有什么作用？

- 删除关联表中的数据时,当前表与其关联的field的操作
- django2.0之后，表与表之间关联的时候,必须要写on_delete参数,否则会报异常

##### django模板中自定义filter和simple_tag的区别

- 自定义filter：{{ 参数1|filter函数名:参数2 }}
  1.可以与if标签来连用
  2.自定义时需要写两个形参

```python
    例子：自定义filter
            1. 在app01下创建一个叫templatetags的Python包
            2. 在templatetags的文件夹下创建py文件  myfilters
            3. 在py文件中写代码
                from django import template
                register = template.Library()
                
                @register.filter
                def add_sb(value,arg='aaa'):
                    return "{}_sb_{}".formart(value,arg)
                    
                @register.filter(name='sb')
                def add_sb(value,arg='aaa'):
                    return "{}_sb_{}".formart(value,arg)     
            4. 使用自定义filter
                {% load myfilters %}
                {{ name|add_sb:'xxx'}}
                {{ name|sb:'xxx'}}
```

- simple_tag:{% simple_tag函数名 参数1 参数2 %}
  1.可以传多个参数,没有限制
  2.不能与if标签来连用

```python
例子：自定义simpletag
    创建
        1 、在app01中创建一个名字是templatetags的包，
        2、在包中创建一个py文件
        3、在py文件中导入
              from django import template
              register = template.Library()
        4、写函数
              @register.simple_tag(name="plus")
              def plus(a,b,c):
                  return '{}+{}+{}'.format(a,b,c)
        5、加装饰器@register.simple_tag(name="plus")
  使用
      1、导入
            {% load mytag %}
      2、使用
           {% plus 1 2 3 %}
```



##### django中csrf的实现机制

1. django第一次响应来自某个客户端的请求时,后端随机产生一个token值，把这个token保存在SESSION状态中;同时,后端把这个token放到cookie中交给前端页面；
2. 下次前端需要发起请求（比如发帖）的时候把这个token值加入到请求数据或者头信息中,一起传给后端；Cookies:{csrftoken:xxxxx}
3. 后端校验前端请求带过来的token和SESSION里的token是否一致。

##### 基于django使用ajax发送post请求时，都可以使用哪种方法携带csrf token？

```
1.后端将csrftoken传到前端，发送post请求时携带这个值发送
data: {
        csrfmiddlewaretoken: '{{ csrf_token }}'
  },

2.获取form中隐藏标签的csrftoken值，加入到请求数据中传给后端
data: {
          csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()
     },

3.cookie中存在csrftoken,将csrftoken值放到请求头中
headers:{ "X-CSRFtoken":$.cookie("csrftoken")}
```



##### django本身提供了runserver，为什么不能用来部署

1. runserver方法是调试 Django 时经常用到的运行方式，它使用Django自带的
    WSGI Server 运行，主要在测试和开发中使用，并且 runserver 开启的方式也是单进程 。

2. uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http 等协议。注意uwsgi是一种通信协议，而uWSGI是实现uwsgi协议和WSGI协议的 Web 服务器。uWSGI具有超快的性能、低内存占用和多app管理等优点，并且搭配着Nginx就是一个生产环境了，能够将用户访问请求与应用 app 隔离开，实现真正的部署 。相比来讲，支持的并发量更高，方便管理多进程，发挥多核的优势，提升性能。

##### django配置实现数据库读写分离

[参考连接](https://blog.csdn.net/linzi1994/article/details/82934612)

1. 在配置文件中添加slave数据库配置
2. 创建数据库操作的路由分发类
3. 配置读写分离路由

##### django中F和Q的作用

* F查询：对数据本身的不同字段进行操作 如:比较和更新
* Q查询：对对象进行复杂查询，并支持and，or，not等操作符

##### django中only和defer的区别

* defer--> 除了指定字段之外
* only--> 只查询几个字段
  * 比如：ret=Book.object.all().only('name')
  * id始终会查，结果是queryset对象,套book对象(里面只有id与name字段)
  * 如果取price，会发生什么？他会再次查询数据库，对数据库造成压力

##### django中的Form组件和ModelForm组件的作用

* Form作用：
    1.在前端生成HTML代码
    2.对数据作有效性校验
    3.返回校验信息并展示
* ModeForm：根据模型类生成From组件,并且可以操作数据库

##### django路由系统中的name的作用

* 用于反向解析路由，相当于给url取个别名，只要这个名字不变，即使对应的url改变
* 通过改名字也能找到该条url

#####  django如何实现单元测试

[参考链接](https://www.cnblogs.com/1204guo/p/8058449.html)

* django的单元测试使用python的unittest模块，这个模块使用基于类的方法来定义测试。类名为django.test

##### 解释orm中db first和code first的含义

* 数据持久化的方式：
  * db first基于已存在的数据库，生成模型
  * code first基于已存在的模型，生成数据库

##### django-debug-toolbar的作用

* 是django的第三方工具包，给django扩展了调试功能，包括查看sql语句，db查询次数，request，headers等

##### django中如何根据数据库表生成model中的类？

1. 在settings中设置要连接的数据库

2. 生成model模型文件

   ```python
   python manage.py inspectdb
   ```

3. 将模型文件导入到models中

   ```python
   python manage.py inspectdb > app/models.py
   ```

   

##### 使用orm和原生sql的优缺点

1. orm的开发速度快,操作简单。使开发更加对象化
2. 执行速度慢、处理多表联查等复杂操作时，orm的语法会变得复杂
3. sql开发速度慢，执行速度快，性能强

##### django的contenttype组件的作用

* 这个组件保存了项目中所有app和model的对应关系,每当我们创建了新的model并执行数据库迁移后，ContentType表中就会自动新增一条记录
* 当一张表和多个表FK关联,并且多个FK中只能选择其中一个或其中n个时,可以利用contenttypes

##### 谈谈你对restful规范的认识

> #首先restful是一种软件架构风格或者说是一种设计风格，并不是标准，它只是提供了一组设计#原则和约束条件，主要用于客户端和服务器交互类的软件。     
> #就像设计模式一样，并不是一定要遵循这些原则，而是基于这个风格设计的软件可以更简洁，更#有层次，我们可以根据开发的实际情况，做相应的改变。
> #它里面提到了一些规范，例如：
> #1.restful 提倡面向资源编程,在url接口中尽量要使用名词，不要使用动词             
> #2、在url接口中推荐使用Https协议，让网络接口更加安全
> #https://www.bootcss.com/v1/mycss？page=3
> #（Https是Http的安全版，即HTTP下加入SSL层，HTTPS的安全基础是SSL，
> #因此加密的详细内容就需要SSL（安全套接层协议））                          
> #3、在url中可以体现版本号
> #https://v1.bootcss.com/mycss
> #不同的版本可以有不同的接口，使其更加简洁，清晰             
> #4、url中可以体现是否是API接口 
> #https://www.bootcss.com/api/mycss            
> #5、url中可以添加条件去筛选匹配
> #https://www.bootcss.com/v1/mycss？page=3             
> #6、可以根据Http不同的method，进行不同的资源操作
> #（5种方法：GET / POST / PUT / DELETE / PATCH）             
> #7、响应式应该设置状态码
> #8、有返回值，而且格式为统一的json格式             
> #9、返回错误信息
> #返回值携带错误信息             
> #10、返回结果中要提供帮助链接，即API最好做到Hypermedia
> #如果遇到需要跳转的情况 携带调转接口的URL
>     　　ret = {
>             code: 1000,
>             data:{
>             id:1,
>             name:'小强',
>             depart_id:http://www.luffycity.com/api/v1/depart/8/
>             }
>     }

##### 接口的幂等性是什么意思？

1. 是系统的接口对外一种承诺(而不是实现)
2. 承诺只要调用接口成功，外部多次调用对系统的影响都是一致的，不会对资源重复操作

##### 为什么要使用API

* 系统间为了调用数据
* 数据传输格式：json和xml

##### 为什么要使用django rest framework框架

> 能自动生成符合 RESTful 规范的 API
> 1.在开发REST API的视图中，虽然每个视图具体操作的数据不同，
> 但增、删、改、查的实现流程基本一样,这部分的代码可以简写
> 2.在序列化与反序列化时，虽然操作的数据不同，但是执行的过程却相似,这部分的代码也可以简写
> REST framework可以帮助简化上述两部分的代码编写，大大提高REST API的开发速度

##### django rest framework框架中都有哪些组件

> 1.序列化组件:serializers  对queryset序列化以及对请求数据格式校验
> 2.路由组件routers 进行路由分发
> 3.视图组件ModelViewSet  帮助开发者提供了一些类，并在类中提供了多个方法
> 4.认证组件 写一个类并注册到认证类(authentication_classes)，在类的的authticate方法中编写认证逻
> 5.权限组件 写一个类并注册到权限类(permission_classes)，在类的的has_permission方法中编写认证逻辑。 
> 6.频率限制 写一个类并注册到频率类(throttle_classes)，在类的的allow_request/wait 方法中编写认证逻辑
> 7.解析器  选择对数据解析的类，在解析器类中注册(parser_classes)
> 8.渲染器 定义数据如何渲染到到页面上,在渲染器类中注册(renderer_classes)
> 9.分页  对获取到的数据进行分页处理, pagination_class
> 10.版本  版本控制用来在不同的客户端使用不同的行为
> 在url中设置version参数，用户请求时候传入参数。在request.version中获取版本，根据版本不同 做不同处理 

##### 简述django rest framework框架的认证流程

1. 用户请求走进来后,走APIView,初始化了默认的认证方法
2. 走到APIView的dispatch方法,initial方法调用了request.user
3. 如果我们配置了认证类,走我们自己认证类中的authentication方法

##### django rest framework如何实现用户的访问频率控制

```
#使用IP/用户账号作为键，每次的访问时间戳作为值，构造一个字典形式的数据，存起来，每次访问时对时间戳列表的元素进行判断，
#把超时的删掉，再计算列表剩余的元素数就能做到频率限制了 
#匿名用户：使用IP控制，但是无法完全控制，因为用户可以换代理IP登录用户：使用账号控制，但是如果有很多账号，也无法限制
```



##### 给用户提供一个接口之前需要提前做什么

1. 跟前端进行交互，确定前端要什么
2. 把需求写成文档保存

##### PV和UV

1. PV：页面访问量，每打开一次页面PV计算+1，页面刷新也是
2. UV：独立访问数，一台电脑终端为一个访客

##### 如何实现用户的登录认证

1. 使用cookie session
2. token 登录成功后生成加密字符串
3. JWT：json web token 缩写 它将用户信息加密到token中，服务器不保存任何用户信息服务器通过使用保存的秘钥来验证token的正确性

##### 简述MVC和MTV

1. MVC软件系统分为三个基本部分：模型(Model)、视图(View)和控制器(Controller)
	* Model：负责业务对象与数据库的映射(ORM)
	* View：负责与用户的交互
	* Control：接受用户的输入调用模型和视图完成用户的请求
2. Django框架的MTV设计模式借鉴了MVC框架的思想,三部分为：Model、Template和View
	* Model(模型)：负责业务对象与数据库的对象(ORM)
	* Template(模版)：负责如何把页面展示给用户
	* View(视图)：负责业务逻辑，并在适当的时候调用Model和Template
* 此外,Django还有一个urls分发器,
* 它将一个个URL的页面请求分发给不同的view处理,view再调用相应的Model和Template

