# Python 常用标准库

---

## 一、模块与包基础概念

### 1.1 什么是模块

模块就是一个包含 Python 函数和变量的 `.py` 文件。文件名就是模块名，一个 `.py` 文件就是一个独立的模块。

```python
# 例如：创建一个名为 my_utils.py 的文件
# my_utils.py 中的内容：
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# 在另一个文件中导入并使用
import my_utils

result = my_utils.add(3, 5)
print(result)  # 8
```

### 1.2 模块的三种来源

1. **内置模块**：Python 解释器自带的，如 `os`、`json`、`time` 等
2. **第三方模块**：由社区开发者贡献，需要安装后才能使用，如 `requests`、`django`
3. **自定义模块**：开发者自己编写的 `.py` 文件

### 1.3 模块的导入语法

```python
# 方式一：import 模块名
import os
import json

# 方式二：import 多个模块
import os, json, time

# 方式三：from ... import ... 精确导入
from os.path import join, dirname, exists

# 方式四：from ... import ... as ... 取别名
import numpy as np
from datetime import datetime as dt
```

### 1.4 什么是包

包就是一个包含多个模块和 `__init__.py` 文件的文件夹。包的创建方式有两种：
- 在 PyCharm 中右键选择 `Python Package`
- 手动创建文件夹并在其中创建 `__init__.py` 文件

```python
# 包结构示例
# my_package/
#   __init__.py
#   module_a.py
#   module_b.py
#   sub_package/
#       __init__.py
#       module_c.py

# 导入包中的模块
from my_package import module_a
from my_package.sub_package import module_c
```

### 1.5 主程序入口

```python
# 每个 Python 文件都有一个内置变量 __name__
# 当文件作为主程序直接运行时，__name__ 的值为 '__main__'
# 当文件作为模块被导入时，__name__ 的值为模块名

def main():
    print("程序开始运行")

if __name__ == '__main__':
    # 只有在直接运行本文件时才执行的测试代码
    main()
```

---

## 二、os 模块 -- 系统操作

`os` 模块是 Python 与操作系统交互的核心模块，提供了大量的文件和目录操作函数。

### 2.1 路径操作（os.path）

#### 获取文件路径信息

```python
import os

# __file__ 代表当前文件的路径
print(f"当前文件: {__file__}")

# 获取当前文件的绝对路径
file_abs_path = os.path.abspath(__file__)
print(f"文件绝对路径: {file_abs_path}")
# /Users/dream/Documents/project/main.py

# 获取当前文件所在的目录路径
file_dir = os.path.dirname(__file__)
print(f"文件所在目录: {file_dir}")
# /Users/dream/Documents/project

# 获取路径中的文件名部分
file_name = os.path.basename(file_abs_path)
print(f"文件名: {file_name}")
# main.py

# 分割路径和文件名
path_part, file_part = os.path.split(file_abs_path)
print(f"目录部分: {path_part}")  # /Users/dream/Documents/project
print(f"文件部分: {file_part}")  # main.py
```

#### 路径判断

```python
import os

target_path = "/Users/dream/Documents/project"

# 判断路径是否存在
print(os.path.exists(target_path))   # True 或 False

# 判断是否是文件
print(os.path.isfile(target_path))   # True 或 False

# 判断是否是目录
print(os.path.isdir(target_path))    # True 或 False

# 判断是否是绝对路径
print(os.path.isabs(target_path))    # True
print(os.path.isabs("./config.ini")) # False
```

#### 路径拼接与分割

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 安全地拼接路径（自动处理不同操作系统的分隔符）
data_dir = os.path.join(BASE_DIR, "data", "users")
print(data_dir)
# Windows: E:\project\data\users
# Mac/Linux: /Users/dream/project/data/users

# 获取系统路径分隔符
print(f"路径分隔符: {os.path.sep}")
# Windows: \
# Mac/Linux: /

# 系统行终止符
print(f"行终止符: {repr(os.linesep)}")
# Windows: '\r\n'
# Mac/Linux: '\n'
```

#### 获取文件元信息

```python
import os
import datetime

file_path = os.path.abspath(__file__)

# 获取文件大小（字节）
size = os.path.getsize(file_path)
print(f"文件大小: {size} 字节")

# 获取最后访问时间
atime = os.path.getatime(file_path)
print(f"最后访问: {datetime.datetime.fromtimestamp(atime)}")

# 获取创建时间
ctime = os.path.getctime(file_path)
print(f"创建时间: {datetime.datetime.fromtimestamp(ctime)}")

# 获取最后修改时间
mtime = os.path.getmtime(file_path)
print(f"最后修改: {datetime.datetime.fromtimestamp(mtime)}")

# 获取文件的详细元信息
stat_info = os.stat(file_path)
print(f"st_size: {stat_info.st_size}")  # 文件大小
print(f"st_uid:  {stat_info.st_uid}")   # 用户ID
print(f"st_gid:  {stat_info.st_gid}")   # 组ID
```

### 2.2 文件和目录操作

#### 创建目录

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 创建单级目录
dir_path = os.path.join(BASE_DIR, "images")
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
    print(f"目录已创建: {dir_path}")

# 创建多级目录（递归创建）
multi_dir = os.path.join(BASE_DIR, "data", "logs", "2024")
# exist_ok=True：目录存在时不报错，不存在则创建
os.makedirs(multi_dir, exist_ok=True)
print(f"多级目录已创建: {multi_dir}")
```

#### 删除目录和文件

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 删除单级空目录
empty_dir = os.path.join(BASE_DIR, "temp")
os.mkdir(empty_dir, exist_ok=True)
os.rmdir(empty_dir)  # 只能删除空目录
print("单级空目录已删除")

# 删除多级空目录
os.makedirs(os.path.join(BASE_DIR, "a", "b", "c"), exist_ok=True)
os.removedirs(os.path.join(BASE_DIR, "a", "b", "c"))
print("多级空目录已删除")

# 删除文件
file_path = os.path.join(BASE_DIR, "temp.txt")
# os.remove(file_path)
# print("文件已删除")
```

#### 重命名

```python
import os

# 重命名文件或目录
old_name = os.path.join(BASE_DIR, "old_config.ini")
new_name = os.path.join(BASE_DIR, "new_config.ini")

# os.rename(old_name, new_name)
# print(f"已重命名: {old_name} -> {new_name}")
```

#### 列出目录内容

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 列出当前目录下的所有文件和子目录名
contents = os.listdir(BASE_DIR)
print(f"目录内容: {contents}")

# 分类列出文件和目录
files = [f for f in contents if os.path.isfile(os.path.join(BASE_DIR, f))]
dirs  = [d for d in contents if os.path.isdir(os.path.join(BASE_DIR, d))]
print(f"文件: {files}")
print(f"目录: {dirs}")
```

#### 工作目录操作

```python
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")

# 切换工作目录
parent_dir = os.path.dirname(current_dir)
os.chdir(parent_dir)
print(f"切换后的工作目录: {os.getcwd()}")

# 切回原目录
os.chdir(current_dir)
```

#### 执行系统命令

