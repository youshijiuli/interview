## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目015：现有2元、3元、5元共三种面额的货币，如果需要找零99元，一共有多少种找零的方式？

> **点评**：还有一个非常类似的题目：“一个小朋友走楼梯，一次可以走1个台阶、2个台阶或3个台阶，问走完10个台阶一共有多少种走法？”，这两个题目的思路是一样，如果用递归函数来写的话非常简单。

```Python
from functools import lru_cache


@lru_cache()
def change_money(total):
    if total == 0:
        return 1
    if total < 0:
        return 0
    return change_money(total - 2) + change_money(total - 3) + \
        change_money(total - 5)
```

> **说明**：在上面的代码中，我们用`lru_cache`装饰器装饰了递归函数`change_money`，如果不做这个优化，上面代码的渐近时间复杂度将会是$O(3^N)$，而如果参数`total`的值是`99`，这个运算量是非常巨大的。`lru_cache`装饰器会缓存函数的执行结果，这样就可以减少重复运算所造成的开销，这是空间换时间的策略，也是动态规划的编程思想。
