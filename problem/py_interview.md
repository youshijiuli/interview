##### 请编写一个函数将ip地址转换成一个整数。如10.3.9.12转换成00001010 00000011 00001001 00001100，然后转换成整数
```python
def ip2int(ip):
    nums=ip.split('.')
    # zfill()函数是补0
    to_bin=[bin(int(i))[2:].zfill(8) for i in nums]
    return int(''.join(to_bin),2)
i=ip2int('127.0.0.1')
print(i)
```

---

##### 有两个字符串列表a和b，每个字符串是由逗号隔开的一些字符
```python
a=[
    'a,1',
    'b,3,22',
    'c,3,4',
]
b=[
    'a,2',
    'b,1',
    'd,5',
]
# 按照a，b中每个字符串的第一个值，合并成c如下：
c=[
    'a,1,2',
    'b,3,22,1',
    'c,3,4',
    'd,5'
]
```
```python
# 解法：

a=[
    'a,1',
    'b,3,22',
    'c,3,4',
]
b=[
    'a,2',
    'b,1',
    'd,5',
]
a_dic={}
for s in a:
    k,v = s.split(',',1)
    a_dic[k]=v
b_dic={}
for s in b:
    k,v = s.split(',',1)
    b_dic[k]=v
c_dic=a_dic
for k,v in b_dic.items():
    if k in c_dic:
        c_dic[k]=','.join([c_dic[k],v])
    else:
        c_dic[k]=v
c=[','.join([k,c_dic[k]]) for k in c_dic]
print(c)
```

---

##### 输入某年某月某日，判断这是这一年的第几天？
```python
date=input('请输入某年某月某日，格式：xxxx.xx.xx')
def get_day(date):
    days1=[31,28,31,30,31,30,31,31,30,31,30,31]
    days2=[31,29,31,30,31,30,31,31,30,31,30,31]
    year,month,day = [int(i) for i in date.split('.')]
    if year % 400 ==0 or (year % 4==0 and year % 100!=0):
         days=days2
    else:
        days=days1
    return sum(days[:month-1])+day
print(get_day(date))
```

---

##### 有一个多层嵌套的列表A=[1,2,3,[4,1,['j1',1,[1,2,3,'aa']]]],请写一段代码将A中的元素全部打印出来
```python
A=[1,2,3,[4,1,['j1',1,[1,2,3,'aa']]]]
def my_print(lis):
    for i in lis:
        if type(i)==list:
            my_print(i)
        else:
            print(i)
my_print(A)
```

---

##### 1，2，3，4，5能组成多少个互不相同且不重复的三位数？
* 排列组合问题： 5\*4\*3=60个

---

##### 从0-99这100个数中随机取出10个，要求不能重复
```python
import random
lis=random.sample(range(0,100),10)
print(lis)
```
