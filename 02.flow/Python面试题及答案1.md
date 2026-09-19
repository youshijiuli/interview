### Python语言特性

#### 38 Python中pass语句的作用是什么？
答：pass语句不会执行任何操作，一般作为占位符或者创建占位程序，whileFalse:pass
#### 39 介绍一下Python下range()函数的用法？
答：列出一组数据，经常用在for  in range()循环中
#### 53 range and xrange
都在循环时使用，xrange内存性能更好。 for i in range(0, 20): for i in xrange(0, 20): What is the difference between range and xrange functions in Python 2.X? range creates a list, so if you do range(1, 10000000) it creates a list in memory with 9999999 elements. xrange is a sequence object that evaluates lazily.
http://stackoverflow.com/questions/94935/what-is-the-difference-between-range-and-xrange-functions-in-python-2-x
