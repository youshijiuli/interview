# Python 文件操作与异常处理

---

## 一、文件操作基础

### 1.1 为什么需要文件操作

程序运行时产生的数据默认存储在内存中，一旦程序结束或计算机断电，内存中的数据就会丢失。为了让数据能够持久化保存，我们需要将数据写入到硬盘的文件中。

Python 提供了内置的 `open()` 函数来打开文件，并返回一个文件对象（句柄），通过这个句柄可以对文件进行读写操作。

### 1.2 文件的两种打开方式

#### 方式一：手动打开和关闭

```python
# 打开文件：句柄 = open(文件路径, 操作模式, 编码格式)
fp = open("data.txt", "w", encoding="utf-8")
# 写入数据
fp.write("hello world")
# 关闭文件（释放系统资源）
fp.close()
```

这种方式需要手动调用 `close()` 方法关闭文件，如果不关闭可能会造成资源泄露。

#### 方式二：使用 with 上下文管理器（推荐）

```python
# with 语句会自动管理文件的打开和关闭，离开 with 代码块时自动关闭文件
with open("data.txt", "w", encoding="utf-8") as fp:
    fp.write("hello world")
# 此处文件已被自动关闭
```

**强烈建议使用 `with` 语句**，它能够确保即使在发生异常的情况下，文件也能被正确关闭。

### 1.3 文件操作模式详解

文件的打开模式决定了我们可以对文件进行什么样的操作。常用的基本模式有以下三种：

#### r 模式 -- 只读模式（read）

```python
# r 模式：只读取文件内容，不能写入
# 如果文件不存在，会抛出 FileNotFoundError
with open("data.txt", "r", encoding="utf-8") as fp:
    data = fp.read()
    print(data)
```

- 默认模式，当不指定 mode 参数时，默认就是 r 模式
- 文件不存在时会报错：`FileNotFoundError: [Errno 2] No such file or directory`

#### w 模式 -- 只写模式（write）

```python
# w 模式：只写入文件内容，不能读取
# 文件不存在时自动创建；文件存在时会清空原有内容再写入（覆盖写）
with open("output.txt", "w", encoding="utf-8") as fp:
    fp.write("这是新写入的内容")
```

- 覆盖写模式：每次打开文件都会清空原有内容
- 文件不存在时自动创建新文件
- 在 with 语句内部可以连续多次 write

#### a 模式 -- 追加模式（append）

```python
# a 模式：在文件末尾追加内容，不能读取
# 文件不存在时自动创建；文件存在时在末尾追加内容
with open("log.txt", "a", encoding="utf-8") as fp:
    fp.write("追加一行日志\n")
```

- 追加写模式：新内容会添加到文件末尾
- 文件不存在时自动创建新文件

### 1.4 扩展模式（+ 和 b）

#### + 模式 -- 读写扩展

```python
# r+ : 既能读又能写（不截断文件）
# w+ : 既能写又能读（先清空文件）
# a+ : 既能追加又能读（从末尾开始写）

# r+ 示例
with open("data.txt", "r+", encoding="utf-8") as fp:
    data = fp.read()   # 先读取
    fp.write("新内容")  # 再写入
```

> **注意**：在实际开发中，通常不建议混用读写模式。对同一个文件，要么只读，要么只写，保持操作单一性。

#### b 模式 -- 二进制模式

```python
# rb : 读取二进制数据（图片、音频、视频、压缩包等）
# wb : 写入二进制数据

# 复制图片示例
with open("source.jpg", "rb") as fp_read:
    image_data = fp_read.read()

with open("copy.jpg", "wb") as fp_write:
    fp_write.write(image_data)
```

- 操作非文本文件（图片、音频、视频等）时必须使用 b 模式
- b 模式下不能指定 encoding 参数（因为不需要字符编码转换）
- b 模式可以单独使用（rb, wb, ab），也可以和 + 组合使用（rb+, wb+）

---

## 二、文件读取方法

### 2.1 read() -- 一次性读取全部内容

```python
with open("data.txt", "r", encoding="utf-8") as fp:
    # 不带参数：读取文件全部内容
    content = fp.read()
    print(content)

    # 带参数：读取指定字符数
    # fp.seek(0)  # 如果上面已读过，需要将指针移回开头
    # content_part = fp.read(10)  # 读取前10个字符
```

