

## Python

##### python list 添加、删除元素

append 添加元素、extend 尾部追加多个元素，也可以合并两个列表

del 删除指定下标元素

##### 列表在指定位置插入元素

insert(下标，值)

##### 列表 del、pop、remove 的区别

del 根据下标删除元素、没有返回值

pop () 可根据下标删除任意位置的元素并将其返回，当括号内为空时则删除该列表最后一个元素并将其返回

remove () 方法可根据值删除元素

##### 字典怎么添加元素

dic['key'] = value

##### 3.1415926怎么输出成3.15

##### 格式化输出怎么保留两位小数

num1 = 3.1415926

print(''%.2f' % num1)

##### Python常用模块及其对应方法

time 模块

- time.time() 返回当前时间戳
- time.localtime([secs]) 将一个时间戳转换为当前时区的struct_time。secs参数未提供，则以当前时间为准。
- time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()) 接收时间元组 返回可读的字符串表示当地时间
- time.sleep([secs]) 执行阻塞

os模块

- os.path.join() 拼接路径信息
- os.mkdir 创建目录
- os.path.split 将path分割成目录和文件名，元组返回
- os.path.isfile 判断是否是文件
- os.path.isdir  判断是否是目录

sys模块

- sys.path.insert() 添加目录进解释器环境，可以直接导包

json模块

- json.dumps() 使字典转换为json格式
- json.loads() 将json解码为字典

##### 列表元素是元组，可以修改元组中的值吗

不可以，但是可以整体修改，相当于重新定义一个元组元素

##### 合并两个字典的多种方法

1、字典的 update 方法

2、dict (d1, **d2) 方法

3、for 循环

##### 列表去重

转换成元组在换成列表

##### json 模块 dumps dump loads load的区别

