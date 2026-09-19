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

---

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
