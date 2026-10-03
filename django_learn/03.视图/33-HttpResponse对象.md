HttpResponse类定义在`django.http`模块中。

HttpRequest对象是浏览器发送过来的请求数据的封装，HttpResponse对象则是你想要返回给浏览器的数据的封装。

HttpRequest对象由Django自动解析HTTP数据包而创建，而HttpResponse对象则由程序员手动创建。

我们编写的每个视图都要实例化、填充和返回一个HttpResponse对象，也就是函数的return值。


## 一、使用方法

### 1. 返回一个字符串

最简单的方式是传递一个string、bytes或者memoryview（Python3.8新增的一种类型）作为页面的内容到HttpResponse构造函数，并返回给用户:

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the Web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
>>> response = HttpResponse(b'Bytestrings are also accepted.')
>>> response = HttpResponse(memoryview(b'Memoryview as well.'))
```

可以将response看做一个类文件对象，使用wirte()方法不断地往里面增加内容。

```python
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the Web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

### 2. 传递可迭代对象

你甚至可以传递一个可迭代的对象给HttpResponse。比如 StreamingHttpResponse 。

HttpResponse会立即处理这个迭代器，并把它的内容存成字符串，最后废弃这个迭代器。比如文件在读取后，会立刻调用close()方法，关闭文件。

### 3. 设置头部字段

可以把HttpResponse对象当作一个字典一样，在其中增加和删除头部字段。

这就是如何设置HTTP头部header信息的方法。

```python
>>> response = HttpResponse()
>>> response['Age'] = 120
>>> del response['Age']
```

注意！与字典不同的是，如果要删除的头部字段如果不存在，del不会抛出KeyError异常。

HTTP的头部字段中不能包含换行。所以如果我们提供的头部字段值包含换行符（CR或者LF），将会抛出BadHeaderError异常。

### 4. 附件形式

让浏览器以文件附件的形式处理响应, 需要声明`content_type`类型和设置`Content-Disposition`头信息。 例如，给浏览器返回一个微软电子表格：

```python
>>> response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
>>> response['Content-Disposition'] = 'attachment; filename="foo.xls"'
```

## 二、属性

### content

响应的内容。bytes类型。

### charset

编码的字符集。 如果没指定，将会从`content_type`中解析出来。

### status_code

响应的状态码，比如200。

### reason_phrase

响应的HTTP原因短语。 使用标准原因短语。

除非明确设置，否则`reason_phrase`由`status_code`的值决定。

### streaming

这个属性的值总是False。由于这个属性的存在，使得中间件能够区别对待流式响应和常规响应。

### closed

如果响应已关闭，那么这个属性的值为True。

## 三、 方法

### `__init__()`

> `__init__(content=b'', content_type=None, status=200, reason=None, charset=None)`

响应的实例化方法。使用content参数和`content-type`实例化一个HttpResponse对象。

content应该是一个迭代器或者字符串。如果是迭代器，这个迭代期返回的应是一串字符串，并且这些字符串连接起来形成response的内容。 如果不是迭代器或者字符串，那么在其被接收的时候将转换成字符串。

`content_type`是可选地，用于填充HTTP的`Content-Type`头部。如果未指定，默认情况下由`DEFAULT_CONTENT_TYPE`和`DEFAULT_CHARSET`设置组成：`text/html; charset=utf-8`。

status是响应的状态码。reason是HTTP响应短语。charset是编码方式。

### `__setitem__(header, value)`

设置头部的键值对。两个参数都必须为字符串类型。

### `__delitem__(header)`

删除头部的某个键。键不存在的话，不会报错。不区分大小写。

`__getitem__(header)`

返回对应键的值。不区分大小写。

### has_header(header)

检查头部中是否有给定的名称（不区分大小写），返回True或 False。

### setdefault(header, value)

设置一个头部，除非该头部已经设置过了。

### set_cookie()

> set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)

**这个方法你必须会，这就是在Django中手动设置COOKIE的方法。**

设置一个Cookie。 参数与Python标准库中的`Morsel.Cookie`对象相同。

max_age: 生存周期，以秒为单位。如果设为None，浏览器开启期间保持，关闭后一同删除。

expires：到期时间。

domain: 用于设置跨域的Cookie。例如`domain=".lawrence.com"`将设置一个`www.lawrence.com`、`blogs.lawrence.com `和`calendars.lawrence.com`都可读的Cookie。 否则，Cookie将只能被设置它的域读取。

secure=True：支持https

**httponly=True**：阻止客户端的js代码访问cookie

使用`samesite='Strict'`或`samesite='Lax'`告诉浏览器在执行跨源请求时不要发送此cookie。并非所有浏览器都支持SameSite，因此它不是Django的CSRF保护的替代品，而是一种深度防御措施。

使用`samesite='None'（string）`显式声明此cookie与所有相同站点和跨站点请求一起发送。

### set_signed_cookie()

