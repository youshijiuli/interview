# 信号机制



django自带一套信号机制来帮助我们在框架的不同位置之间传递信息。也就是说，当某一事件发生时，信号系统可以允许一个或多个发送者（senders）将通知或信号（signals）发送给一组接受者（receivers）。

信号系统包含以下三要素：

* 发送者－信号的发出方

* 信号－信号本身

* 接收者－信号的接受者

Django内置了一整套信号，下面是一些比较常用的：

* django.db.models.signals.pre_save & django.db.models.signals.post_save

`post_save`在ORM模型的save()方法调用之前或之后发送信号

* django.db.models.signals.pre_delete & django.db.models.signals.post_delete

`post_delete`在ORM模型或查询集的delete()方法调用之前或之后发送信号。

* django.db.models.signals.m2m_changed

`m2m_changed`当多对多字段被修改时发送信号。

* django.core.signals.request_started & django.core.signals.request_finished

`request_finished`当接收和关闭HTTP请求时发送信号。

## 一、监听信号

要接收信号，请使用`Signal.connect()`方法注册一个接收器。当信号发送后，会调用这个接收器。

方法原型：

    Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)

参数：

    receiver ：当前信号连接的回调函数，也就是处理信号的函数。 
    sender ：监听从哪个发送方发来的信号。 
    weak ： 是否弱引用
    dispatch_uid ：信号接收器的唯一标识符，以防信号多次发送。 


下面以如何接收每次HTTP请求结束后发送的信号为例，连接到Django内置的`request_finished`信号。

### 1. 编写接收器

接收器其实就是一个Python函数或者方法：

```python
def my_callback(sender, **kwargs):
    print("Request finished!")
```

请注意，所有的接收器都必须接收一个sender参数和一个`**kwargs`通配符参数。

### 2. 连接信号

其实就是监听信号。有两种方法可以连接信号，一种是下面的手动方式：

```python
from django.core.signals import request_finished

request_finished.connect(my_callback)
```

另一种是使用receiver()装饰器：

```python
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```

### 3. 接收特定发送者的信号

一个信号接收器，通常不需要接收所有的信号，只需要接收特定发送者发来的信号，所以需要在sender参数中，指定发送方。下面的例子，只接收MyModel模型的实例保存前的信号。

```python
from django.db.models.signals import pre_save   # 另外一个内置的常用信号
from django.dispatch import receiver
from myapp.models import MyModel


@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs):
    ...
```

`my_handler`函数只在MyModel实例保存时被调用。


### 4. 防止重复信号


为了防止重复信号，可以设置`dispatch_uid`参数来标识你的接收器，标识符通常是一个字符串，如下所示： 

```python
from django.core.signals import request_finished

request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
```

最后的结果是，对于每个唯一的`dispatch_uid`值，你的接收器都只绑定到信号一次。


## 二、自定义信号

除了Django为我们提供的内置信号（比如前面列举的那些），很多时候，我们需要自己定义信号。

所有的信号都是`django.dispatch.Signal`的实例。

下面定义了一个新信号：

```python
import django.dispatch

pizza_done = django.dispatch.Signal()
```


## 三、发送信号


Django中有两种方法用于发送信号。

- Signal.send(sender, **kwargs)

或者

- Signal.send_robust（sender，** kwargs）


必须提供sender参数（大部分情况下是一个类名），并且可以提供任意数量的其他关键字参数。

例如，这样来发送前面的`pizza_done`信号：

```python
class PizzaStore(object):
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
        ...
```

`send()`和`send_robust()`返回一个元组对的列表`[（receiver, response）， ... ]`，表示接收器和响应值二元元组的列表。

## 四、断开信号

    Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)

`Signal.disconnect()`用来断开信号的接收器，和`Signal.connect()`中的参数相同。如果接收器成功断开，返回True，否则返回False。


## 五、信号实例

信号可能不太好理解，下面我在Django内编写一个例子示范一下：

首先在根URLCONF中写一条路由：

```python
from django.urls import path
from django.contrib import admin
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signal/', views.create_signal),
]
```

这个很好理解，我在项目里创建了一个app1应用，在它的views.py中创建了一个create_signal视图，通过`/signal/`可以访问这个视图。这些都不重要，随便配置，只要能正常工作就行。

然后在views.py中自定义一个信号，以及创建create_signal视图：

```python
from django.shortcuts import HttpResponse
import time
import django.dispatch
from django.dispatch import receiver

# 定义一个信号
work_done = django.dispatch.Signal()


def create_signal(request):
    url_path = request.path
    print("我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。")

    # 发送信号，将请求的url地址和时间一并传递过去
    work_done.send(create_signal, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))
    return HttpResponse("200,ok")
```

自定义的信号名叫`work_done`。

`create_signal`视图内，获取请求的url，生成请求的时间，作为参数，传递到send方法。

这样，我们就发送了一个信号。

然后，再写一个接收器：

```python
@receiver(work_done, sender=create_signal)
def my_callback(sender, **kwargs):
    print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))
```

通过装饰器注册为接收器。内部接收字典参数，并解析打印出来。

最终views.py文件如下：

```python
from django.shortcuts import HttpResponse
import time
import django.dispatch
from django.dispatch import receiver

# Create your views here.

# 定义一个信号
work_done = django.dispatch.Signal()


def create_signal(request):
    url_path = request.path
    print("我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。")

    # 发送信号，将请求的IP地址和时间一并传递过去
    work_done.send(create_signal, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))
    return HttpResponse("200,ok")


@receiver(work_done, sender=create_signal)
def my_callback(sender, **kwargs):
    print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))
```

现在可以来测试一下。python manage.py runserver启动服务器。浏览器中访问`http://127.0.0.1:8000/signal/`。重点不再浏览器的返回，而在后台返回的内容：

    我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。
    我在2017-12-18 17:10:12时间收到来自<function create_signal at 0x0000000003AFF840>的信号，请求url为/signal/


这些提示信息，可以在Pycharm中看到，或者在命令行环境中看到。