## 代码题


##### python 实现 ip 地址的存储，32位

##### 两个字符串，有相同的元素就返回 True、没有就返回 False

```python
str1 = '1234'
str2 = '123'

set1 = set(str1)
set2 = set(str2)

if len(str1) > (str2):
	difference_set = set2 - set1
else:
    difference_set = set1 - set2
    
if difference_set:
    print('True')
else:
    print('Flase')
```

##### 取出一个列表中的中间值

提示：(这个提示不是面试官提示的，是自己要去分析多种情况)列表长度有可能是偶数，那么就要取两个中间值，奇数取一个中间值

##### 代码实现单例模式

```python
class Single:
    def __init__(self):
        pass


    @classmethod
    def inner(cls, *args, **kwargs):
        if not hasattr(Single, '_attr'):
            # Single._attr = Single()
            Single._attr = cls()
        return Single._attr

s1 = Single.inner()
# s2 = Single.inner()
print(s1)
s2 = Single.inner()
print(s2)
```

##### 代码实现 json 模块可以序列化 datetime 类型

##### 一个列表中存在若干数据，存在重复数据，取出第二大的数

##### 数据库中一张表存在姓名、学科、成绩，查询每个学科的第一名

##### 用列表推导式将列表中奇数元素的平方放到新的列表中

##### 一个目录下n个不同后缀的文件统计.jpg文件的数量

##### 有一对兔子自第三个月开始，每一个月生一对兔子，之后生的每一对兔子…（想不起来了，这个没做出来）

##### 输入一个字符到文件里，直到输入的为#时，停止输入

##### 求数列2/1，3/2, 5/3, 8/5, 13/8 … 的前n项和

##### 用递归方法求10的乘积 1 * 2 * 3 ... * 10

##### 如果一个数的因子之和等于这个数，那么这个数称为完数（比如6=1+2+3）。根据完数的概念求出1-1000的所有完数