loads: 把 Json 格式[字符串](https://so.csdn.net/so/search?q=字符串&spm=1001.2101.3001.7020)解码转换成 Python 对象

dumps: 实现 [python](https://so.csdn.net/so/search?q=python&spm=1001.2101.3001.7020) 类型转化为 json 字符串，返回一个 str 对象，把一个 Python 对象编码转换成 Json 字符串

dump: 将 Python 内置类型序列化为 json 对象后写入文件

load: 读取文件中 json 形式的字符串元素 转化成 python 类型

##### \__new\_\_方法和\_\_init__方法的区别

- __new__是在实例创建**之前**被调用的，因为它的任务就是创建实例然后返回该实例对象，是个静态方法。
- __init__是当实例对象创建完成后被调用的，然后设置对象属性的一些初始值，通常用在初始化一个类实例的时候。是一个实例方法。
- __new__至少要有一个参数 cls，为当前类
- __new__必须要有返回值，返回实例化出来的实例
- __init__有一个参数 self，就是这个__new__返回的实例
- __init__不需要返回值

##### with 起到了什么作用

它是一种上下文管理协议，目的在于从流程中吧 try...except 和 finally 关键字和资源释放相关代码统统去掉，简化 try...except...finally 的处理流程

##### with 在什么情况下会自动帮我关闭文件

把打开的文件放在 with 语句中，这样 with 语句就会帮我们自动关闭文件

例如: with open('a.txt', r) as f:

##### with 原理

with 通过__enter__ 方法初始化，然后在__exit__中做善后以及处理异常

所以使用 with 处理的对象必须有__enter__() 和 __exit__() 这两个方法

##### 一个对象可以被 with 调用，怎么操作

对象必须有__enter__() 和 __exit__() 这两个方法

##### 除了打开文件，还有什么地方用到了 with

线程中锁的自动获取和释放

远程主机执行命令时自动获取 ssh 的连接和释放

##### yeild

yield 的作用就是把一个函数变成一个生成器

##### 生成器、迭代器、装饰器 的概念、及其应用场景

**生成器：**

- 使用了 yield 的函数被称为生成器
- 在需要的时候才产生结果，而不是立即产生结果。节省内存空间
- 生成器是一个返回迭代器的函数，只能用于迭代操作
- 在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值，并在下一次执行 next () 方法时从当前位置继续运行。
- 调用一个生成器函数，返回的是一个迭代器对象。

**迭代器：**

- 迭代器是一个可以记住遍历的位置的对象
- 迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。
- 优点：省内存
- 迭代器有两个基本的方法：**iter()** 和 **next()**。
- 把一个类作为一个迭代器使用需要在类中实现两个方法 __iter__() 与 __next__() 。
- __iter__() 方法返回一个特殊的迭代器对象， 这个迭代器对象实现了 __next__() 方法并通过 StopIteration 异常标识迭代的完成。
- __next__() 方法（Python 2 里是 next ()）会返回下一个迭代器对象。

**装饰器：**

- 简洁重复代码
- 扩展功能
- 应用场景：授权、日志、

##### 装饰器除了闭包函数还能怎么实现

类 装饰器、闭包装饰器、都分为带参和不带参

##### python 元编程有哪些方法 （元类）

>###### 什么是元编程
>
>软件开发中很重要的一条原则就是 “不要重复自己的工作（Don’t repeat youself）”，也就是说当我们需要复制粘贴代码时候，通常都需要寻找一个更加优雅的解决方案，在 python 中，这类问题常常会归类为 “元编程”
>
>###### 元编程目的
>
>是创建函数和类，并用他们操作代码（例如修改，生成，或者包装自己已有的代码）。尽可能的使代码优雅简洁。具体而言，通过编程的方法，在更高的抽象层次上对一种层次的抽象的特性进行修改
>
>###### 元编程应用
>
>装饰器
>
>元类

##### 什么是元类

##### re 模块正则匹配一个邮箱（手写具体代码）

```python
import re  
text = input("Please input your Email address：\n")  

re.match(r'^\w{0,19}@\w{1,13}.\w{1,10}$',text)
```

##### re 模块的常用方法

search: 扫描整个字符串并返回第一个pattern模式的成功匹配 匹配失败返回None(包含即可)，匹配一次

math: match 必须第一位就开始匹配，否则匹配失败，匹配一次

- search是在要匹配的字符串中  包含正则表达式的内容就可以

findall: 扫描整个字符串，并返回所有pattern所匹配的结果，匹配多次

split: 拆分字符串

sub: 对字符串进行匹配替换

subn: 对字符串进行匹配替换，返回替换后的次数

##### python 设置私有方法

类方法前面加两个下换线，通过公共方法进行属性的暴露及修改

##### python 实现用户权限认证怎么做简单

使用 JWT，继承 ObtainJSONWebToken 类，然后重写 POST 方法对防水墙进行验证

##### python 设计模式

单例、工厂、建造者、观察者

##### python 程序的输出有乱码，怎么解决

coding: utf-8

##### python 解释器执行程序时的过程

当 Python 程序运行时，编译的结果则是保存在内存中的 PyCodeObject 中，当 Python 程序运行结束时，Python 解释器则将 PyCodeObject 保留在 pyc 文件中。当 python 程序第二次执行时，首先程序会从硬盘中运行 pyc 文件，如果找到了则直接载入，否则就重复上面的过程。

##### 计算程序运行的时间差

time.time 进行时间戳的相减

time.clock 计算 cpu 处理的时间

##### python 内存管理机制及其详细内容

1、引用计数: 对变量的使用进行计数，使用加一、不使用减一，存在循环引用问题，及都为一

2、标记清除: 遍历所有的GC Roots对象，可以直接或间接访问到的对象标记为存活的对象，其余的均为非存活对象，应该被清除。

​		    清除的过程将遍历堆中所有的对象，将没有标记的对象全部清除掉。

基于引用计数的回收机制，每次回收内存，都需要把所有对象的引用计数都遍历一遍，这是非常消耗时间的，于是引入了分代回收来提高回收效率，分代回收采用的是用“空间换时间”的策略。

3、分代回收的核心思想是：**在历经多次扫描的情况下，都没有被回收的变量，gc机制就会认为，该变量是常用变量，gc对其扫描的频率会降低，**

相关详情连接：https://like-ycy.github.io/The-salvation-road-of-Linux-engineer/#/docs/Python/2Python%E5%9F%BA%E7%A1%80/07.%E5%9E%83%E5%9C%BE%E5%9B%9E%E6%94%B6%E6%9C%BA%E5%88%B6

##### python 中函数参数的传递类型

引用传递

##### python 面向对象的三大特点以及其详细概念

继承: 子类可以继承父类，并拥有父类的属性和方法

封装: 把数据与功能都整合到一起，可以控制隐藏和开放属性

多态： 对父类的属性和方法可以进行覆盖重写

##### 类的多继承状态下，顺序输出，都有相同的方法，顺序输出

​     a

  b      c

​     d

```python
class A:
    def talk():
        print('A类的talk')
 
class B(A):
    def talk():
        print('B类的talk')

class C(A):
    def talk():
        print('C类的talk')
        
class D(B，C):
    def talk():
        print('D类的talk')

 d = D()
print(d.talk())

# D类的talk
```

##### 新式类和经典类、最根本的一个区别

经典类的钻石继承是深度优先，即从下往上搜索；新式类的继承顺序是采用 C3 算法（非广度优先）

##### python 操作符的顺序

- 括号：()
- 幂运算：**
- 按位取反：~
- 正号、负号：+、-
- 乘、除、取模、取整除：* 、/、 %、 //
- 加、减：+ 、-
- 右移、左移：>> 、<<
- 按位 “与”：&
- 按位 “异或”，按位 “或”：^ 、|
- 比较运算符：<= 、< 、>、 >=
- 等于、不等于：==、!=
- 赋值运算符：=、%=、/=、//=、-=、+=、*=、**=
- 身份运算符：is、is not
- 成员运算符：in、not in
- 逻辑运算符：and or not

##### 类方法、静态方法

静态方法: 静态方法是类中的函数，不需要实例。静态方法主要是用来存放逻辑性的代码，逻辑上属于类，但是和类本身没有关系，也就是说在静态方法中，不会涉及到类中的属性和方法的操作。可以理解为，静态方法是个**独立的、单纯的**函数，它仅仅托管于某个类的名称空间中，便于使用和维护。

​	使用装饰器 @staticmethod。参数随意，没有 “self” 和 “cls” 参数，但是方法体中 不能使用类或实例的任何属性和方法；类和实例对象都可以调用

类方法: 类方法是将类本身作为对象进行操作的方法,，使用装饰器 @classmethod。第一个参数必须是当前类对象，该参数名一般约定为 “cls”，通过它来传递类的属性和方法（不能传实例的属性和方法）;类和实例对象都可以调用

##### dict 的 items 和 iteritems 有什么不同

dict.items () 返回的是一个完整的列表，而 dict.iteritems () 返回的是一个生成器 (迭代器)。

dict.items () 返回列表 list 的所有列表项，形如这样的二元组 list：［(key,value),(key,value),...］, dict.iteritems() 是 generator, yield 2-tuple。相对来说，前者需要花费更多内存空间和时间，但访问某一项的时间较快 (KEY)。后者花费很少的空间，通过 next () 不断取下一个值，但是将花费稍微多的时间来生成下一 item。

##### 深浅拷贝的区别？

深浅拷贝对于不可变类型皆为引用

浅拷贝: 原始可变对象的改变，拷贝对象也会改变

深拷贝: 重新开辟名称空间存储可变类型，原值和拷贝对象的修改互不影响

##### 什么是可变类型什么是不可变类型

不可变: 整型、浮点型、字符串、元组

可变: 列表、字典、集合

可变类型元素的修改不会改变内存空间、不可变类型则为重新开辟空间进行赋值

##### python自带的函数替换文件中的字符是那个函数

str.replace(old, new, max)

max: 替换几次

##### 鸭子模式

##### 变量的命名规则

- 变量名由字母（广义的Unicode字符，不包括特殊字符）、数字和下划线构成
- 数字不能开头
- 大小写敏感（大写的`a`和小写的`A`是两个不同的变量）
- 不要跟关键字和系统保留字（如函数、模块等的名字）冲突

##### 缩进规范

4个空格

##### 字典中的键有什么要求

必须为可哈希的

##### 说一下Unittest

TestCase：用户自定义的测试 case 的[基类](https://so.csdn.net/so/search?q=基类&spm=1001.2101.3001.7020)，调用 run () 方法，会依次调用 setUp 方法、执行用例的方法、tearDown 方法。

TestSuite：[测试用例](https://so.csdn.net/so/search?q=测试用例&spm=1001.2101.3001.7020)集合，可以通过 addTest () 方法手动增加 Test Case，也可以通过 TestLoader 自动添加 Test Case，TestLoader 在添加用例时，会没有顺序。

TestRunner：运行测试用例的驱动类，可以执行 TestCase，也可以执行 TestSuite，执行后 TestCase 和 TestSuite 会自动管理 TESTResult。

TestFixture：简单来说就是做一些测试过程中需要准备的东西，比如创建临时的数据库，文件和目录等，其中 setUp () 和 setDown () 是最常用的方法

整个的流程就是首先要写好 TestCase，然后由 TestLoader 加载 TestCase 到 TestSuite，然后由 TestTestRunner 来运行 TestSuite，运行的结果保存在 TextTestReusult 中，整个过程集成在 unittest.main 模块中。

##### 说一下异常的处理

try...except...finally

try 中代码没有异常，执行else

finally 则为 不管 try 有没有异常都执行

except 单个异常 as 别名

except (多个异常):

except Exception: 万能异常

raise 主动抛出异常

也可以自定义异常类， 继承BaseException

##### 异常种类

> AttributeError 试图访问一个对象没有的树形，比如foo.x，但是foo没有属性x
> IOError 输入/输出异常；基本上是无法打开文件
> ImportError 无法引入模块或包；基本上是路径问题或名称错误
> IndentationError 语法错误（的子类） ；代码没有正确对齐
> IndexError 下标索引超出序列边界，比如当x只有三个元素，却试图访问x[5]
> KeyError 试图访问字典里不存在的键
> KeyboardInterrupt Ctrl+C被按下
> NameError 使用一个还未被赋予对象的变量
> SyntaxError Python代码非法，代码不能编译(个人认为这是语法错误，写错了）
> TypeError 传入对象类型与要求的不符合
> UnboundLocalError 试图访问一个还未被设置的局部变量，基本上是由于另有一个同名的全局变量，
> 导致你以为正在访问它
> ValueError 传入一个调用者不期望的值，即使值的类型是正确的

##### 说一下break

break 语句用来终止循环语句，即循环条件没有 False 条件或者序列还没被完全递归完，也会停止执行循环语句。

reak 语句用在 while 和 for 循环中。

如果您使用嵌套循环，break 语句将停止执行最深层的循环，并开始执行下一行代码。

##### 说一下for while循环之后的else的用法

当 while 循环正常执行完并且中间没有被 break 中止的话，就会执行 else 后面的语句

如果 for 循环中有 [break](https://so.csdn.net/so/search?q=break&spm=1001.2101.3001.7020) 字段等导致 for 循环没有正常执行完毕，那么 else 中的内容也不会执行。

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

## 进程

##### 进程、线程、协程的概念及其优缺点

##### 线程和进程的区别

##### 进程、线程以及协程 用什么模块怎样实现

##### 进程、线程、协程 的应用场景

##### 线程上下文切换为什么比进程快

##### 多进程为什么适合做计算

##### IO 多路复用

##### 异步非阻塞

##### 进程间的通信方式

##### 线程之间怎么通信？

## Mysql

##### select语句获取前面20条数据

select * from app_event order by id limit 0,20

##### mysql索引原理

B + tree

##### mysql 什么是事务

多个sql原子性操作，保证数据正确

##### mysql查询出来的数据进行分页

select * from table limit 0,10

##### char和vachar的区别？

VARCHAR 类型用于存储可变长字符串，是最常见的字符串数据类型。

vachar 适合一下

- 字符串列的最大长度比平均长度大很多
- 列的更新很少，所以碎片不是问题
- 使用了像 UTF-8 这样复杂的字符集，每个字符都使用不同的字节数进行存储

CHAR 类型是定长的：MySQL 总是根据定义的字符串长度分配足够的空间。

CHAR 适合存储很短的字符串，或者所有值都接近同一个长度。例如，CHAR 非常适合存储密码的 MD5 值

##### mysql多表联查

内连接: select * from 表1，表2 where 表1.公共字段=表2.公共字段

左外连接: select * from 表1 left join 表2 on 表1.公共字段=表2.公共字段

右外连接: select * from 表1 right join 表2 on 表1.公共字段=表2.公共字段

交叉连接: select * from 表1 cross join 表2

自然连接: select * from stuinfo natural join stumarks;

##### 如何保证mysql与redis数据的一致性

##### 并发扣款时，保证数据一致性，及数据一致性

##### mysql 模糊查询最后一个单词 like %a

##### mysql 视图

##### mysql 读写分离的作用是什么

##### mysql 读写分离怎么提高性能

##### mysql 设计一张表，应该考虑些什么

##### mysql 用户表太多怎么分表

##### mysql主从复制的几种方式，你们用了哪种

##### mysql 的隔离级别

##### 主键索引的底层是什么？

##### 10G 的数据表，20G 的索引，怎么排查问题

##### 如何保证商品数据的一致性？采用什么方法？具体如果操作？

##### MySQL支持事务吗？详细说一下

## MongoDB

##### mongo 对比 mysql 有什么优势

##### mongo 的应用场景

##### 为什么要用 mongo

## redis

##### 列表怎样增加数据

lpush、rpush

##### 集合、有序集合怎么增加数据

sadd、zadd

##### 怎么实现值的自增

Incr 命令将 key 中储存的数字值增一

##### 有序集合和集合的区别

有序集合多了一个分数，是一个浮点数，对分数进行排序

##### 删除列表第二项

lrem key 2 value

##### redis 的数据类型

##### redis 的主从、哨兵、集群的概念及其优缺点

##### redis 的持久化方式及其优缺点、以及其配置多少秒内有几次操作进行备份

##### redis rdb和aof的区别、以及配置多少秒内几次操作进行保存

##### redis 主从原理

##### redis 的应用场景

##### redis 分布式锁、怎么实现

##### 为什么用 redis 充当消息队列？

##### redis 的数据类型(任意一种）的底层是什么？

## 中间件

##### session 回话的保持

nginx 的 ip_hash，以及将 session 放入到 redis 中

##### 什么是正向代理、什么是反向代理、日常生活中有哪些正向、反向代理的实例

##### nginx 的优化

##### dockerfile 内的各个指令

##### python 操作 k8s 集群的相关模块

##### k8s deployment 怎么保证 pod 处于预期状态

##### gitlab-ci 一个代码库怎么配置多个 k8s 环境，以便于将代码区分发布至测试及生产环境

##### jwt 怎样让同一个账号不能两个人登录（判断一下token是否在有效期内）

##### 用 ik 分词器对 词 进行热更新、以及 ik 分词器的优化

##### 给 ES 添加索引

##### 扩展了一个数据表，怎么动态捕捉添加索引。即动态为新加入的数据进行刷新索引（django内置的就有，save，异步刷新 ES）

##### socket是长连接吗

##### jwt的签名是用的什么算法

##### Celery 实现原理

##### Restful规范具体是什么



## 网络

##### 网络传输7层协议？TCP 和 UDP 在哪一层？

##### TCP 和 UDP 的区别,有配置过吗？

## 算法、设计模式

##### 用过哪些算法

##### 怎么验证算法

空间复杂度和时间复杂度

##### 常用设计模式？在哪用到？

##### 算法题:云梯

## Flask

##### flask-socketio实现了什么功能

##### flask的生命周期

## 代码题

##### python 实现 ip 地址的存储，32位

##### 两个字符串，有相同的元素就返回 True、没有就返回 False

```python
str1 = '1234'
str2 = '123'

set1 = set(str1)
set2 = set(str2)

if len(str1) > (str2):
	difference_set = set2 - set1
else:
    difference_set = set1 - set2
    
if difference_set:
    print('True')
else:
    print('Flase')
```

##### 取出一个列表中的中间值

提示：(这个提示不是面试官提示的，是自己要去分析多种情况)列表长度有可能是偶数，那么就要取两个中间值，奇数取一个中间值

##### 代码实现单例模式

```python
class Single:
    def __init__(self):
        pass


    @classmethod
    def inner(cls, *args, **kwargs):
        if not hasattr(Single, '_attr'):
            # Single._attr = Single()
            Single._attr = cls()
        return Single._attr

s1 = Single.inner()
# s2 = Single.inner()
print(s1)
s2 = Single.inner()
print(s2)
```

##### 代码实现 json 模块可以序列化 datetime 类型

##### 一个列表中存在若干数据，存在重复数据，取出第二大的数

##### 数据库中一张表存在姓名、学科、成绩，查询每个学科的第一名

##### 用列表推导式将列表中奇数元素的平方放到新的列表中

##### 一个目录下n个不同后缀的文件统计.jpg文件的数量

##### 有一对兔子自第三个月开始，每一个月生一对兔子，之后生的每一对兔子…（想不起来了，这个没做出来）

##### 输入一个字符到文件里，直到输入的为#时，停止输入

##### 求数列2/1，3/2, 5/3, 8/5, 13/8 … 的前n项和

##### 用递归方法求10的乘积 1 * 2 * 3 ... * 10

##### 如果一个数的因子之和等于这个数，那么这个数称为完数（比如6=1+2+3）。根据完数的概念求出1-1000的所有完数







