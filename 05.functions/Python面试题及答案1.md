### Python语言特性

#### 1 Python的函数参数传递
看两个如下例子，分析运行结果:
代码一：

a = 1
def fun(a):
    a = 2
fun(a)
print(a)  # 1

代码二：

a = []
def fun(a):
a.append(1)
fun(a)
print(a)  # [1]

所有的变量都可以理解是内存中一个对象的“引用”，或者，也可以看似c中void*的感觉。
这里记住的是类型是属于对象的，而不是变量。而对象有两种,“可更改”（mutable）与“不可更改”（immutable）对象。在python中，strings, tuples, 和numbers是不可更改的对象，而list,dict等则是可以修改的对象。(这就是这个问题的重点)
当一个引用传递给函数的时候,函数自动复制一份引用,这个函数里的引用和外边的引用没有半毛关系了.所以第一个例子里函数把引用指向了一个不可变对象,当函数返回的时候,外面的引用没半毛感觉.而第二个例子就不一样了,函数内的引用指向的是可变对象,对它的操作就和定位了指针地址一样,在内存里进行修改.
#### 2 Python中的元类(metaclass)
元类就是用来创建类的“东西”。你创建类就是为了创建类的实例对象，但是我们已经学习到了Python中的类也是对象。好吧，元类就是用来创建这些类（对象）的，元类就是类的类
这个非常的不常用,详情请看：《深刻理解Python中的元类(metaclass)》
#### 9 迭代器和生成器
在Python中，这种一边循环一边计算的机制，称为生成器：generator。
可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。

这个是stackoverflow里python排名第一的问题,值得一看: http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
#### 10 * args and ** kwargs
用*args和**kwargs只是为了方便并没有强制使用它们.
当你不确定你的函数里将要传递多少参数时你可以用*args.例如,它可以传递任意数量的参数:
```
1	>>> def print_everything(*args):
2     for count, thing in enumerate(args):
3 ...       print '{0}. {1}'.format(count, thing)
4 ..
5 >>> print_everything('apple', 'banana', 'cabbage')
6 0. apple
7 1. banana
8 2. cabbage
```
相似的 ** kwargs允许你使用没有事先定义的参数名:
```
1	>>> def table_things(**kwargs):
2 ...     for name, value in kwargs.items():
3 ...         print '{0} = {1}'.format(name, value)
4 ...
5 >>> table_things(apple = 'fruit', cabbage = 'vegetable')
6 cabbage = vegetable
7 apple = fruit
```
你也可以混着用.命名参数首先获得参数值然后所有的其他参数都传递给*args和**kwargs.命名参数在列表的最前端.例如:
```
1	def table_things(titlestring, ** kwargs)
```
* args和** kwargs可以同时在函数的定义中,但是*args必须在**kwargs前面.
当调用函数时你也可以用*和**语法.例如:
```
1	>>> def print_three_things(a, b, c):
2 ...     print 'a = {0}, b = {1}, c = {2}'.format(a,b,c)
3 ...
4 >>> mylist = ['aardvark', 'baboon', 'cat']
5 >>> print_three_things(*mylist)
6
7 a = aardvark, b = baboon, c = cat
```
就像你看到的一样,它可以传递列表(或者元组)的每一项并把它们解包.注意必须与它们在函数里的参数相吻合.当然,你也可以在函数定义或者函数调用时用*.
http://stackoverflow.com/questions/3394835/args-and-kwargs
#### 11 面向切面编程AOP和装饰器
这个AOP一听起来有点懵,同学面试的时候就被问懵了…
装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量函数中与函数功能本身无关的雷同代码并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。
这个问题比较大,推荐: http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python
中文: http://taizilongxu.gitbooks.io/stackoverflow-about-python/content/3/README.html
#### 13 Python中重载
引自知乎:http://www.zhihu.com/question/20053359
函数重载主要是为了解决两个问题。
1.	可变参数类型。
2.	可变参数个数。
另外，一个基本的设计原则是，仅仅当两个函数除了参数类型和参数个数不同以外，其功能是完全相同的，此时才使用函数重载，如果两个函数的功能其实不同，那么不应当使用重载，而应当使用一个名字不同的函数。
好吧，那么对于情况 1 ，函数功能相同，但是参数类型不同，python 如何处理？答案是根本不需要处理，因为 python 可以接受任何类型的参数，如果函数的功能相同，那么不同的参数类型在 python 中很可能是相同的代码，没有必要做成两个不同函数。
那么对于情况 2 ，函数功能相同，但参数个数不同，python 如何处理？大家知道，答案就是缺省参数。对那些缺少的参数设定为缺省参数即可解决问题。因为你假设函数功能相同，那么那些缺少的参数终归是需要用的。
好了，鉴于情况 1 跟 情况 2 都有了解决方案，python 自然就不需要函数重载了。
#### 17 Python中的作用域
Python 中，一个变量的作用域总是由在代码中被赋值的地方所决定的。
当 Python 遇到一个变量的话他会按照这样的顺序进行搜索：
本地作用域（Local）→当前作用域被嵌入的本地作用域（Enclosing locals）→全局/模块作用域（Global）→内置作用域（Built-in）
#### 20 闭包
闭包(closure)是函数式编程的重要的语法结构。闭包也是一种组织代码的结构，它同样提高了代码的可重复使用性。
当一个内嵌函数引用其外部作作用域的变量,我们就会得到一个闭包. 总结一下,创建一个闭包必须满足以下几点:
1.	必须有一个内嵌函数
2.	内嵌函数必须引用外部函数中的变量
3.	外部函数的返回值必须是内嵌函数
感觉闭包还是有难度的,几句话是说不明白的,还是查查相关资料.
重点是函数运行后并不会被撤销,就像16题的instance字典一样,当函数运行完后,instance并不被销毁,而是继续留在内存空间里.这个功能类似类里的类变量,只不过迁移到了函数上.
闭包就像个空心球一样,你知道外面和里面,但你不知道中间是什么样.
#### 21 lambda函数
其实就是一个匿名函数,为什么叫lambda?因为和后面的函数式编程有关.
#### 22 Python函数式编程
这个需要适当的了解一下吧,毕竟函数式编程在Python中也做了引用.
python中函数式编程支持:
filter 函数的功能相当于过滤器。调用一个布尔函数bool_func来迭代遍历每个seq中的元素；返回一个使bool_seq返回值为true的元素的序列。
```
    >>>a = [1,2,3,4,5,6,7]
>>>b = filter(lambda x: x > 5, a)
>>>print b
>>>[6,7]
map函数是对一个序列的每个项依次执行函数，下面是对一个序列每个项都乘以2：

    >>> a = map(lambda x:x*2,[1,2,3])
>>> list(a)
[2, 4, 6]
reduce函数是对一个序列的每个项迭代调用函数，下面是求3的阶乘：

    >>> reduce(lambda x,y:x*y,range(1,4))
6
```
#### 30 补充缺失的代码
def print_directory_contents(sPath):
    """
    这个函数接受文件夹的名称作为输入参数，
    返回该文件夹中文件的路径，
    以及其包含文件夹中文件的路径。
    """
    # 补充代码
