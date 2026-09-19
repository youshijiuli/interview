# Python 基础语法

---

## 一、计算机基础与 Python 环境搭建

### 1.1 计算机的五大组成部分

计算机由以下五大部件组成：

| 部件 | 功能 | 类比 |
|------|------|------|
| 控制器 | 控制整个硬件系统的协调运行 | 大脑的指挥中枢 |
| 运算器 | 执行算术运算和逻辑运算 | 大脑的计算能力 |
| 存储器 | 存储程序和数据 | 记忆系统 |
| 输入设备 | 向计算机输入数据（键盘、鼠标等） | 感官 |
| 输出设备 | 计算机向用户展示结果（显示器、音箱等） | 表达能力 |

**三大核心硬件：**

| 硬件 | 功能 |
|------|------|
| CPU | 控制器 + 运算器，计算机的大脑，执行程序指令 |
| 硬盘 | 永久存储数据（包括操作系统、应用程序、用户数据），断电不丢失 |
| 内存 | 临时存储正在运行的程序和数据，断电后数据立即丢失，读写速度快 |

**程序的执行流程：**

1. 双击应用图标，将应用数据从硬盘读取到内存
2. CPU 从内存中读取程序数据
3. CPU 发送指令给硬件执行
4. 硬件执行完毕后，结果返回内存
5. 显示器将结果展示给用户
6. 程序结束，数据从内存写回硬盘

**存储单位换算：**

```python
# 存储单位
1B  = 8bit           # 1个字节 = 8个比特位，1个英文字母约占1字节
1KB = 1024B          # 相当于一则短篇故事
1MB = 1024KB         # 相当于一则短篇小说
1GB = 1024MB         # 相当于贝多芬第五乐章交响曲的乐谱内容
1TB = 1024GB         # 相当于一家大型医院中所有的X光图片
1PB = 1024TB         # 相当于50%的全美学术研究图书馆藏书
1EB = 1024PB         # 5EB相当于至今全世界人类所讲过的话语
1ZB = 1024EB         # 如同全世界海滩上的沙子数量总和
1YB = 1024ZB         # 相当于7000位人类体内的微细胞总和
```

### 1.2 操作系统与计算机三层架构

**三层架构：**

- **硬件层**：底层硬件设备
- **操作系统层**：在硬件层之上统筹管理所有硬件资源
- **应用层**：在操作系统之上安装的应用程序

操作系统的出现是为了简化硬件操作，提供统一的接口供应用程序使用。开发者无需重复编写控制硬件的底层代码，只需调用操作系统提供的接口即可。

**常见操作系统：**

- 客户端（PC）：Windows、macOS、Linux
- 移动端（App）：Android、iOS、鸿蒙

**平台：** 硬件 + 操作系统 构成平台。如果某个应用可以在多个平台上使用，就称为"跨平台"。Python 具有极强的跨平台性，一次编写，处处运行。

### 1.3 编程与编程语言

**什么是编程语言：** 人与计算机之间沟通交流的媒介。

**什么是编程：** 将人类能识别的语言翻译成计算机能识别的语言的过程。

**编程语言按照发展阶段的分类：**

#### 1.3.1 机器语言

直接用 0 和 1 组成的二进制指令操作底层硬件。

```python
# 机器语言示例
# 0000 代表 LOAD（加载）
# 0001 代表 STORE（存储）

# 优点：执行效率高，直接操作底层硬件
# 缺点：开发效率低，学习成本高，跨平台性差
```

#### 1.3.2 汇编语言

用英文字母和特殊字符代替机器指令，比机器语言更可读。

```assembly
; 汇编语言示例（Hello World）
section .data
    msg db "Hello, world!", 0xA
    len equ $ - msg
section .text
    global _start
_start:
    mov edx, len
    mov ecx, msg
    mov ebx, 1
    mov eax, 4
    int 0x80
    mov ebx, 0
    mov eax, 1
    int 0x80

# 优点：执行效率高，可执行文件小
# 缺点：开发效率低，跨平台性差，学习成本高
```

#### 1.3.3 高级语言

从人的角度出发，以人类可读的字符编写程序，与操作系统打交道而非直接操作硬件。

**高级语言按照翻译方式分为两种：**

| 类型 | 说明 | 代表语言 |
|------|------|----------|
| 编译型语言 | 将源程序一次性翻译成目标代码再执行，修改后需重新编译 | C、C++、Java、Go |
| 解释型语言 | 边编译边执行，修改后无需重新编译 | Python、PHP、JavaScript |

```python
# 编译型语言特点：
#   优点：执行效率高
#   缺点：开发效率低，跨平台性差

# 解释型语言特点：
#   优点：开发效率高，跨平台性强
#   缺点：执行效率相对较低

# 执行效率：机器语言 > 汇编语言 > 编译型语言 > 解释型语言
# 开发效率：解释型语言 > 编译型语言 > 汇编语言 > 机器语言
# 跨平台性：解释型语言 > 编译型语言 > 汇编语言 > 机器语言
```

### 1.4 Python 介绍

#### 1.4.1 Python 简介

- Python 的创始人是吉多·范罗苏姆（Guido van Rossum）
- 1989 年圣诞节期间开始编写 Python 解释器
- 1991 年发布第一个公开发行版
- 名字来源于 Guido 喜爱的电视剧《Monty Python's Flying Circus》
- 设计理念：简洁、易学易用、可扩展性强

#### 1.4.2 Python 发展史

| 年份 | 事件 |
|------|------|
| 1989 | Guido 开始编写 Python 编译器 |
| 1991 | 第一个 Python 编译器诞生（用 C 语言实现） |
| 1994 | Python 1.0 发布，加入 lambda、map、filter、reduce |
| 2000 | Python 2.0 发布，加入垃圾回收机制 |
| 2008 | Python 3.0 发布（不完全向下兼容 2.x） |
| 2010 | Python 2.7 发布（2.x 最终版本） |
| 2016 | Python 3.6 发布 |
| 2020 | Python 2 正式结束支持 |
| 2023 | Python 3.12 发布 |

> 目前推荐使用 Python 3.10+ 版本，本教程基于 Python 3.10。

#### 1.4.3 Python 的应用领域

- 数据分析
- 人工智能
- 爬虫（数据采集）
- 云计算
- Web 开发
- 图像处理（人脸识别等）
- 自动化运维

#### 1.4.4 Python 解释器的种类

| 解释器 | 说明 |
|--------|------|
| CPython | 官方版本，C 语言编写，**使用最广泛，我们使用的就是这个** |
| Jython | Java 语言编写，可编译为 Java 字节码 |
| IPython | 基于 CPython 的增强交互式解释器 |
| PyPy | Python 语言实现的解释器，有 JIT 编译器，速度快 |
| IronPython | 运行在 .Net 平台上的 Python 解释器 |

### 1.5 Python 解释器安装

#### 1.5.1 下载

1. 打开 Python 官网：https://www.python.org/
2. 点击 Downloads，选择 Windows
3. 搜索需要的版本（如 3.10.11），下载 64-bit 安装包

#### 1.5.2 安装

