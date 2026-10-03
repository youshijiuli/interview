django内置的权限是在auth组件中实现的，而auth组件又依赖信号、content types、admin组件，所以，我们需要先了解这些组件然后再学习django内置权限的实现机制。



## 1.1 信号

### 1.1.1 自定义信号

- 定义信号

	```python
	import django.dispatch
	
	# 自定义信号
	cut_info_signal = django.dispatch.Signal()
	```

- 注册回调

	```python
	from utils.signals import cut_info_signal
	
	
	def callback_1(sender, **kwargs):
	    print("callback-1")
	
	
	def callback_2(sender, **kwargs):
	    print("callback-2")
	
	
	cut_info_signal.connect(callback_1)
	cut_info_signal.connect(callback_2)
	```

- 触发信号

	```python
	from utils.signals import cut_info_signal
	cut_info_signal.send("demo")
	```

将某些动作都注册在一个信号中，一旦达到条件则触发信号(所有回调都执行)。



### 1.1.2 内置信号

```Python
Model signals
    pre_init                    # django的modal执行其构造方法前，自动触发
    post_init                   # django的modal执行其构造方法后，自动触发
    pre_save                    # django的modal对象保存前，自动触发
    post_save                   # django的modal对象保存后，自动触发
    pre_delete                  # django的modal对象删除前，自动触发
    post_delete                 # django的modal对象删除后，自动触发
    m2m_changed                 # django的modal中使用m2m字段操作第三张表
                                # （add,remove,clear）前后，自动触发
    class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
Management signals
    pre_migrate                 # 执行migrate命令前，自动触发
    post_migrate                # 执行migrate命令后，自动触发
    
Request/response signals
    request_started             # 请求到来前，自动触发
    request_finished            # 请求结束后，自动触发
    got_request_exception       # 请求异常后，自动触发
    
Test signals
    setting_changed             # 使用test测试修改配置文件时，自动触发
    template_rendered           # 使用test测试渲染模板时，自动触发
    
Database Wrappers
    connection_created          # 创建数据库连接时，自动触发
```



- 注册信号回调

	```python
	from django.core.signals import request_finished
	from django.core.signals import request_started
	from django.core.signals import got_request_exception
	
	from django.db.models.signals import class_prepared
	from django.db.models.signals import pre_init, post_init
	from django.db.models.signals import pre_save, post_save
	from django.db.models.signals import pre_delete, post_delete
	from django.db.models.signals import m2m_changed
	from django.db.models.signals import pre_migrate, post_migrate
	
	from django.test.signals import setting_changed
	from django.test.signals import template_rendered
	
	from django.db.backends.signals import connection_created
	
	
	def callback(sender, **kwargs):
	    print("xxoo_callback")
	
	post_save.connect(callback) # 例如:插入一条数据，如何进行日志记录？
	```

- 触发信号

	```python
	from app01 import models
	
	def demo(request):
	    models.NewBB.objects.create(name='v1')
	    return HttpResponse("ok")
	```

	





## 信号



# Django4中的信号

参考：https://www.cnblogs.com/Neeo/articles/17589746.html

内置信号的基本写法，在你的项目同名文件夹下的`__init__.py`

```python
# 导入相关信号
from django.core.signals import request_started, request_finished
# 以装饰器的形式激活信号，所以要先导入装饰器
from django.dispatch import receiver

@receiver(request_started)
def my_callback(sender, **kwargs):
    """ 回调函数 """
    print("my_callback", sender)
```

## 插入基本的orm用法

参考这个：https://www.cnblogs.com/Neeo/articles/10967645.html#orm%E7%AE%80%E4%BB%8B

代码就是，models.py:

```python
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')

    def __str__(self):
        return self.name
```

settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'day07',    		#你的数据库名称
        'USER': 'root',   		#你的数据库用户名
        'PASSWORD': '123', 	#你的数据库密码
        'HOST': '', 			#你的数据库主机，留空默认为localhost
        'PORT': '3306', 		#你的数据库端口
    }
}

# orm语句转为具体SQL的语句配置，你们可以自己在笔记中记录一下
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}
```

注意，别忘了在根目录下打开terminal，执行下面两个命令：

```python
python manage.py makemigrations
python manage.py migrate
```





urls.py

```python
from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
]
```

views.py:

```python
from django.shortcuts import render, HttpResponse
from api.models import User

