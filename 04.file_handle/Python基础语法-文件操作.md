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