- `read()` 不带参数时一次性读取全部内容，适合小文件
- `read(n)` 带参数时读取 n 个字符（注意是字符数，不是字节数）
- 对于大文件，一次性读取全部内容可能导致内存不足

### 2.2 readline() -- 逐行读取

```python
with open("data.txt", "r", encoding="utf-8") as fp:
    # 读取第一行
    line1 = fp.readline()
    print(f"第一行: {line1}")

    # 读取第二行
    line2 = fp.readline()
    print(f"第二行: {line2}")

    # 文件末尾返回空字符串 ''
```

- 每次读取一行（包括换行符 `\n`）
- 读到文件末尾时返回空字符串 `''`
- 适合需要逐行处理的场景

### 2.3 readlines() -- 读取所有行到列表

```python
with open("data.txt", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    print(lines)  # ['第一行内容\n', '第二行内容\n', '第三行内容\n']

# 处理每一行
for line in lines:
    print(line.strip())  # 去除末尾换行符
```

- 将每一行作为一个元素存入列表
- 每行末尾保留换行符 `\n`
- 同样不适合超大文件

### 2.4 文件对象的可迭代性

```python
# 文件对象本身是可迭代的，可以直接用 for 循环遍历
with open("data.txt", "r", encoding="utf-8") as fp:
    for line in fp:
        print(line.strip())
```

- 这是处理大文件的最佳方式，每次只读一行到内存
- 不会一次性将整个文件加载到内存中

### 2.5 readable() -- 判断文件是否可读

```python
with open("data.txt", "r", encoding="utf-8") as fp:
    if fp.readable():
        print("该文件可读")
        content = fp.read()
    else:
        print("该文件不可读")
```

---

## 三、文件写入方法

### 3.1 write() -- 写入字符串

```python
with open("output.txt", "w", encoding="utf-8") as fp:
    fp.write("Hello Python\n")
    fp.write("Hello World\n")
    fp.write("第三行内容\n")
```

- `write()` 方法只接受字符串类型参数
- 不会自动添加换行符，需要手动添加 `\n`
- 在 with 语句块内可以多次调用 write，内容会依次写入

### 3.2 writelines() -- 写入可迭代对象

```python
lines = ["第一行\n", "第二行\n", "第三行\n"]

with open("output.txt", "w", encoding="utf-8") as fp:
    fp.writelines(lines)
```

- 接受一个可迭代对象（如列表），将每个元素拼接到一起写入
- 不会自动添加换行符，需要在每个元素末尾手动添加

### 3.3 writable() -- 判断文件是否可写

```python
with open("output.txt", "w", encoding="utf-8") as fp:
    if fp.writable():
        print("该文件可写")
        fp.write("可以开始写入数据")
```

### 3.4 写入非字符串数据

```python
# 如果要将非字符串数据写入文件，需要先转换为字符串
num_list = [1, 2, 3, 4, 5]

# 方式一：直接转字符串
with open("data.txt", "w", encoding="utf-8") as fp:
    fp.write(str(num_list))  # 写入 "[1, 2, 3, 4, 5]"

# 方式二：使用分隔符拼接
with open("data.txt", "w", encoding="utf-8") as fp:
    fp.write("|".join(str(i) for i in num_list))  # 写入 "1|2|3|4|5"
```

---

## 四、文件指针控制

### 4.1 什么是文件指针

当我们打开一个文件进行读写时，Python 会维护一个"文件指针"（也叫光标），它标记了当前读写的起始位置。文件刚打开时，指针默认在文件开头（r 模式）或末尾（a 模式）。

### 4.2 tell() -- 获取当前指针位置

```python
with open("data.txt", "r+", encoding="utf-8") as fp:
    print(fp.tell())  # 0 -- 指针在文件开头
    fp.read(5)        # 读取5个字符
    print(fp.tell())  # 5 -- 指针向后移动了5个字符
```

- 返回值是当前指针位置距离文件开头的**字节数**
- 一个英文字符占 1 个字节，一个中文字符通常占 3 个字节（UTF-8 编码下）

### 4.3 seek() -- 移动文件指针