```python
import os

# 方式一：os.system() -- 在控制台直接显示输出
# os.system("dir")   # Windows
# os.system("ls")    # Mac/Linux

# 方式二：os.popen() -- 获取命令执行结果
# result = os.popen("ls").read()
# print(result)
```

### 2.3 系统信息获取

```python
import os

# 获取操作系统类型标识
print(f"操作系统: {os.name}")
# posix: Mac/Linux
# nt: Windows

# 获取所有环境变量
env_vars = os.environ
print(f"PATH: {env_vars.get('PATH', 'N/A')}")

# 获取特定环境变量
home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
print(f"用户主目录: {home}")

# 系统路径分隔符（用于 PATH 等环境变量）
print(f"路径列表分隔符: {os.pathsep}")
# Windows: ;
# Mac/Linux: :
```

### 2.4 os 模块综合案例

```python
import os
import datetime


def scan_directory(directory_path, indent=0):
    """递归扫描目录并以树形结构打印"""
    if not os.path.exists(directory_path):
        print("目录不存在")
        return

    prefix = "  " * indent

    # 列出目录内容
    try:
        items = sorted(os.listdir(directory_path))
    except PermissionError:
        print(f"{prefix}[权限不足]")
        return

    for item in items:
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            print(f"{prefix}[目录] {item}/")
            scan_directory(item_path, indent + 1)
        else:
            size = os.path.getsize(item_path)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
            print(f"{prefix}[文件] {item} ({size} 字节, {mtime.strftime('%Y-%m-%d %H:%M')})")


# 使用示例
# scan_directory("./project")
```

---

## 三、sys 模块 -- 系统参数与解释器

`sys` 模块为 Python 程序提供了与解释器进行交互的功能，最常用的是命令行参数获取和模块搜索路径管理。

### 3.1 命令行参数 sys.argv

```python
import sys

# sys.argv 是一个列表，包含执行脚本时传递的命令行参数
# sys.argv[0] 是脚本本身的名称
# sys.argv[1:] 是传递的参数

print(f"脚本名: {sys.argv[0]}")
print(f"参数数量: {len(sys.argv) - 1}")
print(f"所有参数: {sys.argv}")


# 案例：实现一个简单的命令行计算器
def cli_calculator():
    if len(sys.argv) != 4:
        print("用法: python calc.py <数字1> <运算符> <数字2>")
        print("示例: python calc.py 10 + 5")
        return

    _, num1_str, operator, num2_str = sys.argv

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                print("错误: 除数不能为零")
                return
            result = num1 / num2
        else:
            print(f"不支持的运算符: {operator}")
            return

        print(f"{num1} {operator} {num2} = {result}")

    except ValueError:
        print("错误: 请输入有效的数字")


# 直接运行脚本时执行
# if __name__ == "__main__":
#     cli_calculator()
# 运行: python calc.py 10 + 5
```

### 3.2 模块搜索路径 sys.path

```python
import sys

# sys.path 是 Python 导入模块时的搜索路径列表
# Python 会按顺序在这些路径中查找要导入的模块
print("模块搜索路径:")
for i, path in enumerate(sys.path):
    print(f"  [{i}] {path}")

# 动态添加搜索路径
sys.path.append("/path/to/your/modules")
sys.path.insert(0, "/path/to/priority/modules")  # 插入到最前面，优先搜索

# 示例：添加当前脚本的父目录到搜索路径
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
```

### 3.3 其他常用 sys 属性和方法

```python
import sys

# 获取 Python 解释器版本
print(f"Python 版本: {sys.version}")
print(f"版本信息元组: {sys.version_info}")

# 获取操作系统平台
print(f"平台: {sys.platform}")
# win32 / darwin / linux

# 获取递归深度限制
print(f"递归深度限制: {sys.getrecursionlimit()}")

# 设置递归深度限制
# sys.setrecursionlimit(2000)

# 获取对象引用计数
x = [1, 2, 3]
print(f"引用计数: {sys.getrefcount(x)}")  # getrefcount 本身也会增加一次引用

# 获取当前平台上整数和字符串的最大值
print(f"整数最大位数: {sys.maxsize}")

# 输出到标准错误流
sys.stderr.write("这是一条错误信息\n")

# 程序退出
# sys.exit(0)  # 正常退出
# sys.exit(1)  # 异常退出
```

### 3.4 sys 模块综合案例

```python
import sys
import os


def create_project_from_cli():
    """根据命令行参数创建项目结构"""
    if len(sys.argv) < 2:
        print("用法: python create_project.py <项目名称> [--with-tests]")
        print("示例: python create_project.py my_app --with-tests")
        sys.exit(1)

    project_name = sys.argv[1]
    include_tests = "--with-tests" in sys.argv

    # 项目目录结构
    dirs = [
        project_name,
        os.path.join(project_name, "src"),
        os.path.join(project_name, "docs"),
        os.path.join(project_name, "data"),
    ]

    if include_tests:
        dirs.append(os.path.join(project_name, "tests"))

    # 创建目录
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"已创建: {d}/")

    # 创建基础文件
    readme = os.path.join(project_name, "README.md")
    with open(readme, "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\n项目说明文档\n")

    main_py = os.path.join(project_name, "src", "main.py")
    with open(main_py, "w", encoding="utf-8") as f:
        f.write('if __name__ == "__main__":\n    print("Hello")\n')

    print(f"\n项目 {project_name} 创建完成!")


# if __name__ == "__main__":
#     create_project_from_cli()
```

---

## 四、json 模块 -- JSON 数据格式

### 4.1 什么是序列化和反序列化

- **序列化**：将 Python 对象（字典、列表等）转换为 JSON 字符串的过程
- **反序列化**：将 JSON 字符串转换为 Python 对象的过程

为什么要序列化？因为不同编程语言之间交换数据需要一个通用的数据格式，JSON（JavaScript Object Notation）正是这种跨语言的通用格式。

### 4.2 序列化与反序列化：Python 对象层面

```python
import json

# 准备一个 Python 字典
user_data = {
    "dream": {
        "username": "dream",
        "password": "521",
        "age": 18,
        "gender": True,
        "hobby": ["music", "rap", "basketball"]
    }
}

# 序列化：Python 对象 -> JSON 字符串
user_json_str = json.dumps(obj=user_data)
print(user_json_str, type(user_json_str))
# 输出: {"dream": {"username": "dream", ...}} <class 'str'>

# 反序列化：JSON 字符串 -> Python 对象
# 如果数据是二进制格式，先转换为字符串再反序列化
user_json_bytes = user_json_str.encode()
user_dict = json.loads(s=user_json_bytes)
print(user_dict, type(user_dict))
# <class 'dict'>
```

### 4.3 序列化与反序列化：文件层面

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

# 序列化并写入 JSON 文件
with open("user_data.json", "w", encoding="utf-8") as fp:
    json.dump(fp=fp, obj=user_data)

# 从 JSON 文件读取并反序列化
with open("user_data.json", "r", encoding="utf-8") as fp:
    data = json.load(fp=fp)

