# Django日志配置

首先，学习Python的logging模块知识：https://www.liujiangblog.com/course/python/71

Django在Python内置的logging模块基础上拓展除了它自己的日志系统。


在Python的logging模块中，主要包含下面四大金刚：

* Loggers： 记录器
* Handlers：处理器
* Filters： 过滤器
* Formatters： 格式化器

> #### Loggers
>
> logger 是日志系统的入口。每个 logger 都是命名了的 bucket， 消息写入 bucket 以便进一步处理。
>
> logger 可以配置 *日志级别*。日志级别描述了由该 logger 处理的消息的严重性。Python 定义了下面几种日志级别：
>
> - `DEBUG`：排查故障时使用的低级别系统信息
> - `INFO`：一般的系统信息
> - `WARNING`：描述系统发生了一些小问题的信息
> - `ERROR`：描述系统发生了大问题的信息
> - `CRITICAL`：描述系统发生严重问题的信息
>
> 每一条写入 logger 的消息都是一条 *日志记录*。每一条日志记录也包含 *日志级别*，代表对应消息的严重程度。日志记录还包含有用的元数据，来描述被记录的事件细节，例如堆栈跟踪或者错误码。
>
> 当 logger 处理一条消息时，会将自己的日志级别和这条消息的日志级别做对比。**如果消息的日志级别匹配或者高于 logger 的日志级别，它就会被进一步处理。否则这条消息就会被忽略掉。**
>
> 当 logger 确定了一条消息需要处理之后，会把它传给 *Handler*。
>
> 
>
> #### Handlers
>
> Handler 是决定如何处理 logger 中每一条消息的引擎。它描述特定的日志行为，比如把消息输出到屏幕、文件或网络 socket。
>
> 和 logger 一样，handler 也有日志级别的概念。如果一条日志记录的级别不匹配或者低于 handler 的日志级别，对应的消息会被 handler 忽略。
>
> 一个 logger 可以有多个 handler，每一个 handler 可以有不同的日志级别。这样就可以根据消息的重要性不同，来提供不同格式的输出。例如，你可以添加一个 handler 把 `ERROR` 和 `CRITICAL` 消息发到寻呼机，再添加另一个 handler 把所有的消息（包括 `ERROR` 和 `CRITICAL` 消息）保存到文件里以便日后分析。
>
> 
>
> #### 过滤器
>
> 在日志从 logger 传到 handler 的过程中，使用 Filter 来做额外的控制。
>
> 默认情况下，只要级别匹配，任何日志消息都会被处理。不过，也可以通过添加 filter 来给日志处理的过程增加额外条件。例如，可以添加一个 filter 只允许某个特定来源的 `ERROR` 消息输出。
>
> Filter 还被用来在日志输出之前对日志记录做修改。例如，可以写一个 filter，当满足一定条件时，把日志记录从 `ERROR` 降到 `WARNING` 级别。
>
> Filter 在 logger 和 handler 中都可以添加；多个 filter 可以链接起来使用，来做多重过滤操作。
>
> 
>
> #### Formatters
>
> 日志记录最终是需要以文本来呈现的。Formatter 描述了文本的格式。一个 formatter 通常由包含 LogRecord attributes 的 Python 格式化字符串组成，不过你也可以为特定的格式来配置自定义的 formatter。具体的格式化设定参考:https://docs.python.org/3/library/logging.html#logrecord-attributes

## 一、在Django视图中使用logging

使用方法非常简单，如下例所示：

```python
# 导入的是基于Python的内置logging库
import logging

# 获取一个默认的logger对象
logger = logging.getLogger(__name__)

def my_view(request, arg1, arg):
    ...
    if bad_mojo:
        # 记录一个错误日志
        logger.error('Something went wrong!')
        
        
# 对于类视图
class PublisherDetail(DetailView):

    model = Publisher
    context_object_name = 'publisher'
    template_name = 'app/my_detail.html'
	
    # 重写get方法
    def get(self,*args,**kwargs):
        logger.warning('有人在访问publisher！')
        return super().get(self,*args, **kwargs)
```