```python
# seek(offset, whence)
# offset: 移动的字节数（正数向右，负数向左）
# whence: 参照位置
#   0 -- 从文件开头开始计算（默认）
#   1 -- 从当前位置开始计算（只支持二进制模式）
#   2 -- 从文件末尾开始计算

with open("data.txt", "r+", encoding="utf-8") as fp:
    # 查看当前指针位置
    print(f"初始位置: {fp.tell()}")  # 0

    # 从开头向后移动6个字节
    fp.seek(6, 0)
    print(f"移动后位置: {fp.tell()}")  # 6

    # 读取指针后面的内容
    data = fp.read()
    print(data)
```

### 4.4 seek 的三种参照模式

```python
# 以二进制模式打开文件来演示三种模式
with open("test.bin", "wb") as fp:
    fp.write(b"0123456789")

with open("test.bin", "rb") as fp:
    # 模式 0：从文件开头计算偏移（文本和二进制都支持）
    fp.seek(3, 0)       # 从开头向右移动 3 个字节
    print(fp.tell())     # 3

    # 模式 1：从当前位置计算偏移（仅支持二进制模式）
    fp.seek(2, 1)       # 从当前位置向右移动 2 个字节
    print(fp.tell())     # 5

    # 模式 2：从文件末尾计算偏移（仅支持二进制模式）
    fp.seek(0, 2)       # 移动到文件末尾
    print(fp.tell())     # 10（文件总大小）

    fp.seek(-3, 2)      # 从末尾向左移动 3 个字节
    print(fp.tell())     # 7
```

### 4.5 指针操作与文件修改

```python
# seek 可以用来实现"定点修改"
with open("data.txt", "r+", encoding="utf-8") as fp:
    # 从开头偏移6个字节
    fp.seek(6, 0)
    # 在指针位置覆盖写入
    fp.write("新内容")
```

**重要注意事项**：

- 在指针位置写入数据是**覆盖写**，不会插入新内容
- 中文在 UTF-8 编码中占 3 个字节，如果指针恰好落在中文字符的中间位置进行写入，会导致文件乱码
- a 模式的原理就是打开时将指针移到文件末尾

### 4.6 指针移动实战案例

```python
# 案例：读取文件最后一行（大文件场景）
def read_last_line(file_path):
    with open(file_path, "rb") as fp:
        # 指针移到末尾
        fp.seek(0, 2)
        file_size = fp.tell()

        # 从末尾向前逐字节读取，直到找到换行符
        buffer = bytearray()
        position = file_size - 1
        while position >= 0:
            fp.seek(position)
            byte = fp.read(1)
            if byte == b'\n' and buffer:
                break
            buffer.extend(byte)
            position -= 1

        # 反转字节序得到正确文本
        return buffer[::-1].decode("utf-8")

# 案例：使用 a 模式实现文件末尾追加
with open("log.txt", "a", encoding="utf-8") as fp:
    fp.write("新日志条目\n")
    # a 模式在打开文件时自动将指针移到末尾
    print(fp.tell())  # 文件大小（字节数）
```

---

## 五、with 上下文管理器详解

### 5.1 with 语句的基本原理

`with` 语句是 Python 的上下文管理协议，它确保资源在使用后被正确释放。

```python
# with 语句的等价写法
# 方式一：with 语法（推荐）
with open("data.txt", "r", encoding="utf-8") as fp:
    content = fp.read()

# 方式二：等价的手动管理
fp = open("data.txt", "r", encoding="utf-8")
try:
    content = fp.read()
finally:
    fp.close()  # 无论是否发生异常，都会执行关闭
```

### 5.2 with 语句的优势

```python
# 1. 自动关闭文件，无需手动调用 close()
# 2. 即使发生异常也能确保文件被关闭
# 3. 代码更简洁清晰

# 反例：没有 with 的代码可能在异常时导致资源泄露
fp = open("data.txt", "r", encoding="utf-8")
data = fp.read()
# 如果上面某行发生异常，fp.close() 不会被执行
fp.close()

# 正例：使用 with 语句
with open("data.txt", "r", encoding="utf-8") as fp:
    data = fp.read()
# 无论是否异常，文件都会被关闭
```

### 5.3 同时管理多个文件