print(data, type(data))  # <class 'dict'>
```

### 4.4 Python 与 JSON 类型对应关系

| Python | JSON |
|--------|------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True | true |
| False | false |
| None | null |

```python
import json

# Python 元组序列化后变为 JSON 数组（反序列化回来是列表，不是元组）
data_tuple = ("music", "rap", "basketball")
json_str = json.dumps(data_tuple)
print(json_str)  # ["music", "rap", "basketball"]
print(json.loads(json_str))  # ['music', 'rap', 'basketball']

# None 和布尔值的转换
data = {"is_admin": True, "avatar": None}
json_str = json.dumps(data)
print(json_str)  # {"is_admin": true, "avatar": null}
```

### 4.5 json.dump / dumps 常用参数

```python
import json

user_data = {
    "name": "痴梦",
    "age": 18,
    "hobby": ["music", "rap", "basketball"]
}

# ensure_ascii=False : 不将中文转义为 Unicode，直接输出中文字符
# indent=4 : 格式化缩进，生成易读的 JSON（pretty-printed json）
with open("user_data.json", "w", encoding="utf-8") as fp:
    json.dump(
        obj=user_data,
        fp=fp,
        ensure_ascii=False,  # 保留中文而不是转为 \uXXXX
        indent=4,            # 缩进4个空格，格式化输出
        sort_keys=True,      # 按键名排序
    )

# 写入后的 JSON 文件内容示例:
# {
#     "age": 18,
#     "hobby": [
#         "music",
#         "rap",
#         "basketball"
#     ],
#     "name": "痴梦"
# }

# separators 参数用于压缩 JSON 输出
compact_json = json.dumps(user_data, ensure_ascii=False, separators=(",", ":"))
print(compact_json)
# {"name":"痴梦","age":18,"hobby":["music","rap","basketball"]}
```

参数说明：
- `ensure_ascii=True`（默认）：中文等非 ASCII 字符会被转义为 Unicode；设为 `False` 则保留原字符
- `indent=None`：不格式化；`indent=4` 则表示缩进 4 个空格
- `sort_keys=False`：不改键顺序；`True` 则按字母序排列键
- `separators=(', ', ': ')`（默认）；改为 `(',', ':')` 可生成最紧凑的输出

### 4.6 json 模块综合案例

```python
import json
import os


