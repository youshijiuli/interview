# python-面试通关宝典

### **高级特性**
#### 64.简述 Python 垃圾回收机制。

```python
引用计数机制：
python里每一个东西都是对象，它们的核心就是一个结构体：PyObject
 typedef struct_object {
 int ob_refcnt;
 struct_typeobject *ob_type;
} PyObject;

PyObject是每个对象必有的内容，其中ob_refcnt就是做为引用计数。当一个对象有新的引用时，它的ob_refcnt就会增加，当引用它的对象被删除，它的ob_refcnt就会减少
#define Py_INCREF(op)   ((op)->ob_refcnt++) //增加计数
#define Py_DECREF(op) \ //减少计数
    if (--(op)->ob_refcnt != 0) \
        ; \
    else \
        __Py_Dealloc((PyObject *)(op))

当引用计数为0时，该对象生命就结束了。
引用计数机制的优点：

简单
实时性：一旦没有引用，内存就直接释放了。不用像其他机制等到特定时机。实时性还带来一个好处：处理回收内存的时间分摊到了平时

```

#### 78.在 Python 中是如何管理内存的？

```
参考71.
```

#### 79.当退出 Python 时是否释放所有内存分配？

```
答案是否定的。那些具有对象循环引用或者全局命名空间引用的变量，在 Python 退出是往往不会被释放

另外不会释放 C 库保留的部分内容。
```

---

# python-面试通关宝典

## **三.数据类型**

### **字符串**

#### 19.列举 Python 中的基本数据类型。

```markdown
Python3 中有六个标准的数据类型：

Number（数字）
String（字符串）
List（列表）
Tuple（元组）
Set（集合）
Dictionary（字典）
Python3 的六个标准数据类型中：

不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）；
可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）。
```

#### 20.如何区别 可变数据类型 和 不可变数据类型？

```markdown
Python3 的六个标准数据类型中：

不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）；
可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）。
```

#### 21.将 "hello world" 转换为首字母大写 "Hello World"。

```python
z = 'hello world'
z.title()
```

#### 22.如何检测字符串中只含有数字？

```python
# 分为两种情况
# 1.不包含正负号 +-
a = '32323'
a.isdigit()
# 2.含有正负号
import re
re.match(r'[+-]?\d+$',a)
```

#### 23.将字符串 "ilovechina" 进行反转。

```python
s = 'ilovechina'
s = s[::-1]
```

#### 24.Python 中的字符串格式化方式你知道哪些？

```python
# Python3.6之后的版本提供了三种字符串格式化的方式
# 1. %s占位符
def foo(name):
  return 'hello %s' % name
# 2. format() 
def foo(name):
  return 'hello {}'.format(name)
# f-string
def foo(name):
  return f'hello {name}'
```

#### 25.有一个字符串开头和末尾都有空格，比如 " adabdw "。要求写一个函数把这个字符串的前后空格都去掉。

```python
s = " adabdw "
s.strip()
```

#### 26.获取字符串 "123456" 最后的两个字符。

```python
s = '123456'

print(s[-2:])
```

#### 27.一个编码为 GBK 的字符串 S，要将其转成 UTF-8 编码的字符串，应如何操作？

```python
s.encode('utf-8')
```

#### 28.字符串 s = "info:xiaoZhang 33 shandong"，用正则切分字符串输出 ['info', 'xiaoZhang', '33', 'shandong']。

```python
import re
s="info:xiaoZhang 33 shandong"
re.split(r'[:\s]',s)
```

#### 29.怎样将字符串转换为小写？

```python
b = 'HHH'
b.lower()
```

#### 30.单引号、双引号和三引号的区别？

```python
s = 'hello'
s= "hello"
双引号可以包含单引号字符，单引号无法包含双引号字符
三引号可以用来加注释，所加注释可以使用__doc__查看
```

#### 31.字符串 a = "你好     中国  "，去除多余空格只留一个空格。

```python
a = "你好     中国  "
s = ' '.join(a.strip().split())
```



### **列表**

#### 32.已知 AList = [1,2,3,1,2]，对 AList 列表元素去重，写出具体过程。

```python
a_list = [1,2,3,1,2]
ss = set(a_list)
```