```python
# 使用 with 同时打开多个文件（用逗号分隔）
with open("source.txt", "r", encoding="utf-8") as fp_in, \
     open("target.txt", "w", encoding="utf-8") as fp_out:
    content = fp_in.read()
    fp_out.write(content.upper())
```

### 5.4 上下文管理协议原理

```python
# with 语句执行过程：
# 1. 执行 open() 返回文件对象
# 2. 调用文件对象的 __enter__() 方法，返回值赋给 as 后的变量
# 3. 执行 with 代码块中的语句
# 4. 无论是否发生异常，最后都会调用文件对象的 __exit__() 方法

# 自定义上下文管理器类
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if exc_type is not None:
            print(f"发生异常: {exc_val}")
        return False  # False 表示不抑制异常

# 使用自定义上下文管理器
with FileManager("test.txt", "w") as fp:
    fp.write("Hello Context Manager")
```

---

## 六、文件修改的两种方式

在实际开发中，我们经常需要修改文件内容。由于文件在硬盘上是顺序存储的，不能直接在原位置"插入"或"删除"内容。因此通常有以下两种修改方式：

### 6.1 方式一：一次性读取修改法

适用于**小文件**，将整个文件读入内存，修改后再写回。

```python
# 将文件中所有的 "Python" 替换为 "Python3"
with open("data.txt", "r", encoding="utf-8") as fp:
    content = fp.read()

# 在内存中修改
content = content.replace("Python", "Python3")

# 写回原文件
with open("data.txt", "w", encoding="utf-8") as fp:
    fp.write(content)
```

**优点**：实现简单，代码清晰
**缺点**：对于大文件会占用大量内存

### 6.2 方式二：逐行读取修改法

适用于**大文件**，逐行读取原文件，修改后写入临时文件，最后替换原文件。

```python
import os

source_file = "data.txt"
temp_file = "data.txt.tmp"

# 逐行读取源文件，处理后将结果写入临时文件
with open(source_file, "r", encoding="utf-8") as fp_read, \
     open(temp_file, "w", encoding="utf-8") as fp_write:
    for line in fp_read:
        # 逐行修改：替换内容、过滤行等
        new_line = line.replace("Python", "Python3")
        fp_write.write(new_line)

# 用临时文件替换原文件
os.remove(source_file)
os.rename(temp_file, source_file)
```

### 6.3 文件修改综合案例

```python
import os

# 综合案例：实现文件内容的批量替换，并添加行号
def modify_file(file_path, old_str, new_str, add_line_number=False):
    """
    修改文件内容
    :param file_path: 文件路径
    :param old_str: 要替换的旧字符串
    :param new_str: 新字符串
    :param add_line_number: 是否添加行号
    """
    temp_path = file_path + ".tmp"
    line_num = 0

    with open(file_path, "r", encoding="utf-8") as fp_src, \
         open(temp_path, "w", encoding="utf-8") as fp_tmp:
        for line in fp_src:
            line_num += 1
            # 替换内容
            new_line = line.replace(old_str, new_str)
            # 可选：添加行号
            if add_line_number:
                new_line = f"{line_num:04d} | {new_line}"
            fp_tmp.write(new_line)

    # 替换原文件
    os.remove(file_path)
    os.rename(temp_path, file_path)
    print(f"文件修改完成，共处理 {line_num} 行")

# 使用示例
# modify_file("report.txt", "2023", "2024", add_line_number=True)
```

### 6.4 基于文件的数据存储方案

将 Python 数据结构（如字典、列表）存储到文件中，需要自己设计存储格式。

```python
# 存储格式约定：username|password|age|gender|role
# 示例数据：dream|521|18|male|admin

# 写入用户数据
user_data = {
    "dream": {"username": "dream", "password": "521", "age": "18", "gender": "male", "role": "admin"},
    "hope":  {"username": "hope",  "password": "123", "age": "20", "gender": "female", "role": "user"}
}

# 写入文件
data_list = []
for user_info in user_data.values():
    # 将每个字段用 | 拼接
    data_line = '|'.join([str(value) for value in user_info.values()])
    data_list.append(data_line + '\n')

with open("user_db.txt", "w", encoding="utf-8") as fp:
    fp.writelines(data_list)

# 从文件读取用户数据
user_data_loaded = {}
with open("user_db.txt", "r", encoding="utf-8") as fp:
    for line in fp:
        username, password, age, gender, role = line.strip().split('|')
        user_data_loaded[username] = {
            "username": username,
            "password": password,
            "age": age,
            "gender": gender,
            "role": role
        }

print(user_data_loaded)
```

