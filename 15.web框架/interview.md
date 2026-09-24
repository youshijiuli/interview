### 7. Python Web 框架

一些知名的 Python Web 框架包括：
- Django: 全功能框架，强调快速开发和“可扩展性”。
- Flask: 轻量级框架，易于上手，适合小型项目或微服务。
- Pyramid: 灵活的框架，适合构建大型、复杂的应用。
- FastAPI: 现代、快速（高性能）的 Web 框架，用于构建 API。

### 8. 数据库数据写入文件

使用 Python 从数据库提取数据并写入文本文件，可以使用 `sqlite3` 或其他数据库适配器，结合 `csv` 模块。以下是一个使用 `sqlite3` 的示例：

```python
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 从 student 表中提取数据
cursor.execute("SELECT * FROM student")
rows = cursor.fetchall()

# 将数据写入 db.txt 文件
with open('db.txt', 'w') as file:
    for row in rows:
        file.write(','.join(map(str, row)) + '\n')

# 关闭连接
conn.close()
```

### 9. MVC开发模式

MVC（Model-View-Controller）模式是一种软件架构模式，用于将应用程序分为三个基本部分：
- **Model**: 管理应用程序的数据和业务逻辑。
- **View**: 负责展示数据（即模型层的数据）给用户。
- **Controller**: 接收用户的输入，调用模型和视图去完成用户的需求。

### 10. Left join 和 right join 的区别

- **Left join**: 返回左表（table1）的所有记录，即使右表（table2）中没有匹配的记录。
- **Right join**: 返回右表（table2）的所有记录，即使左表（table1）中没有匹配的记录。

### Python 代码实现

1. **MVC 示例代码**:
   - 这里提供一个简化的 MVC 示例，具体实现会根据项目需求有所不同。

```python
# Model
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# View
class UserView:
    def display_user(self, user):
        print(f"Name: {user.name}, Age: {user.age}")

# Controller
class UserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_user(self, name, age):
        user = self.model.User(name, age)
        self.view.display_user(user)
```

2. **斐波那契数列**:
   - 使用递归实现斐波那契数列。

```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 示例
print(fibonacci(10))  # 输出第10个斐波那契数
```

3. **Left join 和 right join 示例**:
   - 这里提供一个 SQL 示例，具体实现会根据使用的数据库系统有所不同。

```sql
-- 假设有两个表，table1 和 table2
-- Left join 示例
SELECT table1.*, table2.column2
FROM table1
LEFT JOIN table2 ON table1.id = table2.id;

-- Right join 示例
SELECT table1.*, table2.column2
FROM table1
RIGHT JOIN table2 ON table1.id = table2.id;
```

请注意，这些代码示例提供了解决问题的基本思路和实现。在实际应用中，可能需要根据具体需求进行调整和优化。
