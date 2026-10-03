接触Django一段时间后的，你会知道如何添加并使用静态文件，也大概知道如何配置静态url和静态文件路径。

但你知道这一切功能是怎么来的么？

你或许会说，不就是Django自带的核心功能么？

错了，其实是一个叫做`staticfiles` 的应用带来的，它作为Django的contrib的一个内置应用，和admin、auth、message、session是一个level的，同样被默认加入了`INSTALLED_APPS`中。

> Django的settings.py配置文件中隐藏着太多的秘密，尤其是`INSTALLED_APPS`和`MIDDLEWARE`。

`staticfiles` 应用负责将每个应用中的静态文件收集到指定的位置用于生产环境使用。

## 可配置项

- `STATIC_ROOT`：收集后，放置静态文件的目录。比如`product_statics`，`"/var/www/example.com/static/"`
- `STATIC_URL`： 用于访问静态文件的URL。比如`'/static/'`
- `STATICFILES_DIRS`：全局性的静态文件目录。比如`statics`
- `STATICFILES_STORAGE`： 指定静态文件储存器。通常保持默认。
- `STATICFILES_FINDERS`：指定静态文件查找器。通常保持默认。

## 管理命令

`staticfiles` 应用给我们提供了三个管理命令，通过python manage.py或者django-admin调用。

### collectstatic

将所有app中的静态文件复制收集到`STATIC_ROOT`中。

对应重名的文件，第一个被查找到的被使用，所以平时要注意规范的目录结构和命名。

多次运行collectstatic命令，如果发现新的静态文件的时间戳比`STATIC_ROOT`中同名文件的时间戳更新，就拷贝覆盖，否则跳过。另外，如果你从`INSTALLED_APPS`中移除了某个app，可以使用 `collectstatic --clear` 方法，将该app的静态文件也清理一下。

默认先从`STATICFILES_DIRS`定义的全局静态目录收集文件，然后是各个注册了的app内部的`static`目录收集。

默认情况下，收集的文件接收`FILE_UPLOAD_PERMISSIONS`指定的权限，收集目录接收`FILE_UPLOAD_DIRECTORY_PERMISSIONS`指定的权限。如果你想要指定不同的权限，可以继承静态文件储存类，然后指定相应的属性值，如下所示：

```python
from django.contrib.staticfiles import storage

class MyStaticFilesStorage(storage.StaticFilesStorage):
    def __init__(self, *args, **kwargs):
        kwargs['file_permissions_mode'] = 0o640
        kwargs['directory_permissions_mode'] = 0o760
        super().__init__(*args, **kwargs)
```

然后将配置项`STATICFILES_STORAGE`指定为`'path.to.MyStaticFilesStorage'`。

collectstatic命令可以使用的一些通用选项如下：

* --noinput

   不要提示用户进行任何形式的输入。

* --ignore PATTERN

  忽略匹配此glob模式的文件，目录或路径。使用多次，忽略更多。指定路径时，即使在Windows上也请始终使用正斜杠。

- --dry-run

  除修改文件系统外，执行所有操作。

- --clear

  尝试复制或链接原始文件之前，请清除现有文件。

- --link

  创建到每个文件的符号链接，而不是复制。

- --no-post-process

  不要调用已配置的`STATICFILES_STORAGE`存储后端的`post_process()`方法。

- --no-default-ignore

  不要忽视`'CVS'`，`'.*'` 和`'*~'`等符号。

执行`python manage.py collectstatic --help`获取更多帮助信息

### findstatic

在相关的目录里搜索指定的静态文件。比如：

```python
$ python manage.py findstatic css/base.css admin/js/core.js
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Found 'admin/js/core.js' here:
  /home/polls.com/src/django/contrib/admin/media/js/core.js
```

默认情况下，所有匹配的对象都会列出，使用first参数，可以只显示第一个被搜索到的对象，着对于debug非常有帮助，因为Django静态文件只收集第一个匹配到的对象，所以你可以看到collectstatic到底收集了哪些文件：