每满足`bad_mojo`条件一次，就写入一条错误日志。

实际上，logger对象有下面几个内置方法：

* logger.debug()
* logger.info()
* logger.warning()
* logger.error()
* logger.critical()
* `logger.log()`：手动输出一条指定日志级别的日志消息。(上面五种方法的基础版)
* `logger.exception()`：创建一个包含当前异常堆栈帧的 `ERROR` 级别日志消息。

### 为logger命名

调用`logging.getLogger()`会获取或创建一个logger的实例。不同的logger实例用名字来区分。这个名字是为了在配置日志的时候区分它用于哪个logger。

按照常规，logger的名字通常是该logger所在的Python模块的名字，即 `__name__`。这样可以基于模块来过滤和处理日志请求。不过，如果你有其他的方式来组织你的日志消息，可以为logger提供点号分割的名字来标识它：

```python
# Get an instance of a specific named logger
logger1 = logging.getLogger('project.interesting.stuff')
logger2 = logging.getLogger('project.interesting')
logger3 = logging.getLogger('project')
```

这种圆点路径的logger表示法被视作一种继承关系。`project.interesting`logger是`project.interesting.stuff`logger的父亲；而`project`logger则是`project.interesting`logger的父亲。

为什么设计这种父子层次的树形结构？为的是将子logger的动作向上传播给父logger。这样，你可以在记录器树的根节点定义一组单独的处理程序，并在记录器的子树中捕获所有记录调用。在`project`命名空间中定义的记录器可以同时捕获在`project.interesting`和`project.interesting.stuff`记录器上产生的所有日志动作。

如果你不希望某个logger传播日志给上级，可以单独关闭它，使用propagate属性。

## 二、在Django中配置logging

通常，只是像上面的例子那样简单的使用logging模块是远远不够的，我们一般都要对logging的四大金刚进行一定的配置。

Python和Django都推荐使用字典类型的配置方式，也就是dictConfig。

将配置字典放入项目的settings.py模块中即可。

注意，除了数字、布尔值、列表等情况，键值对都是字符串形式，各种类也不需要额外导入，直接写圆点路径。

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

实际上Python的logging模块提供了好几种配置方式。

**例一，将日志保存到文件中，注意要确保运行Django程序的用户在文件路径上具有写的权力：**


```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

如果你使用上面的样例，请确保Django用户对'filename'对应目录和文件的写入权限。

**例二：**下面这个示例配置的粒度更细，让Django将日志打印到控制台，通常用做开发期间的信息展示。

```python
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```

当配置有多个logger的时候，如下使用：

```python
import logging
django_logger = logging.getLogger('django')
root_logger = logging.getLogger('root')

class PublisherDetail(DetailView):

    model = Publisher
    context_object_name = 'publisher'
    template_name = 'app/my_detail.html'

    def get(self,*args,**kwargs):
        django_logger.warning('有人在访问publisher！')
        root_logger.info('root info')
        return super().get(self,*args, **kwargs)
```

**例三：**下面是一个相当复杂的logging配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}
```

上面的logging配置主要定义了这么几件事情：

* 定义了配置文件的版本，当前版本号为1.0
* 定义了两个formatter：simple和format，分别表示两种文本格式。
* 定义了两个过滤器：SpecialFilter和RequireDebugTrue
* 定义了两个处理器：console和mail_admins
* 配置了三个logger：'django'、'django.request'和'myproject.custom'
* 注意`django.request`logger的propagate属性设为False，这表示它发送邮件后，不会将日志动作传播到它的父亲`django`logger去。

具体的配置含义如下：

### 配置选项

'version'： 版本号

'disable_existing_loggers'：是否关闭默认的日志记录器，默认False。如果设置为True，要小心。

args： 传递位置参数