class UserManager:
    """基于 JSON 文件的用户管理系统"""

    def __init__(self, data_file="users.json"):
        self.data_file = data_file
        self.users = {}
        self._load()

    def _load(self):
        """从 JSON 文件加载用户数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as fp:
                    self.users = json.load(fp)
                print(f"已加载 {len(self.users)} 个用户")
            except json.JSONDecodeError:
                print("JSON 文件格式错误，初始化为空")
                self.users = {}
        else:
            print("用户数据文件不存在，初始化为空")

    def _save(self):
        """保存用户数据到 JSON 文件"""
        with open(self.data_file, "w", encoding="utf-8") as fp:
            json.dump(self.users, fp, ensure_ascii=False, indent=4)

    def register(self, username, password, **extra_info):
        """注册新用户"""
        if username in self.users:
            return False, f"用户名 {username} 已存在"

        self.users[username] = {
            "username": username,
            "password": password,
            **extra_info
        }
        self._save()
        return True, f"用户 {username} 注册成功"

    def login(self, username, password):
        """用户登录"""
        user = self.users.get(username)
        if user is None:
            return False, "用户不存在"
        if user["password"] != password:
            return False, "密码错误"
        return True, f"欢迎回来, {username}"

    def list_users(self):
        """列出所有用户"""
        return [
            {"username": u["username"], "age": u.get("age", "N/A")}
            for u in self.users.values()
        ]


# 使用示例
# um = UserManager("app_users.json")
# um.register("dream", "abc123", age=18, gender="male")
# um.register("hope", "pass456", age=20, gender="female")
# success, msg = um.login("dream", "abc123")
# print(msg)
# print(um.list_users())
```

---

## 五、pickle 模块 -- Python 对象序列化

### 5.1 pickle 与 json 的区别

| 特性 | json | pickle |
|------|------|--------|
| 数据格式 | 文本（JSON 字符串） | 二进制 |
| 跨语言 | 是（通用格式） | 否（仅 Python） |
| 支持类型 | 基本数据类型 | Python 所有对象（包括函数、类） |
| 可读性 | 人类可读 | 不可读（二进制） |
| 安全性 | 相对安全 | 有安全隐患（反序列化可能执行恶意代码） |

### 5.2 pickle 基本用法

```python
import pickle

# 处理 Python 对象层面
user_data = {"username": "dream", "age": 18, "hobby": ["music", "rap"]}

# 序列化：Python 对象 -> 二进制数据
user_bytes = pickle.dumps(obj=user_data)
print(user_bytes)
# b'\x80\x04\x95...'  (二进制数据)

# 反序列化：二进制数据 -> Python 对象
user_dict = pickle.loads(user_bytes)
print(user_dict, type(user_dict))
# {'username': 'dream', 'age': 18, 'hobby': ['music', 'rap']} <class 'dict'>
```

### 5.3 pickle 文件操作

```python
import pickle

user_data = {"username": "dream", "age": 18}

# 序列化并写入文件（二进制模式）
with open("user_data.pkl", "wb") as fp:
    pickle.dump(user_data, fp)

# 从文件读取并反序列化
with open("user_data.pkl", "rb") as fp:
    data = pickle.load(fp)

print(data)  # {'username': 'dream', 'age': 18}
```

### 5.4 pickle 序列化函数和类

这是 pickle 相比 json 最显著的优势 --- 可以序列化 Python 特有的对象。

```python
import pickle

# 序列化函数
def add(x, y):
    return x + y

# 将函数序列化为二进制
func_bytes = pickle.dumps(add)
print(func_bytes, type(func_bytes))
# <class 'bytes'>

# 反序列化得到函数对象
loaded_func = pickle.loads(func_bytes)
print(loaded_func, type(loaded_func))
# <function add at 0x...> <class 'function'>
print(loaded_func(3, 7))  # 10

# 序列化并保存到文件
with open("func.pkl", "wb") as fp:
    pickle.dump(add, fp)

with open("func.pkl", "rb") as fp:
    func_from_file = pickle.load(fp)
print(func_from_file(10, 5))  # 15
```

### 5.5 pickle 实际应用场景

```python
import pickle

# 场景：将函数字典持久化存储，实现简单的插件系统
def login():
    return "执行登录功能"

def register():
    return "执行注册功能"

def logout():
    return "执行退出功能"

# 功能表（键 -> 函数）
func_map = {
    "1": login,
    "2": register,
    "3": logout,
}

# 保存功能表到文件
with open("func_map.pkl", "wb") as fp:
    pickle.dump(func_map, fp)

# 之后可以重新加载功能表
with open("func_map.pkl", "rb") as fp:
    loaded_map = pickle.load(fp)

# 模拟调用
action = "2"
result = loaded_map[action]()
print(result)  # 执行注册功能
```

**安全提示**：由于 pickle 在反序列化时会执行任意代码，**不要从不受信任的来源加载 pickle 数据**。

---

## 六、time 与 datetime 模块 -- 时间处理

### 6.1 time 模块

#### 时间表现形式

Python 中有三种时间表示方式：
1. **时间戳（timestamp）**：从 1970年1月1日 00:00:00 UTC 到现在的秒数（浮点数）
2. **时间元组（struct_time）**：包含 9 个元素的命名元组
3. **格式化时间字符串**：人类可读的格式

#### 获取时间戳

```python
import time

# 获取当前时间戳
timestamp = time.time()
print(f"当前时间戳: {timestamp}")
# 1722560884.2367811
```

#### 时间戳与时间元组的转换

```python
import time

ts = time.time()

# 时间戳 -> 时间元组（本地时间）
local_time = time.localtime(ts)
print(f"本地时间元组: {local_time}")
# time.struct_time(tm_year=2024, tm_mon=8, tm_mday=2, tm_hour=9, tm_min=11, tm_sec=26, ...)

# 时间戳 -> 时间元组（UTC 国际标准时间）
utc_time = time.gmtime(ts)
print(f"UTC时间元组: {utc_time}")

# 时间元组 -> 时间戳
back_to_ts = time.mktime(local_time)
print(f"还原时间戳: {back_to_ts}")
```

时间元组（struct_time）的 9 个字段：

| 索引 | 属性 | 说明 | 取值范围 |
|------|------|------|----------|
| 0 | tm_year | 年份 | 如 2024 |
| 1 | tm_mon | 月份 | 1-12 |
| 2 | tm_mday | 日 | 1-31 |
| 3 | tm_hour | 小时 | 0-23 |
| 4 | tm_min | 分钟 | 0-59 |
| 5 | tm_sec | 秒 | 0-61（闰秒） |
| 6 | tm_wday | 星期几 | 0-6（周一为0） |
| 7 | tm_yday | 一年第几天 | 1-366 |
| 8 | tm_isdst | 夏令时标志 | -1/0/1 |

#### 格式化时间输出

```python
import time

# strftime：将时间元组格式化为字符串
formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"格式化时间: {formatted}")
# 2024-08-02 09:16:44

# 常用格式化符号:
# %Y : 四位年份 (2024)
# %m : 月份 (01-12)
# %d : 日 (01-31)
# %H : 小时 (00-23)
# %M : 分钟 (00-59)
# %S : 秒 (00-59)
# %a : 本地简化星期名 (Mon)
# %A : 本地完整星期名 (Monday)
# %b : 本地简化月份名 (Aug)
# %B : 本地完整月份名 (August)
# %c : 本地日期和时间格式
# %I : 12小时制小时 (01-12)
# %p : 上下午标志 (AM/PM)
# %w : 星期 (0-6，周日为0)
```

#### 字符串解析为时间

```python
import time

# strptime：将格式化字符串解析为时间元组
time_str = "2024-08-02 09:16:44"
time_struct = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
print(f"解析结果: {time_struct}")
# time.struct_time(tm_year=2024, tm_mon=8, tm_mday=2, tm_hour=9, ...)

# 转换为时间戳
time_ts = time.mktime(time_struct)
print(f"对应时间戳: {time_ts}")
```

#### 标准时间格式

```python
import time

# asctime：时间元组 -> 标准格式字符串
print(time.asctime(time.localtime()))
# Fri Aug  2 09:53:47 2024

# ctime：时间戳 -> 标准格式字符串
print(time.ctime(time.time()))
# Fri Aug  2 09:54:30 2024
```

#### 时间格式转换关系

```
时间戳 <---mktime/gmtime/localtime---> 时间元组 <---strftime/strptime---> 格式化字符串
```

### 6.2 datetime 模块

datetime 模块提供了更友好、更面向对象的时间日期操作方式。

#### 获取当前日期时间

```python
import datetime

# 获取当前日期（只含年月日）
today_date = datetime.date.today()
print(f"今天日期: {today_date}")  # 2024-08-02

# 获取当前日期时间（含时分秒微秒）
now = datetime.datetime.today()
print(f"当前时间: {now}")  # 2024-08-02 10:05:33.584242

# 也可以使用 now() 方法
now2 = datetime.datetime.now()
print(f"当前时间(now): {now2}")
```

#### 访问日期时间各属性

```python
import datetime

now = datetime.datetime.now()

print(f"年: {now.year}")        # 2024
print(f"月: {now.month}")       # 8
print(f"日: {now.day}")         # 2
print(f"时: {now.hour}")        # 10
print(f"分: {now.minute}")      # 5
print(f"秒: {now.second}")      # 56
print(f"微秒: {now.microsecond}") # 123456
print(f"星期几: {now.weekday()}") # 0-6 (周一为0)
```

#### 创建指定日期时间

```python
import datetime

# 创建指定日期
d = datetime.date(2024, 8, 2)
print(d)  # 2024-08-02

# 创建指定日期时间
dt = datetime.datetime(2024, 8, 2, 14, 30, 0)
print(dt)  # 2024-08-02 14:30:00
```

#### 时间日期的增减：timedelta

```python
import datetime

# timedelta 表示两个日期时间的差值
# 参数: days, seconds, microseconds, milliseconds, minutes, hours, weeks

# 创建一个时间增减量（7天）
one_week = datetime.timedelta(days=7)

# 当前时间
now = datetime.datetime.today()
print(f"现在: {now}")

# 一周后
next_week = now + one_week
print(f"一周后: {next_week}")

# 一周前
last_week = now - one_week
print(f"一周前: {last_week}")

# 组合使用
ten_days_3_hours = datetime.timedelta(days=10, hours=3)
future = now + ten_days_3_hours
print(f"10天3小时后: {future}")

# 计算两个日期之间的差值
diff = next_week - now
print(f"时间差: {diff}")          # 7 days, 0:00:00
print(f"相差天数: {diff.days}")   # 7
print(f"相差秒数: {diff.total_seconds()}")  # 604800.0
```

#### 日期格式化和解析

```python
import datetime

now = datetime.datetime.now()

# 格式化为字符串
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化: {formatted}")

# 从字符串解析
date_str = "2024-08-02 14:30:00"
parsed = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(f"解析: {parsed}")
```

### 6.3 时间模块综合案例

```python
import time
import datetime


def calculate_age(birth_str):
    """根据生日字符串计算年龄和距离下次生日的天数"""
    birth_date = datetime.datetime.strptime(birth_str, "%Y-%m-%d").date()
    today = datetime.date.today()

    # 计算年龄
    age = today.year - birth_date.year
    # 如果今年生日还没过，年龄减一
    if today.month < birth_date.month or \
       (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1

    # 计算距离下次生日的天数
    next_birthday = datetime.date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = datetime.date(today.year + 1, birth_date.month, birth_date.day)
    days_to_next = (next_birthday - today).days

    return age, days_to_next


# 测试
age, days = calculate_age("2000-06-15")
print(f"年龄: {age} 岁")
print(f"距下次生日: {days} 天")


def timer_decorator(func):
    """计算函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[耗时] {func.__name__}: {end - start:.4f} 秒")
        return result
    return wrapper


