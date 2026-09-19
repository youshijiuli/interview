# python-面试通关宝典

### **高级特性**

#### 63.函数装饰器有什么作用？请列举说明。

```python
函数装饰器可以在不修改原函数的条件下，为原函数添加额外的功能，例如记录日志，运行性能，缓存等
以记录函数运行时间为例，实现一个装饰器
import time
def time_it(func):
    def wrapper(func):
        start_time = time.time()
        res = func()
        end_time = time.time()
        return start_time - end_time
    return wrapper
    
```

#### 65.魔法函数 __call__怎么使用？

```python
class Bar:
    def __call__(self, *args, **kwargs):
        print('i am instance method')

b = Bar()  # 实例化
b()  # 实例对象b 可以作为函数调用 等同于b.__call__ 使用


# OUT: i am instance method



# 带参数的类装饰器
class Bar:

    def __init__(self, p1):
        self.p1 = p1

    def __call__(self, func):
        def wrapper():
            print("Starting", func.__name__)
            print("p1=", self.p1)
            func()
            print("Ending", func.__name__)
        return wrapper


@Bar("foo bar")
def hello():
    print("Hello")
```

#### 66.如何判断一个对象是函数还是方法？

```Python
判断对象是函数或方法应该使用type(obj)
```

#### 67.简述 @classmethod 和 @staticmethod 用法和区别。

```python
一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。

而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。

这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。



既然@staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢

从它们的使用上来看,
@staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
@classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。

而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码
class A(object):
    bar = 1
    def foo(self):
        print 'foo'
 
    @staticmethod
    def static_foo():
        print 'static_foo'
        print A.bar
 
    @classmethod
    def class_foo(cls):
        print 'class_foo'
        print cls.bar
        cls().foo()
 
A.static_foo()
A.class_foo()
```

#### 68.Python 中的接口如何实现？

```python
#抽象类加抽象方法就等于面向对象编程中的接口
from abc import ABCMeta,abstractmethod

class interface(object):
    __metaclass__ = ABCMeta #指定这是一个抽象类
    @abstractmethod  #抽象方法
    def Lee(self):
        pass

    def Marlon(self):
        pass


class RelalizeInterfaceLee(interface):#必须实现interface中的所有函数，否则会编译错误
    def __init__(self):    
        print '这是接口interface的实现'
    def Lee(self):
        print '实现Lee功能'        
    def Marlon(self):
        pass   
```

#### 69.你了解 Python 中的反射吗？

```python
通过字符串映射object对象的方法或者属性
hasattr(obj,name_str): 判断objec是否有name_str这个方法或者属性
getattr(obj,name_str): 获取object对象中与name_str同名的方法或者函数
setattr(obj,name_str,value): 为object对象设置一个以name_str为名的value方法或者属性
delattr(obj,name_str): 删除object对象中的name_str方法或者属性

举个栗子
import requests

class Http(object):


    def get(self,url):
        res = requests.get(url)
        response = res.text
        return response

    def post(self,url):
        res = requests.post(url)
        response = res.text
        return response

# 使用反射后
url = "https://www.jianshu.com/u/14140bf8f6c7"
method = input("请求方法>>>:")
h = Http()

if hasattr(h,method):
    func = getattr(h,method)
    res = func(url)
    print(res)
else:
    print("你的请求方式有误...")
```

#### 70.简述 metaclass 的作用和其应用场景。

```
metaclass我没怎么用过，不能乱说误人子弟，可以看下这篇博文https://www.cnblogs.com/xybaby/p/7927407.html
```

#### 71.对比 hasattr()，getattr() 和 setattr() 的用法。

```python
hasattr(obj,name_str): 判断objec是否有name_str这个方法或者属性
getattr(obj,name_str): 获取object对象中与name_str同名的方法或者函数
setattr(obj,name_str,value): 为object对象设置一个以name_str为名的value方法或者属性
delattr(obj,name_str): 删除object对象中的name_str方法或者属性
```

#### 72.请列举你知道的 Python 的魔法方法及用途。

```
1. __call__:允许一个类的实例像函数一样被调用。实质上说，这意味着 x() 与 x._call_() 是相同的
2.__init__:显示初始化属性
3.__str__,__repr__,定义类的时候，重写这两个方法可以让类更清晰
再就是__setattr__,__getattr__,__delattr__等等
```

#### 73.如何知道一个 Python 对象的类型？

```
type(obj)
```

81.**Python 的传参是传值还是传址？**

```
说传值或者传引用都不准确。非要安一个确切的叫法的话，叫传对象（call by object）
具体可以参考这篇文章：https://foofish.net/python-function-args.html
```

#### 74.Python 中的 元类(metaclass) 使用举例。

```
参考77.
```

#### 75.简述 any() 和 all() 方法。

```python
#any(x)判断x对象是否为空对象，如果都为空、0、false，则返回false，如果不都为空、0、false，则返回true

#all(x)如果all(x)参数x对象的所有元素不为0、''、False或者x为空对象，则返回True，否则返回False
>>> any('123')
True
>>> any([0,1])
True
>>> any([0,'0',''])
True
>>> any([0,''])
False
>>> any([0,'','false'])
True
>>> any([0,'',bool('false')])
True
>>> any([0,'',False])
False
>>> any(('a','b','c'))
True
>>> any(('a','b',''))
True
>>> any((0,False,''))
False
>>> any([])
False
>>> any(())
False
>>> all(['a', 'b', 'c', 'd'])  #列表list，
True
>>> all(['a', 'b', 'c', 'd'])  #列表list，元素都不为空或0
True
>>> all(['a', 'b', '', 'd'])  #列表list，存在一个为空的元素
False
>>> all([0, 1,2, 3])  #列表list，存在一个为0的元素
False
>>> all(('a', 'b', 'c', 'd'))  #元组tuple，元素都不为空或0
True
>>> all(('a', 'b', '', 'd'))  #元组tuple，存在一个为空的元素
False
>>> all((0, 1,2, 3))  #元组tuple，存在一个为0的元素
False
>>> all([]) # 空列表
True
>>> all(()) # 空元组
True
>>> #注意：空元组、空列表返回值为True，这里要特别注意
```

#### 76.用 filter 方法求出列表 a =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 中的所有奇数，并构造新列表。

```python
list(filter(lambda x: x%2==1,a))
```

#### 77.什么是猴子补丁？

```markdown
猴子补丁是一个概念，不是python中发明的，其他动态语言也有这么个概念。 《松本行弘的程序世界》这本书，里面专门有一章讲了猴子补丁的设计，所谓的猴子补丁的含义是指在动态语言中，不去改变源码而对功能进行追加和变更
```
