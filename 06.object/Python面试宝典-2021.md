## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目32：阅读下面的代码说出运行结果。

```Python
class A:
    def who(self):
        print('A', end='')

class B(A):
    def who(self):
        super(B, self).who()
        print('B', end='')

class C(A):
    def who(self):
        super(C, self).who()
        print('C', end='')

class D(B, C):
    def who(self):
        super(D, self).who()
        print('D', end='')

item = D()
item.who()
```

> **点评**：这道题考查到了两个知识点：
>
> 1. Python中的MRO（方法解析顺序）。在没有多重继承的情况下，向对象发出一个消息，如果对象没有对应的方法，那么向上（父类）搜索的顺序是非常清晰的。如果向上追溯到`object`类（所有类的父类）都没有找到对应的方法，那么将会引发`AttributeError`异常。但是有多重继承尤其是出现菱形继承（钻石继承）的时候，向上追溯到底应该找到那个方法就得确定MRO。Python 3中的类以及Python 2中的新式类使用[C3算法](<https://www.jianshu.com/p/a08c61abe895>)来确定MRO，它是一种类似于广度优先搜索的方法；Python 2中的旧式类（经典类）使用深度优先搜索来确定MRO。在搞不清楚MRO的情况下，可以使用类的`mro`方法或`__mro__`属性来获得类的MRO列表。
> 2. `super()`函数的使用。在使用`super`函数时，可以通过`super(类型, 对象)`来指定对哪个对象以哪个类为起点向上搜索父类方法。所以上面`B`类代码中的`super(B, self).who()`表示以B类为起点，向上搜索`self`（D类对象）的`who`方法，所以会找到`C`类中的`who`方法，因为`D`类对象的MRO列表是`D --> B --> C --> A --> object`。

```
ACBD
```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目20：`__init__`和`__new__`方法有什么区别？

Python中调用构造器创建对象属于两阶段构造过程，首先执行`__new__`方法获得保存对象所需的内存空间，再通过`__init__`执行对内存空间数据的填充（对象属性的初始化）。`__new__`方法的返回值是创建好的Python对象（的引用），而`__init__`方法的第一个参数就是这个对象（的引用），所以在`__init__`中可以完成对对象的初始化操作。`__new__`是类方法，它的第一个参数是类，`__init__`是对象方法，它的第一个参数是对象。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目43：运行下面的代码是否会报错，如果报错请说明哪里有什么样的错，如果不报错请说出代码的执行结果。

```Python
class A: 
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

obj = A(1)
obj.__value = 2
print(obj.value)
print(obj.__value)
```

> **点评**：这道题有两个考察点，一个考察点是对`_`和`__`开头的对象属性访问权限以及`@property`装饰器的了解，另外一个考察的点是对动态语言的理解，不需要过多的解释。

```
1
2
```

> **扩展**：如果不希望代码运行时动态的给对象添加新属性，可以在定义类时使用`__slots__`魔法。例如，我们可以在上面的`A`中添加一行`__slots__ = ('__value', )`，再次运行上面的代码，将会在原来的第10行处产生`AttributeError`错误。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目018：说出下面代码的运行结果。

```Python
class Parent:
    x = 1

class Child1(Parent):
    pass

class Child2(Parent):
    pass

print(Parent.x, Child1.x, Child2.x)
Child1.x = 2
print(Parent.x, Child1.x, Child2.x)
Parent.x = 3
print(Parent.x, Child1.x, Child2.x)
```

> **点评**：运行上面的代码首先输出`1 1 1`，这一点大家应该没有什么疑问。接下来，通过`Child1.x = 2`给类`Child1`重新绑定了属性`x`并赋值为`2`，所以`Child1.x`会输出`2`，而`Parent`和`Child2`并不受影响。执行`Parent.x = 3`会重新给`Parent`类的`x`属性赋值为`3`，由于`Child2`的`x`属性继承自`Parent`，所以`Child2.x`的值也是`3`；而之前我们为`Child1`重新绑定了`x`属性，那么它的`x`属性值不会受到`Parent.x = 3`的影响，还是之前的值`2`。

```
1 1 1
1 2 1
3 2 3
```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目23：说一下你知道的Python中的魔术方法。

> **点评**：魔术方法也称为魔法方法，是Python中的特色语法，也是面试中的高频问题。

| 魔术方法                                                     | 作用               |
| ------------------------------------------------------------ | ------------------ |
| `__new__`、`__init__`、`__del__`                             | 创建和销毁对象相关 |
| `__add__`、`__sub__`、`__mul__`、`__div__`、`__floordiv__`、`__mod__` | 算术运算符相关     |
| `__eq__`、`__ne__`、`__lt__`、`__gt__`、`__le__`、`__ge__`   | 关系运算符相关     |
| `__pos__`、`__neg__`、`__invert__`                           | 一元运算符相关     |
| `__lshift__`、`__rshift__`、`__and__`、`__or__`、`__xor__`   | 位运算相关         |
| `__enter__`、`__exit__`                                      | 上下文管理器协议   |
| `__iter__`、`__next__`、`__reversed__`                       | 迭代器协议         |
| `__int__`、`__long__`、`__float__`、`__oct__`、`__hex__`     | 类型/进制转换相关  |
| `__str__`、`__repr__`、`__hash__`、`__dir__`                 | 对象表述相关       |
| `__len__`、`__getitem__`、`__setitem__`、`__contains__`、`__missing__` | 序列相关           |
| `__copy__`、`__deepcopy__`                                   | 对象拷贝相关       |
| `__call__`、`__setattr__`、`__getattr__`、`__delattr__`      | 其他魔术方法       |

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目26：什么是鸭子类型（duck typing）？

鸭子类型是动态类型语言判断一个对象是不是某种类型时使用的方法，也叫做鸭子判定法。简单的说，鸭子类型是指判断一只鸟是不是鸭子，我们只关心它游泳像不像鸭子、叫起来像不像鸭子、走路像不像鸭子就足够了。换言之，如果对象的行为跟我们的预期是一致的（能够接受某些消息），我们就认定它是某种类型的对象。

在Python语言中，有很多bytes-like对象（如：`bytes`、`bytearray`、`array.array`、`memoryview`）、file-like对象（如：`StringIO`、`BytesIO`、`GzipFile`、`socket`）、path-like对象（如：`str`、`bytes`），其中file-like对象都能支持`read`和`write`操作，可以像文件一样读写，这就是所谓的对象有鸭子的行为就可以判定为鸭子的判定方法。再比如Python中列表的`extend`方法，它需要的参数并不一定要是列表，只要是可迭代对象就没有问题。

> **说明**：动态语言的鸭子类型使得设计模式的应用被大大简化。