> set_signed_cookie(key, value, salt='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)

与`set_cookie()`类似，但是在设置之前将对cookie进行加密签名。通常与`HttpRequest.get_signed_cookie()`一起使用。 

### delete_cookie()

> delete_cookie(key, path='/', domain=None, samesite=None)

删除Cookie中指定的key。 

由于Cookie的工作方式，path和domain应该与`set_cookie()`中使用的值相同，否则Cookie不会删掉。

### close()

在请求结束后WSGI服务器会调用此方法，关闭连接

### write(content)

将HttpResponse实例看作类似文件的对象，往里面添加内容。

### flush()

清空HttpResponse实例的内容。

### tell()

将HttpResponse实例看作类似文件的对象，移动位置指针。

### getvalue()

返回HttpResponse.content的值。 此方法将HttpResponse实例看作是一个类似流的对象。

### readable()

返回的值始终为False。判断是否可读

### seekable()

值始终为False。判断指针是否可以移动。

### writable()

值始终为True。判断是否可写。

### writelines(lines)

将一个包含行的列表写入响应对象中。 不添加分行符。

## 四、HttpResponse的子类

Django包含了一系列的HttpResponse的衍生类（子类），用来处理不同类型的HTTP响应。与HttpResponse相同, 这些衍生类存在于`django.http`之中。这些子类并不算复杂，代码也很简单，主要就是响应码的不同。

* class HttpResponseRedirect：重定向，返回302状态码。已经被redirect()替代。
* class HttpResponsePermanentRedirect:永久重定向，返回301状态码。
* class HttpResponseNotModified：未修改的页面，返回304状态码。
* class HttpResponseBadRequest：错误的请求，返回400状态码。
* class HttpResponseNotFound：页面不存在，返回404状态码。
* class HttpResponseForbidden：禁止访问，返回403状态码。
* class HttpResponseNotAllowed：禁止访问，返回405状态码。
* class HttpResponseGone：过期，返回410状态码。
* class HttpResponseServerError：服务器错误，返回500状态码。

其实，你还可以自定义HttpResponse的子类，如下所示：

```python
from http import HTTPStatus
from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT
```

## 五、JsonResponse类

> class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)
>

JsonResponse是HttpResponse的一个子类，是Django提供的用于创建JSON编码类型响应的快捷类。 

它从父类继承大部分行为，并具有以下不同点：

- 它的Content-Type头部为`application/json`


- 它的第一个参数data，应该为一个字典数据类型。
-  只有将safe参数设置为False，才可以将任何可JSON 序列化的对象作为data的参数值，否则会报错。

encoder默认为`django.core.serializers.json.DjangoJSONEncoder`，用于序列化数据。 

典型的用法如下：

```python
>>> from django.http import JsonResponse
>>> response = JsonResponse({'foo': 'bar'})
>>> response.content
b'{"foo": "bar"}'
```

若要序列化非dict对象，必须设置safe参数为False：

```python
>>> response = JsonResponse([1, 2, 3], safe=False)
```

如果不传递safe=False，将抛出一个TypeError。

如果你需要使用不同的JSON 编码器类，可以传递encoder参数给构造函数：

```python
>>> response = JsonResponse(data, encoder=MyJSONEncoder)
```


## 六、StreamingHttpResponse类


StreamingHttpResponse类被用来从Django响应一个流式对象到浏览器。如果生成的响应太长或者是占用的内存较大，这么做更有效率。 例如，生成大型的CSV文件。

StreamingHttpResponse不是HttpResponse的子类（而是兄弟类），但是除了几个明显不同的地方，两者几乎完全相同：

* StreamingHttpResponse接收一个迭代器作为参数。这个迭代器返回bytes类型的字符内容。
* StreamingHttpResponse的内容是一个整体的对象，不能直接访问修改
* StreamingHttpResponse有一个 `streaming_content`属性
* 你不能在StreamingHttpResponse上使用类似文件操作的tell和write方法

由于StreamingHttpResponse的内容无法访问，因此许多中间件无法正常工作。例如，不能为流式响应生成ETag和Content-Length头。

StreamingHttpResponse对象有下面的属性

- **streaming_content**：一个包含响应内容的迭代器，通过HttpResponse.charset编码为bytes类型。
- **status_code**：响应的状态码
- **reason_phrase**：响应的原语
- **streaming**：总是为True


## 七、FileResponse

> class FileResponse(open_file, as_attachment=False, filename='', **kwargs)

文件类型响应。通常用于给浏览器返回一个文件附件。

FileResponse是StreamingHttpResponse的子类，为二进制文件专门做了优化。

FileResponse需要通过二进制模式打开文件，如下:

```python
>>> from django.http import FileResponse
>>> response = FileResponse(open('myfile.png', 'rb'))
>>> return response
```
文件会被自动关闭，所以不需要在上下文管理器中打开。

如果 `as_attachment=True`，则`Content-Disposition` 被设置为 `attachment`,告诉浏览器这是一个附件，以文件形式下载。否则 `Content-Disposition` 会被设置为 `inline` (浏览器默认行为)。

如果open_file参数传递的类文件对象没有名字，或者名字不合适，那么你可以通过filename参数为文件对象指定一个合适的名字。