```python
$ python manage.py findstatic css/base.css --first
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
```

通过将`--verbosity`标志设置为0，可以抑制多余的输出，而只获取路径名：

```python
$ python manage.py findstatic css/base.css --verbosity 0
/home/special.polls.com/core/static/css/base.css
/home/polls.com/core/static/css/base.css
```

通过将`--verbosity`标志设置为2，可以获取搜索到的所有目录：

```python
$ python manage.py findstatic css/base.css --verbosity 2
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Looking in the following locations:
  /home/special.polls.com/core/static
  /home/polls.com/core/static
  /some/other/path/static
```

### runserver

你没有看错！

实际上，如果你在`INSTALLED_APPS`中注册了`staticfiles`应用，那么`staticfiles`应用自带的`runserver`命令会覆盖Django本身的runserver命令，从而提供静态文件访问服务。所以，我们大多数情况下，使用的都是这个加强版的runserver。

它有两个额外的选项：

* --nostatic

  强制关闭静态文件服务（脱裤子放屁，自己先提供，现在又关闭）

  ```
  django-admin runserver --nostatic
  ```

* --insecure

  在DEBUG为False的情况下，强制提供静态文件服务。（谜之用途。生产环境下我用你？）

  ```
  django-admin runserver --insecure
  ```

## Storages

所谓的Storage，就是如何将静态文件储存到某个位置，或提供URL访问的读写工具。它们都是 `FileSystemStorage`的子类。

staticfiles应用内置了两个储存类：

- `StaticFilesStorage`：主要使用的类。
- `ManifestStaticFilesStorage`：上面的子类。只是多了一个MD5哈希码的功能。它会将原文件的哈希码附加到文件名后面，比如`css/styles.css` 会变成 `css/styles.55e7cbb9ba48.css`。

关于Storages，知道基本情况即可，要做更多的深度定制其实相当于修改Django源码了



## Finders

storages负责存储文件，Finder则负责查找出要保存的静态文件。

每个finder都有一个searched_locations属性，包含了要搜索的路径列表：

```python
from django.contrib.staticfiles import finders

result = finders.find('css/base.css')
searched_locations = finders.searched_locations
```

本质上：finder玩弄的是文件和路径回归搜索，storage玩弄的是文件的读写。

## serve视图

我们都知道，在DEBUG为True的开发模式下，runserver这个简易开发服务器可以提供静态文件访问服务。那么这是怎么实现的呢？

实际上在`django.contrib.statifiles.views`模块中，有个serve方法，这个方法在后台调用了`django.views.static.serve`方法（前面视图章节介绍过）。我们可以看看它的源代码：

```python
# django.contrib.statifiles.views

import os
import posixpath

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import Http404
from django.views import static

def serve(request, path, insecure=False, **kwargs):
    if not settings.DEBUG and not insecure:
        raise Http404
    normalized_path = posixpath.normpath(path).lstrip('/')
    absolute_path = finders.find(normalized_path)
    if not absolute_path:
        if path.endswith('/') or path == '':
            raise Http404("Directory indexes are not allowed here.")
        raise Http404("'%s' could not be found" % path)
    document_root, path = os.path.split(absolute_path)
    return static.serve(request, path, document_root=document_root, **kwargs)
```

默认情况下，runserver命令会自动配置访问静态文件的URLconf。

如果你定义了不同的本地开发服务器，你就需要显式地配置URLconf了：

```python
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]
```

注意，开头的`'static'`要和你的`STATIC_URL`配置一致。

## 管理静态文件

本节进行静态文件的综述，查遗补漏，可能有重复的内容。

### 配置静态文件

1. 确保 `INSTALLED_APPS` 包含了 `django.contrib.staticfiles`。

1. 在配置文件中，定义 `STATIC_URL`，例子:

   ```
   STATIC_URL = '/static/'
   ```

1. 在模板中，用 `static` 为给定的相对路径构建 URL。

   ```
   {% load static %}
   <img src="{% static "my_app/example.jpg" %}" alt="My image">
   ```

