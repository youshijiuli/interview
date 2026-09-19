## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目38：举例说明什么情况下会出现`KeyError`、`TypeError`、`ValueError`。

举一个简单的例子，变量`a`是一个字典，执行`int(a['x'])`这个操作就有可能引发上述三种类型的异常。如果字典中没有键`x`，会引发`KeyError`；如果键`x`对应的值不是`str`、`float`、`int`、`bool`以及`bytes-like`类型，在调用`int`函数构造`int`类型的对象时，会引发`TypeError`；如果`a[x]`是一个字符串或者字节串，而对应的内容又无法处理成`int`时，将引发`ValueError`。