@timer_decorator
def slow_function():
    """模拟耗时操作"""
    total = 0
    for i in range(10_000_000):
        total += i
    return total


# slow_function()
```

---

## 七、random 模块 -- 随机数生成

### 7.1 基本随机方法

```python
import random

# 生成 [0.0, 1.0) 之间的随机浮点数
print(f"random(): {random.random()}")

# 生成指定区间的随机浮点数 [a, b]
print(f"uniform(5, 10): {random.uniform(5, 10)}")

# 生成指定区间的随机整数 [a, b]（包含两端）
print(f"randint(1, 10): {random.randint(1, 10)}")

# 生成指定区间内指定步长的随机数 [start, stop)
# 类似 range(start, stop, step)，从中随机取一个
print(f"randrange(1, 10, 2): {random.randrange(1, 10, 2)}")  # 1,3,5,7,9 中随机取
```

### 7.2 序列随机操作

```python
import random

name_list = ["张三", "李四", "王五", "赵六", "孙七", "周八"]

# 从序列中随机选取一个元素
print(f"choice: {random.choice(name_list)}")

# 从序列中随机选取指定数量的元素（不重复）
print(f"sample(3): {random.sample(name_list, 3)}")

# 从序列中随机选取指定数量的元素（可能重复，Python 3.6+）
print(f"choices(k=4): {random.choices(name_list, k=4)}")

# 对序列进行原地乱序（打乱）
print(f"打乱前: {name_list}")
random.shuffle(name_list)
print(f"打乱后: {name_list}")
```

### 7.3 生成随机验证码

```python
import random


def generate_captcha(length=6):
    """生成指定长度的随机验证码（包含大小写字母和数字）"""
    code = ""
    for _ in range(length):
        # 每次随机选择一种类型
        char_type = random.randint(1, 3)
        if char_type == 1:
            # 大写字母 A-Z (ASCII: 65-90)
            code += chr(random.randint(65, 90))
        elif char_type == 2:
            # 小写字母 a-z (ASCII: 97-122)
            code += chr(random.randint(97, 122))
        else:
            # 数字 0-9
            code += str(random.randint(0, 9))

    return code


def generate_captcha_v2(length=6):
    """更简洁的验证码生成方式：从字符池中随机选取"""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(chars, k=length))


# 测试
print(f"验证码: {generate_captcha(6)}")
print(f"验证码v2: {generate_captcha_v2(4)}")

# 批量生成不重复的验证码
codes = set()
while len(codes) < 10:
    codes.add(generate_captcha_v2(6))
for i, code in enumerate(codes, 1):
    print(f"  [{i}] {code}")
```

### 7.4 random 模块综合案例

```python
import random


class DiceGame:
    """简单的骰子游戏"""

    @staticmethod
    def roll(num_dice=1, num_sides=6):
        """掷骰子，返回每次的结果和总和"""
        results = [random.randint(1, num_sides) for _ in range(num_dice)]
        return results, sum(results)

    @staticmethod
    def roll_with_probability():
        """带概率的随机：模拟游戏抽卡"""
        # SSR: 1%, SR: 10%, R: 30%, N: 59%
        pool = (
            ["SSR"] * 1 +
            ["SR"]  * 10 +
            ["R"]   * 30 +
            ["N"]   * 59
        )
        return random.choice(pool)


# 测试掷骰子
results, total = DiceGame.roll(3, 6)
print(f"3个骰子结果: {results}, 总和: {total}")

# 测试抽卡概率（模拟10000次）
from collections import Counter
draws = [DiceGame.roll_with_probability() for _ in range(10000)]
counter = Counter(draws)
for rarity, count in counter.most_common():
    print(f"  {rarity}: {count}次 ({count/100:.1f}%)")
```

---

## 八、hashlib 模块 -- 摘要算法

### 8.1 什么是摘要算法

摘要算法（又称哈希算法、散列算法）是一种单向函数：
- **输入**：任意长度的数据
- **输出**：固定长度的哈希值（通常表示为 16 进制字符串）
- **特点**：不可逆（无法从哈希值反推原始数据）

常见的摘要算法有 MD5、SHA1、SHA256 等。

### 8.2 MD5 加密

```python
import hashlib

# 基本 MD5 加密流程
data = "hello world"

# 1. 生成 MD5 对象
md5 = hashlib.md5()

# 2. 将原始数据转换为二进制
data_bytes = data.encode()

# 3. 对数据进行摘要加密
md5.update(data_bytes)

# 4. 获取加密结果（32位16进制字符串）
encrypted = md5.hexdigest()
print(f"MD5加密: {encrypted}")
# 5eb63bbbe01eeed093cb22bb8f5acdc3

# 也可以获取二进制形式的加密串
binary_result = md5.digest()
print(f"二进制结果: {binary_result}")
```

### 8.3 SHA 系列加密

```python
import hashlib

data = "hello world".encode()

# SHA1（40位16进制）
sha1 = hashlib.sha1(data)
print(f"SHA1: {sha1.hexdigest()}")

# SHA256（64位16进制）
sha256 = hashlib.sha256(data)
print(f"SHA256: {sha256.hexdigest()}")

# SHA512（128位16进制）
sha512 = hashlib.sha512(data)
print(f"SHA512: {sha512.hexdigest()}")
```

### 8.4 加盐加密

由于 MD5 是确定性的（相同输入总是产生相同输出），简单的密码（如 "123456"）可以通过"彩虹表"反向查询出来。为了提高安全性，需要**加盐**。

```python
import hashlib


def hash_password(password, salt):
    """加盐哈希密码"""
    # 将原始密码与盐拼接
    data = (password + str(salt)).encode()
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


# 使用随机盐
import random
import string

salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

password = "123456"
hashed = hash_password(password, salt)
print(f"原始密码: {password}")
print(f"盐值: {salt}")
print(f"加密结果: {hashed}")

# 验证密码
def verify_password(input_password, stored_hash, stored_salt):
    """验证密码是否正确"""
    return hash_password(input_password, stored_salt) == stored_hash


print(f"正确密码验证: {verify_password('123456', hashed, salt)}")
print(f"错误密码验证: {verify_password('654321', hashed, salt)}")
```

### 8.5 文件完整性校验

```python
import hashlib


def get_file_md5(file_path):
    """计算文件的 MD5 哈希值（用于校验文件完整性）"""
    md5 = hashlib.md5()
    with open(file_path, "rb") as fp:
        # 分块读取，避免大文件一次加载到内存
        while True:
            chunk = fp.read(8192)  # 每次读取 8KB
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()


# 比较两个文件是否完全相同
def compare_files(file1, file2):
    md5_1 = get_file_md5(file1)
    md5_2 = get_file_md5(file2)
    print(f"文件1 MD5: {md5_1}")
    print(f"文件2 MD5: {md5_2}")
    return md5_1 == md5_2


