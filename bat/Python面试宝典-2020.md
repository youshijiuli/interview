## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目47：按照题目要求写出对应的函数。

> **要求**：写一个函数，传入的参数是一个列表（列表中的元素可能也是一个列表），返回该列表最大的嵌套深度。例如：列表`[1, 2, 3]`的嵌套深度为`1`，列表`[[1], [2, [3]]]`的嵌套深度为`3`。

```Python
def list_depth(items):
    if isinstance(items, list):
        max_depth = 1
        for item in items:
            max_depth = max(list_depth(item) + 1, max_depth)
        return max_depth
    return 0
```

> **点评**：看到题目应该能够比较自然的想到使用递归的方式检查列表中的每个元素。

---

## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目49：写一个函数实现字符串反转，尽可能写出你知道的所有方法。

> **点评**：烂大街的题目，基本上算是送人头的题目。

**方法一**：反向切片

```Python
def reverse_string(content):
    return content[::-1]
```

**方法二**：反转拼接

```Python
def reverse_string(content):
    return ''.join(reversed(content))
```

**方法三**：递归调用

```Python
def reverse_string(content):
    if len(content) <= 1:
        return content
    return reverse_string(content[1:]) + content[0]
```

**方法四**：双端队列

```Python
from collections import deque

def reverse_string(content):
    q = deque()
    q.extendleft(content)
    return ''.join(q)
```

**方法五**：反向组装

```Python
from io import StringIO

def reverse_string(content):
    buffer = StringIO()
    for i in range(len(content) - 1, -1, -1):
        buffer.write(content[i])
    return buffer.getvalue()
```

**方法六**：反转拼接

```Python
def reverse_string(content):
    return ''.join([content[i] for i in range(len(content) - 1, -1, -1)])
```

**方法七**：半截交换

```Python
def reverse_string(content):
    length, content= len(content), list(content)
    for i in range(length // 2):
        content[i], content[length - 1 - i] = content[length - 1 - i], content[i]
    return ''.join(content)
```

**方法八**：对位交换

```Python
def reverse_string(content):
    length, content= len(content), list(content)
    for i, j in zip(range(length // 2), range(length - 1, length // 2 - 1, -1)):
        content[i], content[j] = content[j], content[i]
    return ''.join(content)
```

> **扩展**：这些方法其实都是大同小异的，面试的时候能够给出几种有代表性的就足够了。给大家留一个思考题，上面这些方法，哪些做法的性能较好呢？我们之前提到过剖析代码性能的方法，大家可以用这些方法来检验下你给出的答案是否正确。

---

## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目46：按照题目要求写出对应的函数。

> **要求**：写一个函数，传入一个有若干个整数的列表，该列表中某个元素出现的次数超过了50%，返回这个元素。

```Python
def more_than_half(items):
    temp, times = None, 0
    for item in items:
        if times == 0:
            temp = item
            times += 1
        else:
            if item == temp:
                times += 1
            else:
                times -= 1
    return temp
```

> **点评**：LeetCode上的题目，在Python面试中出现过，利用元素出现次数超过了50%这一特征，出现和`temp`相同的元素就将计数值加1，出现和`temp`不同的元素就将计数值减1。如果计数值为`0`，说明之前出现的元素已经对最终的结果没有影响，用`temp`记下当前元素并将计数值置为`1`。最终，出现次数超过了50%的这个元素一定会被赋值给变量`temp`。

#### 题目50：按照题目要求写出对应的函数。

> **要求**：列表中有`1000000`个元素，取值范围是`[1000, 10000)`，设计一个函数找出列表中的重复元素。

```Python
def find_dup(items: list):
    dups = [0] * 9000
    for item in items:
        dups[item - 1000] += 1
    for idx, val in enumerate(dups):
        if val > 1:
            yield idx + 1000
```

> **点评**：这道题的解法和[计数排序](<https://www.runoob.com/w3cnote/counting-sort.html>)的原理一致，虽然元素的数量非常多，但是取值范围`[1000, 10000)`并不是很大，只有9000个可能的取值，所以可以用一个能够保存9000个元素的`dups`列表来记录每个元素出现的次数，`dups`列表所有元素的初始值都是`0`，通过对`items`列表中元素的遍历，当出现某个元素时，将`dups`列表对应位置的值加1，最后`dups`列表中值大于1的元素对应的就是`items`列表中重复出现过的元素。

查看更多的Python面试题，请移步到我的知乎专栏[《Python面试宝典》](https://zhuanlan.zhihu.com/c_1228980105135497216)。

---

## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目016：写一个函数，给定矩阵的阶数`n`，输出一个螺旋式数字矩阵。

> 例如：n = 2，返回：
>
> ```
> 1 2
> 4 3
> ```
>
> 例如：n = 3，返回：
>
> ```
> 1 2 3
> 8 9 4
> 7 6 5
> ```

这个题目本身并不复杂，下面的代码仅供参考。

```Python
def show_spiral_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    row, col = 0, 0
    num, direction = 1, 0
    while num <= n ** 2:
        if matrix[row][col] == 0:
            matrix[row][col] = num
            num += 1
        if direction == 0:
            if col < n - 1 and matrix[row][col + 1] == 0:
                col += 1
            else:
                direction += 1
        elif direction == 1:
            if row < n - 1 and matrix[row + 1][col] == 0:
                row += 1
            else:
                direction += 1
        elif direction == 2:
            if col > 0 and matrix[row][col - 1] == 0:
                col -= 1
            else:
                direction += 1
        else:
            if row > 0 and matrix[row - 1][col] == 0:
                row -= 1
            else:
                direction += 1
        direction %= 4
    for x in matrix:
        for y in x:
            print(y, end='\t')
        print()
```

---

## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目33：编写一个函数实现对逆波兰表达式求值，不能使用Python的内置函数。

> **点评**：[逆波兰表达式](<https://baike.baidu.com/item/%E9%80%86%E6%B3%A2%E5%85%B0%E5%BC%8F/128437>)也称为“后缀表达式”，相较于平常我们使用的“中缀表达式”，逆波兰表达式不需要括号来确定运算的优先级，例如`5 * (2 + 3)`对应的逆波兰表达式是`5 2 3 + *`。逆波兰表达式求值需要借助栈结构，扫描表达式遇到运算数就入栈，遇到运算符就出栈两个元素做运算，将运算结果入栈。表达式扫描结束后，栈中只有一个数，这个数就是最终的运算结果，直接出栈即可。

```Python
import operator


class Stack:
    """栈（FILO）"""

    def __init__(self):
        self.elems = []
    
    def push(self, elem):
        """入栈"""
        self.elems.append(elem)
    
    def pop(self):
        """出栈"""
        return self.elems.pop()
    
    @property
    def is_empty(self):
        """检查栈是否为空"""
        return len(self.elems) == 0


def eval_suffix(expr):
    """逆波兰表达式求值"""
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    stack = Stack()
    for item in expr.split():
        if item.isdigit():
            stack.push(float(item))
        else:              
            num2 = stack.pop()
            num1 = stack.pop()
            stack.push(operators[item](num1, num2))
    return stack.pop()
```
