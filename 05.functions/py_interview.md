##### 求以下代码的输出结果
```python
collapse=True
processFunc=collapse and (lambda s:' '.join(s.split())) or (lambda s:s)
print(processFunc('i\tam\ntest\tproject!'))

collapse=False
processFunc=collapse and (lambda s:' '.join(s.split())) or (lambda s:s)
print(processFunc('i\tam\ntest\tproject!'))
```
* 答案：
>i am test project!
>i       am
>test    project!

---

##### *arg和**kwargs的作用
* 用来接收不确定个数的参数，*args通常用来接收不确定个数的非关键字参数，而**kwargs通常用来接收不确定个数的关键字参数

##### 如何在函数中设置一个全局变量？
* 在函数中使用global关键字定义变量

---

##### 一行代码通过filter和lambda函数输出alist=[1,22,2,33,23,32]中索引为奇数的值
```python
alist=[1,22,2,33,23,32]
ss=[x[1] for x in filter(lambda x:x[0]%2==1,enumerate(alist))]
print(ss)
```

---

##### filter、map、reduce的作用。
1. filter() 相当于过滤器的作用
 ```python
s=[1,2,3,5,6,8,9,10,25,12,30]
# 筛选出3的倍数
# 第一个参数为一个返回True或者False的函数，第二个参数为可迭代对象
# 该函数把可迭代对象依次传入第一个函数，如果为True，则筛选
d=filter(lambda x:True if x % 3 == 0 else False,s)
print(list(d))
 ```
2. map()函数，
```python
# 第一个参数为函数，依次将后面的参数传给第一个函数，并执行函数
# 如果有多个参数则，依次将后面的对应传给参数
s=map(lambda x,y:x+y,range(10),range(10))
print(list(s))
ss=map(lambda x:x*x,range(10))
print(list(ss))
```
3. reduce()函数
```python
from functools import reduce
# 开始的时候将可迭代对象的第一个数和第二个数当成x和y
# 然后将第一次函数的执行结果当成x，然后再传入一个数当成y
# 再执行函数
s=reduce(lambda x,y:x+y,range(101))
print(s) # 相当于0+1+2+……+99+100
```

---

##### 是否使用过functools中的函数？他的作用是什么？
1. functools.wraps()
    * 在装饰器中用过，如果不使用wraps，则原始函数的__name__和__doc__的值就会丢失
 2. functools.reduce()
     * 第一个参数是一个函数，第二个参数是一个可迭代对象，代码如下：
```python
# 下面代码相当于从1加到9
from functools import reduce
a=reduce(lambda x,y:x+y,range(10))
print(a)
```

---

##### lambda表达式格式以及应用场景？
* 格式：lambda 参数列表 : 返回表达式
* 应用场景：常见的在filter，reduce以及map中使用。

---

##### 求以下代码结果：
```python
def num():
    return [lambda x:i*x for i in range(4)]
print([m(2) for m in num()])
```
* 答案：[6,6,6,6]

---

