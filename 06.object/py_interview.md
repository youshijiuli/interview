##### 使用with语句的好处是什么
*  使用with后不管with中的代码出现什么错误，都会进行对当前对象进行清理工作。例如file的file.close()方法，无论with中出现任何错误，都会执行file.close（）方法
*  只有支持上下文管理器的对象才能使用with，即在对象内实现了两个方法：__enter__()和__exit__()

##### 写一个的支持with语句的类
[参考链接](https://www.cnblogs.com/yidashi110/p/10091991.html)
```python
class W(object):
    def __init__(self):
        pass
    def __enter__(self):
        print('进入with语句')
        return self
        
    def __exit__(self,*args,**kwargs):
        print('退出with语句')
        
with W() as w:
    print('之前')
    print(w)
    print('之后')
```

---

##### 实现一个单例模式。(尽可能多的方法)
[参考链接](https://www.cnblogs.com/huchong/p/8244279.html)
```python
# 方法一：使用__new__()
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
print(obj1 is obj2)

# 方法二：使用元类来创建
import threading

class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
        
class Singleton(metaclass=SingletonType):
    def __init__(self):
        pass
 
obj1 = Singleton()
obj2 = Singleton()
print(obj1 is obj2)
```

---

##### 什么是反射，以及应用场景
[什么是反射的解释](https://www.cnblogs.com/IT-Scavenger/p/9394306.html)

* 反射就是通过字符串的形式，导入模块；通过字符串的形式，去模块寻找指定函数，并执行。利用字符串的形式去对象（模块）中操作（查找/获取/删除/添加）成员，一种基于字符串的事件驱动！
* 应用场景：当我们动态的输入一个模块名的时候就可以使用到反射。
* 通过hasattr，getattr，delattr，setattr等四个函数来操作

---

##### 如何判断一个对象是否可调用？哪些对象是可调用对象？如何定义一个类，使其对象本身就是可调用对象？
* 使用callable函数判断。
* 可调用对象有7类：
    * 用户自定义函数
    * 内置函数
    * 内置方法
    * 方法(定义在类中的函数)
    * 类
    * 类实例(如果类中定义了__call__方法，那么这个类的实例就是可调用对象)
    * 生成器函数 
* 在类中定义__call__方法，实例对象加()是即调用__call__的方法

---

##### 列举面向对象中带双下划线的特殊方法

>__new__：可以调用其它类的构造方法或者直接返回别的对象来作为本类的实例。
>__init__： 负责类的实例化
>__call__：对象后边加括号，触发执行
>__str__：print打印一个对象时。
>__doc__：类的注释，该属性是无法继承的。
>__getattr__：在使用调用属性（方式、属性）不存在的时候触发
>__setattr__：添加/修改属性会触发它的执行
>__dellattr__：删除属性的时候会触发
>__delete__：采用del删除属性时，触发

##### 双下划线和单下划线的区别

* "单下划线" 开始的成员变量叫做保护变量，意思是只有类对象和子类对象自己能访问到这些变量；
* "双下划线" 开始的是私有成员，意思是只有类对象自己能访问，连子类对象也不能访问到这个数据。

---

##### 实例变量和类变量的区别

* 实例变量是对于每个实例都独有的数据
* 类变量是该类所有实例共享的属性和方法

##### 实例方法、静态方法和类方法的区别
* 实例方法：第一个参数必须是实例对象，通常为self。实例方法只能由实例对象调用。
* 类方法：使用装饰器@classmethod。第一个参数为当前类的对象，通常为cls。实例对象和类对象都可以调用类方法。
* 静态方法：使用装饰器@staticmethod。没有self和cls参数。方法体中不能使用类或者实例的任何属性和方法。实例对象和类对象都可以调用。

##### isinstance和type的作用
* 两者都用来判断对象的类型
* 对于一个类的之类对象的类型判断，type就不行了，而isinstance可以。
```pyyhon
class A(object):
    pass
class B(A):
    pass
    
ba=B()
ab=A()
print(type(ba)==A) # False
print(type(ab)==A) # True
print(isinstance(ab,A)) # True
print(isinstance(ba,A)) # True
```

---

##### 类的加载和实例化过程

1. 在堆内存中生成class对象, 把静态变量和静态方法加载到方法区, 这个堆内存中的class对象是方法区数据的入口
2. 静态变量默认初始化
3. 静态变量显式初始化
4. 执行静态代码块
5. 成员变量默认初始化, 显示初始化
6. 执行构造函数

---

##### 简述面向对象的三大特性？
[参考链接](https://www.cnblogs.com/lfpython/p/7346385.html)
* 继承，封装和多态
    * 继承：
        * 继承就是继承的类直接拥有被继承类的属性而不需要在自己的类体中重新再写一遍，其中被继承的类叫做父类、基类，继承的类叫做派生类、子类。
    * 封装：
        * 封装就是把类中的属性和方法定义为私有的，方法就是在属性名或方法名前加双下划线，而一旦这样定义了属性或方法名后，python会自动将其转换为_类名__属性名（方法名）的格式，在类的内部调用还是用双下划线加属性名或方法名，在类的外部调用就要用_类名__属性名（方法名）。父类的私有属性和方法，子类无法对其进行修改。
    * 多态：
        * 多态就是不同的对象可以调用相同的方法然后得到不同的结果，有点类似接口类的感觉，在python中处处体现着多态，比如不管你是列表还是字符串还是数字都可以使用+和*。

##### 什么是鸭子模型？
* 鸭子类型（英语：duck typing）是动态类型的一种风格。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口，而是由当前方法和属性的集合决定。

##### super的作用
* 当子类中的方法与父类中的方法重名时，子类中的方法会覆盖父类中的方法，那么，如果我们想实现同时调用父类和子类中的同名方法，就需要使用到super()这个函数，用法为super().函数名()

##### mro是什么？
* 对于支持继承的编程语言来说，其方法（属性）可能定义在当前类，也可能来自于基类，所以在方法调用时就需要对当前类和基类进行搜索以确定方法所在的位置。而搜索的顺序就是所谓的「方法解析顺序」（Method Resolution Order，或MRO）。

##### 什么是c3算法？
* c3算法是python新式类中用来产生mro顺序的一套算法。即多继承的查找规则。