---

## 七、异常处理

### 7.1 什么是异常

异常是程序在运行过程中遇到的错误，它会中断程序的正常执行流程。如果不对异常进行处理，程序将直接崩溃退出。

```python
# 常见异常示例
# print(1 / 0)     # ZeroDivisionError: division by zero
# int("abc")        # ValueError: invalid literal for int() with base 10: 'abc'
# [1, 2, 3][5]     # IndexError: list index out of range
# {}["key"]         # KeyError: 'key'
```

### 7.2 Python 常见内置异常分类

| 异常类 | 说明 |
|--------|------|
| `BaseException` | 所有异常的基类 |
| `Exception` | 常规错误的基类（通常捕获这个就够） |
| `TypeError` | 对类型无效的操作 |
| `ValueError` | 传入无效的参数 |
| `ZeroDivisionError` | 除零错误 |
| `IndexError` | 序列中没有此索引 |
| `KeyError` | 映射中没有这个键 |
| `AttributeError` | 对象没有这个属性 |
| `NameError` | 未声明的变量名 |
| `FileNotFoundError` | 文件未找到 |
| `IOError` | 输入/输出操作失败 |
| `SyntaxError` | Python 语法错误 |
| `ImportError` | 导入模块失败 |
| `MemoryError` | 内存溢出 |
| `KeyboardInterrupt` | 用户中断执行（通常按 Ctrl+C） |
| `StopIteration` | 迭代器没有更多值 |
| `IndentationError` | 缩进错误 |
| `AssertionError` | 断言语句失败 |

### 7.3 try/except -- 基本异常捕获

#### 7.3.1 捕获所有异常（不推荐）

```python
try:
    # 可能会发生异常的代码
    result = int("abc")
except:
    # 发生任何异常都会执行这里的代码
    print("发生异常了，请检查代码")
```

这种方式捕获了所有异常但不获取异常信息，不利于调试，**不推荐使用**。

#### 7.3.2 捕获指定类型的异常

```python
try:
    result = int("abc")
except ValueError:
    # 只有发生 ValueError 时才执行
    print("数据转换出错，请输入有效的数字")
```

#### 7.3.3 捕获多个指定类型的异常

```python
try:
    num = int(input("请输入一个数字: "))
    result = 100 / num
    print(f"结果是: {result}")
except (ValueError, ZeroDivisionError) as e:
    # e 是异常对象，包含异常信息
    print(f"发生异常: {e}")
```

#### 7.3.4 捕获所有常规异常（推荐做法）

```python
try:
    # 可能发生异常的代码
    result = some_risky_operation()
except Exception as e:
    # 捕获所有常规异常，并获取异常信息
    print(f"程序运行出错: {e}")
```

- `Exception` 是大多数内置异常和自定义异常的基类
- 使用 `as e` 可以获取异常对象，便于输出错误信息
- 这比裸的 `except:` 更好，因为不会捕获 `KeyboardInterrupt` 和 `SystemExit` 等系统级异常

### 7.4 try/except/else -- 无异常时执行

```python
try:
    num = int(input("请输入一个数字: "))
except ValueError as e:
    print(f"输入的不是有效数字: {e}")
else:
    # try 块没有发生任何异常时执行
    print(f"你输入的数字是: {num}")
```

- `else` 块只在 try 块没有发生异常时执行
- 将只在正常情况下执行的代码放在 else 中，可以使代码逻辑更清晰

### 7.5 try/except/finally -- 无论如何都执行

```python
try:
    fp = open("data.txt", "r", encoding="utf-8")
    content = fp.read()
    print(content)
except FileNotFoundError:
    print("文件不存在，请检查文件路径")
finally:
    # 无论是否发生异常，finally 中的代码都会执行
    # 通常用于释放资源（如关闭文件）
    try:
        fp.close()
        print("文件已关闭")
    except:
        pass
```

- `finally` 块**始终执行**，无论是否发生异常
- 常用于清理资源（关闭文件、释放数据库连接等）
- 如果 try 中有 return，finally 也会在 return 之前执行

