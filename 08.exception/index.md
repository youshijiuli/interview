

## 异常

## 异常的概念

- 程序在运行时，如果 `Python 解释器` **遇到** 到一个错误，**会停止程序的执行，并且提示一些错误信息**，这就是 **异常**
- **程序停止执行并且提示错误信息** 这个动作，我们通常称之为：**抛出(raise)异常**

##  捕获异常

### 简单的捕获异常语法

- 在程序开发中，如果 **对某些代码的执行不能确定是否正确**，可以增加 `try(尝试)` 来 **捕获异常**
- 捕获异常最简单的语法格式：

```
try:
    尝试执行的代码
except:
    出现错误的处理
```

- `try` **尝试**，下方编写要尝试代码，不确定是否能够正常执行的代码
- `except` **如果不是**，下方编写尝试失败的代码

#### 简单异常捕获演练 —— 要求用户输入整数

```
try:
    # 提示用户输入一个数字
    num = int(input("请输入数字："))
except:
    print("请输入正确的数字")
```

### 错误类型捕获

- 在程序执行时，可能会遇到 **不同类型的异常**，并且需要 **针对不同类型的异常，做出不同的响应**，这个时候，就需要捕获错误类型了
- 语法如下：

```
try:
    # 尝试执行的代码
    pass
except 错误类型1:
    # 针对错误类型1，对应的代码处理
    pass
except (错误类型2, 错误类型3):
    # 针对错误类型2 和 3，对应的代码处理
    pass
except Exception as result:
    print("未知错误 %s" % result)
```

- try...except...else  如果没有发生异常，则执行else中的内容
```python
try:
    num = 0 / 10
except Exception as e:
    print('分母不能为0')
    # raise e # 可以选择将异常抛出
else:
    print('没有发生异常..')


try:
    num = int(input("请输入整数："))
    result = 8 / num
    print(result)
except ValueError:
    print("请输入正确的整数")
except ZeroDivisionError:
    print("除 0 错误")
```


- 当 `Python` 解释器 **抛出异常** 时，**最后一行错误信息的第一个单词，就是错误类型**

#### 异常类型捕获演练 —— 要求用户输入整数


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



**需求**

1. 提示用户输入一个整数
2. 使用 `8` 除以用户输入的整数并且输出

```
try:
    num = int(input("请输入整数："))
    result = 8 / num
    print(result)
except ValueError:
    print("请输入正确的整数")
except ZeroDivisionError:
    print("除 0 错误")
```

#### 捕获未知错误

- 在开发时，**要预判到所有可能出现的错误**，还是有一定难度的
- 如果希望程序 **无论出现任何错误**，都不会因为 `Python` 解释器 **抛出异常而被终止**，可以再增加一个 `except`

语法如下：

```
except Exception as result:
    print("未知错误 %s" % result)
```

### 异常捕获完整语法

- 在实际开发中，为了能够处理复杂的异常情况，完整的异常语法如下：

> 提示：
>
> - 有关完整语法的应用场景，在后续学习中，**结合实际的案例**会更好理解
> - 现在先对这个语法结构有个印象即可

```
try:
    # 尝试执行的代码
    pass
except 错误类型1:
    # 针对错误类型1，对应的代码处理
    pass
except 错误类型2:
    # 针对错误类型2，对应的代码处理
    pass
except (错误类型3, 错误类型4):
    # 针对错误类型3 和 4，对应的代码处理
    pass
except Exception as result:
    # 打印错误信息
    print(result)
else:
    # 没有异常才会执行的代码
    pass
finally:
    # 无论是否有异常，都会执行的代码
    print("无论是否有异常，都会执行的代码")
```

- `else` 只有在没有异常时才会执行的代码
- `finally` 无论是否有异常，都会执行的代码
- 之前一个演练的 **完整捕获异常** 的代码如下：

```
try:
    num = int(input("请输入整数："))
    result = 8 / num
    print(result)
except ValueError:
    print("请输入正确的整数")
except ZeroDivisionError:
    print("除 0 错误")
except Exception as result:
    print("未知错误 %s" % result)
else:
    print("正常执行")
finally:
    print("执行完成，但是不保证正确")
```

##  异常的传递

- **异常的传递** —— 当 **函数/方法** 执行 **出现异常**，会 **将异常传递** 给 函数/方法 的 **调用一方**
- 如果 **传递到主程序**，仍然 **没有异常处理**，程序才会被终止

> 提示

- 在开发中，可以在主函数中增加 **异常捕获**
- 而在主函数中调用的其他函数，只要出现异常，都会传递到主函数的 **异常捕获** 中
- 这样就不需要在代码中，增加大量的 **异常捕获**，能够保证代码的整洁

**需求**

1. 定义函数 `demo1()` **提示用户输入一个整数并且返回**
2. 定义函数 `demo2()` 调用 `demo1()`
3. 在主程序中调用 `demo2()`

