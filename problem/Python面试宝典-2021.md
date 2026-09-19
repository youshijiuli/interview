## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目21：输入年月日，判断这个日期是这一年的第几天。

方法一：不使用标准库中的模块和函数。

```Python
def is_leap_year(year):
    """判断指定的年份是不是闰年，平年返回False，闰年返回True"""
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

def which_day(year, month, date):
    """计算传入的日期是这一年的第几天"""
    # 用嵌套的列表保存平年和闰年每个月的天数
    days_of_month = [
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ]
    days = days_of_month[is_leap_year(year)][:month - 1]
    return sum(days) + date
```

方法二：使用标准库中的`datetime`模块。

```Python
import datetime

def which_day(year, month, date):
    end = datetime.date(year, month, date)
    start = datetime.date(year, 1, 1)
    return (end - start).days + 1
```
