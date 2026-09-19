## 十、垃圾回收机制（GC）

### 10.1 什么是垃圾回收

```python
# 垃圾回收机制（Garbage Collection，简称 GC）是 Python 解释器自带的机制
# 专门用来回收不再使用的变量值所占用的内存空间

# 当某个变量值不再被任何变量名引用时，就是"垃圾"
x = 10       # 10 的引用计数为 1（被 x 引用）
y = x        # 10 的引用计数为 2（被 x 和 y 引用）
x = 5        # 10 的引用计数降为 1（只被 y 引用）
y = 5        # 10 的引用计数降为 0（没有引用了）—— 成为垃圾，等待回收
```

### 10.2 内存的堆区与栈区

```python
# 栈区（Stack）：存储变量名与内存地址的关联关系
#   - 局部变量、函数参数等临时信息存放于此
#   - 遵循后进先出（LIFO）
#   - 由编译器自动管理，访问速度快

# 堆区（Heap）：存储变量值（对象本身）
#   - 灵活分配内存，大小动态调整
#   - 多个变量可以引用同一块堆内存
#   - 垃圾回收操作的是堆区的内容
```

### 10.3 三大 GC 机制

```python
# Python 的垃圾回收机制：引用计数为主，标记清除和分代回收为辅

# 【1】引用计数（核心机制）
# 每个对象维护一个引用计数器
# 被引用时计数 +1，引用解除时计数 -1
# 计数为 0 时，对象被立即回收

num = 1       # 1 的引用计数 = 1
age = num     # 1 的引用计数 = 2
num = 2       # 1 的引用计数 = 1
age = 2       # 1 的引用计数 = 0 -> 被回收

# 【2】标记清除（解决循环引用问题）
# 容器对象（如列表、字典）之间可能形成循环引用
# Python 定期扫描，标记可达对象，清除不可达对象

# 循环引用示例：
# a = []
# b = []
# a.append(b)  # a 引用 b
# b.append(a)  # b 引用 a
# 即使 a、b 不再使用，它们的引用计数也不为 0
# 标记清除机制可以处理这种情况

# 【3】分代回收（提高效率）
# 根据对象的存活时间将其分为不同"代"
# 新生代：新创建的对象，GC 扫描频率高
# 青春代：经历过一次 GC 仍存活的对象
# 老年代：长期存活的对象，GC 扫描频率最低

# 这种策略基于：大多数对象很快就变成垃圾，存活越久的对象越可能继续存活
```

### 10.4 小整数池

```python
# Python 为 [-5, 256] 范围内的整数预先创建了内存空间
# 这些范围内的整数无论被赋值多少次，都使用同一块内存

a = 100
b = 100
print(id(a) == id(b))  # True（同一内存地址）

c = 257
d = 257
print(id(c) == id(d))  # False 或 True（取决于 Python 实现）
# 小整数池外的数每次重新定义都可能开辟新空间
```

## 十一、深浅拷贝

> 深浅拷贝需要导入内置模块 `copy`。

### 11.1 浅拷贝（Shallow Copy）

```python
import copy

# 浅拷贝：创建一个新对象，但只复制原对象的顶层元素
# 嵌套的可变对象仍然与原对象共享

original_list = [1, 2, 3, [7, 8, 9]]
shallow = copy.copy(original_list)

# 修改原列表的嵌套列表元素
original_list[3][-1] = 999

print(f"原列表：{original_list}")      # [1, 2, 3, [7, 8, 999]]
print(f"浅拷贝：{shallow}")            # [1, 2, 3, [7, 8, 999]]
# 浅拷贝的嵌套列表也被改变了！（共享同一内存地址）
```

```python
# 浅拷贝示例：只影响嵌套的可变对象
import copy

original = [1, 2, 3, [4, 5]]
shallow = copy.copy(original)

# 修改顶层元素（不可变）
original.append(999)
print(f"原列表：{original}")   # [1, 2, 3, [4, 5], 999]
print(f"浅拷贝：{shallow}")    # [1, 2, 3, [4, 5]]（不受影响）

# 修改嵌套列表元素（可变）
original[3].append(666)
print(f"原列表：{original}")   # [1, 2, 3, [4, 5, 666], 999]
print(f"浅拷贝：{shallow}")    # [1, 2, 3, [4, 5, 666]]（受到了影响！）
```

