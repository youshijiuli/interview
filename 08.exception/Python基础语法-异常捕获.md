## 十四、异常捕获

### 14.1 什么是异常

异常是程序在运行过程中遇到的错误，会导致程序崩溃。我们应该在可能出错的地方进行异常捕获，使程序更健壮。

```python
# 常见的异常示例
# print(1 / 0)          # ZeroDivisionError: division by zero
# int("abc")            # ValueError: invalid literal for int()
# print(unknown_var)    # NameError: name 'unknown_var' is not defined
# [1, 2, 3][10]         # IndexError: list index out of range
# {"a": 1}["b"]         # KeyError: 'b'
```

### 14.2 常见异常类型

```python
# BaseException          所有异常的基类
#   +-- SystemExit       解释器请求退出
#   +-- KeyboardInterrupt 用户中断执行（Ctrl+C）
#   +-- Exception        常规错误的基类
#        +-- ValueError          传入无效参数
#        +-- TypeError           对类型无效的操作
#        +-- NameError           未声明/初始化对象
#        +-- IndexError          序列索引不存在
#        +-- KeyError            映射键不存在
#        +-- ZeroDivisionError   除零错误
#        +-- FileNotFoundError   文件未找到
#        +-- ImportError         导入模块失败
#        +-- AttributeError      对象没有该属性
#        +-- SyntaxError         Python 语法错误
#        +-- IndentationError    缩进错误
```

### 14.3 try/except/else/finally 完整语法

```python
# 基础语法
try:
    # 可能发生异常的代码
    result = 10 / 0
except:
    # 发生异常时执行的代码
    print("发生了异常")

# ======== 完整语法 ========

try:
    # 正常执行可能出错的代码
    num = int(input("请输入数字："))
    result = 100 / num
except ValueError:
    # 捕获特定类型的异常
    print("输入的不是数字！")
except ZeroDivisionError:
    # 捕获除零异常
    print("不能除以零！")
except (TypeError, KeyError) as e:
    # 同时捕获多种异常，并将异常信息赋值给变量 e
    print(f"发生类型/键异常：{e}")
except Exception as e:
    # 捕获所有异常（Exception 是所有常规异常的基类）
    print(f"发生未知异常：{e}")
else:
    # 没有发生任何异常时执行
    print(f"100 / {num} = {result}")
finally:
    # 无论是否发生异常，都会执行
    print("程序执行完毕")
```

### 14.4 主动抛出异常（raise）

```python
# raise 关键字用于主动抛出异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数！")
    if age > 150:
        raise ValueError("年龄超出人类范围！")
    return age

try:
    check_age(-5)
except ValueError as e:
    print(f"校验失败：{e}")
```

### 14.5 断言（assert）

```python
# assert 用于在程序中设置检查点
# 语法：assert 条件, "异常信息"
# 条件为 False 时抛出 AssertionError

def divide(a, b):
    assert b != 0, "除数不能为零！"
    return a / b

print(divide(10, 2))   # 5.0
# print(divide(10, 0)) # AssertionError: 除数不能为零！

# assert 常用于开发和测试阶段，生产环境可用 -O 参数禁用
```
