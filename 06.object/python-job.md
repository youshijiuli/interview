## Python基础知识

### Python中单下划线和双下划线  
`__foo__`:一种约定,Python内部的名字,用来区别其他用户自定义的命名，以防冲突。  
`_foo`:一种约定,用来指定变量私有，程序员用来指定私有变量的一种方式  
`__foo`:这个有真正的意义:解析器用`__classname`、`__foo`来代替这个名字,以区别和其他类相同的命名。

---

## 面向对象

### 基本概念  
多态\封装\组合\继承  
迭代器和生成器  

### Python的面向对象和Java面向对象的区别  
python可面向对象编程，可以不按照面向对象编程。java就必须面向对象编程了，必须建个类  

### Python的实例方法,类方法,静态方法之间的区别及调用关系  
在类里面定义的函数就是方法,类方法需要`@classmethod`修饰并且有个隐藏参数 `cls`,实例方法必须有个参数 `self`, 静态方法必须有`@staticmethod`修饰,类和实例都可以访问静态方法,实例可以访问实例方法也可以访问类方法,类可以访问类方法也可以访问实例方法,访问实例方法  
必须要带参数 `self`, 可以理解为类其实也是一个实例,类访问实例方法不带参数会报错的。类本身可以访问函数,实例却不行  
详细: [Python的实例方法,类方法,静态方法之间的区别及调用关系 ](https://www.cnblogs.com/funfunny/p/5892212.html)  

### python新式类和旧式类的区别  
主要区别是多继承中，新式类采用广度优先搜索，而旧式类是采用深度优先搜索  

### `__new__`和`__init__`的区别  
创建一个新实例时调用`__new__`,初始化一个实例时用`__init__`,这是它们最本质的区别。  
`__new__`是一个静态方法,而`__init__`是一个实例方法。  
`__new__`方法会返回一个创建的实例,而`__init__`什么都不返回。  
只有在`__new__`返回一个cls的实例时后面的`__init__`才能被调用。  
单例模式的实现可以使用`__new__`方法  

### 单例模式__new__方法版本  
```python
class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  
   
class MyClass(Singleton):  
    # ...  
```

### 单例模式装饰器版本  
```python
def singleton(cls, *args, **kw):  
    instances = {}  
    def getinstance():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return getinstance  

  @singleton  
class MyClass:  
    # ...  
```
