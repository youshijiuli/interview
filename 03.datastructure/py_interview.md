##### 描述以下dict的items和iteritems的区别
* python3中没有iteritems
* items和iteritems大致相同，只是items返回的是一个列表，iteritems返回的是一个迭代器。

---

##### 如何查找一个字符串中特定的字符？find和index的差异？
* 使用find和index方法查找

1. find()方法：查找子字符串，若找到返回从0开始的下标值，若找不到返回-1
2.  index()方法：python 的index方法是在字符串里查找子串第一次出现的位置，类似字符串的find方法，不过比find方法更好的是，如果查找不到子串，会抛出异常，而不是返回-1

---

##### 描述以下字典的items()方法和iteritems()方法有啥不同？

* 字典的items方法作用：是可以将字典中的所有项，以列表方式返回。因为字典是无序的，所以用items方法返回字典的所有项，也是没有顺序的。
* 字典的iteritems方法作用：与items方法相比作用大致相同，只是它的返回值不是列表，而是一个迭代器

---

##### or 和 and
* v1=1 or 3
* v2=1 and 3
* v3=0 and 2 and 1
* v4=0 and 2 or 1
* v5=0 and 2 or 1 or 4
* v6=0 or False and 1

* 结果：
       * v1 = 1
       * v2 = 3
       * v3 = 0
       * v4 = 1
       * v5 = 1
       * v6 = False
 * 基本运算规律
    1.  在不加括号时候, and优先级大于or
    2.  x or y 的值只可能是x或y. x为真就是x, x为假就是y
    3.  x and y 的值只可能是x或y. x为真就是y, x为假就是x

---

##### a=range(10),则a[::-3]的值是？
* [9,6,3,0] 或者 range(9,-1,-3)


##### 将下面列表中的元素根据位数合并成字典：
```python

lst = [1,2,4,8,16,32,64,128,256,512,1024,32769,65536,4294967296]

# 结果
{1: [1, 2, 4, 8], 2: [16, 32, 64], 3: [128, 256, 512], 4: [1024], 5: [32769, 65536], 10: [4294967296]}
```
```python

lst = [1,2,4,8,16,32,64,128,256,512,1024,32769,65536,4294967296]
dic={}
for i in lst:
    len_i=len(str(i))
    dic.setdefault(len_i,[]).append(i)
print(dic)
```

---

##### 用尽量简洁的方法将二维数组合并成一维数组
```python
lst = [[1,2,3],[4,5,6],[7,8,9]]
ll=[]
for l in lst:
    # ll+=l
    ll.extend(l)
print(ll)
```

##### 将列表按照下列规则排序：
1. 正数在前，负数在后
2. 正数从小到大
3. 负数从大到小

* 例子：
    * 排序前：[7,-8,5,4,0,-2,-5]
    * 排序后：[0, 4, 5, 7, -2, -5, -8]
```python
lis = [7,-8,5,4,0,-2,-5]
lis=sorted(lis,key=lambda x:(x<0,abs(x))) # 这里排序条件返回元组，先比较第一个，再第二个值
print(lis)
```

---

##### 现有mydict和变量onekey，请写出从mydict中取出onekey的值的方法

> 方法一：mydict[onekey]
> 这种方法，如果mydict中键不存在的时候程序会报错
> 方法二：mydict.get(onekey)
> 这种方法，如果存在，返回值，不存在返回None
> 方法三：mydict.setdefault(onekey,[])
> 这种方法：存在的话返回值，不存在的时候创建一个值，值得内容为第二个参数+

---

##### 写代码：如何由tuple1=('a','b','c','d','e')，和tuple2=(1,2,3,4,5)得到res={'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

```python
tuple1=('a','b','c','d','e')
tuple2=(1,2,3,4,5)
res=dict(zip(tuple1,tuple2))
print(res)
```

##### 1<(2==2)和1<2==2的结果分别是什么？
* 第一个为False，第二个为True，暂时按照第一个类型进行相应的转换

---

