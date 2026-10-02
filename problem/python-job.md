## 编程题

### and or not运算问题  
```python
v = 1 and 2 or 3 and 4  
print(v)  

  # >>> 2  
```

参考：[Python：and和or的特殊性质](http://blog.csdn.net/betabin/article/details/8568804)  
总结：对python而言  
其一, 在不加括号时候, and优先级大于or  
其二, x or y 的值只可能是x或y.  x为真就是x, x为假就是y  
第三, x and y 的值只可能是x或y.  x为真就是y, x为假就是x  
显然,对于, `1 or 5 and 4`: 先算5 and 4, 5为真, 值为4. 再算1 or 4, 1 为真,值为1  
对于, `(1 or 5) and 4`: 先算1 or 5, 1为真, 值为1. 再算1 and 4, 1为真,值为4  

### 排序问题  
list对象 `alist [{'name':'a','age':20},{'name':'b','age':30},{'name':'c','age':25}]`，请按alist中元素的 age 由大到小排序；  
```python
alist = [{'name': 'a', 'age': 20}, {'name': 'b', 'age': 30}, {'name': 'c', 'age': 25}]  
alist.sort(key=lambda x: -x["age"])  
print(alist)  
```

### 打乱一个排好序的 list 对象 alist；  
```python
from random import shuffle    
alist = range(10)  
shuffle(alist)  
print("shuffle", alist)  
```

### 简单实现一个stack；  
```python
class Stack:  
    def __init__(self):  
        self.values = []  
    def push(self, o):  
        self.values.append(o)  
    def pop(self):  
        return self.values.pop()  
s = Stack()  
s.push(1)  
s.push(2)  
assert s.pop() == 2  
assert s.pop() == 1  
s.push(3)  
s.push(4)  
assert s.pop() == 4  
assert s.pop() == 3  
```

### 输入某年某月某日，判断这一天是这一年的第几天？  
```python
from datetime import datetime  
def day_of_year(year, month, day):  
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1  
assert day_of_year(2014, 1, 10) == 10  
```

### 数据类型转换  
将字符串：`"k:1|k1:2|k2:3|k3:4"`，处理成python字典：`{k:1, k1:2, ... }`  
```python
def string_to_dict(string):  
    d = {}  
    for kv in string.split("|"):  
        k, v = kv.split(":")  
        if v.isdigit():  
            v = int(v)  
        d[k] = v  
    return d  
string = "k:1|k1:2|k2:3|k3:4"  
print(string_to_dict(string))  
string2 = "k:1"  
print(string_to_dict(string2))  
```

### 台阶问题/斐波纳挈  
一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法。（用一句代码写斐波那契数列）  
```python
fib = lambda n: n if n <= 2 else fib(n - 1) + fib(n - 2)  
```

### 变态台阶问题  
一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。  
```python
fib = lambda n: n if n < 2 else 2 * fib(n - 1)  
```

### 找零算法（动态规划）  
我购物花费28元，支付100元纸币，我最少会被找零多少张纸币？  
```python
def coinChange(values, money, coinsUsed):  
# values    T[1:n]数组  
# valuesCounts   钱币对应的种类数  
# money  找出来的总钱数  
# coinsUsed   对应于目前钱币总数i所使用的硬币数目  
for cents in range(1, money + 1):  
    minCoins = cents  # 从第一个开始到money的所有情况初始  
    for value in values:  
        if value <= cents:  
            temp = coinsUsed[cents - value] + 1  
            if temp < minCoins:  
                minCoins = temp  
    coinsUsed[cents] = minCoins  
    print('面值为：{0} 的最小硬币数目为：{1} '.format(cents, coinsUsed[cents]))  

  if __name__ == '__main__':  
values = [25, 21, 10, 5, 1]  
money = 63  
coinsUsed = {i: 0 for i in range(money + 1)}  
coinChange(values, money, coinsUsed)  
```

---

## 面试知识点简单汇总（自测）
### 招聘网站的一般要求汇总（面试造火箭系列）：  
具备开发高并发引擎能力  
熟悉HTTP，TCP/IP等常用协议原理  
熟悉Docker相关理念及核心技术  
精通SQL和NoSQL数据库体系架构设计及高可用性解决方案；  
熟悉mysql，redis，mongo等常用数据库，具有数据库开发和设计能力；  
熟悉linux系统，会熟练编写多进程多线程的程序，熟悉网络编程；  
熟悉python异步IO  
熟练使用Linux系统，掌握基本命令，可编写简单的shell脚本  
了解异步框架、集群与负载均衡，消息中间件，容灾备份等技术；  
完成系统 API 接口等开发工作；  

### Python知识点:    
写一个简单的python socket编程  
python2.x 与python3.x的主要区别  
python新式类和旧式类的区别  
请简述线程＼进程＼协程的特性  
什么是闭包?  
Python的实例方法,类方法,静态方法之间的区别及调用关系  
Python内存管理和垃圾回收机制  
Python的装饰器内部实现原理  
描述你知道的设计模式及各模式特点  
常用算法(冒泡,二叉树,快排, 堆排序等)  
线程池的原理和实现  
解释一下 Django 和 Tornado 的关系、差别  
解释下Http协议的特点  
model之F/Q操作, 写一个Q示例  
simple_tag用法  
写一个字典推导式  
Python中单下划线和双下划线  
什么是迭代器  
分别用__new__方法和装饰器实现单例模式  
简述Python的作用域以及Python搜索变量的顺序  
GIL线程全局锁  
Python-copy()与deepcopy()区别  
select,poll和epoll  
可变与不可变类型；  
浅拷贝与深拷贝的实现方式、区别；deepcopy如果你来设计，如何实现；  
__new__() 与 __init__()的区别；  
你知道几种设计模式；  
编码和解码你了解过么；  
列表推导list comprehension和生成器的优劣；  
什么是装饰器；如果想在函数之后进行装饰，应该怎么做；  
手写个使用装饰器实现的单例模式；  
使用装饰器的单例和使用其他方法的单例，在后续使用中，有何区别；  
手写：正则邮箱地址；  
介绍下垃圾回收：引用计数/分代回收/孤立引用环；  
多进程与多线程的区别；CPU密集型适合用什么；  
进程通信的方式有几种；  
介绍下协程，为何比线程还快；  
range和xrange的区别（他妹的我学的py3…）；  
将IP地址字符串（比如“172.0.0.1”）转为32位二进制数的函数。  

### 算法排序部分  
手写快排；堆排；几种常用排序的算法复杂度是多少；快排平均复杂度多少，最坏情况如何优化；  
手写：已知一个长度n的无序列表，元素均是数字，要求把所有间隔为d的组合找出来，你写的解法算法复杂度多少；  
手写：一个列表A=[A1，A2，…,An]，要求把列表中所有的组合情况打印出来；  
手写：用一行python写出1+2+3+…+10**8；  
手写python：用递归的方式判断字符串是否为回文；  
单向链表长度未知，如何判断其中是否有环；  
单向链表如何使用快速排序算法进行排序；  
手写：一个长度n的无序数字元素列表，如何求中位数，如何尽快的估算中位数，你的算法复杂度是多少；  
如何遍历一个内部未知的文件夹（两种树的优先遍历方式）  

### 网络基础部分  
TCP/IP分别在模型的哪一层；  
socket长连接是什么意思；  
select和epoll你了解么，区别在哪；  
TCP UDP区别；三次握手四次挥手讲一下；  
TIME_WAIT过多是因为什么；  
http一次连接的全过程：你来说下从用户发起request——到用户接收到response；  
http连接方式。get和post的区别，你还了解其他的方式么；  
restful你知道么；  
状态码你知道多少，比如200/403/404/504等等；  

### 数据库部分  
MySQL锁有几种；死锁是怎么产生的；  
为何，以及如何分区、分表；  
MySQL的char varchar text的区别；  
了解join么，有几种，有何区别，A LEFT JOIN B，查询的结果中，B没有的那部分是如何显示的（NULL）；  
索引类型有几种，BTree索引和hash索引的区别（我没答上来这俩在磁盘结构上的区别）；  
手写：如何对查询命令进行优化；  
NoSQL了解么，和关系数据库的区别；redis有几种常用存储类型；  
说说慢查询  
说说数据库的优化  

### django项目部分  
都是让简单的介绍下你在公司的项目，不管是不是后端相关的，主要是要体现出你干了什么；  
你在项目中遇到最难的部分是什么，你是怎么解决的；  
你看过django的admin源码么；看过flask的源码么；你如何理解开源；  
MVC / MTV；  
缓存怎么用；  
中间件是干嘛的；  
CSRF是什么，django是如何避免的；XSS呢；  
如果你来设计login，简单的说一下思路；  
session和cookie的联系与区别；session为什么说是安全的；  
uWSGI和Nginx的作用；  

  扩展阅读:  [关于Python的面试题](https://github.com/taizilongxu/interview_python)
