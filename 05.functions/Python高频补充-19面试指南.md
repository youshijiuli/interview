## 13 Python 高频面试题补充

### Q59: Python 中 is 和 == 的区别？

**答：**
- `is` 比较的是对象的**内存地址**（身份），即两个对象是否是同一个
- `==` 比较的是对象的**值**是否相等

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True（值相等）
print(a is b)  # False（不同对象）

# 小整数缓存机制（-5 ~ 256）
x = 256
y = 256
print(x is y)  # True（被缓存）

x = 257
y = 257
print(x is y)  # False（不在缓存范围）
```

---

### Q60: 深拷贝和浅拷贝的区别？

**答：**
- **浅拷贝（shallow copy）**：只复制对象本身，不复制内部的子对象（子对象还是引用）
- **深拷贝（deep copy）**：递归复制对象及其所有子对象

```python
import copy

a = [[1, 2], [3, 4]]

# 浅拷贝
b = copy.copy(a)    # 或 b = a.copy() / b = a[:]
b[0][0] = 999
print(a[0][0])  # 999（被影响）

# 深拷贝
c = copy.deepcopy(a)
c[0][0] = 888
print(a[0][0])  # 999（不受影响）
```

---

### Q61: 迭代器和生成器的区别？

| 对比 | 迭代器（Iterator） | 生成器（Generator） |
|------|-------------------|---------------------|
| 实现方式 | 类实现 `__iter__` 和 `__next__` | 函数中使用 `yield` 关键字 |
| 代码量 | 需要维护状态，代码较多 | 简洁，自动保存状态 |
| 内存 | 需要实现完整的类 | 惰性求值，省内存 |

```python
# 迭代器
class CountDown:
    def __init__(self, start):
        self.count = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        self.count -= 1
        return self.count + 1

# 生成器（更简洁）
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

---

### Q62: 闭包是什么？

**答：** 闭包是指在一个内部函数中，引用了外部函数的变量，并且外部函数的返回值是内部函数。

```python
def outer(x):
    def inner(y):
        return x + y  # inner 引用了 outer 的变量 x
    return inner  # 返回 inner 函数

add_5 = outer(5)  # 创建闭包，x 固定为 5
print(add_5(3))   # 8
print(add_5(10))  # 15
```

**闭包的作用：**
- 保存状态（避免使用全局变量）
- 延迟计算
- 装饰器的底层原理

---

### Q63: 装饰器是什么？有哪些应用场景？

**答：** 装饰器本质是一个函数，它接收一个函数作为参数并返回一个新的函数。用于在不修改原函数代码的前提下增加额外的功能。

```python
# 日志装饰器
def log(func):
    def wrapper(*args, **kwargs):
        print(f'调用函数 {func.__name__}，参数: {args} {kwargs}')
        result = func(*args, **kwargs)
        print(f'函数 {func.__name__} 返回: {result}')
        return result
    return wrapper

@log
def add(a, b):
    return a + b

add(1, 2)
# 输出:
# 调用函数 add，参数: (1, 2) {}
# 函数 add 返回: 3
```

**常见应用场景：**

| 场景 | 示例 |
|------|------|
| 日志记录 | 自动记录函数调用信息 |
| 权限校验 | Django 的 `@login_required` |
| 缓存 | `@cache_page` 缓存响应 |
| 性能测试 | 计时装饰器 |
| 事务管理 | Django 的 `@transaction.atomic` |
| 路由注册 | Flask 的 `@app.route('/')` |
| 重试机制 | 失败自动重试 |

**带参数的装饰器：**
```python
def retry(times=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise e
                    print(f'重试第 {i+1} 次...')
        return wrapper
    return decorator

@retry(times=5)
def unstable_request():
    import random
    if random.random() < 0.7:
        raise Exception('请求失败')
    return '成功'
```

---

### Q64: Python 的内存管理机制？

**答：**

**1. 引用计数为主：**
- 每个对象维护一个引用计数，计数为 0 时自动回收
- `sys.getrefcount(obj)` 可查看引用计数
- 缺点：循环引用无法回收

**2. 标记-清除（Mark-Sweep）辅助：**
- 解决循环引用问题
- 从根对象出发，标记所有可达对象
- 清除不可达对象

**3. 分代回收（Generational Collection）：**
- 分为 0/1/2 三代
- 新创建的对象在 0 代，经过多次 GC 仍存活则晋升
- 0 代回收最频繁，2 代最少

```python
import sys
a = []
b = a
print(sys.getrefcount(a))  # 3（a, b, getrefcount的参数）
```

**4. 小整数对象池：**
- -5 ~ 256 的整数预先创建好，重复使用

**5. 字符串驻留（interning）：**
- 短字符串和由合法标识符组成的字符串会被驻留

---

### Q65: 多线程 vs 多进程 vs 协程？

| 维度 | 多线程 Thread | 多进程 Process | 协程 Coroutine |
|------|--------------|----------------|---------------|
| 适合场景 | I/O 密集型 | CPU 密集型 | I/O 密集型 |
| GIL 限制 | 受限 | 不受限 | 不受限（单线程内） |
| 内存开销 | 小（共享内存） | 大（独立内存） | 极小 |
| 切换开销 | 中等 | 大 | 极小（用户态切换） |
| 数据通信 | 简单（共享变量） | 复杂（IPC） | 简单（共享变量） |
| 并发数量 | 几十-几百 | CPU 核数 | 成千上万 |

```python
# 多线程示例（I/O 密集型）
import threading
import requests

def download(url):
    response = requests.get(url)
    print(f'{url}: {len(response.content)} bytes')

threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads:
    t.start()
for t in threads:
    t.join()

# 协程示例（异步 I/O）
import asyncio
import aiohttp

async def download_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            print(f'{url}: {len(content)} bytes')

async def main():
    tasks = [download_async(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

---