### 7.6 完整的异常处理结构

```python
def read_file_safe(file_path):
    """安全地读取文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as fp:
            content = fp.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return None
    except PermissionError:
        print(f"错误: 没有权限读取文件 '{file_path}'")
        return None
    except UnicodeDecodeError:
        print(f"错误: 文件编码格式不正确")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None
    else:
        # 没有异常时执行
        print(f"文件读取成功，大小: {len(content)} 字符")
        return content
    finally:
        # 始终执行：记录日志、清理操作等
        print(f"读取操作结束")

result = read_file_safe("data.txt")
```

### 7.7 异常处理实战案例

```python
# 案例：多用户登录注册系统，从文件读取数据并处理可能的异常
def load_user_data():
    """从文件加载用户数据，处理文件不存在等异常"""
    user_data = {}
    try:
        with open("users.txt", "r", encoding="utf-8") as fp:
            for line in fp:
                try:
                    username, password, age, gender, role = line.strip().split('|')
                    user_data[username] = {
                        "username": username,
                        "password": password,
                        "age": age,
                        "gender": gender,
                        "role": role
                    }
                except ValueError:
                    # 某行数据格式不正确，跳过该行继续处理
                    print(f"警告: 数据行格式不正确，已跳过: {line.strip()}")
                    continue
    except FileNotFoundError:
        # 文件不存在时返回空字典（首次运行时文件还未创建）
        print("用户数据文件不存在，将创建新文件")
        user_data = {}
    except Exception as e:
        print(f"读取用户数据时发生错误: {e}")
        user_data = {}
    return user_data

# 使用加载的数据
users = load_user_data()
print(f"当前注册用户数: {len(users)}")
```

---

## 八、自定义异常

### 8.1 使用 raise 主动抛出异常

```python
# raise 关键字用于主动抛出异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不能超过150岁")
    return age

try:
    check_age(-5)
except ValueError as e:
    print(f"校验失败: {e}")
```

### 8.2 自定义异常类

当内置异常类无法准确描述业务错误时，可以自定义异常类。

```python
# 自定义异常类，继承自 Exception
class InvalidUsernameError(Exception):
    """用户名不合法异常"""
    def __init__(self, username, message="用户名不合法"):
        self.username = username
        self.message = f"{message}: {username}"
        super().__init__(self.message)


class WeakPasswordError(Exception):
    """弱密码异常"""
    def __init__(self, message="密码强度不足"):
        self.message = message
        super().__init__(self.message)


# 使用自定义异常
def validate_user(username, password):
    """校验用户名和密码"""
    if not username or len(username) < 3:
        raise InvalidUsernameError(username, "用户名长度不能少于3位")

    if len(password) < 6:
        raise WeakPasswordError("密码长度不能少于6位")

    if password.isdigit() or password.isalpha():
        raise WeakPasswordError("密码必须包含字母和数字的组合")

    return True


# 测试
test_cases = [
    ("ab", "123456"),
    ("dream", "12345"),
    ("dream", "abcdef"),
    ("dream", "abc123"),
]

for username, password in test_cases:
    try:
        validate_user(username, password)
        print(f"[通过] 用户名: {username}, 密码: {password}")
    except InvalidUsernameError as e:
        print(f"[用户名错误] {e}")
    except WeakPasswordError as e:
        print(f"[密码错误] {e}")
```

### 8.3 多层自定义异常体系

```python
# 构建业务异常体系
class AppException(Exception):
    """应用基础异常类"""
    def __init__(self, message="应用程序异常", code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DatabaseException(AppException):
    """数据库相关异常"""
    def __init__(self, message="数据库操作异常", code=501):
        super().__init__(message, code)


class ValidationException(AppException):
    """数据校验异常"""
    def __init__(self, message="数据校验失败", code=400):
        super().__init__(message, code)


class AuthenticationException(AppException):
    """认证异常"""
    def __init__(self, message="认证失败", code=401):
        super().__init__(message, code)


# 使用示例
def save_user(user_data, db_connected=True):
    if not db_connected:
        raise DatabaseException("无法连接到数据库", code=501)
    if not user_data.get("username"):
        raise ValidationException("用户名不能为空")
    print(f"用户 {user_data['username']} 保存成功")


try:
    save_user({"age": 18}, db_connected=True)
except AppException as e:
    print(f"[{e.code}] {e.message}")
except Exception as e:
    print(f"未知错误: {e}")
```