```
def demo1():
    return int(input("请输入一个整数："))


def demo2():
    return demo1()

try:
    print(demo2())
except ValueError:
    print("请输入正确的整数")
except Exception as result:
    print("未知错误 %s" % result)
```

## 抛出 `raise` 异常

### 应用场景

- 在开发中，除了 **代码执行出错** `Python` 解释器会 **抛出** 异常之外
- 还可以根据 **应用程序** **特有的业务需求** **主动抛出异常**

**示例**

- 提示用户 **输入密码**，如果 **长度少于 8**，抛出 **异常**

![image-20210401165707052](https://gitee.com/chushi123/picgo/raw/master/picture/image-20210401165707052.png)

**注意**

- 当前函数 **只负责** 提示用户输入密码，如果 **密码长度不正确，需要其他的函数进行额外处理**
- 因此可以 **抛出异常**，由其他需要处理的函数 **捕获异常**

###  抛出异常

- `Python` 中提供了一个 `Exception` **异常类**
- 在开发时，如果满足特定业务需求时，希望抛出异常，可以：
  1. **创建** 一个 `Exception` 的 **对象**
  2. 使用 `raise` **关键字** 抛出 **异常对象**

**需求**

- 定义 `input_password` 函数，提示用户输入密码
- 如果用户输入长度 < 8，抛出异常
- 如果用户输入长度 >=8，返回输入的密码

```
def input_password():

    # 1. 提示用户输入密码
    pwd = input("请输入密码：")

    # 2. 判断密码长度，如果长度 >= 8，返回用户输入的密码
    if len(pwd) >= 8:
        return pwd

    # 3. 密码长度不够，需要抛出异常
    # 1> 创建异常对象 - 使用异常的错误信息字符串作为参数
    ex = Exception("密码长度不够")

    # 2> 抛出异常对象
    raise ex


try:
    user_pwd = input_password()
    print(user_pwd)
except Exception as result:
    print("发现错误：%s" % result)
```




## 032、python中有哪些标准异常类


```python



# BaseException
# 下面有SystemExit/KeyboardInterrupt/GeneratorExit/Exception(其他异常都属于它)


class Exception1(Exception):
    pass

class Exception2(Exception):
    pass



try:
     # func   # 可能会抛出异常的代码
    print(1/0)
except (Exception1, Exception2) as e:  # 可以捕获多个异常并处理
    # 异常处理的代码
    print(e)
else:
    pass
    # pass  # 异常没有发生的时候代码逻辑
finally:
    pass     # 无论异常有没有发生都会执行的代码，一般处理资源的关闭和释放


# 继承Exception实现自定义异常，给异常加上一些附加信息
#
# 不用baseException是因为这样的话ctrl+c的keybord异常就用不了了


```


### 类

| 异常名称 | 描述 |
|-----|-----|
| BaseException	| 所有异常的基类 |
| SystemExit	| 解释器请求退出 |
| KeyboardInterrupt	| 用户中断执行(通常是输入^C) |
| Exception	| 常规错误的基类 |
| StopIteration	| 迭代器没有更多的值 |
| GeneratorExit	| 生成器(generator)发生异常来通知退出 |
| SystemExit	| Python 解释器请求退出 |
| StandardError	| 所有的内建标准异常的基类 |
| ArithmeticError	| 所有数值计算错误的基类 |
| FloatingPointError	| 浮点计算错误 |
| OverflowError	| 数值运算超出最大限制 |
| ZeroDivisionError	| 除(或取模)零 (所有数据类型) |
| AssertionError	| 断言语句失败 |
| AttributeError	| 对象没有这个属性 |
| EOFError	| 没有内建输入,到达EOF 标记 |
| EnvironmentError	| 操作系统错误的基类 |
| IOError	| 输入/输出操作失败 |
| OSError	| 操作系统错误 |
| WindowsError	| 系统调用失败 |
| ImportError	| 导入模块/对象失败 |
| KeyboardInterrupt	| 用户中断执行(通常是输入^C) |
| LookupError	| 无效数据查询的基类 |
| IndexError	| 序列中没有没有此索引(index) |
| KeyError	| 映射中没有这个键 |
| MemoryError	| 内存溢出错误(对于Python 解释器不是致命的) |
| NameError	| 未声明/初始化对象 (没有属性) |
| UnboundLocalError	| 访问未初始化的本地变量 |
| ReferenceError	| 弱引用(Weak reference)试图访问已经垃圾回收了的对象 |
| RuntimeError	| 一般的运行时错误 |
| NotImplementedError	| 尚未实现的方法 |
| SyntaxError	| Python 语法错误 |
| IndentationError	| 缩进错误 |
| TabError	| Tab 和空格混用 |
| SystemError	| 一般的解释器系统错误 |
| TypeError	| 对类型无效的操作 |
| ValueError	| 传入无效的参数 |
| UnicodeError	| Unicode 相关的错误 |
| UnicodeDecodeError	| Unicode 解码时的错误 |
| UnicodeEncodeError	| Unicode 编码时错误 |
| UnicodeTranslateError	| Unicode 转换时错误 |
| Warning	| 警告的基类 |
| DeprecationWarning	| 关于被弃用的特征的警告 |
| FutureWarning	| 关于构造将来语义会有改变的警告 |
| OverflowWarning	| 旧的关于自动提升为长整型(long)的警告 |
| PendingDeprecationWarning	| 关于特性将会被废弃的警告 |
| RuntimeWarning	| 可疑的运行时行为(runtime behavior)的警告 |
| SyntaxWarning	| 可疑的语法的警告 |
| UserWarning	| 用户代码生成的警告 |



## Python

##### 说一下异常的处理

try...except...finally

try 中代码没有异常，执行else

finally 则为 不管 try 有没有异常都执行

except 单个异常 as 别名

except (多个异常):

except Exception: 万能异常

raise 主动抛出异常

也可以自定义异常类， 继承BaseException

##### 异常种类

> AttributeError 试图访问一个对象没有的树形，比如foo.x，但是foo没有属性x
> IOError 输入/输出异常；基本上是无法打开文件
> ImportError 无法引入模块或包；基本上是路径问题或名称错误
> IndentationError 语法错误（的子类） ；代码没有正确对齐
> IndexError 下标索引超出序列边界，比如当x只有三个元素，却试图访问x[5]
> KeyError 试图访问字典里不存在的键
> KeyboardInterrupt Ctrl+C被按下
> NameError 使用一个还未被赋予对象的变量
> SyntaxError Python代码非法，代码不能编译(个人认为这是语法错误，写错了）
> TypeError 传入对象类型与要求的不符合
> UnboundLocalError 试图访问一个还未被设置的局部变量，基本上是由于另有一个同名的全局变量，
> 导致你以为正在访问它
> ValueError 传入一个调用者不期望的值，即使值的类型是正确的



## 面试题

##### 介绍一下try except的用法和作用？
* 主要用来处理异常
* 完整用法如下：
```python
try:
     Normal execution block
except A:
     Exception A handle
except B:
     Exception B handle
except:
     Other exception handle
else:
     if no exception,get here
finally:
     print("finally")   
```

---

##### 写出以下代码的输出结果：
```python
def test():
    try:
        raise ValueError('something wrong')
    except ValueError as e:
        print('error occured')
        return
    finally:
        print('ok')
test()
```
* 结果(finally无论怎样都会执行)
>error occured
>ok

---

##### 什么是断言(assert)?应用场景？
[断言的参考](https://blog.csdn.net/shujuanyaning/article/details/47184541)

* assert是用来检查一个条件，如果它为真，就不做任何事。如果它为假，则会抛出AssertError并且包含错误信息。
* 应用场景：
    1. 防御型编程
    2. 运行时检查程序逻辑
    3. 检查约定
    4. 程序常量
    5. 检查文档


### 如何捕获异常，常用的异常机制有哪些？  
如果我们没有对异常进行任何预防，那么在程序执行的过程中发生异常，就会中断程序，调用python默认的异常处理器，并在终端输出异常信息。  
`try...except...finally`语句:当try语句执行时发生异常，回到try语句层，寻找后面是否有except语句。  
找到except语句后，会调用这个自定义的异常处理器。except将异常处理完毕后，程序继续往下执行。finally语句表示，无论异常发生与否，finally中的语句都要执行。  
assert语句：判断assert后面紧跟的语句是True还是False，如果是True则继续执行print，如果是False则中断程序，调用默认的异常处理器，同时输出assert语句逗号后面的提示信息。  
with语句：如果with语句或语句块中发生异常，会调用默认的异常处理器处理，但文件还是会正常关闭。  


#### 题目38：举例说明什么情况下会出现`KeyError`、`TypeError`、`ValueError`。

举一个简单的例子，变量`a`是一个字典，执行`int(a['x'])`这个操作就有可能引发上述三种类型的异常。如果字典中没有键`x`，会引发`KeyError`；如果键`x`对应的值不是`str`、`float`、`int`、`bool`以及`bytes-like`类型，在调用`int`函数构造`int`类型的对象时，会引发`TypeError`；如果`a[x]`是一个字符串或者字节串，而对应的内容又无法处理成`int`时，将引发`ValueError`。


#### 37 介绍一下except的用法和作用？
答：try…except…except…[else…][finally…]
执行try下的语句，如果引发异常，则执行过程会跳到except语句。对每个except分支顺序尝试执行，如果引发的异常与except中的异常组匹配，执行相应的语句。如果所有的except都不匹配，则异常会传递到下一个调用本代码的最高层try代码中。
try下的语句正常执行，则执行else块代码。如果发生异常，就不会执行
如果存在finally语句，最后总是会执行。
