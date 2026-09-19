## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

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

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

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

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

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
