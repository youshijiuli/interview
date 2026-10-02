## Web 框架之 Django、Tornado
  
### Django请求生命周期  
1. 当用户在浏览器中输入url时，浏览器会生成请求头和请求体发给服务端。请求头和请求体中会包含浏览器的动作(action)，这个动作通常为get或者post，体现在url之中。  
2. url经过Django中的wsgi，再经过Django的中间件,最后url到过路由映射表,在路由中一条一条进行匹配。一旦其中一条匹配成功就执行对应的视图函数,后面的路由就不再继续匹配了。  
3. 视图函数根据客户端的请求查询相应的数据。返回给Django，然后Django把客户端想要的数据做为一个字符串返回给客户端。  
4. 客户端浏览器接收到返回的数据，经过渲染后显示给用户。  

### 解释下django-debug-toolbar的使用  
使用django开发站点时，可以使用`django-debug-toolbar`来进行调试。  
在`settings.py`中添加`debug_toolbar.middleware.DebugToolbarMiddleware`到项目的`MIDDLEWARE_CLASSES` 内。  

### 如何进行Django单元测试  
单元测试存在的意义就是，可以让我们放心的重构代码，可以在重构代码的时候省下测试重构的代码能否正确运行的时间  
[Django 单元测试](https://code.ziqiangxuetang.com/django/django-test.html)  
[Django单元测试基础知识](https://www.jianshu.com/p/34267dd79ad6)  

### model之F/Q操作  
F操作,使用查询条件的值,F()允许Django在未实际链接数据的情况下具有对数据库字段的值的引用, Python都不需获取F内的值, 直接操作后保存, 用法场景例如 字段+1(加减乘除运算) 字段比较如日期比较  
```python
from django.db.models import F, Q  
models.UserInfo.objects.filter().update(salary=F('salary')+500)  
```

### Q操作,构造搜索条件, 用于构造复杂的查询条件如各种筛选过滤  
```python
con = Q()  
q1 = Q()  
q1.connector = 'OR'  
q1.children.append(('id', 1))  
q1.children.append(('id', 2))  
q2 = Q()  
q2.connector = 'OR'  
q2.children.append(('status', '在线'))  
con.add(q1, 'AND')  
con.add(q2, 'AND')  
models.Tb1.objects.filter(con)  
```

### simple_tag用法  
```python
from django import template  
register = template.Library()  

  @register.simple_tag  
def foo()...  
```

### ORM是什么？  
ORM 全称是 Object/Relation Mapping,即对象/关系数据库映射。可以讲ORM理解成一种规范，它概述了这类框架的基本特征，完成面相对象的编程语言到关系数据库的映射。  
ORM可以当成是应用程序和数据的桥梁。  

  基本映射方式 ORM工具提供了持久化类和数据表之间的映射关系，通过这种映射关系的过度，程序员可以很方便地通过持久化类实现数据表的操作。实际上，所有的ORM工具大致都遵循相同的映射思路。  
映射关系：  
1、数据表映射类  
持久化映射到一个数据表。程序使用这个持久化类来创建实例，修改属性，删除实例时，系统自动对这个表进行操作。  
2、数据表的行映射对象（实例）  
持久化类会生成很多实例，每个实例就对应数据表中的一行记录。  
3、数据的列（字段）映射对象的属性  
当程序修改某个持久化对象的指定属性时，ORM将会将其转换成对应数据表中的指定数据行、指定 列的操作。  

### 一般的ORM包括以下四部分：  
一个对持久类对象进行CRUD操作的API；  
一个语言或API用来规定与类和类属性相关的查询；  
一个规定mapping metadata的工具；  
一种技术可以让ORM的实现同事务对象一起进行dirty checking, lazy association fetching以及其他的优化操作。  

### 使用ORM的好处  
应用程序不再直接访问底层数据库，而是以面向对象的操作转换成底层的SQL操作。  
就是把持久化对象的保存、修改、删除等操作，转换成对数据库的操作。  

### 解释一下 Django 和 Tornado 的关系、差别  
python web框架分两种, 一种是django 一种是其他, 其他里又分两种, 一种是tornado, 一种是其他  
django最大的特点是大而全, Django的主要目的是简便、快速的开发数据库驱动的网站。它强调代码复用,多个组件可以很方便的以“插件”形式服务于整个框架  
Tornado是异步非阻塞式服务器，速度快。底层基于epoll  

### Django生产环境部署  
Django + Uwsgi（动态请求） + Nginx（静态请求） 实现生产环境部署  
[Django + Uwsgi + Nginx 实现生产环境部署](https://www.cnblogs.com/alex3714/p/6538374.html)  

### Tornado 的核心是什么？  
Tornado 的核心是 ioloop 和 iostream 这两个模块，前者提供了一个高效的 I/O 事件循环，后者则封装了 一个无阻塞的 socket 。通过向 ioloop 中添加网络 I/O 事件，利用无阻塞的 socket ，再搭配相应的回调 函数，便可达到梦寐以求的高效异步执行。  

### 怎么使用Tornado 异步非阻塞  
非阻塞这部分代码主要就在ioloop.py里  
Future对象 代表将来执行或没有执行的任务的结果。  
两大功能:  
1\挂起当前请求,线程可以处理其他请求  
2\如果给future设置值,当前挂起的请求返回并释放  
事件循环  使用 gen.coroutine 装饰器  
生成器  yield future  

  异步非阻塞tornado模型中使用select或者epoll监听用户请求,当接收到用户请求的时候,首先生成一个Future对象,再把这个socket和future存入一个字典；hold住这个请求并把该请求交给相应的函数处理求,当该函数处理完成后会通过回调函数把结果和状态交给future对象, 这时tornado会把future的数据返回给用户,在这整个过程中, tornado程序是非阻塞的.  

### Tornado 异步模式  
当发送GET请求时，由于方法被 @gen.coroutine装饰且yield 一个 Future对象，那么Tornado会等待，  
等待用户向future对象中放置数据或者发送信号，如果获取到数据或信号之后，就开始执行doing方法。  
异步非阻塞体现在当在Tornaod等待用户向future对象中放置数据时，还可以处理其他请求。  
注意：在等待用户向future对象中放置数据或信号时，此连接是不断开的。  

### @gen.coroutine的作用  
gen.coroutine主要是使用协程的方式实现类似异步的处理效果  
它简化异步代码的编写，避免写回调函数，加快开发效率，提高代码可读性，通过结合 pyhton 的 yield 语句实现协程  
通过 @gen.coroutine 修饰的函数返回值变为 Future, 在调用结束的时候会调用  
Future.set_result，这样就会调用与 Future 相关联的回调