答案
def print_directory_contents(sPath):
    import os                                       
    for sChild in os.listdir(sPath):                
        sChildPath = os.path.join(sPath,sChild)
        if os.path.isdir(sChildPath):
            print_directory_contents(sChildPath)
        else:
            print sChildPath
特别要注意以下几点：
•	命名规范要统一。如果样本代码中能够看出命名规范，遵循其已有的规范。
•	递归函数需要递归并终止。确保你明白其中的原理，否则你将面临无休无止的调用栈（callstack）。
•	我们使用os模块与操作系统进行交互，同时做到交互方式是可以跨平台的。你可以把代码写成sChildPath = sPath + '/' + sChild，但是这个在Windows系统上会出错。
•	熟悉基础模块是非常有价值的，但是别想破脑袋都背下来，记住Google是你工作中的良师益友。
•	如果你不明白代码的预期功能，就大胆提问。
•	坚持KISS原则！保持简单，不过脑子就能懂！
为什么提这个问题：
•	说明面试者对与操作系统交互的基础知识
•	递归真是太好用啦
#### 32 下面代码会输出什么：
def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
    print(l)

f(2)
f(3,[3,2,1])
f(3)
答案：
[0, 1]
[3, 2, 1, 0, 1, 4]
[0, 1, 0, 1, 4]
呃？
第一个函数调用十分明显，for循环先后将0和1添加至了空列表l中。l是变量的名字，指向内存中存储的一个列表。第二个函数调用在一块新的内存中创建了新的列表。l这时指向了新生成的列表。之后再往新列表中添加0、1和4。很棒吧。第三个函数调用的结果就有些奇怪了。它使用了之前内存地址中存储的旧列表。这就是为什么它的前两个元素是0和1了。

#### 34 “猴子补丁”（monkey patching）指的是什么？这种做法好吗？
答案：
“猴子补丁”就是指，在函数或对象已经定义之后，再去改变它们的行为。
举个例子：
import datetime
datetime.datetime.now = lambda: datetime.datetime(2012, 12, 12)
大部分情况下，这是种很不好的做法 - 因为函数在代码库中的行为最好是都保持一致。打“猴子补丁”的原因可能是为了测试。mock包对实现这个目的很有帮助。
为什么提这个问题？
答对这个问题说明你对单元测试的方法有一定了解。你如果提到要避免“猴子补丁”，可以说明你不是那种喜欢花里胡哨代码的程序员（公司里就有这种人，跟他们共事真是糟糕透了），而是更注重可维护性。还记得KISS原则码？答对这个问题还说明你明白一些Python底层运作的方式，函数实际是如何存储、调用等等。
另外：如果你没读过mock模块的话，真的值得花时间读一读。这个模块非常有用。

#### 44 如何在一个function里面设置一个全局的变量？
答：解决方法是在function的开始插入一个global声明：
def f()
global x
