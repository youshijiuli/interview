### Python语言特性

#### 3 @staticmethod和@classmethod
Python其实有3个方法,即静态方法(staticmethod),类方法(classmethod)和实例方法,如下:

class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)

    @classmethod
    def class_foo(cls,x):
        print( "executing class_foo(%s,%s)"%(cls,x))

    @staticmethod
    def static_foo(x):
        print ("executing static_foo(%s)"%x)

a=A()
这里先理解下函数参数里面的self和cls.这个self和cls是对类或者实例的绑定.对于实例方法,我们知道在类里每次定义方法的时候都需要绑定这个实例,就是foo(self, x),为什么要这么做呢?因为实例方法的调用离不开实例,我们需要把实例自己传给函数,调用的时候是这样的a.foo(x)(其实是foo(a, x)).类方法一样,只不过它传递的是类而不是实例,A.class_foo(x).注意这里的self和cls可以替换别的参数,但是python的约定是这俩,还是不要改的好.
对于静态方法其实和普通的方法一样,不需要对谁进行绑定,唯一的区别是调用的时候需要使用a.static_foo(x)或者A.static_foo(x)来调用.
\	实例方法	类方法	静态方法
a = A()	a.foo(x)	a.class_foo(x)	a.static_foo(x)
A	不可用	A.class_foo(x)	A.static_foo(x)
#### 4 类变量和实例变量

    class Person:
    name="aaa"

p1=Person()
p2=Person()
p1.name="bbb"
print(p1.name)  # bbb
print(p2.name)  # aaa
print(Person.name)  # aaa
类变量就是供类使用的变量,实例变量就是供实例使用的.
这里p1.name="bbb"是实例调用了类变量,这其实和上面第一个问题一样,就是函数传参的问题,p1.name一开始是指向的类变量name="aaa",但是在实例的作用域里把类变量的引用改变了,就变成了一个实例变量,self.name不再引用Person的类变量name了.
可以看看下面的例子:

    class Person:
    name=[]

p1=Person()
p2=Person()
p1.name.append(1)
print(p1.name)  # [1]
print(p2.name)  # [1]
print(Person.name)  # [1]
#### 5 Python自省
这个也是python彪悍的特性.
自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.简单一句就是运行时能够获得对象的类型.比如type(),dir(),getattr(),hasattr(),isinstance().
#### 7 Python中单下划线和双下划线
```
1	>>> class MyClass():
2 ...     def __init__(self):
3 ...             self.__superprivate = "Hello"
4 ...             self._semiprivate = ", world!"
5 ...
6 >>> mc = MyClass()
7 >>> print(mc.__superprivate)
8 Traceback (most recent call last):
9  File "<stdin>", line 1, in <module>
10 AttributeError: myClass instance has no attribute '__superprivate'
11 >>> print(mc._semiprivate)
12 , world!
13 >>> print mc.__dict__
14 {'_MyClass__superprivate': 'Hello', '_semiprivate': ', world!'}
```
__foo__:一种约定,Python内部的名字,用来区别其他用户自定义的命名,以防冲突.
-foo:一种约定,用来指定变量私有.程序员用来指定私有变量的一种方式.
-foo:这个有真正的意义:解析器用_classname__foo来代替这个名字,以区别和其他类相同的命名.
详情见:
http://www.zhihu.com/question/19754941

#### 12 鸭子类型
“当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”
我们并不关心对象是什么类型，到底是不是鸭子，只关心行为。
比如在python中，有很多file-like的东西，比如StringIO,GzipFile,socket。它们有很多相同的方法，我们把它们当作文件使用。
又比如list.extend()方法中,我们并不关心它的参数是不是list,只要它是可迭代的,所以它的参数可以是list/tuple/dict/字符串/生成器等.
鸭子类型在动态语言中经常使用，非常灵活，使得python不想java那样专门去弄一大堆的设计模式。
#### 14 新式类和旧式类
这个面试官问了,我说了老半天,不知道他问的真正意图是什么.
这篇文章很好的介绍了新式类的特性: http://www.cnblogs.com/btchenguang/archive/2012/09/17/2689146.html
新式类很早在2.2就出现了,所以旧式类完全是兼容的问题,Python3里的类全部都是新式类.这里有一个MRO问题可以了解下(新式类是广度优先,旧式类是深度优先),<Python核心编程>里讲的也很多.
#### 15 __new__和__init__的区别;
```
这个__new__确实很少见到,先做了解吧.
1.	__new__是一个静态方法,而__init__是一个实例方法.
2.	__new__方法会返回一个创建的实例,而__init__什么都不返回.
3.	只有在__new__返回一个cls的实例时后面的__init__才能被调用.
4.	当创建一个新实例时调用__new__,初始化一个实例时用__init__.
ps: __metaclass__是创建类时起作用.所以我们可以分别使用__metaclass__,__new__和__init__来分别在类创建,实例创建和实例初始化的时候做一些小手脚.
```
#### 16 单例模式
这个绝对常考啊.绝对要记住1~2个方法,当时面试官是让手写的.
##### 1 使用__new__方法
```
    class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class MyClass(Singleton):
    a = 1
```
##### 2 共享属性
创建实例时把所有实例的__dict__指向同一个字典,这样它们具有相同的属性和方法.
```
1	class Borg(object):
2    _state = {}
3    def __new__(cls, *args, **kw):
4        ob = super(Borg, cls).__new__(cls, *args, **kw)
5        ob.__dict__ = cls._state
6      return ob
7
8 class MyClass2(Borg):
9    a = 1
```
##### 3 装饰器版本
```
1	def singleton(cls, *args, **kw):
2    instances = {}
3  def getinstance():
4        if cls not in instances:
5            instances[cls] = cls(*args, **kw)
6        return instances[cls]
7    return getinstance
8
9 @singleton
10 class MyClass:
```
##### 4 import方法
作为python的模块是天然的单例模式
```
    # mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass

my_singleton = My_Singleton()

# to use
from mysingleton import my_singleton

my_singleton.foo()
```
#### 35 阅读下面的代码，它的输出结果是什么？
class A(object):
    def go(self):
        print "go A go!"
    def stop(self):
        print "stop A stop!"
    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print "go B go!"