1. 双击安装包，勾选 "Add Python to PATH"
2. 选择 "Customize installation"（自定义安装）
3. 全部勾选可选项
4. 选择安装路径（建议非 C 盘）
5. 等待安装完成

#### 1.5.3 多版本共存方案

当系统中安装了多个版本的 Python 解释器时：

```bash
# 方案：进入 Python 安装目录，复制 python.exe 并重命名（加上版本号）
# 例如：python.exe -> python310.exe
# 使用时指定版本：
python310 my_script.py
```

若要修改默认 Python 版本，在系统环境变量中将目标版本的路径移到最前面即可。

### 1.6 PyCharm 安装与使用

PyCharm 是 JetBrains 公司出品的专业 Python IDE，内置了丰富的开发工具。

#### 1.6.1 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + / | 行注释/取消行注释 |
| Ctrl + Alt + L | 代码格式化 |
| Ctrl + D | 复制当前行或选定区域 |
| Ctrl + X | 剪切当前行 |
| Ctrl + Y | 删除当前行 |
| Ctrl + B | 跳转到声明 |
| Ctrl + Alt + S | 打开设置对话框 |
| Ctrl + Shift + F10 | 运行 |
| Shift + F9 | 调试 |
| Shift + Enter | 另起一行 |
| Tab / Shift + Tab | 缩进/取消缩进 |
| Alt + Enter | 快速修正 |

### 1.7 PIP 换源

使用 pip 安装第三方包时，默认从国外源下载速度较慢，可以通过换源加速。

#### 1.7.1 永久换源

```bash
# 设置为清华大学镜像源（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 查看当前镜像源
pip config get global.index-url
```

#### 1.7.2 常用国内镜像源

```python
# 清华大学：       https://pypi.tuna.tsinghua.edu.cn/simple/
# 阿里云：         https://mirrors.aliyun.com/pypi/simple/
# 豆瓣：           https://pypi.douban.com/simple/
# 中国科学技术大学： https://pypi.mirrors.ustc.edu.cn/simple/
```

#### 1.7.3 临时换源

```bash
# 仅本次安装使用指定源
pip install 模块名 -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 1.8 虚拟环境

#### 1.8.1 概念

- **系统环境**：安装在计算机全局范围内的 Python 环境，对所有项目可见
- **虚拟环境**：为每个项目创建独立的 Python 运行环境，隔离不同项目的依赖

为什么需要虚拟环境？不同项目可能需要不同版本的同一库（如项目 A 用 Django 3.2，项目 B 用 Django 5.0），虚拟环境可以避免版本冲突。

#### 1.8.2 创建虚拟环境（venv）

```bash
# Python 3.3+ 自带的虚拟环境工具
python -m venv 虚拟环境名称

# 激活虚拟环境（Windows）
虚拟环境名称\Scripts\activate.bat

# 退出虚拟环境
deactivate
```

#### 1.8.3 创建虚拟环境（virtualenv）

```bash
# 安装 virtualenv
pip install virtualenv

# 创建虚拟环境
virtualenv 虚拟环境名称

# 创建指定 Python 版本的虚拟环境
virtualenv -p python310 虚拟环境名称

# Windows 增强工具（可选）
pip install virtualenvwrapper-win
```

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

## 四、基本数据类型

### 4.1 数据类型概述

Python 中有 8 种基本数据类型：

| 数据类型 | 关键字 | 说明 | 是否可变 |
|----------|--------|------|----------|
| 整数类型 | int | 表示整数 | 不可变 |
| 浮点数类型 | float | 表示小数 | 不可变 |
| 字符串类型 | str | 表示文本 | 不可变 |
| 列表类型 | list | 有序可重复的集合 | **可变** |
| 元组类型 | tuple | 有序不可变的集合 | 不可变 |
| 字典类型 | dict | 键值对集合 | **可变** |
| 集合类型 | set | 无序不重复的集合 | **可变** |
| 布尔类型 | bool | 真或假 | 不可变 |

### 4.2 数字类型

#### 4.2.1 整数类型（int）

```python
# 整数类型用于表示整数，是 Python 中最基本的数字类型
age = 18
print(age, type(age))  # 18 <class 'int'>

# 整数可以执行算术运算
print(1 + 1)   # 2
print(10 - 3)  # 7
print(2 * 3)   # 6
print(10 / 2)  # 5.0（注意：除法结果总是浮点数）
```

#### 4.2.2 浮点数类型（float）

```python
# 浮点类型用于表示带有小数部分的数值
salary = 100.23
print(salary, type(salary))  # 100.23 <class 'float'>

# 浮点数也可以进行算术运算
print(1.5 + 2.3)  # 3.8

# 注意：浮点数运算可能存在精度问题
print(3.11 + 1)   # 4.109999999999999（而非 4.11）
# 这是由于计算机底层二进制表示浮点数的限制导致的
```

### 4.3 字符串类型（str）

#### 4.3.1 字符串的定义

```python
# 字符串用于表示文本信息
name = "dream"
print(name, type(name))  # dream <class 'str'>

# 字符串有四种定义方式：
name_1 = "dream"       # 双引号
name_2 = 'dream'       # 单引号
name_3 = '''dream'''   # 三个单引号（支持换行）
name_4 = """dream"""   # 三个双引号（支持换行）

# 三个引号包裹的字符串可以跨行
poem = '''
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。
'''
print(poem)
```

#### 4.3.2 引号嵌套

```python
# 引号嵌套规则：外层使用一种引号，内层使用另一种引号
sentence = 'my name is "dream"'         # 正确：单引号内嵌双引号
sentence = "my name is 'dream'"         # 正确：双引号内嵌单引号

# 以下写法错误：同种引号混淆
# sentence = 'my name is 'dream''       # 错误！
```

#### 4.3.3 字符串的基本操作

```python
# 1. 字符串拼接（+）
print("hello " + "world")  # hello world

# 2. 字符串重复（*）
print("d" * 5)             # ddddd

# 3. 索引取值
# 正向索引：从 0 开始，从左向右
# 负向索引：从 -1 开始，从右向左
print('dream'[0])   # d
print('dream'[1])   # r
print('dream'[-1])  # m
print('dream'[-2])  # a

# 注意：字符串支持索引取值，但不支持索引修改值
# name = "dream"
# name[0] = "s"  # 错误！字符串是不可变类型
```

#### 4.3.4 字符串格式化输出

```python
# 方案一：% 占位符格式化
# %s：字符串占位符
# %d：整数占位符
# %f：浮点数占位符
# %x：十六进制整数占位符
name = "dream"
age = 18
print("my name is %s, my age is %d" % (name, age))
# my name is dream, my age is 18

# 方案二：str.format() 方法
# 按位置传参
print("my name is {}, my age is {}".format("dream", 18))
# 按关键字传参（推荐，更清晰）
print("my name is {name}, my age is {age}".format(name="dream", age=18))

# 方案三：f-string（Python 3.6+，推荐使用）
name = "dream"
age = 18
print(f"my name is {name}, my age is {age}")
# my name is dream, my age is 18

