## Django


##### django生命周期

（1）用户输入网址，浏览器发起请求

（2）[WSGI](https://so.csdn.net/so/search?q=WSGI&spm=1001.2101.3001.7020)（服务器网关接口）创建 socket 服务端，接受请求

（3）中间件处理请求

（4）url 路由，根据当前请求的 url 找到相应的视图[函数](https://so.csdn.net/so/search?q=函数&spm=1001.2101.3001.7020)

（5）进入 view，进行业务处理，执行类或者函数，返回[字符串](https://so.csdn.net/so/search?q=字符串&spm=1001.2101.3001.7020)

（6）再次通过中间件处理相应

（7）WSGI 返回响应

（8）浏览器渲染

##### django 中间件怎么实现，自定义中间件

写一个类（或者继承 MiddlewareMixin 类），然后在 settings 配置文件中进行注册

##### django中间件的五个方法

- process_request(self, req)

  请求进入中间件后，第一个执行的方法，

  在执行视图之前被调用(分配url匹配视图)，每个请求都会被调用，返回None或者response对象

  

- process_view(self, req, view_func, view_args, view_kwargs)

  运行完 process_request 后，就运行这个

  调用视图之前进行调用，每个请求都会调用，返回None或者response对象

  

- process_response(self, req, response)

  每次返回 response 的时候必经的方法

  所有响应在返回浏览器之前都会被调用，返回response

  

- process_exception(self, req, exception)

  当视图抛出异常时进行调用

  

- process_template_response(self,request,response)

  视图 return render 模板时，走 process_template_response 包装返回的响应

##### django 怎么识别 url 的 ，url 分发的原理

使用 include 可以分发到不同的子应用

1. 进来的请求转入 /hello/.

2. Django 通过在 ROOT_URLCONF 配置来决定根 URLconf.

3. Django 在 URLconf 中的所有 URL 模式中，查找第一个匹配 /hello/ 的条目。

4. 如果找到匹配，将调用相应的视图函数

5. 视图函数返回一个 HttpResponse

6. Django 转换 HttpResponse 为一个适合的 HTTP response， 以 Web page 显示出来

##### django request对象是在什么时候创建的

(简单的说：即请求一个页面的时候)请求走到 WSGIHandler 类的时候，执行 cell 方法，将 environ 封装成了 request

##### django orm 查询主表不会查询字表，不进行二次查询

##### django orm 的 objects 的方法只查询两个字段

##### django orm 的几种 on_delete

on_delete = models.CASCADE  删除关联数据的时候，与之的关联也删除
on_delete = models.DO_NOTHING  删除关联数据的时候，什么操作也不做
on_delete = models.PROTRCT  删除关联数据的时候，引发报错
on_delete = models.SET_NULL  删除关联数据的时候，与之关联的只设置为空
on_delete = models.SET_DEFAULT  删除关联数据的时候，与之关联的只设置为默认值
on_delete = models.SET  删除关联数据

##### request怎么获取用户传入的参数

request.data

request.query_params.get('key')

##### request获取用户名和密码

request.POST.get('username')

##### 怎么拿cookie

request.COOKIE['key']

##### 怎么设置cookie

response.set_cookie

##### django 怎么配置 mysql 读写分离

1、配置主从库的连接信息

2、定义一个路由类，db_for_read 返回 slave 配置，db_for_write 返回 write 配置

3、路由类要在 settings 配置文件中的 DATABASE_ROUTER 中进行注册

##### django 怎么返回一个图片和文件等静态资源

使用 HttpResponse 返回一个文件句柄对象的read(), 并指定 content_type='image/jpg'

```python
def show_logo(request):
    path = r"C:\Users\18309\PycharmProjects\untitled\static\img\123.jpg"
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type='image/jpg')
```

##### drf 使用的过程有什么问题吗 (感觉面试官的意思是说说drf的缺点)

##### Auth 模块怎么实现认证的,自己写的认证还是用的第三方,具体怎么实现

字节写的，用的 django 自带的 auth 模块，在此基础上添加 JWT 的校验

##### 跨域怎么配置？是什么原理？具体怎么实现？

django-cors-header

原理：

CORS 需要浏览器和服务器同时支持。目前基本上主流的浏览器都支持 CORS。所以只要后端服务支持 CORS，就能够实现跨域。

##### csrf的了解

跨站请求伪造

攻击者通过伪造用户的浏览器的请求，向访问一个用户自己曾经认证访问过的网站发送出去，使目标网站接收并误以为是用户的真实操作而去执行命令。常用于盗取账号、转账、发送虚假消息等。

防御策略：

- 同源检测，禁止其他域名，Origin Header 确定来源域名
- csrf token: 将 CSRF Token 输出到页面中，页面提交的请求携带这个 Token，判断 token 是否正确

##### 使用ajax 无刷新post提交时，有哪些方法可以防范csrf

防御策略：

- 同源检测，禁止其他域名，Origin Header 确定来源域名
- csrf token: 将 CSRF Token 输出到页面中，页面提交的请求携带这个 Token，判断 token 是否正确

##### 什么是wsgi，uwsgi, uWSGI

WSGI: 是 Web 服务器 (uWSGI) 与 Web 应用程序或应用框架 (Django) 之间的一种低级别的接口

uWSGI 是一个 Web 服务器，它实现了 WSGI 协议、uwsgi、http 等协议。Nginx 中 HttpUwsgiModule 的作用是与 uWSGI 服务器进行交换。

**uwsgi** 是服务器和服务端应用程序的二进制线路协议，规定了怎么把请求转发给应用程序和返回

##### Django rest framework 有哪些组件

- 序列化器
- 视图家族 ModelViewSet
- 权限组件 permissions
- 认证 Authentication
- 分页 pagination_class
- 限流 Throttling
- Request 请求
- Response 响应

##### django 中有哪些组件

orm、cookie和session、auth认证、中间件、路由、视图、Template、admin站点

##### Django ORM 中有哪些方法 (objects的方法)

db_table 设置表名

objects.create 添加数据

objects.bulk_create 添加多条数据

objects.all() 查询所有

objects.filter() 根据字段进行过滤出合适的

objects.exclude  排除指定字段

objects.order_by 以指定字段进行排序

objects.values 返回一个列表、每条数据是一个字典

objects.value_list 将模型对象转换成列表，达到减少内存损耗 ，提高性能，列表中的每一条数据为元组类型

object.first 第一条

object.last 最后一条

object.exists 判断是否存在

##### values与values-list

objects.values 返回一个列表、每条数据是一个字典

objects.value_list 将模型对象转换成列表，达到减少内存损耗 ，提高性能，列表中的每一条数据为元组类型

##### django 常用命令

django-admin.py startproject 创建项目

django-admin.py startapp 创建子应用

python manage.py makemigrations 数据迁移（一般不用）

python manage.py runserver 运行测试服务

python manage.py createsuperuser 创建超级管理员

python manage.py shell django环境终端

---

## Flask


##### flask-socketio实现了什么功能

##### flask的生命周期

---

## Python

##### python 实现用户权限认证怎么做简单

使用 JWT，继承 ObtainJSONWebToken 类，然后重写 POST 方法对防水墙进行验证