# print(f"文件是否相同: {compare_files('file1.txt', 'file2.txt')}")
```

### 8.6 摘要算法的应用场景

1. **密码存储**：数据库中不存明文密码，只存哈希值 + 盐
2. **数据签名**：验证数据来源的合法性（证书签名）
3. **文件完整性校验**：下载文件后比对 MD5/SHA 值，确保文件未被篡改
4. **去重判断**：相同内容产生相同的哈希值，可用于数据去重

**重要提示**：摘要算法不是加密算法。加密可以解密还原，摘要无法反向解密，只能通过撞库（尝试大量可能输入）来猜测原始数据。

---

## 九、logging 模块 -- 日志系统

### 9.1 日志级别

Python logging 模块定义了 5 个日志级别（严重程度递增）：

| 级别 | 数值 | 用途 |
|------|------|------|
| DEBUG | 10 | 详细的调试信息 |
| INFO | 20 | 确认程序按预期运行 |
| WARNING | 30 | 警告信息（程序仍正常运行） |
| ERROR | 40 | 错误信息（程序部分功能受损） |
| CRITICAL | 50 | 严重错误（程序可能崩溃） |

```python
import logging

# 默认日志级别是 WARNING（只输出 WARNING 及以上级别）
logging.debug("调试信息")
logging.info("一般信息")
logging.warning("警告信息")
logging.error("错误信息")
logging.critical("严重错误")
# 只有 WARNING、ERROR、CRITICAL 会输出
```

### 9.2 基础日志配置（basicConfig）

```python
import logging

# 配置日志格式和级别
logging.basicConfig(
    level=logging.DEBUG,                          # 设置最低输出级别
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',                 # 时间格式
)

logging.debug("这是一条调试信息")
logging.info("程序启动成功")
logging.warning("配置文件未找到，使用默认配置")
logging.error("数据库连接失败")
# logging.critical("磁盘空间不足，程序退出")
```

### 9.3 日志输出到文件

```python
import logging

# 同时输出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # 输出到文件
        logging.StreamHandler(),                            # 输出到控制台
    ]
)

logging.info("日志将同时写入文件和控制台")
```

### 9.4 日志的高级配置（使用配置字典）

对于生产环境，推荐使用配置字典来更精细地控制日志行为。

```python
import logging
import logging.config
import os

# 日志配置字典
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(filename)s:%(lineno)d][%(levelname)s]%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s'
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
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,              # 保留5个备份
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 默认日志记录器
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# 应用配置
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# 使用
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

### 9.5 多模块日志实践

```python
import logging
import logging.config
import os


def setup_logger(name, log_file=None, level=logging.DEBUG):
    """创建一个命名的日志记录器"""
    # 创建日志目录
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    if log_file is None:
        log_file = os.path.join(log_dir, f"{name}.log")

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 以上

    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 在不同模块中使用
user_logger = setup_logger("user", "logs/user.log")
order_logger = setup_logger("order", "logs/order.log")

user_logger.info("用户模块初始化完成")
order_logger.info("订单模块初始化完成")
```

### 9.6 日志格式常用变量

| 变量 | 说明 |
|------|------|
| `%(asctime)s` | 时间戳 |
| `%(name)s` | 日志记录器名称 |
| `%(levelname)s` | 日志级别 |
| `%(filename)s` | 发出日志调用的源文件名 |
| `%(lineno)d` | 发出日志调用的源代码行号 |
| `%(funcName)s` | 发出日志调用的函数名 |
| `%(threadName)s` | 线程名称 |
| `%(thread)d` | 线程ID |
| `%(message)s` | 日志消息正文 |

---

## 十、re 模块 -- 正则表达式

### 10.1 正则表达式基本概念

正则表达式（Regular Expression）是一种文本模式匹配工具，用于在字符串中按照指定的规则查找、匹配、替换内容。re 模块是 Python 内置的正则表达式模块。

### 10.2 字符组（Character Class）

```python
import re

# 字符组 [ ] ：匹配方括号内的任意一个字符
text = "0123abcABC"

# [0-9] 匹配任意一个数字
print(re.findall("[0-9]", text))     # ['0', '1', '2', '3']

# [a-z] 匹配任意一个小写字母
print(re.findall("[a-z]", text))     # ['a', 'b', 'c']

# [A-Z] 匹配任意一个大写字母
print(re.findall("[A-Z]", text))     # ['A', 'B', 'C']

# [0-9a-zA-Z] 匹配任意数字或字母
print(re.findall("[0-9a-zA-Z]", text))
# ['0', '1', '2', '3', 'a', 'b', 'c', 'A', 'B', 'C']

# [^0-9] 匹配非数字的字符
print(re.findall("[^0-9]", text))
# ['a', 'b', 'c', 'A', 'B', 'C']
```

### 10.3 元字符（Metacharacters）

| 元字符 | 说明 |
|--------|------|
| `.` | 匹配除换行符以外的任意字符 |
| `\d` | 匹配数字 [0-9] |
| `\D` | 匹配非数字 |
| `\w` | 匹配字母、数字、下划线 [a-zA-Z0-9_] |
| `\W` | 匹配非字母数字下划线 |
| `\s` | 匹配任意空白符（空格、制表符、换行符等） |
| `\S` | 匹配非空白符 |
| `\n` | 匹配换行符 |
| `\t` | 匹配制表符 |
| `^` | 匹配字符串的开头 |
| `$` | 匹配字符串的结尾 |
| `|` | 或（匹配左边或右边） |
| `()` | 分组，也用于提升优先级 |
| `[]` | 字符组 |
| `[^]` | 排除字符组 |

```python
import re

text = "Hello World 123 !@#"

# \d 匹配数字
print(re.findall(r"\d", text))  # ['1', '2', '3']

# \D 匹配非数字
print(re.findall(r"\D", text))  # 所有非数字字符

# \w 匹配字母数字下划线
print(re.findall(r"\w", text))  # ['H','e','l','l','o','W','o','r','l','d','1','2','3']

# \s 匹配空白符
print(re.findall(r"\s", text))  # [' ', ' ', ' ']

# ^ 匹配开头
print(re.findall(r"^H\w+", "Hello World"))   # ['Hello']

# $ 匹配结尾
print(re.findall(r"\w+$", "Hello World"))    # ['World']

# | 或
print(re.findall(r"Hello|Hi", "Hello World")) # ['Hello']
```

### 10.4 量词（Quantifiers）

量词用于指定前面的字符或表达式重复的次数。**默认是贪婪匹配**（尽可能多地匹配），可以在量词后加 `?` 变成非贪婪匹配。

| 量词 | 说明 |
|------|------|
| `*` | 重复 0 次或更多次 |
| `+` | 重复 1 次或更多次 |
| `?` | 重复 0 次或 1 次 |
| `{n}` | 恰好重复 n 次 |
| `{n,}` | 重复 n 次或更多次 |
| `{n,m}` | 重复 n 到 m 次 |

