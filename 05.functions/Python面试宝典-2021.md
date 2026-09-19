## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

####  题目005：Lambda函数是什么，举例说明的它的应用场景。

> **点评**：这个题目主要想考察的是Lambda函数的应用场景，潜台词是问你在项目中有没有使用过Lambda函数，具体在什么场景下会用到Lambda函数，借此来判断你写代码的能力。因为Lambda函数通常用在高阶函数中，主要的作用是通过向函数传入函数或让函数返回函数最终实现代码的解耦合。

Lambda函数也叫匿名函数，它是功能简单用一行代码就能实现的小型函数。Python中的Lambda函数只能写一个表达式，这个表达式的执行结果就是函数的返回值，不用写`return`关键字。Lambda函数因为没有名字，所以也不会跟其他函数发生命名冲突的问题。

> **扩展**：面试的时候有可能还会考你用Lambda函数来实现一些功能，也就是用一行代码来实现题目要求的功能，例如：用一行代码实现求阶乘的函数，用一行代码实现求最大公约数的函数等。
>
> ```Python
> fac = lambda x: __import__('functools').reduce(int.__mul__, range(1, x + 1), 1)
> gcd = lambda x, y: y % x and gcd(y % x, x) or x
> ```

Lambda函数其实最为主要的用途是把一个函数传入另一个高阶函数（如Python内置的`filter`、`map`等）中来为函数做解耦合，增强函数的灵活性和通用性。下面的例子通过使用`filter`和`map`函数，实现了从列表中筛选出奇数并求平方构成新列表的操作，因为用到了高阶函数，过滤和映射数据的规则都是函数的调用者通过另外一个函数传入的，因此这`filter`和`map`函数没有跟特定的过滤和映射数据的规则耦合在一起。

```Python
items = [12, 5, 7, 10, 8, 19]
items = list(map(lambda x: x ** 2, filter(lambda x: x % 2, items)))
print(items)    # [25, 49, 361]
```

> **扩展**：用列表的生成式来实现上面的代码会更加简单明了，代码如下所示。
>
> ```Python
> items = [12, 5, 7, 10, 8, 19]
> items = [x ** 2 for x in items if x % 2]
> print(items)    # [25, 49, 361]
> ```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目27：说一下Python中变量的作用域。

Python中有四种作用域，分别是局部作用域（**L**ocal）、嵌套作用域（**E**mbedded）、全局作用域（**G**lobal）、内置作用域（**B**uilt-in），搜索一个标识符时，会按照**LEGB**的顺序进行搜索，如果所有的作用域中都没有找到这个标识符，就会引发`NameError`异常。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目24：函数参数`*arg`和`**kwargs`分别代表什么？

Python中，函数的参数分为位置参数、可变参数、关键字参数、命名关键字参数。`*args`代表可变参数，可以接收`0`个或任意多个参数，当不确定调用者会传入多少个位置参数时，就可以使用可变参数，它会将传入的参数打包成一个元组。`**kwargs`代表关键字参数，可以接收用`参数名=参数值`的方式传入的参数，传入的参数的会打包成一个字典。定义函数时如果同时使用`*args`和`**kwargs`，那么函数可以接收任意参数。

#### 题目39：说出下面代码的运行结果。

```Python
def extend_list(val, items=[]):
    items.append(val)
    return items

list1 = extend_list(10)
list2 = extend_list(123, [])
list3 = extend_list('a')
print(list1)
print(list2)
print(list3)
```

> **点评**：Python函数在定义的时候，默认参数`items`的值就被计算出来了，即`[]`。因为默认参数`items`引用了对象`[]`，每次调用该函数，如果对`items`引用的列表进行了操作，下次调用时，默认参数还是引用之前的那个列表而不是重新赋值为`[]`，所以列表中会有之前添加的元素。如果通过传参的方式为`items`重新赋值，那么`items`将引用到新的列表对象，而不再引用默认的那个列表对象。这个题在面试中经常被问到，通常不建议使用容器类型的默认参数，像PyLint这样的代码检查工具也会对这种代码提出质疑和警告。

```
[10, 'a']
[123]
[10, 'a']
```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目011：Python中为什么没有函数重载？