### 8.4 raise from -- 异常链

```python
# 使用 raise ... from ... 保留异常链，便于追踪问题根源
def process_data(file_path):
    try:
        with open(file_path, "r") as fp:
            data = fp.read()
    except FileNotFoundError as e:
        # 将原始异常包装后重新抛出，保留异常链
        raise RuntimeError(f"处理数据失败: 找不到文件 {file_path}") from e

    # 继续处理数据
    return len(data)


try:
    process_data("not_exist.txt")
except RuntimeError as e:
    print(f"运行时错误: {e}")
    print(f"原始错误: {e.__cause__}")
```

---

## 九、断言（assert）

### 9.1 assert 基本用法

```python
# assert 语法：assert 条件表达式, "可选的错误信息"
# 当条件为 False 时，抛出 AssertionError 异常

def divide(a, b):
    # 断言除数不能为零
    assert b != 0, "除数不能为零"
    return a / b


print(divide(10, 2))   # 5.0
# print(divide(10, 0))  # AssertionError: 除数不能为零
```

### 9.2 assert 的应用场景

```python
# 1. 调试阶段的参数校验
def calculate_discount(price, discount_rate):
    assert 0 <= discount_rate <= 1, "折扣率必须在0到1之间"
    assert price > 0, "价格必须大于0"
    return price * (1 - discount_rate)

# 2. 接口前置条件检查
def save_to_database(data):
    assert isinstance(data, dict), "数据必须是字典类型"
    assert "id" in data, "数据必须包含id字段"
    # ... 保存到数据库的逻辑

# 3. 循环中的条件检查
for i in range(10):
    # 替代原来的 if + raise 写法
    # if i == 2:
    #     raise ValueError("不能为2")
    assert i != 2, f"i不能为2，当前i={i}"
    print(i)
```

### 9.3 assert 与 if/raise 的区别

```python
# 方式一：assert（调试用，生产环境可通过 -O 参数禁用）
assert condition, "错误信息"

# 方式二：if + raise（始终生效，不会被禁用）
if not condition:
    raise ValueError("错误信息")
```

**关键区别**：

- `assert` 断言可以在运行时通过 `python -O`（优化模式）全局禁用
- `if + raise` 是正常的代码逻辑，不会被禁用
- **assert 适合调试阶段的内部检查，而不是生产环境的数据校验**

### 9.4 assert 实战案例

```python
# 模拟一套 API 参数校验体系
def create_order(user_id, product_id, quantity):
    """创建订单 - 用 assert 进行参数合法性断言"""
    # 前置条件断言
    assert isinstance(user_id, int) and user_id > 0, \
        f"无效的用户ID: {user_id}"
    assert isinstance(product_id, int) and product_id > 0, \
        f"无效的产品ID: {product_id}"
    assert isinstance(quantity, int) and 1 <= quantity <= 100, \
        f"无效的购买数量: {quantity}（允许范围 1-100）"

    # 如果上面所有断言通过，执行业务逻辑
    order = {
        "order_id": hash((user_id, product_id, quantity)),
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "created"
    }
    return order


# 测试
try:
    order = create_order(1001, 5001, 3)
    print(f"订单创建成功: {order}")
except AssertionError as e:
    print(f"订单创建失败: {e}")

try:
    order = create_order(1001, 5001, 200)
except AssertionError as e:
    print(f"订单创建失败: {e}")
```

---

## 十、综合案例

### 10.1 简单日志分析器