### 11.2 深拷贝（Deep Copy）

```python
import copy

# 深拷贝：创建一个完全独立的新对象，递归地复制所有嵌套对象
original_list = [1, 2, 3, [7, 8, 9]]
deep = copy.deepcopy(original_list)

# 修改原列表的嵌套列表元素
original_list[3][-1] = 999

print(f"原列表：{original_list}")  # [1, 2, 3, [7, 8, 999]]
print(f"深拷贝：{deep}")           # [1, 2, 3, [7, 8, 9]]
# 深拷贝的嵌套列表不受影响！（完全独立的副本）
```

### 11.3 浅拷贝 vs 深拷贝 总结

| 特性 | 浅拷贝 | 深拷贝 |
|------|--------|--------|
| 创建方式 | `copy.copy(obj)` | `copy.deepcopy(obj)` |
| 顶层元素 | 复制（新对象） | 复制（新对象） |
| 嵌套可变对象 | 共享同一内存地址 | 递归复制（完全独立） |
| 修改原对象嵌套部分 | 新对象也受影响 | 新对象不受影响 |
| 性能 | 较快 | 较慢（需要递归复制） |

---

## 十五、推导式

推导式（解析式）是 Python 中简洁构建数据结构的语法。

### 15.1 列表推导式

```python
# 语法：[表达式 for 变量 in 可迭代对象 if 条件]

# 生成 0-9 的列表
num_list = [i for i in range(10)]
print(num_list)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 生成 0-9 的平方列表
squares = [i ** 2 for i in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 对字符串中的每个字符做处理
upper_chars = [c.upper() for c in "dream"]
print(upper_chars)  # ['D', 'R', 'E', 'A', 'M']

# ======== 带条件的列表推导式 ========
# 获取偶数
evens = [i for i in range(10) if i % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# 实际应用：过滤和变换数据
words = ["hello", "world", "python", "java"]
long_words = [w.upper() for w in words if len(w) > 4]
print(long_words)  # ['HELLO', 'WORLD', 'PYTHON']

# ======== 嵌套循环 ========
# 语法：[表达式 for 变量1 in 可迭代1 for 变量2 in 可迭代2]
num_one = [1, 2, 3]
num_two = [4, 5, 6]

# 等价于双重循环的笛卡尔积
products = [i * j for i in num_one for j in num_two]
print(products)  # [4, 5, 6, 8, 10, 12, 12, 15, 18]

# ======== 行列转换 ========
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

# 使用列表推导式进行行列转换
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)
# [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

### 15.2 字典推导式

```python
# 语法：{键表达式: 值表达式 for 变量 in 可迭代对象 if 条件}

# 从一个元组列表创建字典
items = [('name', '橡皮擦'), ('age', 18), ('like', 'python')]
data_dict = {key: value for key, value in items}
print(data_dict)  # {'name': '橡皮擦', 'age': 18, 'like': 'python'}

# 快速生成平方数字典
squares = {x: x**2 for x in range(6)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 带条件的字典推导式
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 键值反转
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # {1: 'a', 2: 'b', 3: 'c'}
```

### 15.3 生成器表达式（元组推导式）

```python
# 语法：(表达式 for 变量 in 可迭代对象 if 条件)
# 注意：这不是真正的元组推导式，而是生成器表达式
# 生成器是惰性求值的，不会立即生成所有元素

gen = (i for i in range(10) if i % 2 == 0)
print(gen)  # <generator object <genexpr> at 0x...>

# 转换为列表
print(list(gen))  # [0, 2, 4, 6, 8]

# 生成器的优势：节省内存，适合处理大量数据
# 对比：
big_list = [i for i in range(1000000)]      # 立即占用大量内存
big_gen = (i for i in range(1000000))       # 占用极少内存，用到时才生成
```

### 15.4 集合推导式

```python
# 语法：{表达式 for 变量 in 可迭代对象 if 条件}

# 生成唯一值的集合
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(unique_squares)  # {16, 1, 4, 9}

# 带条件的集合推导式
vowels = {c for c in "hello world" if c in "aeiou"}
print(vowels)  # {'e', 'o'}
```