> **点评**：C++、Java、C#等诸多编程语言都支持函数重载，所谓函数重载指的是在同一个作用域中有多个同名函数，它们拥有不同的参数列表（参数个数不同或参数类型不同或二者皆不同），可以相互区分。重载也是一种多态性，因为通常是在编译时通过参数的个数和类型来确定到底调用哪个重载函数，所以也被称为编译时多态性或者叫前绑定。这个问题的潜台词其实是问面试者是否有其他编程语言的经验，是否理解Python是动态类型语言，是否知道Python中函数的可变参数、关键字参数这些概念。

首先Python是解释型语言，函数重载现象通常出现在编译型语言中。其次Python是动态类型语言，函数的参数没有类型约束，也就无法根据参数类型来区分重载。再者Python中函数的参数可以有默认值，可以使用可变参数和关键字参数，因此即便没有函数重载，也要可以让一个函数根据调用者传入的参数产生不同的行为。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目012：用Python代码实现Python内置函数max。

> **点评**：这个题目看似简单，但实际上还是比较考察面试者的功底。因为Python内置的`max`函数既可以传入可迭代对象找出最大，又可以传入两个或多个参数找出最大；最为关键的是还可以通过命名关键字参数`key`来指定一个用于元素比较的函数，还可以通过`default`命名关键字参数来指定当可迭代对象为空时返回的默认值。

下面的代码仅供参考：

```Python
def my_max(*args, key=None, default=None):
    """
    获取可迭代对象中最大的元素或两个及以上实参中最大的元素
    :param args: 一个可迭代对象或多个元素
    :param key: 提取用于元素比较的特征值的函数，默认为None
    :param default: 如果可迭代对象为空则返回该默认值，如果没有给默认值则引发ValueError异常
    :return: 返回可迭代对象或多个元素中的最大元素
    """
    if len(args) == 1 and len(args[0]) == 0:
        if default:
            return default
        else:
            raise ValueError('max() arg is an empty sequence')
    items = args[0] if len(args) == 1 else args
    max_elem, max_value = items[0], items[0]
    if key:
        max_value = key(max_value)
    for item in items:
        value = item
        if key:
            value = key(item)
        if value > max_value:
            max_elem, max_value = item, value
    return max_elem
```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目25：写一个记录函数执行时间的装饰器。

> **点评**：高频面试题，也是最简单的装饰器，面试者**必须要掌握的内容**。

方法一：用函数实现装饰器。

```Python
from functools import wraps
from time import time


def record_time(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f'{func.__name__}执行时间: {time() - start}秒')
        return result
        
    return wrapper
```

方法二：用类实现装饰器。类有`__call__`魔术方法，该类对象就是可调用对象，可以当做装饰器来使用。

```Python
from functools import wraps
from time import time


class Record:
    
    def __call__(self, func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            print(f'{func.__name__}执行时间: {time() - start}秒')
            return result
        
        return wrapper
```

> **说明**：装饰器可以用来装饰类或函数，为其提供额外的能力，属于设计模式中的**代理模式**。

> **扩展**：**装饰器本身也可以参数化**，例如上面的例子中，如果不希望在终端中显示函数的执行时间而是希望由调用者来决定如何输出函数的执行时间，可以通过参数化装饰器的方式来做到，代码如下所示。

```Python
from functools import wraps
from time import time


def record_time(output):
    """可以参数化的装饰器"""
	
	def decorate(func):
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			start = time()
			result = func(*args, **kwargs)
			output(func.__name__, time() - start)
			return result
            
		return wrapper
	
	return decorate
```

#### 题目48：按照题目要求写出对应的装饰器。

> **要求**：有一个通过网络获取数据的函数（可能会因为网络原因出现异常），写一个装饰器让这个函数在出现指定异常时可以重试指定的次数，并在每次重试之前随机延迟一段时间，最长延迟时间可以通过参数进行控制。

方法一：

```Python
from functools import wraps
from random import random
from time import sleep


def retry(*, retry_times=3, max_wait_secs=5, errors=(Exception, )):

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except errors:
                    sleep(random() * max_wait_secs)
            return None

        return wrapper

    return decorate
```

方法二：