##### yield from 和 yield 的区别
[简述yield和yield from](https://blog.csdn.net/lamusique/article/details/85845225)

```python
# 下面a()和b()是等价的
def a():
    yield from [1,2,3,4,5]
def b():
    for i in [1,2,3,4,5]:
        yield i
for i in a():
    print(i)
for i in b():
    print(i)
```
* yield将一个函数变成一个生成器
* yield 返回一个值
* yield from后面接可迭代对象，一个一个返回值。

---

##### 下面代码的执行结果是
```python
a=1
def bar():
    a+=3
    
bar()
print(a)
```
* 答案：运行出错

---

##### 如何判断一个值是方法还是函数？
[参考链接](https://blog.csdn.net/amoscn/article/details/77074403)
1. 使用type()来判断，如果是method为方法，如果是function则是函数。
2. 与类和实例无绑定关系的function都属于函数（function）
3. 与类和实例有绑定关系的function都属于方法

---

##### python如何定义函数时如何书写可变参数和关键字参数？
```python
def func(a,*args,b=1,**kwargs):
    pass
```

##### python中enumerate的意思是什么？
* 枚举的意思，同时得到可迭代对象，如列表和元组的索引和值，以元组形式返回

---

##### 使用生成器编写一个函数实现生成指定个数的斐波那契数列
```python
def fib2(imax):
    t,a,b=0,0,1
    while t<imax:
        yield b
        a,b=b,a+b
        t+=1
        
for i in fib2(10):
    print(i)
```

---

##### 生成器与函数的区别？
* 生成器和函数的主要区别在于函数 return a value，生成器 yield a value同时标记或记忆point of the yield 以便于在下次调用时从标记点恢复执行。 yield 使函数转换成生成器，而生成器反过来又返回迭代器。
```python
# 简单实现生成器
def dec():
    n=0
    for i in range(10):
        yield n
        n+=i
        
for i in dec():
    print(i)
```

##### 列表推导式[i for i in range(10)]和生成式表达式(i for i in range(10))的区别
[参考文章](https://blog.csdn.net/qq_36523839/article/details/79807866)

1. 列表推导式的结果是一个列表。
2. 生成器表达式的结果是一个生成器，它和列表推导式类似，它一次处理一个对象，而不是一口气处理和构造整个数据结构，可以节约内存。

---

##### 简述生成器，迭代器，装饰器以及应用场景
[参考链接](https://blog.csdn.net/weixin_39387409/article/details/85089652)

1. 迭代器对象实现了iter()方法
2. 迭代器实现了iter()和next()方法，迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束
3. 生成器是迭代器的一种，一个函数调用时返回一个迭代器，这个函数就叫生成器。通常带有yield
4. 装饰器是一个以函数作为参数，并返回一个替换函数的可执行函数，是闭包的一种应用。通常用来给一个函数添加功能

---

#### 写出如下代码的输出结果
[参考链接](https://www.cnblogs.com/z-x-y/p/9157238.html)

```python
def decorator_a(func):
    print('Get in decorator_a')
    def inner_a(*args, **kwargs):
        print('Get in inner_a')
        return func(*args, **kwargs)
    return inner_a
    
def decorator_b(func):
    print('Get in decorator_b')
    def inner_b(*args, **kwargs):
        print('Get in inner_b')
        return func(*args, **kwargs)
    return inner_b
    
@decorator_b #f=decorator_b(f)
@decorator_a #f=decorator_a(f)
def f(x):
    print('Get in f')
    return x * 2
f(1)
```
* 答案
>Get in decorator_a
>Get in decorator_b
>Get in inner_b
>Get in inner_a
>Get in f

* 解释
 >当我们对f传入参数1进行调用时，inner_b被调用了，他会先打印Get in inner_b,然后在inner_b内部调用了inner_a,所以会再打印Get in inner_a,然后再inner_a内部调用原来的f,并且将结果作为最终的返回总结：装饰器函数在被装饰函数定义好后立即执行从下往上执行函数调用时从上到下执行

---

##### 实现一个装饰器，通过一次调用，使函数重复执行5次
```python
from functools import wraps
def dec(func):
    @wraps(func)
    def inner(*args,**kwargs):
        result=[func(*args,**kwargs) for i in range(5)]
        return result
    return inner
    
@dec
def add(x,y):
    return x+y
print(add(1,2))
```

---

##### 实现一个装饰器，限制该函数被调用的频率，如10秒一次

```python
import time
from functools import wraps
def dec(func):
    key=func.__name__
    cache={key:None}
    @wraps(func)
    def inner(*args,**kwargs):
        result=None
        if cache.get(key) is None:
            cache[key]=time.time()
            result=func(*args,**kwargs)
            print('执行函数中')
        else:
            now=time.time()
            if now-cache[key]>10:
                cache[key]=now
                result=func(*args,**kwargs)
                print('执行函数中')
            else:
                print('函数执行受限')
        return result
    return inner
    
@dec
def add(x,y):
    print(x+y)
    
add(1,2)
add(1,3)
time.sleep(10)
add(3,4)
```

---

##### python递归的最大层数？
* 1000

---

##### 什么是闭包
* 在函数中可以（嵌套）定义另一个函数时，如果内部的函数引用了外部的函数的变量，则可能产生闭包。闭包可以用来在一个函数与一组“私有”变量之间创建关联关系。在给定函数被多次调用的过程中，这些私有变量能够保持其持久性。
```python
# 内部函数使用了外部函数的变量，就相当于闭包
def func1():
    a=1
    def inner():
        return a
    return inner
print(func1()())
```