# f-string 支持表达式
a = 10
b = 20
print(f"{a} + {b} = {a + b}")  # 10 + 20 = 30
```

### 4.4 列表类型（list）

#### 4.4.1 列表的定义

```python
# 列表用于存储多个值，用方括号 [] 包裹，元素之间用逗号分隔
user_names = ["dream", "hope", "opp"]
print(user_names, type(user_names))  # ['dream', 'hope', 'opp'] <class 'list'>
```

#### 4.4.2 列表索引取值

```python
user_names = ["dream", "hope", "opp"]

# 正向索引（从0开始）
print(user_names[0])   # dream
print(user_names[1])   # hope

# 负向索引（从-1开始）
print(user_names[-1])  # opp
print(user_names[-3])  # dream

# 列表支持索引修改值（因为列表是可变的）
user_names[0] = "new_dream"
print(user_names)  # ['new_dream', 'hope', 'opp']
```

#### 4.4.3 列表嵌套

```python
# 列表可以多层嵌套
data_info = ["dream", "hope", "opp", [18, 19, 20, ["music", "run", "swim"]]]

# 访问嵌套列表中的元素
print(data_info[0])                  # dream
print(data_info[3])                  # [18, 19, 20, ['music', 'run', 'swim']]
print(data_info[3][0])               # 18
print(data_info[3][3])               # ['music', 'run', 'swim']
print(data_info[3][3][0])            # music

# 复杂嵌套的格式化输出
print(f"my name is {data_info[0]}, my age is {data_info[3][0]}, my hobby is {data_info[3][3][0]}")
# my name is dream, my age is 18, my hobby is music
```

### 4.5 字典类型（dict）

#### 4.5.1 字典的定义

```python
# 字典以键值对（key:value）形式存储数据
# 多个键值对之间用逗号分隔，整体用大括号 {} 包裹
# 字典的 key 通常使用不可变类型（字符串、数字）

person_info = {
    "name": "dream",
    "age": 18,
    "gender": "male"
}

# 字典的特点：
# - key 对 value 有描述性，能明确表示值的含义
# - 字典通过 key 访问，而非索引
# - Python 3.7+ 字典保持插入顺序
```

#### 4.5.2 字典的取值

```python
person_info = {
    "name": "dream",
    "age": 18,
    "gender": "male"
}

# 方式一：字典[key] 取值
print(person_info["name"])  # dream

# 如果 key 不存在会报错
# print(person_info["hobby"])  # KeyError: 'hobby'

# 方式二：字典.get(key) 取值（推荐）
print(person_info.get("name"))   # dream
print(person_info.get("hobby"))  # None（不存在时返回 None 而非报错）

# get() 可以指定默认值
print(person_info.get("hobby", "music"))  # music
```

#### 4.5.3 字典与列表的嵌套

```python
info = {
    'name': 'Dream',
    'addr': {
        '国家': '中国',
        'info': [666, 999, {'编号': 466722, 'hobby': ['read', 'study', 'music']}]
    }
}

print(f"""
    my name is {info.get('name')}
    my 国家 is {info.get('addr').get('国家')}
    my 编号 is {info.get('addr').get('info')[2].get('编号')}
    my hobby is {', '.join(info.get('addr').get('info')[2].get('hobby'))}
""")
```

### 4.6 元组类型（tuple）

```python
# 元组是一种不可变的序列类型，用圆括号 () 包裹
# 与列表的主要区别：元组的元素不能被修改、删除或添加

num_tuple = (1, 2, 3)
print(num_tuple, type(num_tuple))  # (1, 2, 3) <class 'tuple'>

# 支持索引取值，但不能索引修改
print(num_tuple[0])   # 1
# num_tuple[0] = 999  # 错误！TypeError: 'tuple' object does not support item assignment

# 重要：定义只有一个元素的元组时必须加逗号
single_tuple = (1,)        # 这是一个元组
not_tuple = (1)            # 这是整数 1，而非元组
print(type(single_tuple))  # <class 'tuple'>
print(type(not_tuple))     # <class 'int'>

# 字符串后面不要随便加逗号，否则会变成元组
name = "dream",
print(name, type(name))  # ('dream',) <class 'tuple'>

# 元组解包
name_age = ("dream", 18)
name, age = name_age
print(name)  # dream
print(age)   # 18
```

### 4.7 布尔类型（bool）

```python
# 布尔类型只有两个值：True 和 False
# 用于逻辑判断、条件控制等场景

is_active = True
is_deleted = False

# Python 中判断为 False 的情况（假值）：
print(bool(False))  # False  # 布尔值 False
print(bool(0))      # False  # 数字 0
print(bool(""))     # False  # 空字符串
print(bool([]))     # False  # 空列表
print(bool({}))     # False  # 空字典
print(bool(()))     # False  # 空元组
print(bool(set()))  # False  # 空集合
print(bool(None))   # False  # None 值

# 其他情况均为 True（真值）：
print(bool(True))   # True   # 布尔值 True
print(bool(1))      # True   # 非零数字
print(bool(-1))     # True   # 负数也是真
print(bool(" "))    # True   # 有内容的字符串（空格也算）
print(bool([1]))    # True   # 非空列表
```

> 口诀：**除了 0、空（空字符串/空列表/空字典/空元组/空集合）、False、None，其他都是 True。**

### 4.8 集合类型（set）

```python
# 集合是一种无序且不重复的数据类型，用大括号 {} 包裹
# 集合会自动去重

num_set = {1, 2, 3, 1, 1, 1, 1, 11, 1}
print(num_set, type(num_set))  # {1, 2, 3, 11} <class 'set'>
# 注意：重复的 1 被自动去除了

# 集合中元素是无序的（数字类型通常不会打乱，但字符串会）
dream_set = {"d", "r", "e", "a", "m"}
print(dream_set)  # 顺序可能与定义时不同

# 注意：集合中不能存放可变类型（列表、字典）
# set_list = {[1, 2]}   # 错误！TypeError: unhashable type: 'list'
# set_dict = {{"a": 1}} # 错误！TypeError: unhashable type: 'dict'

# 集合的添加和删除
name_set = {"dream", "opp"}
name_set.add("oppp")        # 添加元素
name_set.remove("opp")      # 删除指定元素
print(name_set)             # {'dream', 'oppp'}

# 集合运算：并集、交集、差集
set_a = {1, 2, 3, 4, 5, 6}
set_b = {4, 5, 6, 7, 8, 9}

print(set_a.union(set_b))        # 并集 {1, 2, 3, 4, 5, 6, 7, 8, 9}
print(set_a.intersection(set_b)) # 交集 {4, 5, 6}
print(set_a.difference(set_b))   # 差集 {1, 2, 3}
```

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

## 六、运算符

### 6.1 算术运算符

```python
a = 10
b = 3