1. 将你的静态文件保存至程序中名为 `static` 的目录中。例如 `my_app/static/my_app/example.jpg`。

> 开发项目时，当使用 了`django.contrib.staticfiles`，会在 `DEBUG=True` 的情况下由 `runserver` 自动提供静态文件访问服务（参考 `django.contrib.staticfiles.views.serve()`）。但该方法 **极度低效** 且 **不怎么安全**，所以这 **不适合生产环境**。

你的工程可能包含未与任何应用绑定的静态资源，比如base.html。除了在 apps 中使用 `static/` 目录，你可以在配置文件中定义一个目录列表 (`STATICFILES_DIRS`) ，Django 会从中寻找静态文件:

```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]
```

### 开发时提供静态文件服务

若你未在 `INSTALLED_APPS` 中注册 `django.contrib.staticfiles`，你仍能手动通过 `django.views.static.serve()` 为静态文件提供服务。但这不适合生产环境！

例如，若 `STATIC_URL` 为 `/static/`，你能通过添加以下代码片段至 urls.py 完成目的:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

该方法只能在 debug 模式下生效，且要求域名是本地localhost的（例如 `localhost:8000/static/`），不是一个 外部URL (例如 `http://static.example.com/`)。

并且只为实际的 `STATIC_ROOT` 目录提供服务；它不会像 `django.contrib.staticfiles` 一样搜索静态文件。

### 开发期间保存用户上传的文件

开发期间，你能用 `django.views.static.serve()` 视图为用户上传的媒体文件提供服务。但这不适合生产环境！

例如，若 `MEDIA_URL` 定义为 `/media/`，你可以通过将以下代码片段加入 urls.py 实现目的:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

该方法只能在 debug 模式下生效，且要求域名是本地localhost的（例如 `localhost:8000/media/`），不是一个 外部URL (例如 `http://static.example.com/`)。

## 部署静态文件

### 在同一服务器同时提供Web和静态文件服务

操作步骤类似这样：

- 将代码推送至部署服务器。
- 在服务器上运行 `collectstatic`，将所有的静态文件拷贝至 `STATIC_ROOT`。
- 配置 Web 服务器，使其在 `STATIC_URL` 下为 `STATIC_ROOT` 目录下的文件提供静态文件服务。

### 使用专用服务器提供静态文件服务

大多数大型 Django 站点使用一个独立的 Web 服务器——即，该服务器并未运行 Django，只提供静态文件服务。这种服务器一般运行一种不同的 Web 服务器——更快，更简单。常见选项如下：

- Nginx
- 一个 Apache 的精简版本

如何配置这些服务器超出了本文范围；查阅这些服务器各自的文档获取介绍。

由于静态文件服务器并不运行 Django，你需要将部署策略改成这样：

- 当静态文件改变时，本地运行 `collectstatic`。
- 将本地 `STATIC_ROOT` 推送到静态文件服务器提供服务的目录。 推荐使用rsync工具，因为它可以只传输文件修改部分的数据。

### 从云服务或 CDN 提供静态文件服务

另一种常见的策略是从类似阿里云的云存储服务商或 CDN (content delivery network) 提供静态文件服务。这能让你忽略提供静态文件服务可能出现的问题，提高Web 页面加载速度（尤其是在用 CDN 的时候）。

使用这些服务时，基本的工作流程与上面类似，除了要将静态文件传输给存储服务商或 CDN，而不是用 `rsync` 将静态文件传输给服务器。

一般来说大型的服务商都会提供相应的存储后端API，我们只需要编写一个自定义存储后端，将服务商的API接入进来，然后配置一下即可。

例如，若你已在 `myproject.storage.S3Storage` 中写了一个 S3 存储后端，可以这么用:

```
STATICFILES_STORAGE = 'myproject.storage.S3Storage'
```

然后你自需要运行collectstatic命令就行了，剩下的交给CDN。