##### python是如何进行内存管理的？python的程序会内存泄漏吗？说说有没有什么方面阻止或者检测内存泄漏？
[整体参考文章](https://www.jianshu.com/p/2b683cb5837c)
* python是如何进行内存管理的[参考文章](https://blog.csdn.net/u010967872/article/details/80301633)
    1. 引用计数
        * Python内部使用引用计数，来保持追踪内存中的对象，Python内部记录了对象有多少个引用，就是引用计数，当对象被创建时就创建了一个引用计数，当对象不再需要的时候，这个对象的引用计数为0时，他被垃圾回收。
    2. 垃圾回收
        * 当内存中有不再使用的部分时，垃圾收集器就会把他们清理掉。他会去检查那些引用计数为0的对象，然后清除其在内存中的空间。当然除了引用计数为0的会被清除，还有一种情况也会被垃圾收集器清掉，当两个对象相互引用时，他们本身其他引用已经为0了。
    3. 内存池机制
        * Python提供了对内存的垃圾收集机制，但是他将不用的内存放到内存池而不是反回给操作系统。
* python的程序会内存泄漏吗？
    * 会发生内存泄漏，在Python程序里，内存泄漏是由于一个长期持有的对象不断的往一个dict或者list对象里添加新的对象, 而又没有即时释放，就会导致这些对象占用的内存越来越多，从而造成内存泄漏。另外，对象的交叉引用也会造成内存无法释放的问题。
* 说说有没有什么方面阻止或者检测内存泄漏？
    1. 程序员管理好每个python对象的引用，尽量在不需要使用对象的时候，断开所有引用
    2. 尽量少通过循环引用组织数据，可以改用weakref做弱引用或者用id之类的句柄访问对象
    3. 通过gc模块的接口可以检查出每次垃圾回收有哪些对象不能自动处理，再逐个逐个处理

---

##### 以下代码输出什么？

```python
lis=['a','b','c','d','e']
print(lis[10:])
```
* 答案：[]

##### python哪些类型的数据才能作为字典的key？
* 可哈希的类型

---

##### 列表中保留顺序和不保留顺序去重
  [参考文章](https://blog.csdn.net/Jerry_1126/article/details/84677212)

  * 不保留顺序
```python
lis=[3, 1, 4, 2, 3]
print(list(set(lis)))
```
  * 保留顺序
```python
lis=[3, 1, 4, 2, 3]
T=[]
[T.append(i) for i in lis if i not in T])
print(T)

# 或者
T=sorted(set(lis), key=lis.index)
print(T)
```

---

##### 求下面代码结果
```python
v=dict.fromkeys(['k1','k2'],[])
v['k1'].append(666)
print(v)
v['k1']=777
print(v)
```
* 结果：
{'k1': [666], 'k2': [666]}
{'k1': 777, 'k2': [666]}


##### 一行代码实现删除列表中的所有的重复的值
```python
lis=[1,1,2,1,22,5]
lis=list(set(lis))
```

##### 如何实现"1.2.3"变成['1','2','3']?
```python
s="1,2,3"
s=s.split(',')
```

##### 如何实现['1','2','3']变成[1,2,3]
```python
ss=['1', '2', '3']
ss=[int(i) for i in ss]
```

##### 比较：a=[1,2,3]和b=[(1),(2),(3)]以及c=[(1,),(2,),(3,)]的区别
* a和b的结果相同，列表里面的值相同，类型也相同
* c中的列表里面的值是元组类型的


##### 如何用一行代码生成[1,4,9,16,25,36,49,64,81,100]?
```python
lis=[i**2 for i in range(1,11)]
```

##### 常用字符串格式化有哪几种？
1. 使用百分号
```python
print('hello %s and %s'%('friend','another friend'))
```
2. 使用format
```python
print('hello {first} and {second}'.format(first='friend',second='another friend'))
```

---

##### 将列表alist=[{'name':'a','age':25},{'name':'b','age':30},{'name':'c','age':20}]，按照age的值从大到小排列。

```python
alist=[{'name':'a','age':25},{'name':'b','age':30},{'name':'c','age':20}]
blist=sorted(alist,key=lambda x:x['age'],reverse=True)
print(blist)
```

---

##### python的垃圾回收机制
[python垃圾回收机制详解](https://testerhome.com/topics/16556)

* 概述：python采用的是引用计数机制为主，标记-清除和分代收集两种机制为辅的策略
* 引用计数：
    * 每当新的引用指向该对象时，引用计数加1，当对该对象的引用失效时，引用计数减1，当对象的引用计数为0时，对象被回收。缺点是，需要额外的空间来维护引用计数，并且无法解决对象的循环引用。
* 分代回收：（具体见上面链接）
    * 以时间换空间的回收方式
* 标记清除：
    * 活动对象会被打上标记，会把那些没有被打上标记的非活动对象进行回收。


##### python的可变类型和不可变类型的区别
* 可变类型有：列表，字典等
* 不可变类型有：数字，字符串，元组等
* 这里的可变不可变是指内存中的那块内容是否可以被改变。

---

##### 有一个列表lis=['This','is','a','Man','B','!']，对它进行大小写无关的排序

```python
lis=['This','is','a','Man','B','!']
lis=sorted(lis,key=str.lower)
print(lis)

---

##### 判断dict中有没有某个key。
* key in dict.keys()  判断


##### a = dict(zip(('a','b','c','d','e'),(1,2,3,4,5))) 请问a是什么？
* {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}


##### 在python中如何拷贝一个对象，并说明他们之间的区别

1. 赋值（=），就是创建了对象的一个新的引用，修改其中任意一个变量都会影响到另一个。
2. 浅拷贝：创建一个新的对象，但它包含的是对原始对象中包含项的引用（copy模块的copy()函数）
3. 深拷贝：创建一个新的对象，并且递归的复制它所包含的对象（修改其中一个，另外一个不会改变）（copy模块的deep.deepcopy()函数）

---

##### 求出以下代码的输出结果
```python
mydict={'a':1,'b':2}
def func(d):
    d['a']=0
    return d
    
func(mydict)
mydict['c']=2
print(mydict)
```
* 结果
>{'a': 0, 'b': 2, 'c': 2}

---

##### 对字典d={'a':30,'g':17,'b':25,'c':18,'d':50,'e':36,'f':57,'h':25}按照value字段进行排序

```python
d={'a':30,'g':17,'b':25,'c':18,'d':50,'e':36,'f':57,'h':25}
dd=sorted(d.items(),key=lambda x:x[1])
print(dd)
```

##### 找出两个列表中相同的元素和不同的元素
```python
list1=[1,2,3,5,8,7,11,10]
list2=[5,15,25,10]
sim=[i for i in list1 if i in list2]
diff=[i for i in list1+list2 if i not in sim]
print(sim)
print(diff)
```

---

##### 把a='aaabbcccdddde'这种形式的字符串，压缩成a3b2c3d4e1这种形式。
```python
a='aaabbcccdddde'
aa=''
for i in sorted(list(set(a)),key=a.index):
    aa=aa+i+str(a.count(i))
print(aa)
```

---

##### 如何实现字符串的反转？如：name=felix，反转成name=xilef

```python
    name = "felix"
    # 方法一：
    name=name[::-1]
    # 方法二：
    name2=list(name)
    name2.reverse()
    name=''.join(name2)
    # 方法三：
    from functools import reduce
    name=reduce(lambda x, y: y+x, name)
```

---

##### 简述python字符串的驻留机制
[python字符串驻留机制参考文档](https://www.cnblogs.com/asmer-stone/p/4802800.html)

* 相同对象的引用都指向内存中的同一个位置，这个也叫python的字符串驻留机制
* python的引用计数机制，并不是对所有的数字，字符串，他只对”[0-9][a-z][A-Z]
和"_"(下划线)  ”有效“，当字符串中由其他字符比如“！ @ # ￥ % -”时字符驻留机制是不起作用的。

---

##### ascii、Unicode、utf-8、gbk的区别
* ascii 是最早美国用的标准信息交换码，把所有的字母的大小写，各种符号用 二进制来表示，共有256中，加入些拉丁文等字符，1bytes代表一个字符
* Unicode是为了统一世界各国语言的不用，统一用2个bytes代表一个字符，可以表达2^16=65556个，称为万国语言，特点：速度快，但浪费空间
* utf-8 为了改变Unicode的这种缺点，规定1个英文字符用1个字节表示，1个中文字符用3个字节表示，特点；节省空间，速度慢，用在硬盘数据传输，网络数据传输，相比硬盘和网络速度，体现不出来的
* gbk  是中文的字符编码，用2个字节代表一个字符

---

##### 阅读以下代码，写输出结果
```python
lis = [2,4,5,6,7]
for i in lis:
    if i % 2==0:
        lis.remove(i)
print(lis)
```
* 结果：[4, 5, 7]

##### 对列表[3,1,-4,-2]按照绝对值排序
```python
lis=[3,1,-4,-2]
lis=sorted(lis,key=lambda x:abs(x))
print(lis)
```

---

##### 如何打乱一个排好序的列表
* 使用random.shuffle()
```python
import random
alist=[1,2,3,4,5,6]
random.shuffle(alist)
print(alist)
```

---

##### 请列举布尔值位False的常见值

* 0、''、[]、{}、tuple()、None、set()

##### 列举字符串、列表、元组、字典每个常用的5个方法
* 字符串---[字符串方法总结](https://www.cnblogs.com/chendai21/p/8137285.html)
    1. strip() ->去掉字符串两端的空白符
    2. split() ->对字符串进行分割，默认按照空格分割
    3. join() ->字符串连接
    4. startwith(),endwith() ->判断是否以啥开头或者结尾
    5. replace() -> 字符串替换
    6. find() -> 查找字符串，存在返回第一个索引，不存在返回-1
* 列表---[列表方法总结](https://www.cnblogs.com/smelond/p/7857701.html)
    1. count() ->统计在列表中出现的个数
    2. apped() ->在列表末尾添加值
    3. pop() ->删除一个对象，默认最后一个
    4. remove() ->删除指定的第一个匹配项
    5. insert() ->插入对象
    6. index() ->获取索引
 * 元组
     1. count() ->统计在元组中出现的个数
     2. index() ->获取索引
 * 字典
     1. keys() ->获取所有的键
     2. pop() ->删除指定的键的键值对
     3. popitem() ->随机删除一个键值对
     4. update() ->更新字典，参数为一个字典，如果键已存在，则更改，不存在则添加
     5. setdefault() ->如果键存在则，返回该键对应的值，如果不存在，设置该键为设置的默认值，然后返回该键对应的值
     6. get() ->返回键对应的值
     7. fromkeys() ->创建字典，第一个参数为可迭代对象，每个值变成字典的键，第二个参数为每个键的默认值

##### is和==的区别
* is比较的是两个对象的id是否相同
* ==比较的是两个对象的值是否相同

---

##### 简述python的深浅拷贝
* 浅拷贝只是对另外一个变量的内存地址的拷贝，这两个变量指向同一个内存地址的变量值。
    * 浅拷贝的特点：
        * 共用一个值
        * 这两个变量的内存地址一样
        * 对其中一个变量的值改变，另外一个变量的值也会改变
* 深拷贝是一个变量对另外一个变量的值拷贝
    * 深拷贝的特点：
        * 两个变量的内存地址不同
        * 两个变量各有自己的值，且互不影响
        * 对其任意一个变量的值的改变不会影响另外一个
* 如果是不可变类型，则深浅拷贝只拷贝引用，如果是可变类型，浅拷贝只拷贝第一层引用，深拷贝无论多少层引用都拷贝

---

##### 有如下代码：
```python
import copy
a=[1,2,3,[4,5],6]
b=a
c=copy.copy(a)
d=copy.deepcopy(a)
b.append(10)
c[3].append(11)
d[3].append(12)
```
* 求a，b，c，d
* 答案：
> a：[1, 2, 3, [4, 5, 11], 6, 10]
> b：[1, 2, 3, [4, 5, 11], 6, 10]
> c：[1, 2, 3, [4, 5, 11], 6]
> d：[1, 2, 3, [4, 5, 12], 6]

---

##### 在什么情况下y!=x-(x-y)会成立？
* x，y是两个不相等的非空集合
