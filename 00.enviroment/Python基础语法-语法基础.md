## 二、注释

### 2.1 单行注释

```python
# 这是单行注释，以 # 开头
# 注释的内容不会被作为代码执行
name = "dream"  # 这是行尾注释
```

### 2.2 多行注释

```python
'''
这是多行注释
使用三个单引号包裹
可以跨越多行
'''

"""
这也是多行注释
使用三个双引号包裹
同样可以跨越多行
"""
```

> 注意：多行注释本质上是未被赋值的字符串字面量，在特定场景下（如 docstring）有特殊含义。

## 三、变量与常量

### 3.1 什么是变量

变量是用于存储数据值的标识符，可以通过变量名访问和操作这些数据。变量就像程序中的一个容器，用于存储和管理数据。

程序执行的本质就是一系列状态的变化，变量的存在使得程序能够灵活地处理数据，而不是每次硬编码数据值。

```python
# 变量就是可以变化的量
age = 18       # 年龄
name = "张三"  # 姓名
score = 95.5   # 分数
```

### 3.2 变量的定义与调用

```python
# 变量定义：变量名 = 变量值
# = 是赋值符号，将右侧的值赋给左侧的变量名
name = "dream"
age = 18

# 变量调用：直接使用变量名
print(name)  # dream
print(age)   # 18

# 内部原理：
# 在内存中开辟一块空间存储变量值，然后用变量名指向这块内存空间地址
name = "dream"  # 在内存中存储 "dream"，name 指向这块内存
name = "hope"   # 重新赋值，"dream" 的引用被移除，"hope" 被存储
```

### 3.3 变量的三大特性

```python
name = "dream"

# 特性一：变量值 —— 直接打印变量名获取
print(name)     # dream

# 特性二：变量类型 —— 使用 type() 函数查看
print(type(name))  # <class 'str'>

# 特性三：内存地址 —— 使用 id() 函数查看
print(id(name))    # 例如：140722345678912
```

### 3.4 变量名的命名规范

```python
# 规则一：变量名可以是 字母（大小写）+ 数字 + 下划线 _ 的任意组合
user_name = "dream"      # 正确
_username = "dream"      # 正确
User_name = "dream"      # 正确
USER01_NAME = "dream"    # 正确

# 规则二：数字不能作为变量名的开头
# 01_name = "dream"      # 错误！不能以数字开头

# 规则三：关键字不能作为变量名
# if_user 虽然包含 if 但不是纯关键字，可以接受
# def = "dream"          # 错误！def 是关键字
# if = "dream"           # 错误！if 是关键字
# class = "dream"        # 错误！class 是关键字
```

### 3.5 变量名的命名风格

```python
# 大驼峰（PascalCase）：每个单词首字母大写
UserName = "dream"

# 小驼峰（camelCase）：第一个单词首字母小写，其余单词首字母大写
userName = "dream"

# 下划线命名（snake_case，Python 推荐风格）：
# 全小写单词用下划线连接
user_name = "dream"
```

> Python 官方推荐使用 **snake_case**（小写字母 + 下划线）命名风格，遵循 PEP8 规范。

### 3.6 常量

常量是程序运行过程中不会轻易改变的量。在 Python 中，常量通常用全大写字母声明，虽然 Python 语法上允许修改，但约定上不应修改。

```python
# Python 中常量的命名约定：全大写
PI = 3.1415926
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Python 中常量本质上仍是变量，可以在语法层面被修改
# 但按照约定，我们不应修改全大写命名的"常量"
# PI = 3.14  # 语法允许，但不建议这样做
```

> 注意：在 C/Java 等语言中常量定义后不可修改，但 Python 没有真正的常量机制，完全依赖开发者自觉遵守约定。

---

## 五、程序与用户交互

### 5.1 输入（input）

```python
# input() 用于接收用户的键盘输入
# input 接收的所有输入均为字符串类型

username = input("请输入用户名：")
password = input("请输入密码：")

print(username, type(username))  # 用户输入的内容 <class 'str'>

# 如果需要数字类型，需要进行类型转换
age = input("请输入年龄：")  # 用户输入 "18"
age = int(age)               # 转换为整数
print(age, type(age))        # 18 <class 'int'>

# 类型转换的前提：字符串内容必须是合法的数字格式
# int("abc")  # 错误！ValueError
```

### 5.2 输出（print）

```python
# print() 用于向控制台输出内容

# 基本输出
print("Hello World")

# 输出变量
name = "dream"
print(name)

# print 的 end 参数（默认值为 \n 换行符）
print(1, end="*")
print(2)
# 输出：1*2

# 一次输出多个值
print("姓名", "年龄", "性别")  # 姓名 年龄 性别
print("a", "b", "c", sep="-")  # a-b-c
```