kwargs：传递命名参数，键值对

root：默认的日志记录器

func：回调函数

loggers:

* handlers: 处理器的列表
* filter：过滤器列表
* level：日志级别
* propagate:布尔值。决定是否向上传播到父记录器。

handlers：

* class：一个处理器类
* filename：使用文件处理器时，指定保存日志的文件
* level：日志级别
* filters：过滤器类列表
* formatter：一个格式化器
* email_backend：邮件处理器的邮件后端
* stream：流管道，比如`ext://sys.stdout`,`ext://sys.stderr`

formatters：

* format： 文本格式
* style：格式化文本的分隔符的样式，默认为百分符号，可选`{`，`$`等

filters：

* （）：指定自定义的类型
* foo：bar，传递参数

### 默认的日志配置

默认情况下，Django对日志进行了如下默认配置，也就是为啥我们什么都没做，但是还能看见警告信息的来源：

当`DEBUG=True`时：

一个名为`django`的logger将发送所有`INFO`级别及以上的信息到控制台，包括它的子孙后代logger的信息（django.server除外）

当`DEBUG=False`时：

一个名为`django`的logger将发送所有`ERROR`及以`CRITICAL`的信息到`AdminEmailHandler`，包括它的子孙后代logger的信息（django.server除外）。也就是说给管理员发一封邮件。

无论DEBUG怎么设定，`django`logger都将发送`INFO`级别及以上的信息到控制台。

除`django.server`以外的所有记录器都将日志记录传播给其父目录，直至根`django`记录器。根`django`记录器配置了`console`和`mail_admins`处理器。

下面是默认配置的源代码，它位于`django.utils.log`模块中：

```python
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```

### 关闭日志配置

如果你不想使用Django默认的日志配置，可以设置`LOGGING_CONFIG = None`。但这不是说关闭了logging功能，只是关闭了Django的自动记录器，你完全可以自己手动指定一个配置：

```python
# settings.py

LOGGING_CONFIG = None

import logging.config
logging.config.dictConfig(...)
```



## 三、Django对logging模块的扩展

Django对logging模块进行了一定的扩展，用来满足Web服务器专门的日志记录需求。

他们都位于`django.utils.log`模块，通常，你不需要直接导入他们，而是在dictConfig配置字典中直接引用即可。

### 1. 记录器 Loggers

Django额外提供了几个其内建的logger。

* django： 不要直接使用这个记录器，用下面的。这是一个汇总的记录器，^-^
* django.request： 记录与处理请求相关的日志消息。5XX错误被记录为`ERROR`消息；4XX错误记录为`WARNING`消息。接收额外参数：`status_code`和`request`
* django.server： 记录runserver命令启动的开发服务器在处理请求时的日志消息。只用于开发阶段。5XX错误被记录为`ERROR`消息；4XX错误记录为`WARNING`消息。其它的都是INFO级别。接收额外参数：`status_code`和`request`。
* django.template: 记录与渲染模板相关的日志。缺少上下文变量将记录为DEBUG级别的日志。
* django.db.backends: 与数据库交互的代码相关的消息。默认都是DEBUG级别。出于性能方面的考虑，仅在`settings.DEBUG=True`时才启用SQL日志记录。
* `django.security.*`：

security记录器将在抛出`SuspiciousOperation`异常以及其他与安全相关的错误时记录日志 。每个安全性错误子类型都有一个子记录器。日志事件的级别取决于处理异常的位置。大多数事件都记录为warning，而到达WSGI处理程序的任何`SuspiciousOperation`事件都将记录为ERROR。例如，当一个黑名单主机访问服务器时，Django将返回400响应，并且将ERROR日志记录到 `django.security.DisallowedHost`记录器中。

默认情况下，这些日志事件将传播到祖先`django`记录器，该记录器在`DEBUG=False`时将ERROR日志邮件发送给管理员。

