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

---

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
