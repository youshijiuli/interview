## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目35：如何剖析Python代码的执行性能？

剖析代码性能可以使用Python标准库中的`cProfile`和`pstats`模块，`cProfile`的`run`函数可以执行代码并收集统计信息，创建出`Stats`对象并打印简单的剖析报告。`Stats`是`pstats`模块中的类，它是一个统计对象。当然，也可以使用三方工具`line_profiler`和`memory_profiler`来剖析每一行代码耗费的时间和内存，这两个三方工具都会用非常友好的方式输出剖析结构。如果使用PyCharm，可以利用“Run”菜单的“Profile”菜单项对代码进行性能分析，PyCharm中可以用表格或者调用图（Call Graph）的方式来显示性能剖析的结果。

下面是使用`cProfile`剖析代码性能的例子。

`example.py`

```Python
import cProfile


def is_prime(num):
    for factor in range(2, int(num ** 0.5) + 1):
        if num % factor == 0:
            return False
    return True


class PrimeIter:

    def __init__(self, total):
        self.counter = 0
        self.current = 1
        self.total = total

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.total:
            self.current += 1
            while not is_prime(self.current):
                self.current += 1
            self.counter += 1
            return self.current
        raise StopIteration()


cProfile.run('list(PrimeIter(10000))')
```

如果使用`line_profiler`三方工具，可以直接剖析`is_prime`函数每行代码的性能，需要给`is_prime`函数添加一个`profiler`装饰器，代码如下所示。

```Python
@profiler
def is_prime(num):
    for factor in range(2, int(num ** 0.5) + 1):
        if num % factor == 0:
            return False
    return True
```

安装`line_profiler`。

```Bash
pip install line_profiler
```

使用`line_profiler`。

```Bash
kernprof -lv example.py
```

运行结果如下所示。

```
Line #    Hits    Time      Per Hit  % Time  Line Contents
==============================================================
     1                                       @profile
     2                                       def is_prime(num):
     3    86624   48420.0   0.6      50.5        for factor in range(2, int(num ** 0.5) + 1):
     4    85624   44000.0   0.5      45.9            if num % factor == 0:
     5    6918     3080.0   0.4       3.2                return False
     6    1000      430.0   0.4       0.4        return True
```