```python
import re

text = "122223"

# * : 0 次或多次
print(re.findall(r"1(2*)3", text))  # ['2222']

# + : 1 次或多次
print(re.findall(r"1(2+)3", text))  # ['2222']

# ? : 0 次或 1 次
print(re.findall(r"1(2?)3", text))  # []  (2出现了多次，?只匹配0或1次，所以不匹配)
# 匹配 "123" 的情况
print(re.findall(r"1(2?)3", "123"))  # ['2']

# {n} : 正好 n 次
print(re.findall(r"1(2{2})3", "1223"))  # ['22']

# {n,} : n 次或更多
print(re.findall(r"1(2{2,})3", text))  # ['2222']

# {n,m} : n 到 m 次
print(re.findall(r"1(2{2,4})3", text))  # ['2222']
```

#### 贪婪匹配 vs 非贪婪匹配

```python
import re

text = "李杰和李莲英和李二棍子"

# 贪婪匹配（默认）：尽可能多
print(re.findall(r"李.*", text))   # ['李杰和李莲英和李二棍子']
print(re.findall(r"李.+", text))   # ['李杰和李莲英和李二棍子']

# 非贪婪匹配：加 ? 尽可能少
print(re.findall(r"李.*?", text))  # ['李', '李', '李']
print(re.findall(r"李.+?", text))  # ['李杰', '李莲', '李二']
```

### 10.5 re 模块的常用方法

#### findall -- 查找所有匹配

```python
import re

text = "联系方式: dream@qq.com, hope@163.com, admin@gmail.com"

# 匹配所有邮箱
pattern = r"\w+@\w+.\w+"
emails = re.findall(pattern, text)
print(emails)
# ['dream@qq.com', 'hope@163.com', 'admin@gmail.com']
```

#### search -- 查找第一个匹配

```python
import re

text = "联系方式: dream@qq.com, hope@163.com"

# search 返回第一个匹配的 Match 对象
result = re.search(r"\w+@\w+.\w+", text)
if result:
    print(f"匹配内容: {result.group()}")   # dream@qq.com
    print(f"起始位置: {result.start()}")    # 6
    print(f"结束位置: {result.end()}")      # 18
    print(f"起止范围: {result.span()}")     # (6, 18)
else:
    print("未匹配到内容")
```

#### match -- 从开头匹配

```python
import re

# match 必须从字符串开头位置开始匹配
print(re.match(r"\d+", "123abc"))    # 匹配成功: <re.Match object>
print(re.match(r"\d+", "abc123"))    # 匹配失败: None

# match 成功时同样返回 Match 对象
result = re.match(r"(\d+)-(\d+)", "123-456")
if result:
    print(result.group())    # 123-456  (整体匹配)
    print(result.group(1))   # 123      (第一个分组)
    print(result.group(2))   # 456      (第二个分组)
    print(result.groups())   # ('123', '456')
```

#### split -- 按正则切割

```python
import re

text = "apple, banana; peach  orange"

# 按逗号、分号、空格切割
result = re.split(r"[,;\s]+", text)
print(result)  # ['apple', 'banana', 'peach', 'orange']

# 如果分组中包含了切割符，切割符也会保留在结果中
text2 = "dream1dream2dream3dream4"
print(re.split(r"(\d+)", text2))
# ['dream', '1', 'dream', '2', 'dream', '3', 'dream', '4', '']
```

#### sub / subn -- 替换

```python
import re

text = "联系方式: dream@qq.com, hope@163.com"

# sub: 替换所有匹配项
# sub(正则, 替换内容, 原始文本, 替换次数)
result = re.sub(r"\w+@", "****@", text)
print(result)  # 联系方式: ****@qq.com, ****@163.com

# 只替换前 1 次
result = re.sub(r"\w+@", "****@", text, count=1)
print(result)  # 联系方式: ****@qq.com, hope@163.com

# subn: 返回 (替换后的字符串, 替换次数)
result, count = re.subn(r"\w+@", "****@", text)
print(f"替换结果: {result}, 替换次数: {count}")
```

#### finditer -- 返回迭代器

```python
import re

text = "联系方式: dream@qq.com, hope@163.com, admin@gmail.com"
pattern = re.compile(r"\w+@(\w+).\w+")

# finditer 返回迭代器，适合大量匹配的场景
for match in re.finditer(pattern, text):
    print(f"邮箱: {match.group()}, 域名: {match.group(1)}")
```

#### compile -- 预编译正则表达式

```python
import re

# 对于需要多次使用的正则，先编译可以提高效率
phone_pattern = re.compile(r"^1[3456789]\d{9}$")

phones = ["13812345678", "12345678901", "15987654321", "abc"]

for phone in phones:
    if phone_pattern.match(phone):
        print(f"{phone} : 有效手机号")
    else:
        print(f"{phone} : 无效手机号")
```

### 10.6 模式修正符（Flags）

```python
import re

# re.I : 忽略大小写
text = "Hello HELLO hello"
print(re.findall(r"hello", text, re.I))
# ['Hello', 'HELLO', 'hello']

# re.S : 让 . 匹配包括换行符在内的所有字符
text = "第一行\n第二行"
print(re.findall(r".+", text))      # ['第一行', '第二行']
print(re.findall(r".+", text, re.S)) # ['第一行\n第二行']

# re.M : 多行模式，^ 和 $ 匹配每行的开头和结尾
text = "apple\nbanana\ncherry"
print(re.findall(r"^[a-z]+", text, re.M))
# ['apple', 'banana', 'cherry']

# 组合使用
print(re.findall(r"hello", text, re.I | re.S))
```

### 10.7 常用正则表达式模板

```python
import re

# 手机号：1开头 + 3-9任选一 + 9位数字
phone_pattern = r"^1[3456789]\d{9}$"

# 邮箱：用户名@域名.后缀
email_pattern = r"^\w+([-+.]\w+)*@\w+([-.]\w+)*.\w+([-.]\w+)*$"

# 身份证号（18位）
id_card_pattern = r"^\d{17}[\dXx]$"

# URL
url_pattern = r"^https?://([\w-]+.)+[\w-]+(/[\w-./?%&=]*)?$"

# 日期格式 YYYY-MM-DD
date_pattern = r"^\d{4}-\d{1,2}-\d{1,2}$"

# 密码（字母开头，6-18位，只能包含字母数字下划线）
password_pattern = r"^[a-zA-Z]\w{5,17}$"

# 强密码（必须包含大小写字母和数字，8-10位）
strong_password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$"


def validate_data(data, pattern, field_name):
    """通用数据校验函数"""
    if re.match(pattern, data):
        return True, f"{field_name} 格式正确"
    return False, f"{field_name} 格式不正确"


# 测试
test_phone = "13812345678"
valid, msg = validate_data(test_phone, phone_pattern, "手机号")
print(msg)
```

### 10.8 正则表达式综合案例