class C(A):
    def go(self):
        super(C, self).go()
        print "go C go!"
    def stop(self):
        super(C, self).stop()
        print "stop C stop!"

class D(B,C):
    def go(self):
        super(D, self).go()
        print "go D go!"
    def stop(self):
        super(D, self).stop()
        print "stop D stop!"
    def pause(self):
        print "wait D wait!"

class E(B,C): pass

a = A()
b = B()
c = C()
d = D()
e = E()

# 说明下列代码的输出结果

a.go()
b.go()
c.go()
d.go()
e.go()

a.stop()
b.stop()
c.stop()
d.stop()
e.stop()

a.pause()
b.pause()
c.pause()
d.pause()
e.pause()
答案
输出结果以注释的形式表示：
a.go()
# go A go!

b.go()
# go A go!
# go B go!

c.go()
# go A go!
# go C go!

d.go()
# go A go!
# go C go!
# go B go!
# go D go!

e.go()
# go A go!
# go C go!
# go B go!

a.stop()
# stop A stop!

b.stop()
# stop A stop!

c.stop()
# stop A stop!
# stop C stop!

d.stop()
# stop A stop!
# stop C stop!
# stop D stop!

e.stop()
# stop A stop!

a.pause()
# ... Exception: Not Implemented

b.pause()
# ... Exception: Not Implemented

c.pause()
# ... Exception: Not Implemented

d.pause()
# wait D wait!

e.pause()
# ...Exception: Not Implemented
为什么提这个问题？
因为面向对象的编程真的真的很重要。不骗你。答对这道问题说明你理解了继承和Python中super函数的用法。

#### 36 阅读下面的代码，它的输出结果是什么？
```
class Node(object):
    def __init__(self,sName):
        self._lChildren = []
        self.sName = sName
    def __repr__(self):
        return "<Node '{}'>".format(self.sName)
    def append(self,*args,**kwargs):
        self._lChildren.append(*args,**kwargs)
    def print_all_1(self):
        print self
        for oChild in self._lChildren:
            oChild.print_all_1()
    def print_all_2(self):
        def gen(o):
            lAll = [o,]
            while lAll:
                oNext = lAll.pop(0)
                lAll.extend(oNext._lChildren)
                yield oNext
        for oNode in gen(self):
            print oNode

oRoot = Node("root")
oChild1 = Node("child1")
oChild2 = Node("child2")
oChild3 = Node("child3")
oChild4 = Node("child4")
oChild5 = Node("child5")
oChild6 = Node("child6")
oChild7 = Node("child7")
oChild8 = Node("child8")
oChild9 = Node("child9")
oChild10 = Node("child10")

oRoot.append(oChild1)
oRoot.append(oChild2)
oRoot.append(oChild3)
oChild1.append(oChild4)
oChild1.append(oChild5)
oChild2.append(oChild6)
oChild4.append(oChild7)
oChild3.append(oChild8)
oChild3.append(oChild9)
oChild6.append(oChild10)

# 说明下面代码的输出结果

oRoot.print_all_1()
oRoot.print_all_2()
```
```
答案
oRoot.print_all_1()会打印下面的结果：
<Node 'root'>
<Node 'child1'>
<Node 'child4'>
<Node 'child7'>
<Node 'child5'>
<Node 'child2'>
<Node 'child6'>
<Node 'child10'>
<Node 'child3'>
<Node 'child8'>
<Node 'child9'>
oRoot.print_all_1()会打印下面的结果：
<Node 'root'>
<Node 'child1'>
<Node 'child2'>
<Node 'child3'>
<Node 'child4'>
<Node 'child5'>
<Node 'child6'>
<Node 'child8'>
<Node 'child9'>
<Node 'child7'>
<Node 'child10'>
```
为什么提这个问题？
因为对象的精髓就在于组合（composition）与对象构造（object construction）。对象需要有组合成分构成，而且得以某种方式初始化。这里也涉及到递归和生成器（generator）的使用。
生成器是很棒的数据类型。你可以只通过构造一个很长的列表，然后打印列表的内容，就可以取得与print_all_2类似的功能。生成器还有一个好处，就是不用占据很多内存。
有一点还值得指出，就是print_all_1会以深度优先（depth-first）的方式遍历树(tree),而print_all_2则是宽度优先（width-first）。有时候，一种遍历方式比另一种更合适。但这要看你的应用的具体情况。

#### 52 super init
super() lets you avoid referring to the base class explicitly, which can be nice. But the main advantage comes with multiple inheritance, where all sorts of fun stuff can happen. See the standard docs on super if you haven't already.

Note that the syntax changed in Python 3.0: you can just say super().<code>__init__</code>() instead of super(ChildB, self).<code>__init__</code>() which IMO is quite a bit nicer.
http://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
[http://blog.csdn.net/mrlevo520/article/details/51712440](http://blog.csdn.net/mrlevo520/article/details/51712440)
