# python-面试通关宝典

### **其他内容**

#### 83.解释一下 Python 中 pass 语句的作用。

```markdown
Python pass 是空语句，是为了保持程序结构的完整性。

pass 不做任何事情，一般用做占位语句。
```

#### 84.简述你对 input() 函数的理解。

```
在python3中，input()获取用户输入，不论用户输入的是什么，获取到的都是字符串类型的。
```

#### 85.Python 中的 is 和 == 有什么区别？

```markdown
is比较的是两个对象的id值是否相等，也就是比较两个对象是否为同一个实例对象，是否指向同一个内存地址。

==比较的是两个对象的内容是否相等，默认会调用对象的__eq__()方法。
```

#### 86.Python 中的作用域有哪些？

```python
L （Local） 局部作用域
E （Enclosing） 闭包函数外的函数中
G （Global） 全局作用域
B （Built-in） 内建作用域
```

#### 87.三元运算写法和应用场景。

```python
条件语句比较简单时可以使用三元运算符，最常见的就是 
res = 'test True' if expression is True else 'test False'
```

#### 88.了解 enumerate 吗？

```python
# 遍历列表时候，携带索引index
a = ['a','b','c']
for index,item in enumerate(a):
    print(index,item)
```

#### 89.列举 5 个 Python 中的标准模块。

```python
json,re,random,datetime,codecs
```

#### 90.如何在函数中设置一个全局变量？

```Python
使用global关键字
```

#### 91.pathlib 的用法举例。

```python
from pathlib import Path

data_folder = Path("source_data/text_files/")

file_to_open = data_folder / "raw_data.txt"

f = open(file_to_open)

print(f.read())
```

#### 92.请对 Python 中的异常处理写一个简单的应用场景。

```Python
class NameTooShortError(ValueError): 
    pass
def validate(name):
    if len(name) < 10:
        raise NameTooShortError(name)
        
# 使用自定义异常类，使得发生异常时的错误更容易排查
```

#### 93.Python 中递归的最大次数是多少？如何突破？

```pyhton
python解释器限制最大的递归深度是999，可以通过
import sys
sys.setrecursionlimit(10000)  # set the maximum depth as 10000
重新设置最大递归深度
```

#### 94.什么是面向对象的 MRO？

```
对于支持继承的编程语言来说，其方法（属性）可能定义在当前类，也可能来自于基类，所以在方法调用时就需要对当前类和基类进行搜索以确定方法所在的位置。而搜索的顺序就是所谓的「方法解析顺序」（Method Resolution Order，或MRO）。对于只支持单继承的语言来说，MRO 一般比较简单；而对于 Python 这种支持多继承的语言来说，MRO 就复杂很多。
```

#### 95.简述 isinstance 的作用以及应用场景。

```python
来判断一个对象是否是一个已知的类型
举个栗子：
 p= 'sfa'
 isinstance(p,str)
 True
```

#### 96.什么是断言？并描述一个应用场景。

```python
Python 的断言语句是一种调试工具，用来测试某个断言条件。如果断言条件 为真，则程序将继续正常执行;但如果条件为假，则会引发 AssertionError 异常并显示相关 的错误消息。
```

#### 97.lambda 表达式格式以及应用场景。

```python
d = {'a':2,'b':1,'c':3,'d':'4'}
sorted(d,key=lambda x :x[1]) 
# 将字典d按照值排序
```

#### 98.新式类和旧式类的区别有哪些？

```
Python 有两种类：经典类（classic class）和新式类（new-style class）。两者的不同之处在于新式类继承自 object。在 Python 2.1 以前，经典类是唯一可用的形式；Python 2.2 引入了新式类，使得类和内置类型更加统一；在 Python 3 中，新式类是唯一支持的类。
```

#### 99.dir() 是用来干什么的？

```
dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。
```

#### 100.一个包里有三个模块，demo1.py、demo2.py 和 demo3.py，但使用 from tools import * 导入模块时，如何保证只有 demo1、demo3 被导入？

```python
但若想使用from pacakge_1 import *这种形式的写法，需在  init.py中加上：   all = [‘file_a’, ‘file_b’] #package_1下有file_a.py和file_b.py，在导入时init.py文件将被执行。 
但不建议在 init.py中写模块，以保证该文件简单。不过可在init.py导入我们需要的模块，以便避免一个个导入、方便使用。
```

#### 101.列举 5 个 Python 中的异常类型以及其含义。

```
1. ArithmeticError 此基类用于派生针对各种算术类错误而引发的内置异常: OverflowError, ZeroDivisionError, FloatingPointError
2. BufferError 当与 缓冲区 相关的操作无法执行时将被引发。
3. LookupError 此基类用于派生当映射或序列所使用的键或索引无效时引发的异常: IndexError, KeyError。 这可以通过 codecs.lookup() 来直接引发
4. ImportError 当 import 语句尝试加载模块遇到麻烦时将被引发。 并且当 from ... import 中的 "from list" 存在无法找到的名称时也会被引发
5. IndexError 当序列抽取超出范围时将被引发。 （切片索引会被静默截短到允许的范围；如果指定索引不是整数则 TypeError 会被引发
```