print(a + b)   # 13   # 加法
print(a - b)   # 7    # 减法
print(a * b)   # 30   # 乘法
print(a / b)   # 3.3333333333333335  # 除法（结果总是浮点数）
print(a % b)   # 1    # 取余（求模）
print(a ** b)  # 1000 # 幂运算（10的3次方）
print(a // b)  # 3    # 整除（取商，向下取整）
```

### 6.2 比较运算符

```python
a = 10
b = 3

print(a > b)   # True   # 大于
print(a >= b)  # True   # 大于等于
print(a < b)   # False  # 小于
print(a <= b)  # False  # 小于等于
print(a == b)  # False  # 等于
print(a != b)  # True   # 不等于
```

### 6.3 赋值运算符

```python
a = 10
b = 3

# 基本赋值
a += b   # 等价于 a = a + b
print(a)  # 13

a -= b   # 等价于 a = a - b
print(a)  # 10

a *= b   # 等价于 a = a * b
print(a)  # 30

a /= b   # 等价于 a = a / b
print(a)  # 10.0

a %= b   # 等价于 a = a % b，结果 1.0
print(a)

a //= b  # 等价于 a = a // b，结果 0.0
print(a)

a **= b  # 等价于 a = a ** b
```

#### 6.3.1 链式赋值

```python
# 将同一个值同时赋给多个变量
a = b = c = d = 99
print(a, b, c, d)  # 99 99 99 99
```

#### 6.3.2 交叉赋值

```python
# 交换两个变量的值，无需借助中间变量
a = 10
b = 20

a, b = b, a

print(a)  # 20
print(b)  # 10
```

#### 6.3.3 解压赋值

```python
# 将可迭代类型中的元素按位置分别赋值给变量
num_list = [1, 2, 3]
a, b, c = num_list

print(a)  # 1
print(b)  # 2
print(c)  # 3

# 注意：变量数量必须与元素数量一致
# a, b = num_list       # 错误！变量太少
# a, b, c, d = num_list # 错误！变量太多

# 使用下划线 _ 来存储不需要的变量值（约定俗成）
a, b, _ = num_list
print(a, b)  # 1 2
```

### 6.4 逻辑运算符

```python
a = 10
b = -10

# and（与）：两边都为 True 才返回 True
print(a > 0 and b < 0)   # True
print(a > 0 and b > 0)   # False

# or（或）：任意一边为 True 就返回 True
print(a > 0 or b < 0)    # True
print(a > 0 or b > 0)    # True

# not（非）：取反
print(not a < 0)         # True（a<0 是 False，取反后是 True）

# 连续多个逻辑运算
print(10 > 0 and 5 > 0 and 3 < 0)   # False（一假全假）
print(10 > 0 and 5 > 0 or 3 < 0)    # True
print(10 > 0 or 5 > 0 or 3 < 0)     # True（一真全真）

# 运算优先级：not > and > or
# 可以用括号 () 提高优先级
print(3 > 4 and 4 > 3 or 1 == 3 and 'x' == 'x' or 3 > 3)
# 等价于 ((3>4 and 4>3) or (1==3 and 'x'=='x') or (3>3))
#         (False    or    False          or   False) = False

print(3 > 4 and (4 > 3 or 1 == 3) and ('x' == 'x' or 3 > 3))
# 等价于 (False and True and True) = False
```

### 6.5 成员运算符

```python
# in / not in：判断某个成员是否在集合中
num_list = [1, 2, 3]

print(1 in num_list)       # True
print(6 in num_list)       # False
print(6 not in num_list)   # True

# 成员运算符也可用于字符串
print("d" in "dream")      # True
print("x" not in "dream")  # True
```

### 6.6 身份运算符

```python
# is / is not：判断两个变量是否引用同一个对象（比较内存地址）
a = 1
b = "1"

print(a == b)        # False  # == 比较值是否相等
print(a is b)        # False  # is 比较内存地址是否相等
print(a is not b)    # True

# == 和 is 的区别
name = "dream"
name_one = "dream"

print(name == name_one)   # True  # 值相等
print(name is name_one)   # True  # 内存地址也相同（字符串驻留机制）
print(id(name))           # 查看内存地址
print(id(name_one))       # 查看内存地址（通常相同）
```

> **总结：`==` 比较的是值是否相等，`is` 比较的是内存地址是否相等。**

## 七、流程控制语句

### 7.1 流程控制的三种结构

```python
# 顺序结构：按照代码编写的顺序从上到下依次执行
# 分支结构：根据条件判断执行不同的代码
# 循环结构：重复执行某段代码
```

### 7.2 顺序结构

```python
# 程序默认按照顺序依次执行，一句接一句执行
print("step 1")
print("step 2")
print("step 3")
```

### 7.3 分支结构（if/elif/else）

#### 7.3.1 单分支结构

```python
# 如果条件成立，就执行条件内的代码
score = 89

if score >= 90:
    print("优秀")

# 注意：Python 使用缩进（通常4个空格）来表示代码块
```

#### 7.3.2 双分支结构

```python
# 条件成立执行 if 内的代码，否则执行 else 内的代码
score = 60

if score >= 90:
    print("优秀")
else:
    print("还需努力")
```

#### 7.3.3 多分支结构

```python
# 依次判断每个条件，遇到第一个满足的就执行对应代码，不再向后判断
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 70:
    print("中等")
elif score >= 60:
    print("及格")
else:
    print("不及格")
# 输出：良好
```

#### 7.3.4 分支嵌套

```python
age = 20

if age >= 18:
    if age == 20:
        print("你现在正值最好的年纪")
    print("你已成年，可以为自己的行为负责")
elif age >= 12:
    print("青少年时期")
else:
    print("童年时期")
```

### 7.4 三元运算（三目运算符）

三元运算是对简单 if...else... 判断的简化写法。

```python
a, b = 10, 20

# 传统的 if...else...
if a > b:
    print(a)
else:
    print(b)

# 三元表达式写法
# 语法：为真的结果 if 条件 else 为假的结果
print(a if a > b else b)  # 20

# 更多技巧
# 利用元组索引：布尔值 True=1, False=0
print((b, a)[a < b])          # 10

# 利用字典键
print({True: a, False: b}[a < b])  # 20

# 三元表达式只适用于简单的逻辑判断，复杂的逻辑应使用 if...else...
```

### 7.5 循环结构

#### 7.5.1 while 循环

```python
# while 循环：当条件为真时重复执行代码块
# 语法：
# while 条件:
#     循环体

count = 0
while count < 5:
    print(count)
    count += 1
# 输出：0 1 2 3 4
```

#### 7.5.2 for 循环

```python
# for 循环：遍历可迭代对象中的每个元素
# 语法：
# for 变量 in 可迭代对象:
#     循环体

# 遍历字符串
for char in "dream":
    print(char)

# 遍历列表
for num in [1, 2, 3, 4, 5]:
    print(num)

# 遍历字典（默认遍历键）
data = {"name": "dream", "age": 18}
for key in data:
    print(key)        # name age
    print(data[key])  # dream 18
```

#### 7.5.3 range 关键字

```python
# range() 用于生成一个整数序列
# range(起始, 结束, 步长) —— 左闭右开（包含起始，不包含结束）

print(list(range(1, 5)))     # [1, 2, 3, 4]
print(list(range(0, 10, 2))) # [0, 2, 4, 6, 8]—— 步长为 2
print(list(range(5)))        # [0, 1, 2, 3, 4]—— 起始默认为 0

# 在 Python 2.x 中 range() 直接返回列表
# 在 Python 3.x 中 range() 返回一个可迭代对象，需要时再生成，节省内存

# range 配合 for 循环控制执行次数
for i in range(3):
    print(f"第 {i+1} 次执行")
```

#### 7.5.4 continue 关键字

```python
# continue：跳出本次循环，继续下一次循环
count = 0

while count < 5:
    count += 1
    if count == 3:
        print(f"跳过 count={count}")
        continue  # 不执行下面的 print
    print(count)

# 输出：
# 1
# 2
# 跳过 count=3
# 4
# 5
```

#### 7.5.5 break 关键字

```python
# break：立即终止整个循环
count = 0

while count < 10:
    count += 1
    if count == 5:
        print(f"count 等于 5，循环终止")
        break
    print(count)

# 输出：
# 1
# 2
# 3
# 4
# count 等于 5，循环终止
```

#### 7.5.6 标志位

```python
# 使用标志位灵活控制循环的退出
count = 0
tag = True  # 标志位

while tag:
    count += 1
    if count == 3:
        print(f"跳过 count={count}")
        continue
    elif count == 4:
        print(f"count 等于 4，结束循环")
        tag = False  # 修改标志位来终止循环
    else:
        print(count)

# 输出：
# 1
# 2
# 跳过 count=3
# count 等于 4，结束循环
```

#### 7.5.7 while...else 与 for...else

```python
# 当循环正常结束（未被 break 中断）时，会执行 else 块
count = 0

while count < 3:
    count += 1
    print(count)
else:
    print("循环正常结束")

# 输出：
# 1
# 2
# 3
# 循环正常结束
```

```python
# 如果循环被 break 中断，else 块不会执行
count = 0

while count < 5:
    count += 1
    if count == 3:
        break
    print(count)
else:
    print("循环正常结束")  # 不会执行
```

#### 7.5.8 死循环与避免

```python
# 死循环：循环条件始终为 True，永不终止
# 应避免编写死循环，除非有明确的退出机制

# 不当的死循环（不要这样做）
# while True:
#     print(1)  # 永远执行，无法停止

# 正确的无限循环：搭配 break 使用
while True:
    user_input = input("输入 q 退出：")
    if user_input == "q":
        print("程序退出")
        break
```

### 7.6 循环遍历字典的全部方式

```python
data = {"name": "dream", "age": 18, "gender": "male"}

# 遍历键
for key in data.keys():
    print(key)

# 遍历值
for value in data.values():
    print(value)

# 遍历键值对
for key, value in data.items():
    print(f"{key} = {value}")
```

## 八、数据类型内置方法详解

### 8.1 整数和浮点数的内置方法

#### 8.1.1 强制类型转换

```python
# int()：将符合整数格式的字符串转换为整数
num_str = "55"
num_str_int = int(num_str)
print(num_str_int, type(num_str_int))  # 55 <class 'int'>

# float()：将符合浮点数格式的字符串转换为浮点数
print(float("1.11"))          # 1.11
print(float("3.14"))          # 3.14

# 注意：无法转换的字符串会抛出异常
# int("abc")      # ValueError
# float("hello")  # ValueError
```

#### 8.1.2 进制转换

```python
# 十进制转其他进制
print(bin(999))  # 0b1111100111   # 二进制（以 0b 开头）
print(oct(999))  # 0o1747         # 八进制（以 0o 开头）
print(hex(999))  # 0x3e7          # 十六进制（以 0x 开头）

# 其他进制转十进制（使用 int() 并指定基）
print(int("0b1111100111", 2))  # 999  # 二进制 -> 十进制
print(int("0o1747", 8))        # 999  # 八进制 -> 十进制
print(int("0x3e7", 16))        # 999  # 十六进制 -> 十进制
```

#### 8.1.3 判断字符串是否为数字

```python
# isdigit()：判断字符串是否全部是数字字符
print("123".isdigit())       # True
print("4".isdigit())         # True
print("3.14".isdigit())     # False（包含小数点）
print("abc".isdigit())       # False

# isdecimal()：判断字符串是否只包含十进制数字
print("123".isdecimal())     # True
print("四".isdecimal())      # False
print("Ⅳ".isdecimal())      # False

# 注意：Python 没有内置方法判断字符串是否为浮点数格式
```

#### 8.1.4 输入校验示例

```python
# 利用 isdigit() 对用户输入进行校验
age = input("请输入年龄：")
if age.isdigit():
    age = int(age)
    print(f"你的年龄是 {age}")
else:
    print(f"输入 '{age}' 不是合法的数字")
```

### 8.2 字符串的内置方法

#### 8.2.1 必须掌握的方法

```python
# 1. 字符串拼接
# 方式一：+ 号拼接
print("hello" + " " + "world")

# 方式二：join() 方法（推荐用于大量拼接）
print("".join(["1", "2", "3"]))        # "123"
print("|".join(["1", "2", "3"]))       # "1|2|3"
print("-".join("dream"))               # "d-r-e-a-m"

# 2. 切片（Slice）
# 语法：字符串[起始索引:结束索引:步长]
# 注意：左闭右开，包含起始索引，不包含结束索引
word = "dream"
#  d  r  e  a  m
#  0  1  2  3  4
# -5 -4 -3 -2 -1

print(word[1:3])       # "re"（索引1到2，不含3）
print(word[1:4:2])     # "ra"（步长为2）
print(word[::-1])      # "maerd"（字符串反转）
print(word[-3:-1])     # "ea"

# 3. 计算长度
print(len("dream"))    # 5

# 4. 成员运算
print("d" in "dream")  # True

# 5. 去除特殊字符 strip()
# strip() 默认去除首尾的空格和换行符
print("  dream  ".strip())           # "dream"
print("$dream$".strip("$"))          # "dream"
print("$dream$".lstrip("$"))         # "dream$"（只去左边）
print("$dream$".rstrip("$"))         # "$dream"（只去右边）

# 6. 切分字符串 split()
# 按照指定分隔符切割字符串，返回列表
names = "dream|opp|hope"
print(names.split("|"))             # ['dream', 'opp', 'hope']

# 切分后直接解包
user_pwd = "username:password"
username, password = user_pwd.split(":")
print(f"用户名：{username}，密码：{password}")

# 7. 字符串重复
print("hello" * 3)  # "hellohellohello"

# 8. 大小写转换
name = "UserName"
print(name.upper())  # "USERNAME"（全大写）
print(name.lower())  # "username"（全小写）

# 9. 首尾字符判断
print("dream".startswith("d"))  # True  # 是否以指定前缀开头
print("dream".endswith("m"))    # True  # 是否以指定后缀结尾
print("dream".endswith("x"))    # False

# 10. 替换字符 replace()
name = "dream"
print(name.replace("d", "a"))   # "aream"（将 d 替换为 a）
# 注意：replace() 不会修改原字符串（字符串是不可变的），而是返回新字符串

# 11. 判断是否是纯数字
print("123".isdigit())  # True
print("abc".isdigit())  # False
```

#### 8.2.2 查找方法

```python
# find()：从左向右查找，返回索引位置，找不到返回 -1
print("draeam".find("a"))    # 2
print("draeam".find("x"))    # -1

# rfind()：从右向左查找
print("draeam".rfind("a"))   # 4

# index()：从左向右查找，找不到会报错
print("draeam".index("a"))   # 2
# print("draeam".index("x")) # ValueError: substring not found

# rindex()：从右向左查找，找不到也会报错
print("draeam".rindex("a"))  # 4

# count()：统计字符在字符串中出现的次数
print("draeam".count("a"))   # 2
```

#### 8.2.3 填充和对齐

```python
name = "dream"

# center()：居中填充
# center(总宽度, 填充字符)
print(name.center(len(name) + 2, "*"))   # "*dream*"
print(name.center(len(name) + 3, "*"))   # "**dream*"（奇数时右侧优先）

# ljust()：左对齐（右侧填充）
print(name.ljust(len(name) + 3, "-"))    # "dream---"

# rjust()：右对齐（左侧填充）
print(name.rjust(len(name) + 3, "-"))    # "---dream"

# zfill()：用 0 填充至指定长度（从左侧填充）
print(name.zfill(len(name) + 3))         # "000dream"
```

#### 8.2.4 大小写扩展方法

```python
# capitalize()：首字母大写（只对第一个单词生效）
sentence = "my name is dream."
print(sentence.capitalize())   # "My name is dream."

# title()：每个单词的首字母大写
print(sentence.title())        # "My Name Is Dream."

# swapcase()：大小写翻转
name = "UserName"
print(name.swapcase())         # "uSERnAME"
```

### 8.3 列表的内置方法

#### 8.3.1 强制类型转换

```python
# 可以将可迭代类型转换为列表
print(list("dream"))                          # ['d', 'r', 'e', 'a', 'm']
print(list((1, 2, 3)))                        # [1, 2, 3]
print(list({1, 2, 3}))                        # [1, 2, 3]
print(list({"name": "dream", "age": 18}))     # ['name', 'age']（只取键）
```

#### 8.3.2 添加元素

```python
num_list = [1, 2, 3]

# append()：在列表末尾追加元素
num_list.append(4)
print(num_list)  # [1, 2, 3, 4]

# insert()：在指定索引位置插入元素
num_list.insert(0, 999)
print(num_list)  # [999, 1, 2, 3, 4]

# extend()：扩展列表，将另一个可迭代对象的元素逐个追加到末尾
num_list_two = [5, 6, 7]
num_list.extend(num_list_two)
print(num_list)  # [999, 1, 2, 3, 4, 5, 6, 7]
```

#### 8.3.3 删除元素

```python
num_list = [1, 2, 3, 4, 5, 6]

# remove()：按值删除，删除第一个匹配的元素
num_list.remove(4)
print(num_list)  # [1, 2, 3, 5, 6]
# 注意：如果元素不存在会报错

# pop()：按索引弹出元素（返回被删除的元素）
print(num_list.pop())     # 6（默认弹出最后一个）
print(num_list)           # [1, 2, 3, 5]
print(num_list.pop(0))    # 1（弹出指定索引位置的元素）
print(num_list)           # [2, 3, 5]

# del：按索引删除（Python 内置语句，没有返回值）
del num_list[0]
print(num_list)  # [3, 5]

# clear()：清空列表
num_list.clear()
print(num_list)  # []
```

#### 8.3.4 排序与反转

```python
num_list = [1, 4, 2, 8, 6, 3, 9]

# reverse()：反转列表元素的顺序（修改原列表）
num_list.reverse()
print(num_list)  # [9, 3, 6, 8, 2, 4, 1]

# sort()：排序（修改原列表）
num_list.sort()
print(num_list)  # [1, 2, 3, 4, 6, 8, 9]

# sort(reverse=True)：降序排序
num_list.sort(reverse=True)
print(num_list)  # [9, 8, 6, 4, 3, 2, 1]

# sorted()：返回排序后的新列表（不修改原列表）
original = [3, 1, 4, 1, 5, 9]
new_sorted = sorted(original)
print(original)   # [3, 1, 4, 1, 5, 9]（原列表不变）
print(new_sorted) # [1, 1, 3, 4, 5, 9]（新列表已排序）
```

> **总结：`sort()` 修改原列表，无返回值；`sorted()` 返回新列表，不修改原列表。**

### 8.4 元组的内置方法

```python
# 元组是不可变类型，方法较少
# 主要用于数据保护，不允许修改元素

# 强制类型转换
print(tuple("dream"))                         # ('d', 'r', 'e', 'a', 'm')
print(tuple([1, 2, 3]))                       # (1, 2, 3)
print(tuple({"name": "dream", "age": 18}))    # ('name', 'age')（只取键）

# 索引取值（支持但不支持修改）
num_tuple = (1, 2, 3, 4, 5)
print(num_tuple[0])   # 1
print(num_tuple[-1])  # 5
# num_tuple[0] = 999  # 错误！元组不支持元素修改

# 切片
print(num_tuple[1:3])   # (2, 3)
print(num_tuple[::-1])  # (5, 4, 3, 2, 1)（反转）

# 计算长度
print(len(num_tuple))  # 5

# 成员运算
print(3 in num_tuple)  # True

# 元组拼接（返回新元组，不修改原元组）
t1 = (1, 2, 3)
t2 = (4, 5, 6)
print(t1 + t2)  # (1, 2, 3, 4, 5, 6)

# 元组重复
print(t1 * 3)  # (1, 2, 3, 1, 2, 3, 1, 2, 3)
```

### 8.5 字典的内置方法

#### 8.5.1 取值

```python
data_dict = {
    "name": "dream",
    "age": 18,
    "gender": "male"
}

# 方式一：字典[key]（键不存在则报错）
print(data_dict["name"])        # dream

# 方式二：字典.get(key)（键不存在返回 None）
print(data_dict.get("name"))    # dream
print(data_dict.get("hobby"))   # None
print(data_dict.get("hobby", "music"))  # music（可设置默认值）
```

#### 8.5.2 增加与修改

```python
data_dict = {
    "name": "dream",
    "age": 18
}

# 字典[key] = value —— 有则修改，无则新增
data_dict["name"] = "hope"     # 修改已有键的值
data_dict["gender"] = "male"   # 新增键值对
print(data_dict)  # {'name': 'hope', 'age': 18, 'gender': 'male'}

# update(字典) —— 批量添加/更新
data_dict.update({"phone": "123456", "age": 20})
print(data_dict)  # {'name': 'hope', 'age': 20, 'gender': 'male', 'phone': '123456'}

# setdefault(key, default) —— 如果键不存在则设置默认值
data_dict.setdefault("hobby", "music")
print(data_dict)  # {'name': 'hope', 'age': 20, 'gender': 'male', 'phone': '123456', 'hobby': 'music'}
# 如果键已存在，setdefault 不会修改其值
data_dict.setdefault("hobby", "sports")  # hobby 仍然是 "music"
```

#### 8.5.3 删除

```python
data_dict = {
    "phone": "123456",
    "addr": "中国上海",
    "id": "001"
}

# del 字典[key]：删除指定键值对
del data_dict["phone"]
print(data_dict)  # {'addr': '中国上海', 'id': '001'}

# pop(key)：弹出指定键值对（返回被删除的值）
res = data_dict.pop("addr")
print(res)        # 中国上海
print(data_dict)  # {'id': '001'}

# popitem()：弹出最后一个键值对（Python 3.7+ 保证有序）
print(data_dict.popitem())  # ('id', '001')

# clear()：清空字典
data_dict.clear()
print(data_dict)  # {}
```

#### 8.5.4 获取键、值、键值对

```python
data_dict = {
    "name": "dream",
    "age": 18,
    "gender": "male"
}

# keys()：获取所有键
print(data_dict.keys())     # dict_keys(['name', 'age', 'gender'])
print(list(data_dict.keys()))  # ['name', 'age', 'gender']

# values()：获取所有值
print(data_dict.values())   # dict_values(['dream', 18, 'male'])

# items()：获取所有键值对
print(data_dict.items())    # dict_items([('name', 'dream'), ('age', 18), ('gender', 'male')])

# 遍历键值对
for key, value in data_dict.items():
    print(f"{key} = {value}")
```

#### 8.5.5 其他方法

```python
data_dict = {"name": "dream", "age": 18}

# len()：计算字典中键值对的数量
print(len(data_dict))  # 2

# 成员运算：判断键是否存在
print("name" in data_dict)   # True
print("dream" in data_dict)  # False（成员运算针对键，不是值）
```

### 8.6 集合的内置方法

```python
# 集合的特点：无序、不重复

# 强制类型转换
print(set("dream"))                           # {'d', 'r', 'e', 'a', 'm'}
print(set([1, 2, 3, 1, 2]))                  # {1, 2, 3}（自动去重）

# 添加元素
num_set = {1, 2, 3, 4, 5}
num_set.add(6)               # 添加单个元素
print(num_set)                # {1, 2, 3, 4, 5, 6}

num_set.update([7, 8, 9])    # 添加多个元素
print(num_set)                # {1, 2, 3, 4, 5, 6, 7, 8, 9}

# 删除元素
num_set.remove(9)             # 删除指定元素，元素不存在则报错
num_set.discard(10)           # 删除指定元素，元素不存在不报错

print(num_set.pop())          # 弹出第一个元素
num_set.clear()               # 清空集合

# 常用公共方法
s = {1, 2, 3}
print(len(s))      # 3          # 计算长度
print(2 in s)      # True       # 成员运算
for item in s:                   # 遍历循环
    print(item)
```

## 九、可变类型与不可变类型

### 9.1 两组容易混淆的概念：数据结构 vs 内存区域

初学者经常把"堆/栈"四个字混作一谈，实际上它们在两个完全不同的语境下出现：

**(1) 数据结构层面：栈（Stack）与队列（Queue）**

| 结构 | 特点 | 操作 |
|------|------|------|
| 栈（Stack） | 后进先出 LIFO（Last In First Out） | 入栈 push、出栈 pop |
| 队列（Queue） | 先进先出 FIFO（First In First Out） | 入队 enqueue、出队 dequeue |

Python 中可以用 `list` 模拟这两种结构：

```python
# 用 list 模拟栈（LIFO）
stack_demo = [1, 2, 3]
stack_demo.append(4)        # 入栈 -> [1, 2, 3, 4]
top = stack_demo.pop()      # 出栈，弹出最后一个 -> 4

# 用 list 模拟队列（FIFO）；注意 pop(0) 性能较差，工程上推荐 collections.deque
queue_demo = [1, 2, 3]
queue_demo.append(4)        # 入队 -> [1, 2, 3, 4]
head = queue_demo.pop(0)    # 出队，弹出第一个 -> 1
```

**(2) 内存层面：堆（Heap）与栈（Stack）**

这是另一组完全不同的概念，指的是**程序运行时内存的两种分区**：

- **栈区（Stack）**：存放局部变量、函数调用帧（栈帧），由解释器/编译器自动分配释放，遵循 LIFO（函数先调用后返回）。
- **堆区（Heap）**：存放对象本身（如 `list`、`dict`、字符串、实例等），生命周期由 GC 管理，与"先进先出"无关。

> ⚠️ 注意：内存中"栈"的 LIFO 指的是**栈帧的入栈/出栈顺序**（函数调用关系），而不是变量的"先用后弃"。
>
> 内存堆/栈区的更多细节将在 §10.2 中展开。

### 9.2 可变类型与不可变类型的区分

核心区分依据：**当值被修改时，内存地址是否变化。**

- **不可变类型**：修改值后内存地址改变
- **可变类型**：修改值后内存地址不变

```python
# 不可变类型：整型
num = 1
print(id(num))  # 例如：140722345678912
num = 2
print(id(num))  # 地址改变了

# 不可变类型：字符串
name = "dream"
print(id(name))
name = "hope"
print(id(name))  # 地址改变了

# 不可变类型：浮点数
num = 1.0
print(id(num))
num = 2.0
print(id(num))  # 地址改变了

# 不可变类型：布尔
flag = True
print(id(flag))
flag = False
print(id(flag))  # 地址改变了

# 不可变类型：元组
t = (1, 2, 3)
print(id(t))
t = t + (4, 5)
print(id(t))  # 地址改变了

# ====== 可变类型 ======

# 可变类型：列表
name = [1, 2, 3]
print(id(name))  # 例如：4311500864
name.append(8)
print(id(name))  # 4311500864（地址不变！）

# 可变类型：字典
data = {"name": "dream"}
print(id(data))  # 例如：4311500864
data["age"] = 18
print(id(data))  # 4311500864（地址不变！）

# 可变类型：集合
s = {"name", "dream"}
print(id(s))
s.add("18")
print(id(s))  # 地址不变！
```

### 9.3 Python 的参数传递方式

```python
# Python 的参数传递既不是纯粹的值传递也不是纯粹的引用传递
# 规则：
#   传递不可变类型时，在函数中修改不会影响原来的变量（类似值传递）
#   传递可变类型时，在函数中修改会影响原来的变量（类似引用传递）

def test_func(num, lst):
    num = 100        # 不可变类型，不影响外部变量
    lst.append(4)    # 可变类型，影响外部变量

a = 1
my_list = [1, 2, 3]
test_func(a, my_list)
print(a)         # 1（未改变）
print(my_list)   # [1, 2, 3, 4]（已改变）
```

> **总结：不可变类型有 int、float、str、bool、tuple；可变类型有 list、dict、set。**

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

## 十二、字符编码

### 12.1 什么是字符编码

字符编码是将人类可读的字符与计算机可识别的二进制数据之间建立起一一对应的映射关系。

- **编码（encode）**：将字符转换为二进制数据
- **解码（decode）**：将二进制数据转换为字符

### 12.2 字符编码发展史

#### 12.2.1 阶段一：ASCII（一家独大）

计算机起源于美国，最初只需要表示英文字符。ASCII 码表使用 1 个字节（8 位）表示一个字符，共能表示 256 个字符。

```python
# ASCII 常用字符对照
# A - Z ：65 - 90
# a - z ：97 - 122
# 0 - 9 ：48 - 57

# 使用 ord() 查看字符的 ASCII 码
print(ord('A'))   # 65
print(ord('a'))   # 97
print(ord('0'))   # 48

# 使用 chr() 将 ASCII 码转换为字符
print(chr(65))    # 'A'
print(chr(97))    # 'a'
```

#### 12.2.2 阶段二：各国有各自的编码（诸侯割据）

随着计算机普及，各国都希望用自己的语言编码：

| 地区 | 编码 |
|------|------|
| 美国 | ASCII |
| 中国 | GBK（国标扩展） |
| 日本 | Shift_JIS |
| 韩国 | EUC-KR |

各国有各自的编码表，导致跨国交流时出现乱码。

#### 12.2.3 阶段三：Unicode（一统天下）

Unicode（万国码）包含了所有语言的字符与数字的映射关系，解决了乱码问题。

#### 12.2.4 UTF-8（最常用的编码格式）

UTF-8 是 Unicode 的一种实现方式，使用变长字节编码：

- 英文字符：1 个字节
- 中文字符：3 个字节（大部分）

### 12.3 编码与解码操作

```python
# 编码（encode）：字符串 -> 二进制数据（bytes）
name = "中国"
age = "d梦"

print(name.encode())                        # b'\xe4\xb8\xad\xe5\x9b\xbd'
print(age.encode())                         # b'd\xe6\xa2\xa6'
print(age.encode(encoding="gbk"))           # b'd\xc3\xce'
print(age.encode(encoding="shift_jis"))     # b'd\x9a\xeb'

# 解码（decode）：二进制数据 -> 字符串
name_b = b'\xe4\xb8\xad\xe5\x9b\xbd'
name_b_gbk = b'd\xc3\xce'

print(name_b.decode())                      # 中国（默认 utf-8）
print(name_b_gbk.decode(encoding="gbk"))    # d梦（用 gbk 解码）

# 注意：编码和解码必须使用相同的字符集，否则出现乱码
```

```python
# Python 文件头声明编码（Python 2.x 时代需要，3.x 默认 UTF-8）
# -*- coding: UTF-8 -*-
```

## 十三、文件操作

### 13.1 打开文件的两种方式

```python
# 方式一：open() + close()（需手动关闭文件）
fp = open("test.txt", "w", encoding="utf-8")
fp.write("hello world")
fp.close()  # 必须手动关闭，否则可能导致数据丢失或资源泄漏

# 方式二：with 语句（推荐！自动管理文件资源）
with open("test.txt", "w", encoding="utf-8") as fp:
    fp.write("hello world")
# 离开 with 代码块时，文件自动关闭，无需手动 close
```

### 13.2 文件操作的三种基本模式

```python
# 【1】r 模式（read）：只读模式
# - 只能读取，不能写入
# - 文件不存在会报错 FileNotFoundError
with open("test.txt", "r", encoding="utf-8") as fp:
    data = fp.read()
    print(data)

# 【2】w 模式（write）：只写模式
# - 只能写入，不能读取
# - 文件不存在则自动创建
# - 每次打开都会清空文件内容（覆盖写）
with open("test.txt", "w", encoding="utf-8") as fp:
    fp.write("你好，世界")

# 【3】a 模式（append）：追加模式
# - 只能在文件末尾追加内容
# - 文件不存在则自动创建
# - 不会清空原有内容
with open("test.txt", "a", encoding="utf-8") as fp:
    fp.write("追加的内容\n")
```

### 13.3 扩展模式

```python
# 【1】+ 模式：扩展权限
# r+：既能读又能写
# w+：既能写又能读（会清空文件）
# a+：既能追加又能读

# r+ 模式示例
with open("test.txt", "r+", encoding="utf-8") as fp:
    data = fp.read()       # 先读取
    fp.write("新内容")     # 再写入

# 【2】b 模式：操作二进制数据
# rb：读取二进制文件（如图片、音频、视频）
# wb：写入二进制文件
# ab：追加二进制数据

# 读取图片二进制数据
with open("photo.jpg", "rb") as fp:
    data = fp.read()

# 写入图片二进制数据
with open("photo_copy.jpg", "wb") as fp:
    fp.write(data)
```

### 13.4 文件读取方法

```python
# 假设 test.txt 内容如下：
# 第一行内容
# 第二行内容
# 第三行内容

with open("test.txt", "r", encoding="utf-8") as fp:
    # read()：一次性读取全部内容
    content = fp.read()

    # read(数字)：读取指定字符数（不是行数）
    # fp.read(5)：读取前 5 个字符

    # readline()：读取一行
    line = fp.readline()
    print(line)  # 第一行内容

    # readlines()：读取所有行，返回列表
    lines = fp.readlines()
    print(lines)  # ['第一行内容\n', '第二行内容\n', '第三行内容\n']

    # 逐行遍历（推荐，内存友好）
    for line in fp:
        print(line.strip())

    # readable()：判断文件是否可读
    print(fp.readable())  # True
```

### 13.5 文件写入方法

```python
with open("output.txt", "w", encoding="utf-8") as fp:
    # write()：写入字符串
    fp.write("hello world\n")

    # writelines()：写入列表（不会自动加换行符）
    lines = ["第一行\n", "第二行\n", "第三行\n"]
    fp.writelines(lines)

    # writable()：判断文件是否可写
    print(fp.writable())  # True

    # 在同一个 with 块中连续 write 可以持续写入
    fp.write("追加1\n")
    fp.write("追加2\n")
```

### 13.6 控制文件内指针移动

```python
with open("test.txt", "r+", encoding="utf-8") as fp:
    # tell()：获取当前指针位置（字节数）
    print(fp.tell())  # 0（文件开头）

    # read() 读取后指针会移动
    data = fp.read(5)
    print(fp.tell())  # 读取了 5 个字符后的字节位置

    # seek()：移动指针到指定位置
    # seek(字节偏移量, 参照位置)
    #   0：从文件开头算起（默认）
    #   1：从当前位置算起（仅二进制模式支持）
    #   2：从文件末尾算起

    fp.seek(0, 0)   # 移动到文件开头
    fp.seek(0, 2)   # 移动到文件末尾

    # 注意：文本模式下 seek 的中文问题
    # 一个中文字符占 3 个字节（UTF-8），移动时要注意对齐
    # 如果 seek 到中文的中间字节，可能导致乱码
```

```python
# 二进制模式下的 seek 操作
with open("photo.jpg", "rb") as fp:
    fp.seek(5, 0)    # 从文件头偏移 5 个字节
    print(fp.tell())  # 5
    fp.seek(5, 1)    # 从当前位置偏移 5 个字节
    print(fp.tell())  # 10
```

### 13.7 文件存取数据示例

```python
# 将结构化数据写入文件，再从文件读取

# 写入
user_data = {
    "dream": {"username": "dream", "password": "521", "age": "18"},
    "hope":  {"username": "hope",  "password": "666", "age": "20"}
}

with open("users.txt", "w", encoding="utf-8") as fp:
    for user_info in user_data.values():
        line = "|".join([str(v) for v in user_info.values()]) + "\n"
        fp.write(line)

# 读取
loaded_data = {}
with open("users.txt", "r", encoding="utf-8") as fp:
    for line in fp:
        username, password, age = line.strip().split("|")
        loaded_data[username] = {
            "username": username,
            "password": password,
            "age": age
        }

print(loaded_data)
```

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