```Python
from functools import wraps
from random import random
from time import sleep


class Retry(object):

    def __init__(self, *, retry_times=3, max_wait_secs=5, errors=(Exception, )):
        self.retry_times = retry_times
        self.max_wait_secs = max_wait_secs
        self.errors = errors

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return func(*args, **kwargs)
                except self.errors:
                    sleep(random() * self.max_wait_secs)
            return None

        return wrapper
```

> **点评**：我们不止一次强调过，装饰器几乎是Python面试必问内容，这个题目比之前的题目稍微复杂一些，它需要的是一个参数化的装饰器。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目008：说一下你对Python中迭代器和生成器的理解。

> **点评**：很多人面试者都会写迭代器和生成器，但是却无法准确的解释什么是迭代器和生成器。如果你也有同样的困惑，可以参考下面的回答。

迭代器是实现了迭代器协议的对象。跟其他编程语言不通，Python中没有用于定义协议或表示约定的关键字，像`interface`、`protocol`这些单词并不在Python语言的关键字列表中。Python语言通过魔法方法来表示约定，也就是我们所说的协议，而`__next__`和`__iter__`这两个魔法方法就代表了迭代器协议。可以通过`for-in`循环从迭代器对象中取出值，也可以使用`next`函数取出迭代器对象中的下一个值。生成器是迭代器的语法升级版本，可以用更为简单的代码来实现一个迭代器。

> **扩展**：面试中经常让写生成斐波那契数列的迭代器，大家可以参考下面的代码。
>
> ```Python
> class Fib(object):
>  
>  def __init__(self, num):
>      self.num = num
>      self.a, self.b = 0, 1
>      self.idx = 0
> 
>  def __iter__(self):
>      return self
> 
>  def __next__(self):
>      if self.idx < self.num:
>          self.a, self.b = self.b, self.a + self.b
>          self.idx += 1
>          return self.a
>      raise StopIteration()
> ```
>
> 如果用生成器的语法来改写上面的代码，代码会简单优雅很多。
>
> ```Python
> def fib(num):
>  a, b = 0, 1
>  for _ in range(num):
>      a, b = b, a + b
>      yield a
> ```

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目010：下面这段代码的执行结果是什么。

```Python
def multiply():
    return [lambda x: i * x for i in range(4)]

print([m(100) for m in multiply()])
```

运行结果：

```
[300, 300, 300, 300]
```

上面代码的运行结果很容易被误判为`[0, 100, 200, 300]`。首先需要注意的是`multiply`函数用生成式语法返回了一个列表，列表中保存了4个Lambda函数，这4个Lambda函数会返回传入的参数乘以`i`的结果。需要注意的是这里有闭包（closure）现象，`multiply`函数中的局部变量`i`的生命周期被延展了，由于`i`最终的值是`3`，所以通过`m(100)`调列表中的Lambda函数时会返回`300`，而且4个调用都是如此。

如果想得到`[0, 100, 200, 300]`这个结果，可以按照下面几种方式来修改`multiply`函数。

方法一：使用生成器，让函数获得`i`的当前值。

```Python
def multiply():
    return (lambda x: i * x for i in range(4))

print([m(100) for m in multiply()])
```

或者

```Python
def multiply():
    for i in range(4):
        yield lambda x: x * i

print([m(100) for m in multiply()])
```

方法二：使用偏函数，彻底避开闭包。

```Python
from functools import partial
from operator import __mul__

def multiply():
    return [partial(__mul__, i) for i in range(4)]

print([m(100) for m in multiply()])
```

#### 题目28：说一下你对闭包的理解。

闭包是支持一等函数的编程语言（Python、JavaScript等）中实现词法绑定的一种技术。当捕捉闭包的时候，它的自由变量（在函数外部定义但在函数内部使用的变量）会在捕捉时被确定，这样即便脱离了捕捉时的上下文，它也能照常运行。简单的说，可以将闭包理解为**能够读取其他函数内部变量的函数**。正在情况下，函数的局部变量在函数调用结束之后就结束了生命周期，但是**闭包使得局部变量的生命周期得到了延展**。使用闭包的时候需要注意，闭包会使得函数中创建的对象不会被垃圾回收，可能会导致很大的内存开销，所以**闭包一定不能滥用**。