def index(request):
    # 创建命令
    # obj = User.objects.create(name='zhangkai')
    # print(obj)
    # 更新方式1
    # obj = User.objects.filter(name='zhangkai1').first()
    # obj.name = "zhangkai2"
    # print(obj)
    # obj.save()


    # 更新方式2
    # User.objects.filter(name='zhangkai').update(name="zhangkai3")

    # 删除
    # User.objects.filter(name='zhangkai3').delete()

    # 查询
    User.objects.filter(name='zhangkai3')  # 根据条件查询 相当于select * from api_user where name='zhangaki';
    User.objects.all()  # 查所有，相当于select * from api_user;

    return HttpResponse("INDEX")
```

## 内置信号的用法示例

### 新增模型类对象，触发的相关信号

views.py:

```python
from django.shortcuts import render, HttpResponse
from api.models import User



# ----------- 内置信号的用法 --------------
def index(request):
    # 什么时候模型类对象调用save方法？答案是创建对象的时候，和更新对象的时候
    obj = User.objects.create(name='zhangkai')
    print(obj)



    return HttpResponse("INDEX")
```

`demo/__init__.py`

```python
from django.db.models.signals import pre_init, post_init, pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

@receiver(pre_init)
def pre_init_callback(sender, **kwargs):
    """ 每当实例化一个 Django 模型时，这个信号都会在模型的 __init__() 方法的开头发出 """
    print('pre_init_callback', sender)
    print('pre_init_callback', kwargs)

@receiver(post_init)
def post_init_callback(sender, **kwargs):
    """ 和 pre_init 一样，但这个是在 __init__() 方法完成后发送的 """
    print('post_init_callback', sender)
    print('post_init_callback', kwargs)

@receiver(pre_save)
def pre_save_callback(sender, **kwargs):
    """ 这是在模型的 save() 方法开始时发送的 """
    print('pre_save_callback', sender)
    print('pre_save_callback', kwargs)
    print('pre_save_callback', kwargs['instance'].name)


@receiver(post_save)
def post_save_callback(sender, **kwargs):
    """ 就像 pre_save 一样，但在 save() 方法的最后发送 """
    print('post_save_callback', sender)
    print('post_save_callback', kwargs)
    print('post_save_callback', kwargs['instance'].name)
```

以及，打印效果：

```bash
pre_init_callback <class 'api.models.User'>
pre_init_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000159F5287DC0>, 'args': (), 'kwargs': {'name': 'zhangkai'}}
post_init_callback <class 'api.models.User'>
post_init_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000159F5287EE0>, 'instance': <User: zhangkai>}
pre_save_callback <class 'api.models.User'>
pre_save_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000159F5287FD0>, 'instance': <User: zhangkai>, 'raw': False, 'using': 'default', 'update_fields': None}
pre_save_callback zhangkai
post_save_callback <class 'api.models.User'>
post_save_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000159F52C4100>, 'instance': <User: zhangkai>, 'created': True, 'update_fields': None, 'raw': False, 'using': 'default'}
post_save_callback zhangkai
zhangkai
```

### 编辑模型类对象，触发的相关信号

`views.py`:

```python
from django.shortcuts import render, HttpResponse
from api.models import User

# ----------- 内置信号的用法 --------------
def index(request):
    # 什么时候模型类对象调用save方法？答案是创建对象的时候，和更新对象的时候
    # 新增
    # obj = User.objects.create(name='zhangkai')
    # print(obj)

    # 编辑
    obj = User.objects.filter(name='zhangkai2').first()
    old = obj.name
    obj.name = "zhangkai888"
    new = obj.name
    # log.info(f'{old}-->{new}')
    obj.save()

    return HttpResponse("INDEX")
```

`demo/__init__.py`：

```python
from django.db.models.signals import pre_init, post_init, pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

@receiver(pre_init)
def pre_init_callback(sender, **kwargs):
    """ 每当实例化一个 Django 模型时，这个信号都会在模型的 __init__() 方法的开头发出 """
    print('pre_init_callback', sender)
    print('pre_init_callback', kwargs)


@receiver(post_init)
def post_init_callback(sender, **kwargs):
    """ 和 pre_init 一样，但这个是在 __init__() 方法完成后发送的 """
    print('post_init_callback', sender)
    print('post_init_callback', kwargs)


@receiver(pre_save)
def pre_save_callback(sender, **kwargs):
    """ 这是在模型的 save() 方法开始时发送的 """
    print('pre_save_callback', sender)
    print('pre_save_callback', kwargs)
    print('pre_save_callback', kwargs['instance'].name)