* django.security.csrf： 记录CSRF验证失败日志。
* django.db.backends.schema： 记录查询导致数据库修改的日志。 

对于这些logger，直接在代码里通过类似`django_request_logger = logging.getLogger('django.request')`的方式获取。


### 2. 处理器 Handlers

Django额外提供了一个handler，也就是`AdminEmailHandler`。这个处理器将它收到的每个日志信息用邮件发送给站点管理员。

```
class AdminEmailHandler(include_html=False, email_backend=None, reporter_class=None)
```

如果`AdminEmailHandler`包含`request`属性，则请求的完整详细信息将包含在电子邮件中。如果客户的IP地址在`INTERNAL_IPS`设置中，则电子邮件主题将包含短语“内部IP” ；如果没有，它将包括“ EXTERNAL IP”。

如果日志记录包含堆栈跟踪信息，则该堆栈跟踪将包含在电子邮件中。

`AdminEmailHandler`的`include_html`参数用于控制回溯电子邮件是否包含HTML附件，该附件包含调试Web页面的完整内容（如果`DEBUG`为True则应生成的内容）。要在您的配置中设置此值，请将其包含在`django.utils.log.AdminEmailHandler`的配置字典中，如下所示：

```python
'handlers': {
    'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'include_html': True,
    }
},
```

还可以指定处理器使用的邮件发送后端，否则会使用 `EMAIL_BACKEND`指定的默认后端 ：

```python
'handlers': {
    'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'email_backend': 'django.core.mail.backends.filebased.EmailBackend',
    }
},
```



### 3. 过滤器Filters

Django还额外提供几个过滤器。

* CallbackFilter(callback)

  这个过滤器接受一个回调函数，并对每个传递给过滤器的日志调用它。如果回调函数返回False，将不会进行日志的处理。

  例如，要过滤掉`UnreadablePostError`错误，你可以这么写过滤器：

  ```python
  from django.http import UnreadablePostError
  
  def skip_unreadable_post(record):
      if record.exc_info:
          exc_type, exc_value = record.exc_info[:2]
          if isinstance(exc_value, UnreadablePostError):
              return False
      return True
  ```

  然后，将它用在配置字典中：

  ```python
  'filters': {
      'skip_unreadable_posts': {
          '()': 'django.utils.log.CallbackFilter',
          'callback': skip_unreadable_post,
      }
  },
  'handlers': {
      'mail_admins': {
          'level': 'ERROR',
          'filters': ['skip_unreadable_posts'],
          'class': 'django.utils.log.AdminEmailHandler'
      }
  },
  ```

  

* RequireDebugFalse： 这个过滤器只会在`settings.DEBUG==False`时通过检查。也就是说要在生产环境下，才通过过滤。比如：

  ```python
  'filters': {
      'require_debug_false': {
          '()': 'django.utils.log.RequireDebugFalse',
      }
  },
  'handlers': {
      'mail_admins': {
          'level': 'ERROR',
          'filters': ['require_debug_false'],
          'class': 'django.utils.log.AdminEmailHandler'
      }
  },
  ```

  

* **RequireDebugTrue** 

  和上面的正好相反，要求是开发环境。

## 四、自定义Filter

Filter类：

```python
import logging

class Start_with_django(logging.Filter):
    def filter(self, record):
        if record.msg.startswith('django'):
            return True
        else:
            return False
```

配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters':{
        'start_with_django':{
            '()':'path.to.Start_with_django',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'my_debug.log',
        },
        'sh':{
            'class':'logging.StreamHandler',
            'level':'INFO',
            'filters':['start_with_django',],
        }
    },
    'loggers': {
        'my': {
            'handlers': ['sh'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

测试：

```python
import logging


my_logger = logging.getLogger('my')


def logger_test(request):
    my_logger.error('这是来自my记录器的日志')
    my_logger.info('这是来自my记录器的日志')
    my_logger.info('django这是来自my记录器的日志')
    return HttpResponse('200,ok')
```