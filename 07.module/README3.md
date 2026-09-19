# Python基础

## 模块与包
### 3.输入日期， 判断这一天是这一年的第几天？
```python
import datetime
def dayofyear():
    year = input("请输入年份: ")
    month = input("请输入月份: ")
    day = input("请输入天: ")
    date1 = datetime.date(year=int(year),month=int(month),day=int(day))
    date2 = datetime.date(year=int(year),month=1,day=1)
    return (date1-date2).days+1
```
### 4.打乱一个排好序的list对象alist？
```python
import random
alist = [1,2,3,4,5]
random.shuffle(alist)
print(alist)
```

---

# Python高级

## 正则表达式
### 94.请写出一段代码用正则匹配出ip？
### 95.a = “abbbccc”，用正则匹配为abccc,不管有多少b，就出现一次？
### 96.Python字符串查找和替换？
### 97.用Python匹配HTML g tag的时候，<.> 和 <.*?> 有什么区别
### 98.正则表达式贪婪与非贪婪模式的区别？
### 99.写出开头匹配字母和下划线，末尾是数字的正则表达式？
### 100.正则表达式操作
### 101.请匹配出变量A 中的json字符串。
### 102.怎么过滤评论中的表情？
### 103.简述Python里面search和match的区别
### 104.请写出匹配ip的Python正则表达式
### 105.Python里match与search的区别？
