# Python 函数与模块

## 目录

1. [函数定义与调用](#一函数定义与调用)
2. [函数参数](#二函数参数)
3. [函数返回值](#三函数返回值)
4. [函数类型注解](#四函数类型注解)
5. [名称空间与作用域](#五名称空间与作用域)
6. [闭包函数](#六闭包函数)
7. [装饰器](#七装饰器)
8. [迭代器与可迭代对象](#八迭代器与可迭代对象)
9. [生成器](#九生成器)
10. [模块与包](#十模块与包)
11. [序列化模块](#十一序列化模块)
12. [os 模块](#十二os-模块)
13. [时间模块](#十三时间模块)
14. [随机模块](#十四随机模块)
15. [摘要算法模块](#十五摘要算法模块)
16. [日志模块](#十六日志模块)
17. [subprocess 模块](#十七subprocess-模块)
18. [re 正则表达式模块](#十八re-正则表达式模块)
19. [常用内置函数](#十九常用内置函数)

---

## 一、函数定义与调用

### 1.1 什么是函数

函数就是一系列代码的集合体，相当于提前做好的工具。函数能够帮助我们实现重复代码的复用，减少代码冗余。

在前面的学习中，我们掌握了基本数据类型和流程控制语句。随着开发的功能越来越多，代码会越来越冗余。解决方式就是将可复用的逻辑封装成函数，哪里需要就调用哪里。

### 1.2 函数的定义

借助 `def` 关键字来定义函数：

```python
# 函数的定义语法
def 函数名(参数):
    """函数文档字符串（可选）"""
    函数体代码
```

**示例：**

```python
# 【1】无参无返回值的函数
def login():
    """显示登录欢迎信息"""
    print("欢迎来到登录功能!")

# 【2】有一个参数但没有返回值的函数
def login(username):
    """带用户名的登录欢迎信息"""
    print(f"欢迎 {username} 来到登录功能!")

# 【3】有多个参数但没有返回值
def add(x, y):
    """计算两数之和并打印"""
    result = x + y
    print(f"当前加法的结果是 {result}")

# 【4】有参数有返回值的函数
def add(x, y):
    """计算两数之和并返回"""
    result = x + y
    return result
```

### 1.3 函数的调用方式

```python
# 【1】直接调用 —— 直接根据函数名调用
def add(x, y):
    return x + y

result = add(1, 2)
print(result)  # 3

# 【2】间接调用 —— 将函数名赋值给另一个变量再调用
# 函数名本身存储的是函数的内存地址
print(add)  # <function add at 0x102a4a050>

res = add          # 将函数地址赋值给新变量
print(res(5, 6))   # 30

# 【3】表达式调用 —— 将函数的返回值作为表达式的一部分
def add(x, y):
    return x * y

def func(a, b):
    return a + b

# add(1, 6) 的返回值 6 作为 func 的第一个参数
print(func(add(1, 6), 3))  # 9

# 【4】函数作为参数 —— 将函数当作参数传给另一个函数
def get_username_password():
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()
    return username, password

def login():
    username, password = get_username_password()
    if username == "dream" and password == "521":
        print("登录成功")
    else:
        print("登录失败")

# 【5】使用函数字典进行动态调度
def login():
    print("登录功能")

def register():
    print("注册功能")

func_dict = {
    "1": login,
    "2": register
}

while True:
    func_id = input("请输入功能ID: ").strip()
    if func_id not in func_dict:
        print("当前功能不存在")
        continue
    func = func_dict.get(func_id)
    func()  # 根据用户输入的ID动态调用对应函数
```

---

## 二、函数参数

### 2.1 形参与实参

- **形参（形式参数）**：在函数定义阶段，写在函数名后面小括号里的变量名，用于接收外部传入的数据。
- **实参（实际参数）**：在函数调用时实际传入的具体值。

```python
def add(x, y):      # x 和 y 是形参
    return x + y

add(1, 2)           # 1 和 2 是实参
```

### 2.2 位置参数与关键字参数

按照传值方式的不同，参数分为位置参数和关键字参数：

```python
def login(username, password):
    print(f"username: {username}")
    print(f"password: {password}")

# 【1】按照位置传递参数 —— 必须严格按照形参定义的顺序传值
login("dream", "521")

# 【2】按照关键字传递参数 —— 根据形参的名字指定传值，顺序可以调换
login(username="dream", password="521")
login(password="521", username="dream")  # 顺序无关

# 【3】混合使用 —— 关键字参数必须放在位置参数后面
login("dream", password="521")  # 正确
# login(password="521", "dream")  # 错误！关键字参数后不能再有位置参数
```

### 2.3 默认参数

在函数定义阶段给形参赋予一个初始值，如果调用时没有传入该参数则使用默认值：

```python
def student(name, age, class_no, gender="male"):
    """学生信息录入，默认性别为男"""
    print(f"姓名: {name}, 年龄: {age}, 性别: {gender}, 班级: {class_no}")

# 大部分学生为男生，少数为女生
student(name="dream", age=18, class_no=1)               # 使用默认值 male
student(name="dream", age=18, class_no=1)               # 使用默认值 male
student(name="pop", age=18, class_no=1, gender="female")  # 覆盖默认值

# 注意：默认参数必须放在位置参数后面
# def student(name, age, gender="male", class_no):  # 错误写法
```

**默认参数的陷阱 —— 可变数据类型作为默认值：**

```python
# 错误做法：用空列表作为默认参数
def append_list(num, num_list=[]):
    num_list.append(num)
    return num_list

print(append_list(1))  # [1]
print(append_list(2))  # [1, 2]  不是预期的 [2]
print(append_list(3))  # [1, 2, 3]  不是预期的 [3]
# 原因：默认参数在函数定义时只创建一次，之后每次调用共享同一个列表对象

# 正确做法：用 None 作为默认值，函数内部判断后创建新列表
def append_list(num, num_list=None):
    if num_list is None:
        num_list = []
    num_list.append(num)
    return num_list

print(append_list(1))  # [1]
print(append_list(2))  # [2]
print(append_list(3))  # [3]
```

### 2.4 可变长位置参数 `*args`

当调用函数时传入的位置参数个数超过形参定义的个数时，多余的位置参数会被 `*args` 以元组的形式接收：

```python
def add(x, y, *args):
    print(f"x={x}, y={y}")
    print(f"多余的位置参数: {args}")

add(1, 2, 3, 4, 5)
# x=1, y=2
# 多余的位置参数: (3, 4, 5)

# * 的解包作用
num_list = [1, 2, 3]
print(*num_list)  # 1 2 3 （将列表元素逐个解包输出）

def login(username, password):
    print(username, password)

user_data = ["dream", 521]
login(*user_data)  # 将列表解包后按位置传入函数
```

### 2.5 可变长关键字参数 `**kwargs`

多余的关键字参数会被 `**kwargs` 以字典的形式接收：

```python
def add(x, y, *args, **kwargs):
    print(f"x={x}, y={y}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

add(x=1, y=2, z=3, u=5)
# x=1, y=2
# args=()
# kwargs={'z': 3, 'u': 5}
```

### 2.6 命名关键字参数

在 `*` 之后的形参称为命名关键字参数，调用时必须使用 `key=value` 的形式传值：

```python
# * 作为分隔符，后面的 z 是命名关键字参数
def add(x, y, *, z):
    print(f"x={x}, y={y}, z={z}")

add(1, 2, z=9)       # 正确
# add(1, 2, 9)       # 错误！z 必须以关键字形式传值

# 命名关键字参数也可以有默认值
def register(name, age, *, sex='male', height):
    print(f"Name: {name}, Age: {age}, Sex: {sex}, Height: {height}")

register('Dream', 18, height='1.8m')
# Name: Dream, Age: 18, Sex: male, Height: 1.8m

# 如果已经有了 *args，命名关键字参数不需要单独的 *
def register(name, age, *args, sex='male', height):
    print(f"Name: {name}, Age: {age}, Args: {args}, Sex: {sex}, Height: {height}")

register('Dream', 18, 1, 2, 3, height='1.8m')
# Name: Dream, Age: 18, Args: (1, 2, 3), Sex: male, Height: 1.8m
```

### 2.7 参数顺序总结

函数定义时参数的推荐顺序：

```
def 函数名(位置参数, 默认参数, *args, 命名关键字参数, **kwargs):
    函数体
```

---

## 三、函数返回值

### 3.1 return 语句

- 函数通过 `return` 语句返回执行结果。
- 如果函数没有 `return` 语句，默认返回 `None`。
- `return` 之后的代码不会被执行。

```python
def add(x, y):
    result = x + y
    return result

res = add(1, 6)
print(res)  # 7

# 没有 return 的函数默认返回 None
def say_hello():
    print("Hello!")

result = say_hello()  # 打印 Hello!，但 result 为 None
```

### 3.2 返回多个值

当 `return` 后面跟着多个值时，实际返回的是一个元组：

```python
def get_username_password():
    """获取用户名和密码，返回多个值"""
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()
    return username, password  # 实际返回 (username, password) 元组

# 用解包赋值接收多个返回值
username, password = get_username_password()
print(username, password)
```

### 3.3 函数返回值的链式调用

一个函数的返回值可以直接作为另一个函数的参数：

```python
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

# add 的返回值 7 作为 multiply 的第一个参数
print(multiply(add(1, 6), 3))  # 21
```

---

## 四、函数类型注解

Python 3.5 之后引入的类型注解可以帮助增强代码的可读性和维护性。类型注解是**弱约束**，不遵守不会报错但会有警告提示。

### 4.1 基础语法

```python
def 函数名(参数名: 参数类型) -> 返回值类型:
    函数体
    return 返回值
```

### 4.2 内置类型注解

```python
# 整数类型
def process_int(data: int) -> None:
    print(f"the data is {data} and the type is {type(data)}")

# 浮点数类型
def process_float(data: float) -> None:
    print(f"the data is {data} and the type is {type(data)}")

# 字符串类型
def process_str(data: str) -> None:
    print(f"the data is {data} and the type is {type(data)}")

# 布尔类型
def process_bool(data: bool) -> None:
    print(f"the data is {data} and the type is {type(data)}")
```

### 4.3 类型别名（List、Dict、Tuple、Set）

```python
from typing import List, Dict, Tuple, Set

# 整数列表
def process_numbers(data: List[int]) -> None:
    print(f"这是一个整数列表: {data}")

# 字符串键、整数值的字典
def process_dict(data: Dict[str, int]) -> None:
    print(f"这是一个字典: {data}")

# 字符串元素的元组
def process_tuple(data: Tuple[str]) -> None:
    print(f"这是一个元组: {data}")

# 整数元素的集合
def process_set(data: Set[int]) -> None:
    print(f"这是一个集合: {data}")
```

### 4.4 Union 和 Optional

```python
from typing import Union, Optional

# Union：参数可以接受多种类型
def double_or_square(number: Union[int, float]) -> Union[int, float]:
    if isinstance(number, int):
        return number * 2
    else:
        return number ** 2

# Optional：参数可以是指定类型或 None
def greet(name: Optional[str]) -> str:
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello, World!"
```

### 4.5 泛型与生成器注解

```python
from typing import TypeVar, List, Generator

# 泛型函数
T = TypeVar('T')

def get_first_element(items: List[T]) -> T:
    return items[0]

first = get_first_element([1, 2, 3])  # 推导类型为 int

# 生成器函数注解
def generate_numbers(n: int) -> Generator[int, None, None]:
    for i in range(n):
        yield i
```

---

## 五、名称空间与作用域

### 5.1 名称空间

名称空间就是存放变量名和变量值映射关系的地方。

| 名称空间 | 说明 | 生命周期 |
|----------|------|----------|
| 内建名称空间 | Python 解释器自带的名称空间（`def`、`if`、`else` 等关键字） | 解释器启动时创建，关闭时销毁 |
| 全局名称空间 | 在 `.py` 文件中定义的变量名、函数名、类名 | 文件被执行时创建，执行完毕销毁 |
| 局部名称空间 | 在函数或类内部定义的变量 | 函数调用时创建，调用结束销毁 |

**加载顺序**：内建 --> 全局 --> 局部

**查找顺序**：局部 --> 全局 --> 内建

### 5.2 作用域（LEGB 规则）

作用域就是变量名和变量值可以被访问的范围，遵循 **LEGB** 规则：

| 层级 | 缩写 | 名称 | 说明 |
|------|------|------|------|
| 1 | L | Local | 嵌套作用域（函数的函数内部） |
| 2 | E | Enclosing | 局部作用域（函数内部） |
| 3 | G | Global | 全局作用域（文件顶层） |
| 4 | B | Built-in | 内建作用域（Python 自带） |

**查找顺序**：L --> E --> G --> B（从内向外查找）

```python
# 演示 LEGB 规则
age = 18  # 全局作用域

def student():
    age = 28  # 局部作用域
    print(f"student age is {age}")

    def inner():
        age = 38  # 嵌套作用域
        print(f"inner age is {age}")

    inner()

student()           # student age is 28  /  inner age is 38
print(f"global age is {age}")  # global age is 18
```

### 5.3 global 和 nonlocal 关键字

- **global**：在局部作用域中修改全局的不可变数据类型时，需要先用 `global` 声明。
- **nonlocal**：在内嵌函数中修改外层函数的局部变量时，需要先用 `nonlocal` 声明。

```python
# global 示例 —— 修改全局不可变数据类型
age = 18
print(f"全局 age={age}, id={id(age)}")

def change_age():
    global age      # 声明要修改全局变量
    age = 28
    print(f"change_age age={age}, id={id(age)}")

change_age()
print(f"全局 age={age}, id={id(age)}")
# 全局 age=18, id=4366205712
# change_age age=28, id=4366206032
# 全局 age=28, id=4366206032

# nonlocal 示例 —— 修改外层函数的局部变量
def outer():
    count = 100

    def inner():
        nonlocal count  # 声明要修改外层 enclosing 变量
        count = 200
        print(f"inner count={count}")

    inner()
    print(f"outer count={count}")

outer()
# inner count=200
# outer count=200

# 注意事项：
# 1. 修改全局可变数据类型（列表、字典）时，不需要 global
#    因为可变数据类型修改的是同一块内存空间
user_dict = {"age": 99}
def func():
    user_dict["age"] = 999  # 不需要 global，直接修改
func()
print(user_dict["age"])  # 999

# 2. 内嵌作用域无法直接修改全局作用域的不可变数据类型
```

---

## 六、闭包函数

### 6.1 函数的特性回顾

```python
# 【1】函数可以被引用（赋值给变量）
def add(x, y):
    return x + y

res = add   # 将函数内存地址赋值给变量
res(1, 2)   # 通过变量调用

# 【2】函数可以作为容器类型（列表、字典）的元素
func_dict = {"add": add}

# 【3】函数可以作为参数传递给另一个函数
def calculate(x, y, func):
    return func(x, y) + x + y

print(calculate(x=1, y=4, func=add))  # 10

# 【4】函数可以作为另一个函数的返回值
def outer():
    def add(x, y):
        return x + y
    return add  # 返回内部函数的地址

inner_func = outer()
print(inner_func(1, 2))  # 3
```

### 6.2 什么是闭包

**闭包函数**：函数内部再定义一个函数，并且这个内部函数用到了外部函数的变量，把内部函数以及引用的外部变量合称为闭包。

闭包 = 内嵌函数 + 外部作用域的变量引用

```python
def add():
    age = 18
    print(locals())  # {'age': 18}

    def inner():
        print(age)            # inner 使用了外部函数的变量 age
        print(locals())       # {'age': 18}

    inner()

add()
```

### 6.3 闭包的应用场景

**场景一：保持状态**

```python
import requests

# 不使用闭包的方式：每次都要传同样的 URL
def get(url):
    return requests.get(url).text

get('https://www.python.org')
get('https://www.python.org')

# 使用闭包的方式：URL 被保存在闭包中，只需调用一次
def page(url):
    def get():
        return requests.get(url).text  # url 被保存在闭包中
    return get

python_page = page('https://www.python.org')
python_page()  # 不需要再传 URL
python_page()  # 可以多次调用
```

**场景二：装饰器（最重要）**

闭包是实现装饰器的基础，装饰器会在下一章详细介绍。

---

## 七、装饰器

### 7.1 什么是装饰器

- **装饰**：为被装饰对象添加新的功能。
- **器**：工具/器具。

装饰器的作用是：**在不修改被装饰对象源代码和调用方式的前提下，为被装饰对象添加额外的功能**。

装饰器遵循**开放封闭原则**：
- 对扩展开放：可以扩展新功能。
- 对修改封闭：不修改原有代码。

**应用场景**：日志记录、性能测试、事务处理、缓存、权限校验等。

### 7.2 无参装饰器

#### 装饰器的推导过程

```python
import time

# 原始函数
def index():
    print("index 运行")
    time.sleep(2)
    return "index 运行结束"

# 需求：给 index 增加计时功能，但不修改原函数代码和调用方式

# 第一步：写一个包装函数
def timer(func):
    def inner():
        start_time = time.time()
        res = func()         # 执行真正的函数
        end_time = time.time()
        print(f"总耗时: {end_time - start_time}s")
        return res
    return inner

# 第二步：用装饰器"包装"原函数
index = timer(index)  # index 现在指向的是 inner 函数的内存地址

# 第三步：调用方式和原来一模一样
result = index()
# index() --> timer 内的 inner() --> func() --> 真正的 index()
```

#### 无参装饰器模板

```python
def outer(func):
    """
    无参装饰器模板
    :param func: 真正的函数内存地址
    """
    def inner():
        # 第一步：在正式执行函数之前做一些校验或预处理
        # 第二步：执行真正的函数
        result = func()
        # 第三步：对返回结果进行定制化处理
        return result
    return inner
```

#### 无参装饰器实战 —— 登录验证

```python
login_dict = {"username": None}

def login_auth(func):
    """装饰器：在调用函数前验证登录状态"""
    def inner():
        if not login_dict.get("username"):
            return False, "请先登录!"
        res = func()
        return res
    return inner

@login_auth  # 等价于 withdraw = login_auth(withdraw)
def withdraw():
    print("取款 starting ...")
    time.sleep(2)
    return True, "取款成功"

@login_auth
def insert():
    print("存款 starting ...")
    time.sleep(2)
    return True, "存款成功"
```

### 7.3 有参装饰器

当被装饰的函数有参数时，需要用 `*args` 和 `**kwargs` 来兼容所有参数情况：

```python
login_dict = {"username": "dream", "password": "521"}

def withdraw(username, money):
    print(f"当前用户 {username} 正在提现 {money} 元")

def transform(username, to_username, money):
    print(f"当前用户 {username} 给 {to_username} 转账了 {money} 元")

# 有参装饰器 —— 用 *args 和 **kwargs 兼容任意参数
def login_auth(func):
    def inner(*args, **kwargs):
        print(f"args: {args}")
        print(f"kwargs: {kwargs}")
        if login_dict.get("username"):
            return func(*args, **kwargs)  # 解包传递给真正的函数
        else:
            return False, "请先登录!"
    return inner

withdraw = login_auth(withdraw)
res = withdraw(username="dream", money=999)

transform = login_auth(transform)
res = transform("dream", "opp", 888)
```

#### 有参装饰器模板

```python
def outer(func):
    def inner(*args, **kwargs):
        # 第一步：在正式进入 func 之前进行校验
        # 第二步：正式执行原本的函数
        result = func(*args, **kwargs)
        # 第三步：对返回结果进行处理
        return result
    return inner
```

### 7.4 语法糖

Python 提供了 `@` 语法糖，使装饰器的使用更加简洁：

```python
# 定义装饰器
def login_auth(func):
    def inner(*args, **kwargs):
        if not login_dict.get("username"):
            return "当前未登录，请先登录!"
        return func(*args, **kwargs)
    return inner

# 语法糖写法
@login_auth  # 等价于 withdraw = login_auth(withdraw)
def withdraw(username, money):
    return f"当前 {username} 取款 {money} 元!"

@login_auth
def transform(username, to_username, money):
    return f"当前 {username} 给 {to_username} 转账 {money} 元!"

print(withdraw("dream", 521))
print(transform("dream", "hope", 521))
```

### 7.5 多层语法糖

多层装饰器的包装顺序：**从下向上包装**（离函数近的先包装）
执行顺序：**从上向下执行**（离函数远的先执行）

```python
login_dict = {"username": "dream", "role": "admin"}

def login_decorator(func):
    def inner(*args, **kwargs):
        print("执行 login_decorator")
        if not login_dict.get("username"):
            return "当前未登录，请先登录!"
        return func(*args, **kwargs)
    return inner

def permission_decorator(func):
    def inner(*args, **kwargs):
        print("执行 permission_decorator")
        if login_dict.get("role") != "admin":
            return "当前没有权限访问!"
        return func(*args, **kwargs)
    return inner

# 包装顺序：从下向上
# 第一步 withdraw = permission_decorator(真正的withdraw)
# 第二步 withdraw = login_decorator(permission_decorator的inner)
@login_decorator       # 第二个包装
@permission_decorator  # 第一个包装（离函数最近）
def withdraw(username, money):
    return f"当前 {username} 取款 {money} 元!"

# 执行顺序：从上向下
# 先执行 login_decorator，再执行 permission_decorator，最后执行 withdraw
res = withdraw("Dream", "9999")
print(res)
# 输出：
# 执行 login_decorator
# 执行 permission_decorator
# ...
```

### 7.6 有参语法糖

有时需要给装饰器传递额外参数，可以通过再封装一层来实现：

```python
login_dict = {"username": "dream", "role": "admin"}

def decorator(tag):
    """根据 tag 选择使用哪个装饰器"""
    if tag == "login":
        def login_decorator(func):
            def inner(*args, **kwargs):
                print("login_decorator")
                if not login_dict.get("username"):
                    return "当前未登录，请先登录!"
                return func(*args, **kwargs)
            return inner
        return login_decorator

    elif tag == "permission":
        def permission_decorator(func):
            def inner(*args, **kwargs):
                print("permission_decorator")
                if login_dict.get("role") != "admin":
                    return "当前没有权限访问!"
                return func(*args, **kwargs)
            return inner
        return permission_decorator

# 有参语法糖的使用
@decorator(tag='login')        # 等价于 @login_decorator
@decorator(tag='permission')   # 等价于 @permission_decorator
def withdraw(username, money):
    return f"当前 {username} 取款 {money} 元!"

print(withdraw("Dream", 999))
# 输出顺序：
# login_decorator
# permission_decorator
# ...
```

### 7.7 装饰器的修复技术（wraps）

当使用装饰器后，用 `help()` 查看被装饰的函数会显示装饰器内嵌函数的注释，而不是原函数的注释。这可能导致敏感信息泄露。使用 `functools.wraps` 可以修复：

```python
from functools import wraps

login_dict = {"username": "dream"}

def login_auth(func):
    @wraps(func)  # 关键：保留原函数的元信息
    def inner(*args, **kwargs):
        """
        装饰器内部注释（不会对外暴露）
        """
        if not login_dict.get("username"):
            return "未登录，请先登录!"
        result = func(*args, **kwargs)
        return result
    return inner

@login_auth
def withdraw(username, money):
    """
    取款功能 —— 从指定账户取款
    :param username: 取款人账号
    :param money: 取款金额
    :return: 取款结果
    """
    return f"当前用户 {username} 余额 {money} 元"

# 使用 help 查看时只显示原函数的注释
help(withdraw)
# Help on function withdraw in module __main__:
# withdraw(username, money)
#     取款功能 —— 从指定账户取款
#     ...
```

---

## 八、迭代器与可迭代对象

### 8.1 可迭代对象（Iterable）

具有 `__iter__()` 方法的对象就是可迭代对象。以下 Python 内置类型都是可迭代对象：

- 字符串（str）
- 列表（list）
- 元组（tuple）
- 字典（dict）
- 集合（set）

```python
# 检测对象是否有 __iter__ 方法
name = "dream"
print(name.__iter__())        # <str_iterator object ...>

print([1, 2, 3].__iter__())   # <list_iterator object ...>
print((1, 2, 3).__iter__())   # <tuple_iterator object ...>
print({"a": 1}.__iter__())    # <dict_keyiterator object ...>
print({1, 2, 3}.__iter__())   # <set_iterator object ...>

# 整数和浮点数不是可迭代对象
# print(1.__iter__())  # 报错！
```

### 8.2 迭代器对象（Iterator）

同时具有 `__iter__()` 和 `__next__()` 方法的对象就是迭代器对象。

```python
# 将可迭代对象转为迭代器对象
name_iter = "Dream".__iter__()  # 等价于 iter("Dream")

# 使用 __next__() 逐个取值（等价于 next()）
print(name_iter.__next__())  # D
print(name_iter.__next__())  # r
print(name_iter.__next__())  # e
print(name_iter.__next__())  # a
print(name_iter.__next__())  # m
# print(name_iter.__next__())  # 取完后再取会抛出 StopIteration 异常
```

**迭代器的特性：**

- 迭代器是一次性的，取完之后无法回退。
- 要再次遍历，必须重新创建一个新的迭代器对象。
- for 循环内部会自动处理 `StopIteration` 异常。

### 8.3 迭代器的优缺点

**优点：**

- 为序列和非序列类型提供了统一的迭代取值方式。
- **惰性计算**：只在需要时才计算下一个值，同一时刻内存中只有一个值，可以处理无限大的数据流。

**缺点：**

- 除非取尽，否则无法获取迭代器的长度。
- 只能取下一个值，不能回到开头，是"一次性"的。
- 如果多个循环共用同一个迭代器，只有一个循环能取到值。

### 8.4 for 循环的工作原理

```python
# for 循环背后的机制等价于：
# 1. 获取可迭代对象的迭代器：iter(obj)
# 2. 循环调用 next() 取值
# 3. 捕获 StopIteration 异常并退出循环

# 手动模拟 for 循环
num_list = [11, 22, 33, 44, 55]
iterator = iter(num_list)  # 获取迭代器
while True:
    try:
        item = next(iterator)  # 尝试取下一个值
        print(item)
    except StopIteration:
        break  # 取完则退出
```

---

## 九、生成器

### 9.1 什么是生成器

生成器是一种特殊的迭代器，可以在需要时生成数据，而不必提前从内存中生成并存储整个数据集。生成器在处理大数据集时具有节省内存、提高效率的特点。

### 9.2 创建生成器的方式

**方式一：生成器表达式（类似列表推导式，但用圆括号）**

```python
# 列表推导式 —— 一次性生成所有数据到内存
num_list = [x * 2 for x in range(5)]
print(num_list)  # [0, 2, 4, 6, 8]

# 生成器表达式 —— 惰性生成，仅在需要时产生数据
g = (x * 2 for x in range(5))
print(g)  # <generator object <genexpr> at 0x1291d1e70>

print(next(g))  # 0
print(next(g))  # 2
print(next(g))  # 4
print(next(g))  # 6
print(next(g))  # 8
# print(next(g))  # StopIteration
```

**方式二：使用 `yield` 关键字**

```python
def my_generator():
    """使用 yield 的函数就是一个生成器函数"""
    yield 1
    yield 2
    yield 3

# 调用生成器函数不会立即执行，而是返回一个生成器对象
iter_obj = my_generator()
print(iter_obj)  # <generator object my_generator at 0x104307840>

print(next(iter_obj))  # 1
print(next(iter_obj))  # 2
print(next(iter_obj))  # 3
```

### 9.3 yield 详解

`yield` 可以暂停函数的执行，保存当前的状态，等待下一次取值时继续执行：

```python
def eater():
    print("当前开始吃饭")
    while True:
        food = yield       # 程序在这里暂停，等待 send() 传入值
        print(f"开始吃 {food}")

# 创建生成器对象
eat_iter = eater()

# 必须先启动生成器（执行到第一个 yield）
next(eat_iter)  # 输出：当前开始吃饭

# 使用 send() 向生成器传值
eat_iter.send("鱼香肉丝")   # 输出：开始吃 鱼香肉丝
eat_iter.send("宫保鸡丁")   # 输出：开始吃 宫保鸡丁

# 注意：刚创建的生成器不能直接 send 非 None 值，
# 必须先调用一次 next() 或 send(None) 来启动生成器。
```

### 9.4 用装饰器自动启动生成器

```python
def init(func):
    """装饰器：自动启动生成器"""
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)   # 创建生成器对象
        next(g)                      # 自动启动
        return g
    return inner

@init
def eater():
    print("当前开始吃饭")
    while True:
        food = yield
        print(f"开始吃 {food}")

# 现在可以直接 send，无需手动启动
eat_iter = eater()
eat_iter.send("鱼香肉丝")  # 直接使用，方便
eat_iter.send("宫保鸡丁")
```

### 9.5 用 yield 实现 range

```python
def my_range(start, end, step=1):
    """用生成器实现自定义 range"""
    while start < end:
        yield start
        start += step

g = my_range(1, 5)
print(next(g))  # 1
print(next(g))  # 2
print(next(g))  # 3
print(next(g))  # 4

# 可以用 for 循环遍历
for i in my_range(1, 10, 2):
    print(i)  # 1, 3, 5, 7, 9
```

---

## 十、模块与包

### 10.1 什么是模块

在 Python 中，一个 `.py` 文件就是一个模块，文件名就是模块名。模块是一系列功能的集合体。

**模块的优点：**

- 极大地提高程序员的开发效率。
- 多个功能通过统一的接口进行调用。
- 代码复用，避免重复编写。

**模块的来源：**

1. **内置模块**：Python 解释器自带的模块（如 `os`、`random`、`re` 等）
2. **第三方模块**：别人开发好的，需要安装后使用（如 `pandas`、`requests` 等）
3. **自定义模块**：自己编写的 `.py` 文件

### 10.2 模块的导入语法

```python
# 【1】import 导入 —— 导入整个模块
import random
print(random.randint(1, 10))
print(random.choice([1, 2, 3, 4, 5]))

# 【2】from...import... 导出 —— 导入模块中的指定内容
from random import randint, choice
print(randint(1, 10))
print(choice([1, 2, 3, 4, 5]))

# 【3】使用 as 取别名
import random as rd
print(rd.randint(1, 10))

# 【4】从包/子模块中导入
from control.Add import add
from control.multy import multy
```

### 10.3 循环导入问题

当模块 A 导入模块 B，而模块 B 也在导入模块 A 时，会发生循环导入，导致程序出错。

**解决方案：**

```python
# 方案一：将 import 语句放在文件末尾（不推荐）

# 方案二：延迟导入 —— 在函数内部需要时才导入
def some_function():
    from other_module import some_func
    some_func()
```

### 10.4 什么是包

包是包含多个模块和 `__init__.py` 文件的文件夹。包是模块的集合体。

**创建包的两种方式：**

1. 在 PyCharm 中右键文件夹，选择 `New` -> `Python Package`
2. 手动创建文件夹，并在其中创建 `__init__.py` 文件

```python
# 包的目录结构示例
# control/               # 包名（文件夹）
#   __init__.py           # 包的初始化文件
#   add.py                # 模块
#   multy.py              # 模块

# 使用方式一：从包中详细导入
from control.add import add
from control.multy import multy

# 使用方式二：在 __init__.py 中注册后直接从包名导入
# __init__.py 内容：
# from .add import add
# from .multy import multy
from control import add, multy
```

### 10.5 相对路径和绝对路径

- **绝对路径**：从盘符（或根目录）开始写的完整路径
- **相对路径**：从当前文件夹开始写的路径

```python
# .  代表当前目录
# .. 代表上一级目录

from .module import something     # 当前目录下的 module
from ..package import something   # 上一级目录下的 package
```

### 10.6 `__name__` 与主文件入口

每个 `.py` 文件都有一个 `__name__` 属性：

- 当文件作为主程序直接运行时，`__name__` 的值为 `"__main__"`
- 当文件作为模块被导入时，`__name__` 的值为模块名

```python
# 典型用法：将测试代码放在 if __name__ == '__main__': 下
def add(x, y):
    return x + y

if __name__ == '__main__':
    # 只有在直接运行本文件时才会执行
    print(add(1, 2))
```

### 10.7 模块导入时发生了什么

```python
# import a  会执行以下步骤：
# 1. 找到 a 模块所在的文件位置
# 2. 从上至下依次加载 a 模块中的所有代码
# 3. 加载完 a 模块后回到原本的文件
# 4. 将 a 模块中的所有名称空间添加到当前文件的名称空间内，并命名为 a
# 5. 只有通过 a.x 才能访问 a 模块中的 x
```

---

## 十一、序列化模块

### 11.1 序列化与反序列化

- **序列化**：将 Python 对象（字典/列表/元组等）转换成字符串的过程
- **反序列化**：将字符串转换回 Python 对象的过程

**为什么要序列化？**
因为文件中没有字典、列表等 Python 数据类型的概念，要想将 Python 数据持久化到文件，或者在不同程序间传递数据，就需要进行序列化。

### 11.2 json 模块

JSON 是一种通用的跨语言数据交换格式，Python 有，Go、C、Java、JavaScript 也都有。

**Python 对象与 JSON 的对应关系：**

| Python | JSON |
|--------|------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True | true |
| False | false |
| None | null |

#### （1）处理 Python 对象

```python
import json

user_data = {
    "dream": {
        "username": "dream",
        "password": "521",
        "age": 18,
        "gender": True,
        "hobby": ["music", "rap", "basketball"]
    }
}

# 序列化 —— 将 Python 对象转换为 JSON 字符串
user_data_json_str = json.dumps(obj=user_data)
print(user_data_json_str, type(user_data_json_str))
# {"dream": {"username": "dream", ...}} <class 'str'>

# 反序列化 —— 将 JSON 字符串转换为 Python 对象
user_data_dict = json.loads(s=user_data_json_str)
print(user_data_dict, type(user_data_dict))
# {'dream': {'username': 'dream', ...}} <class 'dict'>
```

#### （2）处理 JSON 文件

```python
# 将 Python 对象写入 JSON 文件
with open("user_data.json", "w", encoding="utf-8") as fp:
    json.dump(obj=user_data, fp=fp, ensure_ascii=False)

# 从 JSON 文件读取并转换为 Python 对象
with open("user_data.json", "r", encoding="utf-8") as fp:
    data = json.load(fp=fp)

print(data, type(data))
```

**常用参数说明：**
- `ensure_ascii=False`：使用 Unicode 编码而不是只支持 ASCII，这样中文才能正常显示
- `indent`：设置缩进，让 JSON 文件更易读（pretty-print）
- `sort_keys`：按键名排序

### 11.3 pickle 模块

`pickle` 是 Python 独有的序列化模块，能够处理 JSON 无法序列化的 Python 对象（如函数、类等）。

```python
import pickle

# 操作 Python 对象 —— 与 json 用法类似
user_data = {"username": "dream"}

# 序列化 —— 转换为二进制数据
user_data_bytes = pickle.dumps(user_data)
print(user_data_bytes)
# b'\x80\x04\x95\x17\x00\x00\x00...'

# 反序列化 —— 从二进制数据恢复
user_data_dict = pickle.loads(user_data_bytes)
print(user_data_dict)  # {'username': 'dream'}

# 操作文件
def add(x, y):
    return x + y

# 将函数序列化保存到文件（json 做不到这一点）
with open("func_data", "wb") as fp:
    pickle.dump(add, fp)

# 从文件恢复函数
with open("func_data", "rb") as fp:
    obj = pickle.load(fp)

print(obj(1, 6))  # 7 —— 函数恢复正常可用
```

---

## 十二、os 模块

`os` 模块主要用于处理文件路径和文件夹操作。

### 12.1 路径相关操作 `os.path.*`

```python
import os
import datetime

# __file__ 代表当前文件的路径

# 获取当前文件的绝对路径
file_path_abs = os.path.abspath(__file__)
# /Users/dream/Documents/.../script.py

# 获取当前文件所在的文件夹路径
file_dir_abs = os.path.dirname(__file__)
# /Users/dream/Documents/.../

# 判断当前文件路径是否存在
print(os.path.exists("/some/path"))  # True 或 False

# 拼接文件路径（自动处理不同系统的分隔符）
img_dir = os.path.join(file_dir_abs, "img")
# /Users/dream/Documents/.../img

# 切割文件路径（返回 (目录部分, 文件名部分)）
print(os.path.split(file_path_abs))
# ('/Users/dream/...', 'script.py')

# 获取路径最后部分的文件名或文件夹名
print(os.path.basename(file_path_abs))  # script.py

# 判断路径是否是文件
print(os.path.isfile(file_path_abs))    # True

# 判断路径是否是文件夹
print(os.path.isdir(file_dir_abs))      # True

# 判断路径是否是绝对路径
print(os.path.isabs("/absolute/path"))   # True
print(os.path.isabs("./relative/path"))  # False

# 获取文件的时间信息
print(os.path.getatime(file_path_abs))   # 最后访问时间（时间戳）
print(os.path.getctime(file_path_abs))   # 创建时间（时间戳）
print(os.path.getmtime(file_path_abs))   # 最后修改时间（时间戳）

# 转换为可读时间格式
print(datetime.datetime.fromtimestamp(os.path.getatime(file_path_abs)))

# 获取文件大小（字节）
print(os.path.getsize(file_path_abs))     # 3053

# 获取当前系统的路径分隔符
print(os.path.sep)  # Windows: \    Mac/Linux: /
```

### 12.2 文件/文件夹操作 `os.*`

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 【1】创建单级文件夹
img_dir = os.path.join(BASE_DIR, "img")
os.mkdir(img_dir)

# 【2】创建多级文件夹
nested_dir = os.path.join(BASE_DIR, "img", "girl")
os.makedirs(nested_dir, exist_ok=True)  # exist_ok=True 存在时不报错

# 【3】删除单级文件夹（文件夹必须为空）
os.rmdir(img_dir)

# 【4】删除多级文件夹（所有层级必须为空）
os.removedirs(nested_dir)

# 【5】列出当前文件夹下的所有文件名
file_list = os.listdir(BASE_DIR)

# 【6】重命名文件或文件夹
os.rename("old_name", "new_name")

# 【7】删除文件
os.remove("file_path")

# 【8】获取文件元信息
stat_info = os.stat(file_path)
# 包含：st_mode（权限）、st_size（大小）、st_atime（访问时间）等

# 【9】获取当前工作目录
print(os.getcwd())

# 【10】切换工作目录
os.chdir("/new/path")

# 【11】执行系统命令
os.system("ls")        # 结果直接输出到控制台
result = os.popen("ls").read()  # 获取命令执行结果
```

### 12.3 系统信息相关

```python
# 获取路径分隔符
print(os.sep)       # Windows: \    Mac/Linux: /

# 获取行终止符
print(os.linesep)   # Windows: \r\n    Mac/Linux: \n

# 获取环境变量分隔符
print(os.pathsep)   # Windows: ;    Mac/Linux: :

# 查看所有环境变量
print(os.environ)

# 查看操作系统标识
print(os.name)      # Windows: nt    Mac/Linux: posix
```

---

## 十三、时间模块

### 13.1 time 模块

时间的三种表示形式：
1. **时间戳**：从 1970 年 1 月 1 日午夜开始经过的秒数
2. **格式化时间字符串**：人类可读的日期格式
3. **时间元组（struct_time）**：结构化的时间数据

```python
import time

# 【1】获取当前时间戳
time_stamp = time.time()
print(time_stamp)  # 1722560884.2367811

# 【2】时间戳 -> 时间元组（国际时间 UTC）
time_tuple_utc = time.gmtime(time_stamp)
print(time_tuple_utc)
# time.struct_time(tm_year=2024, tm_mon=8, tm_mday=2, ...)

# 【3】时间戳 -> 时间元组（本地时间）
time_tuple_local = time.localtime(time_stamp)
print(time_tuple_local)

# 【4】时间元组 -> 格式化字符串
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(time_str)  # 2024-08-02 09:16:44

# 【5】格式化字符串 -> 时间元组
time_struct = time.strptime("2024-08-02 09:16:44", "%Y-%m-%d %H:%M:%S")

# 【6】时间元组 -> 时间戳
print(time.mktime(time.localtime()))  # 1722563512.0

# 【7】标准时间格式输出
print(time.asctime(time.localtime()))  # Fri Aug  2 09:53:47 2024
print(time.ctime(time.time()))         # Fri Aug  2 09:54:30 2024
```

**常用格式化符号：**

| 符号 | 含义 | 范围 |
|------|------|------|
| %Y | 年份 | 完整年份 |
| %m | 月份 | 01-12 |
| %d | 日 | 01-31 |
| %H | 小时（24小时制） | 00-23 |
| %M | 分钟 | 00-59 |
| %S | 秒 | 00-61 |
| %I | 小时（12小时制） | 01-12 |
| %p | AM/PM | - |
| %a | 简化星期名 | - |
| %A | 完整星期名 | - |
| %b | 简化月份名 | - |
| %B | 完整月份名 | - |

**三种时间格式的转换关系：**

```
时间戳 <--> 时间元组 <--> 格式化字符串
  |  gmtime/localtime    |  strftime
  |  mktime              |  strptime
```

### 13.2 datetime 模块

`datetime` 模块提供了更直观的日期时间操作方式：

```python
import datetime

# 【1】自定义日期
print(datetime.date(2020, 10, 1))  # 2020-10-01

# 【2】获取当前日期/时间
date_obj = datetime.date.today()
print(date_obj)  # 2024-08-02

datetime_obj = datetime.datetime.today()
print(datetime_obj)  # 2024-08-02 10:05:33.584242

# 【3】获取日期时间的各个属性
print(datetime_obj.year)      # 2024
print(datetime_obj.month)     # 8
print(datetime_obj.day)       # 2
print(datetime_obj.hour)      # 10
print(datetime_obj.minute)    # 5
print(datetime_obj.second)    # 56

# 【4】日期时间运算 —— timedelta
# 参数：days, seconds, microseconds, milliseconds, minutes, hours, weeks
t_day = datetime.timedelta(days=7)
date_old = datetime.datetime.today()
date_new = date_old + t_day   # 7天后的时间
date_before = date_old - t_day  # 7天前的时间

print(date_new - date_old)    # 7 days, 0:00:00
```

---

## 十四、随机模块

`random` 模块用于生成随机数和随机操作：

```python
import random

# 【1】生成 0 到 1 之间的随机小数
print(random.random())

# 【2】生成指定区间内的随机小数
print(random.uniform(5, 6))   # 5 到 6 之间

# 【3】生成指定区间内的随机整数（包含两端）
print(random.randint(1, 10))  # 1 到 10 随机

# 【4】生成指定区间内指定步长的随机整数
print(random.randrange(1, 10, 2))  # 1 到 9 的奇数随机

# 【5】随机返回列表中的一个元素
name_list = ["张三", "李四", "王五"]
print(random.choice(name_list))

# 【6】随机返回列表中的多个元素
print(random.sample(name_list, 2))  # 随机返回 2 个不重复元素

# 【7】随机打乱列表（影响原列表）
random.shuffle(name_list)
print(name_list)

# 【8】应用场景 —— 生成随机验证码
def get_code(n):
    """生成 n 位包含大写字母、小写字母和数字的随机验证码"""
    code = ""
    for i in range(n):
        num_big = chr(random.choice(range(65, 91)))      # 随机大写字母 A-Z
        num_small = chr(random.choice(range(97, 123)))   # 随机小写字母 a-z
        num_int = random.choice([str(i) for i in range(10)])  # 随机数字 0-9
        code += random.choice([num_big, num_small, num_int])
    return code

print(get_code(6))  # 例如：A3bK9p
```

---

## 十五、摘要算法模块

### 15.1 什么是摘要算法

摘要算法（又称哈希算法、散列算法）通过一个函数将任意长度的数据转换为一个**固定长度**的字符串（通常是 32 位十六进制字符串）。目的就是验证数据传输前后的**数据完整性**。

**注意：**摘要算法是**单向加密**，只能加密不能反向解密。这不是加密算法。

### 15.2 hashlib 模块

```python
import hashlib

# 【1】基本加密流程
def encrypted(data):
    # 步骤一：生成 md5 对象
    md5 = hashlib.md5()
    # 步骤二：将原始数据转为二进制
    data = data.encode()
    # 步骤三：对原始数据进行摘要加密
    md5.update(data)
    # 步骤四：获取加密后的十六进制字符串
    result = md5.hexdigest()  # 32 位十六进制字符串
    return result

print(encrypted("123456"))  # e10adc3949ba59abbe56e057f20f883e

# 【2】加盐 —— 提高数据安全性
def encrypted_with_salt(data, salt):
    """加盐加密：在原始数据后添加随机字符串再加密"""
    md5 = hashlib.md5()
    original_data = (data + str(salt)).encode()
    md5.update(original_data)
    return md5.hexdigest()

print(encrypted_with_salt("123456", salt=6666))
```

**关于撞库**：

网页上能够"解密" MD5 是因为有人预先计算了大量常见字符串的 MD5 值并存入数据库。用户输入密文后去数据库查表，找到了就返回原文。这种方式称为**撞库**。加盐可以有效防止撞库。

### 15.3 摘要算法的应用场景

1. **数据签名**：将一段信息生成密文，用于验证证书真伪。
2. **验证数据完整性**：传输文件时附带密文，接收方重新计算并比对，如果一致则说明数据未被篡改。

---

## 十六、日志模块

`logging` 模块用于记录程序运行过程中的重要信息、错误等。相比 `print`，`logging` 可以控制输出级别、输出位置、输出格式等。

### 16.1 快速使用

```python
import logging

# 配置日志基本设置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建日志记录器
logger = logging.getLogger(__name__)

# 不同级别的日志
logger.debug("调试信息，最详细的日志")   # DEBUG 级别
logger.info("普通信息，记录运行状态")    # INFO 级别
logger.warning("警告信息，可能有潜在问题") # WARNING 级别
logger.error("错误信息，程序出错")       # ERROR 级别
logger.critical("严重错误，可能导致崩溃") # CRITICAL 级别
```

### 16.2 日志级别

日志级别从低到高依次为：

```
DEBUG < INFO < WARNING < ERROR < CRITICAL
```

设置日志级别后，低于该级别的日志会被忽略。

### 16.3 日志配置字典（生产环境推荐）

```python
import logging
import logging.config
import os

# 日志配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join('logs', 'app.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

def get_logger(name=''):
    """获取日志记录器"""
    logging.config.dictConfig(LOGGING_DIC)
    logger = logging.getLogger(name)
    return logger

# 使用示例
if __name__ == '__main__':
    logger = get_logger(name="user")
    logger.info("这是一条信息日志")
    logger.error("这是一条错误日志")
```

---

## 十七、subprocess 模块

`subprocess` 模块能够启动一个新的进程，执行系统命令并获取输入、输出和错误信息。

### 17.1 Popen

```python
import subprocess

# 在 macOS/Linux 上执行命令
response = subprocess.Popen(
    "ls",              # 要执行的命令
    shell=True,        # 使用 shell 模式
    stdout=subprocess.PIPE,  # 正确的输出管道
    stderr=subprocess.PIPE,  # 错误的输出管道
)

# 从管道中读取结果（读取后管道清空）
# macOS/Linux 默认编码为 utf-8，Windows 默认编码为 gbk
stdout_result = response.stdout.read().decode('utf-8')
stderr_result = response.stderr.read().decode('utf-8')

print(stdout_result)
print(stderr_result)
```

### 17.2 run

```python
def run_command(command_list):
    """执行命令并返回结果"""
    response = subprocess.run(
        command_list,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"   # 自动解码，不需要 .decode()
    )
    if response.returncode == 0:  # 返回码为 0 表示成功
        return response.stdout
    else:
        return response.stderr

result = run_command(["ls", "/some/path"])
print(result)
```

### 17.3 call

```python
# 直接在控制台输出结果，并返回状态码
return_code = subprocess.call(["python", "--version"])

# 安装第三方包
subprocess.call(["pip", "install", "coloredlogs"])
```

---

## 十八、re 正则表达式模块

### 18.1 正则表达式简介

正则表达式（Regular Expression）是一种文本模式，包括普通字符和特殊字符（元字符）。它用于在文本中按指定规则进行匹配和提取内容。

### 18.2 字符组

字符组用 `[]` 表示，匹配字符组中的任意一个字符：

```python
import re

# 匹配单个数字
print(re.findall("[0123456789]", "a1b2c3"))  # ['1', '2', '3']

# 范围简写
print(re.findall("[0-9]", "a1b2c3"))        # ['1', '2', '3']
print(re.findall("[a-z]", "AbCdEf"))        # ['b', 'd', 'f']
print(re.findall("[A-Z]", "AbCdEf"))        # ['A', 'C', 'E']

# 多种范围组合
print(re.findall("[0-9a-zA-Z]", "a1B2c3#"))  # ['a', '1', 'B', '2', 'c', '3']
```

### 18.3 元字符

| 元字符 | 含义 |
|--------|------|
| `.` | 匹配除换行符以外的任意一个字符 |
| `\w` | 匹配字母、数字、下划线 |
| `\W` | 匹配非字母、非数字、非下划线 |
| `\s` | 匹配任意空白符（空格、制表符、换行符） |
| `\S` | 匹配非空白符 |
| `\d` | 匹配数字 |
| `\D` | 匹配非数字 |
| `\n` | 匹配换行符 |
| `\t` | 匹配制表符 |
| `^` | 匹配字符串的开始 |
| `$` | 匹配字符串的结尾 |
| `a|b` | 匹配 a 或 b |
| `()` | 匹配括号中的表达式，也表示一个组 |
| `[...]` | 匹配字符组中的字符 |
| `[^...]` | 匹配不在字符组中的字符 |

```python
data = "hello 123 _world"

print(re.findall("\w", data))   # 字母数字下划线
# ['h', 'e', 'l', 'l', 'o', '1', '2', '3', '_', 'w', 'o', 'r', 'l', 'd']

print(re.findall("\d", data))   # 数字
# ['1', '2', '3']

print(re.findall("\s", data))   # 空白符
# [' ', ' ']

print(re.findall(r"^\w", data)) # 以字母数字下划线开头
# ['h']

print(re.findall(r"\w$", data)) # 以字母数字下划线结尾
# ['d']
```

### 18.4 量词

量词控制前面字符的重复次数，默认是**贪婪匹配**（尽可能多地匹配）：

| 量词 | 含义 |
|------|------|
| `*` | 重复零次或更多次 |
| `+` | 重复一次或更多次 |
| `?` | 重复零次或一次 |
| `{n}` | 重复恰好 n 次 |
| `{n,}` | 重复 n 次或更多次 |
| `{n,m}` | 重复 n 到 m 次 |

```python
# *  零次或更多次
print(re.findall(r"01([0-9]*)3", "012222223"))  # ['222222']

# +  一次或更多次
print(re.findall(r"01([0-9]+)3", "0123"))       # ['2']

# ?  零次或一次
print(re.findall(r"01([0-9]?)3", "0123"))       # ['2']

# {n}  恰好 n 次
print(re.findall(r"01([0-9]{3})3", "012223"))   # ['222']

# {n,}  至少 n 次
print(re.findall(r"01([0-9]{3,})3", "012222223")) # ['222222']

# {n,m}  n 到 m 次
print(re.findall(r"01([0-9]{3,6})3", "012222223")) # ['222222']
```

### 18.5 贪婪匹配与取消

量词默认是贪婪匹配，在量词后面加 `?` 可以取消贪婪匹配：

```python
data = "李杰和李莲英和李二棍子和李"

# 贪婪匹配 —— 尽可能多拿
print(re.findall("李.*", data))
# ['李杰和李莲英和李二棍子和李']

# 取消贪婪 —— 尽可能少拿
print(re.findall("李.*?", data))
# ['李', '李', '李', '李']  （但因为 findall 的机制，实际每个独立匹配）
```

### 18.6 模式修正符

```python
# re.I  忽略大小写
print(re.findall("[a-z]", "abcdABCD"))           # ['a', 'b', 'c', 'd']
print(re.findall("[a-z]", "abcdABCD", re.I))     # ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']

# re.S  让 . 匹配换行符
# re.M  多行匹配，影响 ^ 和 $
# re.U  根据 Unicode 字符集解析字符
# re.X  让正则表达式更具可读性
```

### 18.7 re 模块常用方法

```python
import re

data = "李杰和李莲英和李二棍子和李"

# 【1】findall —— 查找所有匹配，返回列表
print(re.findall("李.+?", data))
# ['李杰', '李莲', '李二']

# 【2】search —— 查找第一个匹配，返回 Match 对象（没有则返回 None）
result = re.search("李.+?", data)
print(result.group())  # 李杰

# 【3】match —— 从开头匹配，返回 Match 对象（没有则返回 None）
result = re.match("李.+?", data)
print(result.group())  # 李杰

result = re.match("赵.+?", data)
print(result)  # None，因为开头不是"赵"

# 【4】split —— 用正则表达式切割字符串
print(re.split("和", data))
# ['李杰', '李莲英', '李二棍子', '李']

# 【5】sub —— 替换匹配的内容，返回替换后的字符串
print(re.sub("和", "|", data))
# 李杰|李莲英|李二棍子|李

print(re.sub("和", "|", data, count=1))  # 只替换一次
# 李杰|李莲英和李二棍子和李

# 【6】subn —— 替换并返回 (替换结果, 替换次数)
print(re.subn("和", "|", data))
# ('李杰|李莲英|李二棍子|李', 3)

# 【7】compile —— 编译正则表达式（多次使用时可提高效率）
pattern = re.compile("和")
result = re.subn(pattern, "|", data)

# 【8】finditer —— 返回迭代器，内存更友好
result_iter = re.finditer("李.+?", data)
for match in result_iter:
    print(match.group())
```

### 18.8 正则表达式分组优先级

```python
# 普通 split：分隔符消失
print(re.split("\d+", "dream1dream2dream3dream"))
# ['dream', 'dream', 'dream', 'dream', '']

# 用 () 分组 split：分隔符保留
print(re.split("(\d+)", "dream1dream2dream3dream"))
# ['dream', '1', 'dream', '2', 'dream', '3', 'dream', '']
```

### 18.9 常用正则表达式

```python
# 手机号码
pattern_phone = r"^(?:+86)?1[3-9]\d{9}$"

# 邮箱
pattern_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"

# 身份证号
pattern_id = r"^\d{17}[\dXx]$"

# URL
pattern_url = r"^https?://[^\s]+$"

# 用户名（字母开头，5-16位）
pattern_username = r"^[a-zA-Z][a-zA-Z0-9_]{4,15}$"
```

### 18.10 手机号验证示例

```python
import re

# 传统方式
def check_phone(phone):
    if not phone.isdigit():
        return "手机号必须是数字!"
    if len(phone) != 11:
        return "手机号必须是11位!"
    if phone[:2] not in ["13", "15", "17", "18"]:
        return "手机号开头不正确!"
    return f"手机号 {phone} 格式正确"

# 正则方式
def check_phone_re(phone):
    pattern = r"^1[3456789]\d{9}$"
    if not re.match(pattern, phone):
        return "手机号格式不正确!"
    return f"手机号 {phone} 格式正确"

phone = input("请输入手机号: ").strip()
print(check_phone_re(phone))
```

---

## 十九、常用内置函数

### 19.1 数据类型转换（8个）

| 函数 | 作用 |
|------|------|
| `str()` | 转换为字符串 |
| `int()` | 转换为整数 |
| `float()` | 转换为浮点数 |
| `list()` | 转换为列表 |
| `tuple()` | 转换为元组 |
| `set()` | 转换为集合 |
| `dict()` | 转换为字典 |
| `bool()` | 转换为布尔值 |

### 19.2 进制转换（3个）

```python
print(bin(10))    # 十进制转二进制：'0b1010'
print(oct(10))    # 十进制转八进制：'0o12'
print(hex(10))    # 十进制转十六进制：'0xa'
```

### 19.3 数学运算（8个）

```python
# abs() —— 绝对值
print(abs(-5))  # 5

# divmod() —— 返回 (商, 余数)
print(divmod(7, 3))  # (2, 1)

# round() —— 四舍五入
print(round(4.51))     # 5
print(round(4.051, 1)) # 4.1  (保留一位小数)

# pow() —— 幂运算
print(pow(2, 3))       # 8     (2^3)
print(pow(2, 3, 5))    # 3     (2^3 % 5)

# sum() —— 求和
print(sum([1, 2, 3, 4, 5]))  # 15

# min() —— 最小值
print(min([3, 1, 4, 1, 5]))  # 1

# max() —— 最大值
print(max([3, 1, 4, 1, 5]))  # 5

# complex() —— 复数
print(complex(2, 3))  # (2+3j)
```

### 19.4 数据结构相关（9个）

```python
# reversed() —— 反转序列
print(list(reversed([1, 2, 3])))  # [3, 2, 1]

# slice() —— 切片对象
num_list = [1, 2, 3, 4, 5, 6]
print(num_list[0:3])               # [1, 2, 3]
print(num_list[slice(0, 3)])       # [1, 2, 3]

# len() —— 计算长度
print(len([1, 2, 3]))  # 3

# sorted() —— 排序（返回新列表，不改变原列表）
print(sorted([3, 1, 2]))                        # [1, 2, 3]
print(sorted([3, 1, 2], reverse=True))          # [3, 2, 1]

# sorted() 结合 key 参数按自定义规则排序
names = ['Adam', 'Barta', 'Bob', 'Lisaaaa']
print(sorted(names, key=len))  # ['Bob', 'Adam', 'Barta', 'Lisaaaa']

# enumerate() —— 枚举（返回索引和值的元组）
name_list = ['Adam', 'Barta', 'Bob', 'Lisaaaa']
for index, name in enumerate(name_list, start=1):
    print(f"第{index}个: {name}")

# format() —— 格式化输出
print(format("hello", "^20"))  # 居中对齐，宽度 20
print(format("hello", "<20"))  # 左对齐
print(format("hello", ">20"))  # 右对齐
print(format(999, "b"))  # 二进制：'1111100111'
print(format(999, "x"))  # 十六进制小写：'3e7'

# bytes() —— 字符串转二进制
data = "今天你吃饱了吗"
print(data.encode())                     # b'...'
print(bytes(data, encoding="utf-8"))     # b'...'

# bytearray() —— 字符串转字节数组
print(bytearray(data, encoding="utf-8"))

# repr() —— 返回对象的原始字符串表示
sentence = "my name is \n dream"
print(repr(sentence))  # 'my name is \n dream'
```

### 19.5 字符编码（3个）

```python
# ord() —— 字符 -> ASCII 码数字
print(ord('A'))  # 65
print(ord('Z'))  # 90

# chr() —— ASCII 码数字 -> 字符
print(chr(65))      # A
print(chr(97))      # a

# ascii() —— 获取字符的 ASCII 表示
print(ascii("A"))   # 'A'
print(ascii("@"))   # '@'
```

### 19.6 调用判断与属性查看（4个）

```python
# callable() —— 判断对象是否可调用（加括号执行）
def index():
    pass

class Student:
    pass

print(callable(index))    # True
print(callable(Student))  # True
print(callable(100))      # False

# dir() —— 查看对象的所有属性和方法
import os
print(dir(os))

# id() —— 查看对象的内存地址
print(id("hello"))

# type() —— 查看对象的类型
print(type("hello"))  # <class 'str'>
```

### 19.7 高阶函数（3个）

#### zip —— 拉链函数

将多个可迭代对象中对应位置的元素打包成元组：

```python
name_list = ["dream", "hope", "opp"]
age_list = [18, 19, 20]
gender_list = ["male", "female", "male"]
addr_list = ["上海", "北京", "广东", "深圳"]

# zip 返回一个迭代器，元素个数以最短的序列为准
result = zip(name_list, age_list, gender_list, addr_list)
print(list(result))
# [('dream', 18, 'male', '上海'),
#  ('hope', 19, 'female', '北京'),
#  ('opp', 20, 'male', '广东')]   （"深圳"被丢弃）
```

#### filter —— 过滤函数

根据条件过滤可迭代对象中的元素：

```python
num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# filter 接收一个函数和一个可迭代对象，保留函数返回 True 的元素
result = filter(lambda x: x % 2 == 1, num_list)
print(list(result))  # [1, 3, 5, 7, 9]

# 等价列表推导式
print([i for i in num_list if i % 2 == 1])
```

#### map —— 映射函数

对可迭代对象中的每个元素执行指定函数：

```python
num_list = [1, 2, 3, 4, 5]

def pow_self(x):
    return x ** x

result = map(pow_self, num_list)
print(list(result))
# [1, 4, 27, 256, 3125]

# 使用 lambda 简化
result = map(lambda x: x ** 2, num_list)
print(list(result))  # [1, 4, 9, 16, 25]
```

### 19.8 lambda 匿名函数

匿名函数是没有名字的函数，语法简洁，常用于高阶函数中作为参数：

```python
# 语法：lambda 形参名: 返回值

# 普通函数
def add(x, y):
    return x + y

# 等价匿名函数
add_lambda = lambda x, y: x + y

print(add(1, 2))       # 3
print(add_lambda(1, 2))  # 3

# 常见用法：作为 sorted、filter、map 的 key/参数
names = ['Bob', 'Lisaaaa', 'Adam']
print(sorted(names, key=lambda x: len(x)))  # ['Bob', 'Adam', 'Lisaaaa']

nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4, 6]
```

### 19.9 逻辑判断（2个）

```python
# all() —— 所有元素为 True 才返回 True
print(all([1, 2, 3]))         # True
print(all([1, 0, 3]))         # False（0 为假值）

# any() —— 任一元素为 True 就返回 True
print(any([0, '', False]))    # False
print(any([0, '', 1]))        # True
```

### 19.10 作用域与迭代器相关（5个）

```python
# globals() —— 查看全局名称空间
print(globals())

# locals() —— 查看局部名称空间
def func():
    name = "local"
    print(locals())  # {'name': 'local'}
func()

# range() —— 生成可迭代的 range 对象
print(list(range(0, 5)))  # [0, 1, 2, 3, 4]

# iter() —— 获取迭代器对象
num_iter = iter([1, 2, 3])

# next() —— 从迭代器取下一个值
print(next(num_iter))  # 1
print(next(num_iter))  # 2
```

### 19.11 输入输出（2个）

```python
# input() —— 从标准输入读取用户输入
name = input("请输入你的名字: ")

# print() —— 输出到标准输出
print("Hello World!", end="\n", sep=" ")
```

### 19.12 执行字符串代码（3个）

```python
# eval() —— 执行简单表达式，有返回值
result = eval("1 + 2 + 3")
print(result)  # 6

# exec() —— 执行代码块，无返回值
code = """
for i in range(3):
    print(i)
"""
exec(code)  # 输出 0, 1, 2

# compile() —— 编译代码，交给 eval/exec 执行
code_obj = compile("print('hello')", "", "exec")
exec(code_obj)  # 输出 hello
```

### 19.13 面向对象相关函数（11个）

```python
# isinstance() —— 判断对象是否是指定类型
print(isinstance("hello", str))   # True
print(isinstance(123, int))       # True

# issubclass() —— 判断类是否是另一个类的子类
# issubclass(ChildClass, ParentClass)

# classmethod —— 类方法装饰器
# staticmethod —— 静态方法装饰器
# property —— 属性装饰器
# super() —— 调用父类方法
# object() —— 所有类的基类

# getattr() —— 获取对象属性
# setattr() —— 设置对象属性
# delattr() —— 删除对象属性
# hasattr() —— 判断对象是否有指定属性
```

### 19.14 其他常用函数

```python
# hash() —— 获取哈希值（只能哈希不可变数据类型）
print(hash("dream"))          # 可哈希
# print(hash([1, 2]))         # TypeError: 列表不可哈希

# open() —— 打开文件
fp = open("文件路径", mode='r', encoding="utf-8")

# __import__() —— 动态导入模块
os_module = __import__("os")
print(os_module.name)

# breakpoint() —— 调用调试器（Python 3.7+）
# breakpoint()

# frozenset() —— 不可变集合
frozen = frozenset({1, 2, 3})
# frozen.add(4)  # 报错！不可变

# vars() —— 查看对象的属性字典
print(vars())
```

---

> 本文档涵盖了 Python 函数、装饰器、迭代器、生成器、模块与包、常用内置模块（json、os、time、random、hashlib、logging、subprocess、re）以及常用内置函数的全部核心知识点，适合作为 Python 函数与模块专题的学习参考。