```python
"""
日志分析器：读取日志文件，统计错误信息，生成分析报告
"""
import os
from collections import Counter


def analyze_log(input_file, output_file):
    """分析日志文件并生成报告"""
    error_counter = Counter()
    total_lines = 0
    error_lines = 0

    try:
        # 检查输入文件
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"日志文件不存在: {input_file}")

        # 读取并分析日志
        with open(input_file, "r", encoding="utf-8") as fp_in:
            for line in fp_in:
                total_lines += 1

                # 提取错误类型
                if "ERROR" in line:
                    error_lines += 1
                    # 尝试提取错误的具体类型
                    parts = line.split("ERROR")
                    if len(parts) > 1:
                        error_detail = parts[1].strip()
                        error_counter[error_detail[:50]] += 1
                    else:
                        error_counter["Unknown Error"] += 1
                elif "WARNING" in line:
                    error_lines += 1
                    error_counter["WARNING"] += 1

        # 写入分析报告
        with open(output_file, "w", encoding="utf-8") as fp_out:
            fp_out.write("=" * 60 + "\n")
            fp_out.write("日志分析报告\n")
            fp_out.write("=" * 60 + "\n\n")

            fp_out.write(f"总行数: {total_lines}\n")
            fp_out.write(f"有问题的行数: {error_lines}\n")
            fp_out.write(f"错误率: {error_lines/total_lines*100:.2f}%\n")
            fp_out.write("\n" + "-" * 60 + "\n\n")
            fp_out.write("错误/警告分布:\n")

            for error_type, count in error_counter.most_common(10):
                fp_out.write(f"  [{count:5d}次] {error_type}\n")

        print(f"分析完成！报告已保存到: {output_file}")

    except FileNotFoundError as e:
        print(f"错误: {e}")
    except PermissionError:
        print(f"错误: 没有权限读取或写入文件")
    except Exception as e:
        print(f"分析过程中出现未知错误: {e}")
    finally:
        print(f"日志分析任务结束，共处理 {total_lines} 行")


# analyze_log("app.log", "analysis_report.txt")
```

### 10.2 安全文件写入器

```python
"""
安全文件写入器：确保写入过程中不会丢失原文件数据
"""
import os
import tempfile
import shutil


class SafeFileWriter:
    """安全的文件写入工具，先写入临时文件，成功后再替换原文件"""

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.encoding = encoding
        self.temp_path = None
        self.file_obj = None

    def __enter__(self):
        # 创建临时文件
        dir_name = os.path.dirname(self.file_path) or "."
        fd, self.temp_path = tempfile.mkstemp(
            suffix=".tmp",
            prefix="safe_write_",
            dir=dir_name
        )
        os.close(fd)
        self.file_obj = open(self.temp_path, "w", encoding=self.encoding)
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()

        if exc_type is not None:
            # 发生异常：删除临时文件，保留原文件
            os.remove(self.temp_path)
            print(f"写入失败，原文件未受影响。错误: {exc_val}")
            return False  # 不抑制异常

        # 无异常：用临时文件替换原文件
        try:
            shutil.move(self.temp_path, self.file_path)
            print(f"文件写入成功: {self.file_path}")
        except Exception as e:
            try:
                os.remove(self.temp_path)
            except:
                pass
            raise e


# 使用示例
data_to_write = [
    "这是第一行重要数据\n",
    "这是第二行重要数据\n",
    "这是第三行重要数据\n",
]

try:
    with SafeFileWriter("important_data.txt") as fp:
        for line in data_to_write:
            fp.write(line)
    # 如果 with 块正常结束，文件已安全替换
    print("数据写入完成")
except Exception as e:
    print(f"数据写入失败: {e}")
```

---

## 本章小结

| 知识点 | 核心内容 |
|--------|----------|
| 文件打开 | `open()` 函数，with 上下文管理器 |
| 操作模式 | r（读）、w（覆盖写）、a（追加写）、b（二进制）、+（读写） |
| 读取方法 | read()、readline()、readlines()、for 循环遍历 |
| 写入方法 | write()、writelines() |
| 指针控制 | seek() 移动、tell() 获取位置 |
| 文件修改 | 一次性读取修改（小文件）、逐行修改（大文件） |
| 异常捕获 | try/except/else/finally 结构 |
| 抛出异常 | raise 关键字 |
| 自定义异常 | 继承 Exception 类 |
| 断言 | assert 条件表达式，调试用 |

**核心编程建议**：

1. 文件操作始终使用 `with` 语句，让 Python 自动管理资源的打开和关闭
2. 处理大文件时避免一次性读入内存，使用逐行读取
3. 异常处理要具体，优先捕获特定类型的异常，最后再兜底捕获 `Exception`
4. 永远不要在 `except` 块中留下空的 `pass`，至少要记录日志
5. `assert` 用于开发阶段的内部逻辑校验，生产环境的数据校验应使用 `if/raise`