@receiver(post_save)
def post_save_callback(sender, **kwargs):
    """ 就像 pre_save 一样，但在 save() 方法的最后发送 """
    print('post_save_callback', sender)
    print('post_save_callback', kwargs)
    print('post_save_callback', kwargs['instance'].name)
```

日志：

```bash
pre_init_callback <class 'api.models.User'>
pre_init_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000186F4937DC0>, 'args': (1, 'zhangkai2'), 'kwargs': {}}
post_init_callback <class 'api.models.User'>
post_init_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000186F4937EE0>, 'instance': <User: zhangkai2>}
zhangkai2
pre_save_callback <class 'api.models.User'>
pre_save_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000186F4937FD0>, 'instance': <User: zhangkai888>, 'raw': False, 'using': 'default', 'update_fields': None}
pre_save_callback zhangkai888
post_save_callback <class 'api.models.User'>
post_save_callback {'signal': <django.db.models.signals.ModelSignal object at 0x00000186F4974100>, 'instance': <User: zhangkai888>, 'created': False, 'update_fields': None, 'raw': False, 'using': 'default'}
post_save_callback zhangkai888
```



### 删除模型类对象，触发的相关信号

`views.py`:

```python
from django.shortcuts import render, HttpResponse
from api.models import User



# ----------- 内置信号的用法 --------------

def index(request):
    # 什么时候模型类对象调用save方法？答案是创建对象的时候，和更新对象的时候
    # 新增
    # obj = User.objects.create(name='zhangkai')
    # print(obj)

    # 编辑
    # obj = User.objects.filter(name='zhangkai2').first()
    # old = obj.name
    # obj.name = "zhangkai888"
    # new = obj.name
    # # log.info(f'{old}-->{new}')
    # obj.save()

    # 删除
    obj_list = User.objects.filter(name='zhangkai888')
    # print(111, obj_list)  # <QuerySet [<User: zhangkai888>, <User: zhangkai888>, <User: zhangkai888>]>
    for obj in obj_list:
        obj.delete()

    return HttpResponse("INDEX")
```

`demo/__init__.py`：

```python
from django.db.models.signals import pre_init, post_init, pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

@receiver(pre_init)
def pre_init_callback(sender, **kwargs):
    """ 每当实例化一个 Django 模型时，这个信号都会在模型的 __init__() 方法的开头发出 """
    print('pre_init_callback', sender)
    print('pre_init_callback', kwargs)


@receiver(post_init)
def post_init_callback(sender, **kwargs):
    """ 和 pre_init 一样，但这个是在 __init__() 方法完成后发送的 """
    print('post_init_callback', sender)
    print('post_init_callback', kwargs)





@receiver(pre_save)
def pre_save_callback(sender, **kwargs):
    """ 这是在模型的 save() 方法开始时发送的 """
    print('pre_save_callback', sender)
    print('pre_save_callback', kwargs)
    print('pre_save_callback', kwargs['instance'].name)


@receiver(post_save)
def post_save_callback(sender, **kwargs):
    """ 就像 pre_save 一样，但在 save() 方法的最后发送 """
    print('post_save_callback', sender)
    print('post_save_callback', kwargs)
    print('post_save_callback', kwargs['instance'].name)


@receiver(pre_delete)
def pre_delete_callback(sender, **kwargs):
    """ 在模型的 delete() 方法和查询集的 delete() 方法开始时发送 """
    print('pre_delete_callback', sender)
    print('pre_delete_callback', kwargs)


@receiver(post_delete)
def post_delete_callback(sender, **kwargs):
    """ 就像 pre_delete 一样，但在模型的 delete() 方法和查询集的 delete() 方法结束时发送 """
    print('post_delete_callback', sender)
    print('post_delete_callback', kwargs)
```

日志：

```bash
post_init_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD6FE7EE0>, 'instance': <User: zhangkai888>}
pre_delete_callback <class 'api.models.User'>
pre_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70241F0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
post_delete_callback <class 'api.models.User'>
post_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70242E0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
pre_delete_callback <class 'api.models.User'>
pre_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70241F0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
post_delete_callback <class 'api.models.User'>
post_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70242E0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
pre_delete_callback <class 'api.models.User'>
pre_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70241F0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
post_delete_callback <class 'api.models.User'>
post_delete_callback {'signal': <django.db.models.signals.ModelSignal object at 0x0000026FD70242E0>, 'instance': <User: zhangkai888>, 'using': 'default', 'origin': <User: zhangkai888>}
```