#### 102.copy 和 deepcopy 的区别是什么？

```python
copy 即所谓的浅拷贝，赋值的时候非递归地复制子对象的引用；
deepcopy 即所谓的深拷贝，赋值的时候递归复制子对象。
举个栗子，
xs = [1,2,[2,3,4],3]
ys = xs # 浅拷贝
zs = deepcopy(xs) # 深拷贝
xs[2][0] = 5
print(ys)
[1,2,[2,3,4],3]
print(xs)
[1,2,[5,3,4],3]

print(zs)
[1,2,[5,3,4],3] # 由于深拷贝已经递归复制了子对象，所以内部的List也发生改变

```

#### 103.请阐述代码中经常遇到的 *args, **kwargs 的含义及用法。

```
这两个是python中的可变参数。*args表示任何多个位置参数，它是一个tuple；**kwargs表示关键字参数，它是一个dict。并且同时使用*args和**kwargs时，必须*args参数列要在**kwargs前
```

#### 104.Python 中会有函数或成员变量包含单下划线前缀和结尾，或双下划线前缀结尾，它们的区别是什么？

```python
前置单下划线_var:命名约定，用来表示该名称仅在内部使用。一般对 Python 解释器没 有特殊含义(通配符导入除外)，只能作为对程序员的提示。
后置单下划线 var_:命名约定，用于避免与 Python 关键字发生命名冲突。
前置双下划线__var:在类环境中使用时会触发名称改写，对 Python 解释器有特殊含义。
前后双下划线__var__:表示由 Python 语言定义的特殊方法。在自定义的属性中要避免
使用这种命名方式。
```

#### 105.简述 w、a+ 和 wb 文件写入模式的区别。

```
w:写入时会覆盖上一次的写入
a+:追加写入
wb:以二进制文件形式写入
```

#### 106.举例 sort 和 sorted 的区别。

```
sort()与sorted()的不同在于，sort是在原位重新排列列表，而sorted()是产生一个新的列表
```

#### 107.什么是负索引？

```
负索引和正索引不同，它是从右边开始检索。例如：使用负索引取出列表的最后一个数
lis[-1] # 取出列表的最后一个元素
lis[-2] # 取出列表的倒数第二个元素
```

#### 108.pprint 模块是干什么的？

```
print()和pprint()都是python的打印模块，功能基本一样，唯一的区别就是pprint()模块打印出来的数据结构更加完整，每行为一个数据结构，更加方便阅读打印输出结果。特别是对于特别长的数据打印，print()输出结果都在一行，不方便查看，而pprint()采用分行打印输出，所以对于数据结构比较复杂、数据长度较长的数据，适合采用pprint()打印方式
```

#### 109.解释一下 Python 中的赋值运算符。

```
在python中，使用 = 可以给变量赋值。
在算术运算时，为了简化代码的编写，Python还提供了一系列与算术运算符对应的赋值运算符
例如，c += a 等效于 c=c+a

```

#### 110.解释一下 Python 中的逻辑运算符。

```
and, or, not
```

#### 111.讲讲 Python 中的位运算符。

```
&	按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0	(a & b) 输出结果 12 ，二进制解释： 0000 1100
|	按位或运算符：只要对应的二个二进位有一个为1时，结果位就为1	(a | b) 输出结果 61 ，二进制解释： 0011 1101
^	按位异或运算符：当两对应的二进位相异时，结果为1	(a ^ b) 输出结果 49 ，二进制解释： 0011 0001
~	按位取反运算符：对数据的每个二进制位取反,即把1变为0,把0变为1	(~a ) 输出结果 -61 ，二进制解释： 1100 0011， 在一个有符号二进制数的补码形式。
<<	左移动运算符：运算数的各二进位全部左移若干位，由”<<”右边的数指定移动的位数，高位丢弃，低位补0	a << 2 输出结果 240 ，二进制解释： 1111 0000
>>	右移动运算符：把”>>”左边的运算数的各二进位全部右移若干位，”>>”右边的数指定移动的位数	a >> 2 输出结果 15 ，二进制解释： 0000 1111
```

#### 112.**在 Python 中如何使用多进制数字？**

```
1、二进制数字由0和1组成，我们使用0b或0B前缀表示二进制数

print(int(0b1010))#10
2、使用bin()函数将一个数字转换为它的二进制形式

print(bin(0xf))#0b1111
3、八进制数由数字0-7组成，用前缀0o或0O表示8进制数

print(oct(8))#0o10
4、十六进数由数字0-15组成，用前缀0x或者0X表示16进制数

print(hex(16))#0x10
print(hex(15))#0xf
 
```

#### 113.怎样声明多个变量并赋值？

```python
a,b = 1,2
```