```python
import re


def extract_log_info(log_line):
    """从单行日志中提取关键信息"""
    # 假设日志格式: [2024-08-02 10:30:45] [ERROR] [模块名] 错误描述
    pattern = r"[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})] [(\w+)] [(\w+)] (.+)"
    match = re.match(pattern, log_line)
    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2),
            "module": match.group(3),
            "message": match.group(4),
        }
    return None


def parse_config_file(content):
    """解析简易配置文件（key = value 格式）"""
    config = {}
    pattern = r"^\s*(\w+)\s*=\s*(.+?)\s*(?:#.*)?$"
    for line in content.split("\n"):
        match = re.match(pattern, line)
        if match:
            config[match.group(1)] = match.group(2)
    return config


# 测试日志提取
# log = "[2024-08-02 10:30:45] [ERROR] [database] 连接超时: 无法连接到 192.168.1.1:3306"
# info = extract_log_info(log)
# print(info)

# 测试配置解析
# config_text = """
# host = 127.0.0.1
# port = 8080    # 服务器端口
# debug = true
# """
# config = parse_config_file(config_text)
# print(config)
```

---

## 十一、subprocess 模块 -- 系统命令与进程

### 11.1 subprocess 简介

`subprocess` 模块用于启动新进程、执行系统命令，并可以与子进程进行输入输出交互。它是 `os.system()` 和 `os.popen()` 的现代替代方案。

### 11.2 Popen -- 灵活的子进程管理

`Popen` 是 subprocess 最底层的接口，提供最大的灵活性。

```python
import subprocess

# 执行系统命令
# args: 要执行的命令
# shell=True: 通过 shell 执行命令
# stdout: 标准输出管道
# stderr: 标准错误管道

# macOS/Linux 示例
# response = subprocess.Popen(
#     "ls",
#     shell=True,
#     stdout=subprocess.PIPE,  # 捕获标准输出
#     stderr=subprocess.PIPE   # 捕获标准错误
# )
# print(response.stdout.read().decode('utf-8'))

# Windows 示例
response = subprocess.Popen(
    "dir",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
# Windows 默认使用 GBK 编码
# print(response.stdout.read().decode('gbk'))
```

```python
import subprocess

# 错误命令示例：执行不存在的命令
# response = subprocess.Popen(
#     "dirr",  # 错误的命令
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE
# )

# 读取标准输出和标准错误
# 注意：管道只能读取一次，读取后管道为空
# stdout_data = response.stdout.read()
# stderr_data = response.stderr.read()
# if stdout_data:
#     print("标准输出:", stdout_data.decode('gbk'))
# if stderr_data:
#     print("标准错误:", stderr_data.decode('gbk'))
```

### 11.3 run -- 推荐的高层接口

`subprocess.run()` 是 Python 3.5+ 推荐的命令执行方式，更简洁易用。

```python
import subprocess

# 基本用法
# result = subprocess.run(
#     ["python", "--version"],
#     capture_output=True,  # 同时捕获 stdout 和 stderr
#     text=True             # 以文本模式返回（而非字节）
# )
# print(f"返回码: {result.returncode}")
# print(f"输出: {result.stdout}")


def run_command(command_list, encoding="utf-8", timeout=30):
    """安全地执行命令并返回结果"""
    try:
        result = subprocess.run(
            command_list,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding=encoding,
            timeout=timeout
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, f"执行异常: {e}"


# 使用示例
# success, output = run_command(["echo", "Hello from subprocess"])
# if success:
#     print(f"成功: {output}")
# else:
#     print(f"失败: {output}")
```

### 11.4 call -- 直接输出到控制台

```python
import subprocess

# call 会将命令的输出直接打印到控制台
# subprocess.call(["echo", "Hello World"])
# subprocess.call(["python", "--version"])

# 也可以通过 pip 安装包（带确认交互时会阻塞）
# subprocess.call(["pip", "install", "requests"])
```

### 11.5 subprocess 综合案例

```python
import subprocess
import os


class SystemMonitor:
    """系统监控工具：调用系统命令获取系统信息"""

    @staticmethod
    def get_disk_usage():
        """获取磁盘使用情况"""
        result = subprocess.run(
            "df -h" if os.name == "posix" else "wmic logicaldisk get size,freespace,caption",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout

    @staticmethod
    def get_running_processes():
        """获取运行中的进程列表"""
        cmd = "ps aux" if os.name == "posix" else "tasklist"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    @staticmethod
    def ping_host(host, count=4):
        """ping 指定主机"""
        count_flag = "-c" if os.name == "posix" else "-n"
        result = subprocess.run(
            ["ping", count_flag, str(count), host],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # 提取平均延迟
            return True, result.stdout
        else:
            return False, f"无法连接到 {host}"

    @staticmethod
    def execute_python_script(script_path):
        """执行指定的 Python 脚本"""
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr


# 使用示例
# monitor = SystemMonitor()
# print(monitor.get_disk_usage())
# success, info = monitor.ping_host("www.baidu.com")
# print(f"Ping结果: {'成功' if success else '失败'}")
```

---

## 本章小结

| 模块 | 核心功能 | 关键方法 |
|------|----------|----------|
| os | 系统操作、文件路径 | path.join/exists/isdir, mkdir/makedirs, listdir/rename |
| sys | 解释器交互 | argv, path, exit, platform |
| json | JSON 序列化 | dumps/loads（对象）, dump/load（文件） |
| pickle | Python 对象序列化 | dumps/loads, dump/load（二进制） |
| time | 时间处理 | time/sleep, strftime/strptime, localtime/gmtime |
| datetime | 日期时间 | datetime.now(), timedelta, strftime/strptime |
| random | 随机数 | random(), randint(), choice(), shuffle() |
| hashlib | 摘要加密 | md5(), sha256(), update(), hexdigest() |
| logging | 日志记录 | basicConfig, getLogger, info/debug/error |
| re | 正则表达式 | findall, search, match, sub, split, compile |
| subprocess | 系统命令 | Popen, run, call |

**核心编程建议**：

1. **路径拼接始终使用 `os.path.join()`**，不要手动拼接字符串，以保证跨平台兼容
2. **配置数据存储使用 JSON**，它是跨语言的标准格式，人类可读
3. **密码绝不存储明文**，使用 hashlib + 随机盐进行摘要存储
4. **生产环境必须配置日志**，而不是使用 `print()` 进行调试
5. **正则表达式先编译再使用**，在需要多次匹配的场景中可以提高效率
6. **不要从不受信任的来源加载 pickle 数据**，存在安全风险







## 面试题



## 4 Python命名中的单下划线(_)和双下划线(__)

在Python中，双下划线开头和结尾的命名默认为Python的内部变量/方法，用以区分用户变量。例如场景的`__init__()`,`__dict__`,`__dir__`等。

单下划线开头的命名默认为私有变量，不会在`from a import *`中被导入

双下划线开头，但是没有下划线结尾的命名，Python在解释的时候会默认对其进行重命名为`_类名__变量`。

```python
class A():
    def __init__(self) -> None:
        self._b = "self._b"
        self.__c = "self.__c"
a = A()
print(a._b) # 输出：self._b
# print(a.__c) # 报错：AttributeError: 'A' object has no attribute '__c'
print(a.__dict__) # 输出：{'_b': 'self._b', '_A__c': 'self.__c'}
# 我们发现__c变量被自动重命名为_A__c了
print(a._A__c) # 输出：self.__c
```

在Python中，当一个文件夹下有一个`__init__.py`文件，则Python会识别这个文件夹为一个Python包


