# Python设计模式

代码直戳: https://github.com/faif/python-patterns

# 创建型模式

## 工厂方法


实例 -> 类 -> 类工厂

## 抽象工厂

简单来说就是把一些具有相同方法的类再进行封装,抽象共同的方法以供调用.是工厂方法的进阶版本.

实例 -> 类 -> 类工厂 -> 抽象工厂

## 惰性初始化 Lazy evaluation

这个Python里可以使用@property实现,就是当调用的时候才生成.

## 生成器 Builder

![](img/builder.png)

Builder模式主要用于构建一个复杂的对象，但这个对象构建的算法是稳定的，对象中的各个部分经常变化。Builder模式主要在于应对复杂对象各个部分的频繁需求变动。但是难以应对算法的需求变动。这点一定要注意，如果用错了，会带来很多不必要的麻烦。

重点是将复杂对象的建造过程抽象出来（抽象类别），使这个抽象过程的不同实现方法可以构造出不同表现（属性）的对象。

简单的说：子对象变化较频繁，对算法相对稳定。

## 单例模式 Singleton

一个类只有一个实例

## 原型模式

特点是通过复制一个已经存在的实例来返回新的实例,而不是新建实例.

多用于创建复杂的或者耗时的实例,因为这种情况下,复制一个已经存在的实例使程序运行更高效;或者创建值相等,只是命名不一样的同类数据.

## 对象池 Object pool

一个对象池是一组已经初始化过且可以使用的对象，而可以不用在有需求时创建和销毁对象。池的用户可以从池子中取得对象，对其进行操作处理，并在不需要时归还给池子而非销毁 而不是销毁它. 

在Python内部实现了对象池技术.例如像小整型这样的数据引用非常多,创建销毁都会消耗时间,所以保存在对象池里,减少开销.

# 结构型模式

## 修饰模型 Decorator

Python里就是装饰器.

## 代理模式 Proxy

例如Python里的引用计数.

# 行为型模式

## 迭代器 

迭代容器里所有的元素.






## 14 Python中的单例模式

单例模式是一种特别重要的设计模式，通过单例模式可以保证系统中一个类只有一个实例并且该实例易于被外界访问，方便控制实例个数并节约系统资源。实现单例模式的常用方法如下：

### 1 通过`import`导入

在Python中使用`import`来导入一个对象，则是天然的单例模式。因为模块在第一次导入时，会生成 `.pyc` 文件，当第二次导入时，就会直接加载 `.pyc` 文件，而不会再次执行模块代码。因此，我们只需把相关的函数和数据定义在一个模块中，就可以获得一个单例对象了。例如：

```python
# a.py中
class A(object):
    def fun(self):
        pass
test_a = A

# b.py中
from a import test_a
```



### 2 使用装饰器

```python
def Singleton(cls):
    _state = {}
    def _singleton(*args, **kargs):
        if cls not in _state:
            _state[cls] = cls(*args, **kargs)
        return _state[cls]
    return _singleton


@Singleton
class A(object):
    a = 1
    def __init__(self, x=0):
        self.x = x

a1 = A()
a2 = A()

print("id(a1): ",id(a1))
print("id(a2): ",id(a2))

print("a1.a: ",a1.a)
print("a2.a: ",a2.a)

a1.a = 2
print("a1.a: ",a1.a)
a2.a = 3
print("a2.a: ",a2.a)

print("a1.a: ",a1.a)

# 输出为：
# id(a1):  2973113231736
# id(a2):  2973113231736
# a1.a:  1
# a2.a:  1
# a1.a:  2
# a2.a:  3
# a1.a:  3
```



### 3 使用类实现

使用类实现的时候需要加锁，否则在多线程中无法保证单实例

```python
import time
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


def task(arg):
    obj = Singleton.instance()
    print(obj)
for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()
time.sleep(20)
obj = Singleton.instance()
print(obj)

# 输出：
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
# <__main__.Singleton object at 0x0000022E7C561E80>
```



### 4 基于`__new__`方法实现

当我们实例化一个对象时，是**先执行了类的__new__方法**（我们没写时，默认调用object.__new__），**实例化对象**；然后**再执行类的__init__方法**，对这个对象进行初始化，所有我们可以基于这个，实现单例模式

```python
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instance

obj1 = Singleton()
obj2 = Singleton()
print(obj1)
print(obj2)

def task(arg):
    obj = Singleton()
    print(obj)

for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()

# 输出
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
# <__main__.Singleton object at 0x0000017B102EA978>
```