#### 33.如何将 "1,2,3" 变成 ["1","2","3"]？

```python
s = "1,2,3"
s.split(',')
```

#### 34.给定两个 list，A 和 B，找出相同元素和不同元素。

```python
# 最直接的方法
list_a = [1,2,3,4,5,6]
list_b = [2,3,6]
same_l = []
not_same = []
for i in list_a:
    if i not in list_b:
        not_same.append(i)
for j in list_b:
    if j not in list_a:
        not_same.append(j)
for x in list_a:
  if x in list_b:
       same_l.append(x)
# 奇技淫巧
list_a = [1,2,3,4,5,6]
list_b = [2,3,6]
set1 = set(list_a)
set2 = set(list_b)
# 相同元素
print(set1&set2)
# 不同元素
print(set1^set2)
```

#### 35.用一行代码展开该列表 [[1,2],[3,4],[5,6]]，得出[1,2,3,4,5,6]。

```python
mm = [[1,2],[3,4],[5,6]]
[j for a in mm for j in a]
```

#### 36.合并列表 [1,5,7,9] 和 [2,2,6,8]。

```python
a = [1,5,7,9]
b = [2,2,6,8]
# 方法1
a.extend(b)
# 方法2
a[0:0] = b
# 方法3
a += b
```

#### 37.如何打乱一个列表的元素？

```python
import random
a = [1,5,7,9]
random.shuffle(a)
```



### **字典**

#### 38.字典操作中 del 和 pop 有什么区别？

```markdown
del 操作删除键值对，不返回值；
pop 操作删除键值对的同时，返回键所对应的值。
```

#### 39.将如下字典按照年龄排序。

```Python
d1 = [
    {'name':'alice', 'age':38},
    {'name':'bob', 'age':18},
    {'name':'Carl', 'age':28},
]
```

```python
sorted(d1,key=lambda x:x['age'])
```

#### 40.请合并下面两个字典 a = {"A":1,"B":2}，b = {"C":3,"D":4}。

```python
# python3合并字典有三种方式
# 1.
a = {'a':1,'b':2}
b = {'c':3,'d':4}
c = {}
c.update(a)
c.update(b)
# 2.
c = dict(a,**b)
# 3.
c = {**a,**b} # 官方推荐这种方式
```

#### 41.如何使用生成式的方式生成一个字典，写一段功能代码。

```python
{x:x*x for x in range(6)}
```

#### 42.如何把 元组 ("a","b") 和 元组(1,2)，变为字典{"a":1,"b":2}？

```python
a = ('a','b')
b = (1,2)
z=zip(a,b)
c = dict(z)
```



### **综合数据类型**

#### 43.Python 常用的数据结构的类型及其特性？

```markdown
List,tuple,dict,set是比较常用的数据结构，queue,heap,deque,ProrityQueue，multiprocessing.Queue等进阶的数据结构类型。特性就去查查吧，写在这里太长了。
```

#### 44.如何将 元组("A","B") 和 元组(1,2) 合并成 字典{"A":1,"B":2}？

```Python
a = ('A','B')
b = (1,2)
z=zip(a,b)
c = dict(z)
```

#### 45.Python 里面如何实现 tuple 和 list 的转换？

```python
tuple(list) # tuple转list
list(tuple) # list 转tuple
```

#### 46.我们知道对于列表可以使用切片操作进行部分元素的选择，那么如何对生成器类型的对象实现相同的功能呢？

```python
使用自带的itertools库进行实现，具体实现方式 itertools.islice(生成器对象，起始位置，结束位置)，即可实现切片功能。
```

#### 47.请将 [i for i in range(3)] 改成 生成器。

```python
(i for i in range(3))
```

#### 48.将 a="hello" 和 b="你好" 编码成 bytes 类型。

```python
a.encode()
b.encode()
```

#### 49.下面的代码输出结果是什么？

```Python
a = (1,2,3,[4,5,6,7],8)
a[2] = 2
报错，元组是不可变对象，不支持修改
```

#### 50.下面的代码输出的结果是什么？

```Python
a = (1,2,3,[4,5,6,7],8)
a[5] = 2
报错，元组是不可变对象，下标越界
```
