# MySQL数据库从入门到精通

---

# 第一部分：数据库基础概念

## 1.1 存储数据的演变过程

在计算机发展过程中，数据存储方式经历了几个重要阶段：

1. **基于内存存储**：最早使用列表、字典等内存数据结构存储数据，程序关闭后数据丢失。
2. **基于文件存储**：将数据存储到文本文件中（如TXT文件），实现数据持久化。
3. **基于JSON文件存储**：以字典形式将数据序列化到JSON文件中，支持结构化存储。
4. **基于TCP网络存储**：通过客户端和服务端进行数据的传递，实现远程数据存取。
5. **并发+网络存储**：实现多用户同时操作服务端数据。

本质上，数据存储从单机走向了互联网模式。

## 1.2 数据库的本质

数据库本质上是一个**基于网络通信的应用程序**。服务端负责存储数据，客户端负责查询和操作数据。

## 1.3 关系型数据库 vs 非关系型数据库

### 1.3.1 关系型数据库（RDBMS）

- **代表产品**：MySQL、Oracle、SQL Server、DB2、SQLite、PostgreSQL
- **数据存储形式**：以**表结构**（Table）存储数据，类似Excel表格
- **特点**：
  - 表与表之间可以建立关联关系
  - 每个字段（列）会限制存储数据的格式和类型
  - 支持复杂的增删改查操作
  - 数据持久化存储在硬盘上，断电不丢失

### 1.3.2 非关系型数据库（NoSQL）

- **代表产品**：Redis、MongoDB、HBase、Memcached
- **数据存储形式**：通常以**键值对**（Key-Value）形式存储数据
- **特点**：
  - 通常基于内存工作，读取速度非常快
  - 服务重启后数据可能丢失
  - 不支持复杂的查询操作
  - 适合做缓存、临时数据存储

### 1.3.3 实际应用中的选择

关系型和非关系型数据库通常**结合使用**：

- 需要持久性存储的数据放在**关系型数据库**中（如用户信息、订单数据）
- 频繁访问的热数据放在**非关系型数据库**中（如缓存、会话数据）

### 1.3.4 数据库核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **库（Database）** | 数据库管理系统中存储数据的容器 | 文件夹 |
| **表（Table）** | 数据库中的基本组成单位，用于存储数据 | Excel文件 |
| **记录（Record）** | 表中的一行数据 | 文件中的一行 |
| **表头（Header）** | 表中的第一行，描述字段含义 | Excel的表头 |
| **字段（Field）** | 表中的列，定义数据类型和约束 | Excel中的列 |

---

# 第二部分：MySQL安装与配置

## 2.1 下载与安装

1. 访问MySQL官网，根据操作系统下载对应的安装包
2. 解压下载好的压缩包，放到指定目录
3. 配置环境变量，将MySQL的`bin`目录添加到系统PATH中

关键可执行文件：
- `mysql.exe`：TCP客户端
- `mysqld.exe`：TCP服务端

## 2.2 MySQL配置文件（my.ini）

在MySQL安装目录下创建`my.ini`文件（也可以是`my.cnf`），内容如下：

```ini
[mysqld]
# 设置3306端口
port=3306
# 设置MySQL的安装目录
basedir="C:\WinApps\MySQL"
# 设置MySQL数据库的数据存放目录
datadir="C:\WinApps\MySQL\data"
# 允许最大连接数
max_connections=200
# 允许连接失败的次数
max_connect_errors=10
# 服务端使用的字符集默认为utf8mb4
character-set-server=utf8mb4
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
# 默认使用mysql_native_password插件认证
default_authentication_plugin=mysql_native_password

[mysql]
# 设置MySQL客户端默认字符集
default-character-set=utf8mb4

[client]
# 设置MySQL客户端连接服务端时默认使用的端口
port=3306
# 设置MySQL客户端的默认字符集
default-character-set=utf8mb4
```

## 2.3 初始化与启动MySQL服务

```bash
# 1. 创建data目录（在MySQL安装目录下）
mkdir data

# 2. 初始化MySQL服务（会生成临时密码）
mysqld --initialize --console

# 3. 注册MySQL为系统服务
mysqld --install

# 4. 启动MySQL服务
net start mysql

# 5. 停止MySQL服务
net stop mysql

# 6. 移除MySQL系统服务
mysqld --remove
```

## 2.4 登录数据库与修改密码

```bash
# 登录数据库（需要输入初始化时生成的临时密码）
mysql -uroot -p

# 修改密码
ALTER USER 'root'@'localhost' IDENTIFIED BY '你的新密码';
FLUSH PRIVILEGES;
```

## 2.5 免密码登录配置

在`my.ini`文件的`[mysql]`节中添加：

```ini
[mysql]
user="root"
password="你的密码"
```

配置后直接输入`mysql`即可登录。

## 2.6 跳过授权表修改密码（忘记密码时使用）

```bash
# 1. 停止MySQL服务
net stop mysql

# 2. 跳过授权表启动（会阻塞）
mysqld --skip-grant-tables

# 3. 打开新窗口，直接回车登录
mysql -uroot -p
# 直接回车即可进入

# 4. 修改密码
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
FLUSH PRIVILEGES;
EXIT;
```

---

# 第三部分：SQL语句基础

## 3.1 SQL语句的由来

早期每个公司基于TCP开发自己的数据库系统，操作语句各不相同。后来业界约定俗成，使用一套通用的语句来操作关系型数据库，这就是**SQL（Structured Query Language，结构化查询语言）**的诞生。

- **SQL**：操作关系型数据库的通用语言
- **NoSQL**：操作非关系型数据库的通用语言

## 3.2 SQL语法规范

1. SQL语句**关键字不区分大小写**，但建议关键字大写，数据库名、表名、字段名小写
2. 如数据库名、表名、字段名与关键字同名，使用**反引号（`）**圈起来，避免冲突
3. SQL语句以**英文分号（;）**结尾
4. 字符串和日期类型的值用**单引号**括起来
5. 单词之间使用半角空格隔开
6. 关键词不能跨多行或简写

## 3.3 注释语法

```sql
-- 单行注释方式一

# 单行注释方式二

/*
多行注释
可以跨多行
*/
```

## 3.4 SQL语句分类

### 3.4.1 DDL（Data Definition Language，数据定义语言）

用于创建或删除数据库以及数据表的结构：

| 关键字 | 作用 |
|--------|------|
| `CREATE` | 创建数据库和表等对象 |
| `DROP` | 删除数据库和表等对象 |
| `ALTER` | 修改数据库和表等对象的结构 |
| `TRUNCATE` | 清空表数据，重置自增计数 |

### 3.4.2 DML（Data Manipulation Language，数据操纵语言）

用于对数据表中的数据进行增删改查：

| 关键字 | 作用 |
|--------|------|
| `SELECT` | 查询表中的数据 |
| `INSERT` | 向表中插入新数据 |
| `UPDATE` | 修改表中的数据 |
| `DELETE` | 删除表中的数据 |

### 3.4.3 DCL（Data Control Language，数据控制语言）

用于控制数据库的操作权限，包括用户权限及数据操作权限：

| 关键字 | 作用 |
|--------|------|
| `GRANT` | 赋予用户操作权限 |
| `REVOKE` | 取消用户的操作权限 |

### 3.4.4 TCL（Transaction Control Language，事务控制语言）

用于管理事务的提交与回滚：

| 关键字 | 作用 |
|--------|------|
| `BEGIN` / `START TRANSACTION` | 开启事务 |
| `COMMIT` | 提交事务，确认对数据库的变更 |
| `ROLLBACK` | 回滚事务，取消对数据库的变更 |
| `SAVEPOINT` | 设置事务保存点 |

> 注：早期教材有时将 `COMMIT`/`ROLLBACK` 归入 DCL，但按当前主流划分应单独属于 TCL。

### 3.4.5 DQL（Data Query Language，数据查询语言）

DQL是DML的一部分，专门用于数据查询，核心关键字是`SELECT`。包含子句：

- `FROM`：指定查询的表
- `WHERE`：过滤条件
- `GROUP BY`：分组
- `HAVING`：分组后过滤
- `ORDER BY`：排序
- `LIMIT`：限制结果数量

## 3.5 MySQL客户端常用命令

| 命令 | 描述 |
|------|------|
| `help` | 查看系统帮助 |
| `status` | 查看数据库管理系统的状态信息 |
| `exit` | 退出数据库终端连接 |
| `quit` | 退出数据库终端连接 |
| `\c` | 当打错命令想重新写时使用 |
| `\G` | 格式化输出（每条记录纵向显示） |

---

# 第四部分：数据库操作

## 4.1 创建数据库

```sql
-- 基本语法：创建数据库
CREATE DATABASE 数据库名字;

-- 如果数据库不存在则创建，否则忽略
CREATE DATABASE IF NOT EXISTS 数据库名字;

-- 创建数据库并指定默认编码格式（推荐utf8mb4）
CREATE DATABASE IF NOT EXISTS 数据库名字 CHARSET utf8mb4;
```

**示例：**

```sql
-- 创建一个名为day01的数据库
CREATE DATABASE IF NOT EXISTS day01;
-- Query OK, 1 row affected (0.00 sec)

-- 创建数据库并指定GBK编码
CREATE DATABASE IF NOT EXISTS day03 CHARSET 'gbk';
-- Query OK, 1 row affected (0.00 sec)
```

> **注意**：`utf8mb4`是真正的UTF-8编码，支持emoji表情等4字节字符，建议始终使用`utf8mb4`而非`latin1`（不支持中文）或`utf8`（MySQL中的`utf8`实际只支持3字节）。

## 4.2 查看数据库

```sql
-- 查看当前所有数据库
SHOW DATABASES;

-- 模糊查询数据库中带有指定字符的数据库名
SHOW DATABASES LIKE '%01%';

-- 查看指定数据库的创建SQL语句
SHOW CREATE DATABASE 数据库名字;
```

**示例：**

```sql
SHOW CREATE DATABASE day01;

-- 输出：
-- +----------+-------------------------------------------------------------------+
-- | Database | Create Database                                                   |
-- +----------+-------------------------------------------------------------------+
-- | day01    | CREATE DATABASE `day01` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
-- +----------+-------------------------------------------------------------------+
```

## 4.3 修改数据库

```sql
-- 修改数据库的默认编码集
ALTER DATABASE 数据库名字 CHARSET 'utf8mb4';
```

**示例：**

```sql
-- 将day03数据库的编码从gbk改为utf8mb4
ALTER DATABASE day03 CHARSET 'utf8mb4';
-- Query OK, 1 row affected (0.00 sec)
```

## 4.4 删除数据库

```sql
-- 删除指定数据库（如果存在则删除）
DROP DATABASE IF EXISTS 数据库名字;
```

> **严重警告**：使用`DROP DATABASE`命令时要非常谨慎！MySQL不会给出任何确认提示。删除数据库后，数据库中存储的所有数据表和数据将一同被删除且无法恢复。建议在删除前先备份。

## 4.5 切换/选择数据库

```sql
-- 切换到指定的数据库
USE 数据库名字;

-- 查看当前所在的数据库名字
SELECT DATABASE();
```

**示例：**

```sql
USE day01;
-- Database changed

SELECT DATABASE();
-- +------------+
-- | database() |
-- +------------+
-- | day01      |
-- +------------+
```

---

# 第五部分：数据表操作

## 5.1 创建数据表

```sql
-- 创建表的完整语法
CREATE TABLE [IF NOT EXISTS] 表名 (
    字段名1 数据类型[(宽度)] [约束条件] [COMMENT '注释'],
    字段名2 数据类型[(宽度)] [约束条件] [COMMENT '注释'],
    ...
    字段名n 数据类型[(宽度)] [约束条件] [COMMENT '注释'],
    PRIMARY KEY (一个或多个字段名)   -- 主键定义
) [ENGINE = 存储引擎] [CHARSET = 字符集];
```

**注意事项：**
- 创建表时，**字段名和字段类型是必须的**，宽度和约束条件是可选的
- 同一张表中字段名不能重复
- 多个字段之间用逗号（,）分隔，**最后一个字段后面不能加逗号**
- 约束条件可以写多个
- SQL语句只有遇到分号（;）才算一句完整语句

**示例：**

```sql
CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户编号',
    name VARCHAR(10) COMMENT '用户名',
    age INT COMMENT '年龄'
);
-- Query OK, 0 rows affected (0.02 sec)
```

## 5.2 查看数据表

```sql
-- 查看当前库下的所有表
SHOW TABLES;

-- 查看创建表的SQL语句
SHOW CREATE TABLE 表名;

-- 格式化输出建表语句（纵向显示）
SHOW CREATE TABLE 表名 \G;

-- 查看表结构
DESCRIBE 表名;
-- 简写
DESC 表名;
```

**示例：**

```sql
DESC user;
-- +-------+-------------+------+-----+---------+-------+
-- | Field | Type        | Null | Key | Default | Extra |
-- +-------+-------------+------+-----+---------+-------+
-- | name  | varchar(10) | YES  |     | NULL    |       |
-- | age   | int(4)      | YES  |     | NULL    |       |
-- +-------+-------------+------+-----+---------+-------+
```

字段说明：
- `Field`：字段名
- `Type`：字段类型
- `Null`：是否允许为空（YES/NO）
- `Key`：键类型（PRI主键/UNI唯一/MUL外键）
- `Default`：默认值
- `Extra`：额外信息（如auto_increment）

## 5.3 修改数据表（ALTER TABLE）

### 5.3.1 修改字段类型和名称

```sql
-- 只修改字段类型（不改名字）
ALTER TABLE 表名 MODIFY 字段名 字段类型(宽度) [约束条件];

-- 修改字段名和类型（可以同时改名字和类型）
ALTER TABLE 表名 CHANGE 原字段名 新字段名 字段类型(宽度) [约束条件];

-- 修改表名（重命名）
ALTER TABLE 原表名 RENAME 新表名;
```

### 5.3.2 添加字段

```sql
-- 默认在表末尾添加字段
ALTER TABLE 表名 ADD 字段名 字段类型 [约束条件];

-- 在指定字段之后添加字段
ALTER TABLE 表名 ADD 字段名 字段类型 [约束条件] AFTER 原字段名;

-- 在表开头添加字段
ALTER TABLE 表名 ADD 字段名 字段类型 [约束条件] FIRST;
```

### 5.3.3 删除字段

```sql
-- 删除指定字段
ALTER TABLE 表名 DROP 字段名;
```

### 5.3.4 修改主键自增起始值

```sql
ALTER TABLE 表名 AUTO_INCREMENT = 指定值;
```

**示例：**

```sql
-- 修改字段类型
ALTER TABLE user MODIFY name VARCHAR(255);

-- 重命名表
ALTER TABLE user RENAME new_user;

-- 在末尾添加字段
ALTER TABLE new_user ADD gender INT;

-- 在name字段后添加字段
ALTER TABLE new_user ADD addr VARCHAR(255) AFTER name;

-- 在开头添加字段
ALTER TABLE new_user ADD id INT FIRST;
```

## 5.4 删除数据表

```sql
-- 删除指定表（数据无法恢复！）
DROP TABLE 表名;

-- 安全的删除方式
DROP TABLE IF EXISTS 表名;

-- 清空表中所有数据（保留表结构，重置自增主键）
TRUNCATE TABLE 表名;
```

**TRUNCATE vs DELETE：**
- `TRUNCATE`：清空表数据，重置自增主键计数，DDL操作，不能回滚
- `DELETE FROM 表名`：逐行删除数据，不重置自增主键，DML操作，可以回滚

## 5.5 跨库操作表

```sql
-- 在未切换数据库的情况下操作其他库的表
CREATE TABLE 库名.表名(字段名 字段类型);
```

---

# 第六部分：数据操作（INSERT/UPDATE/DELETE/SELECT）

## 6.1 插入数据（INSERT）

```sql
-- 插入单条数据
INSERT [INTO] 表名 (字段名1, 字段名2, ...) VALUES (值1, 值2, ...);

-- 插入多条数据
INSERT INTO 表名 (字段名1, 字段名2, ...) VALUES
    (值1, 值2, ...),
    (值1, 值2, ...);

-- 如果不指定字段名，则按表的字段顺序插入所有字段值
INSERT INTO 表名 VALUES (值1, 值2, ...);
```

**示例：**

```sql
-- 创建测试表
CREATE TABLE t2 (
    name VARCHAR(25),
    age INT
);

-- 插入一条数据
INSERT INTO t2 (name, age) VALUES ('dream', 18);

-- 插入多条数据
INSERT INTO t2 (name, age) VALUES
    ('dream_one', 18),
    ('dream_two', 28);

-- 查看结果
SELECT * FROM t2;
-- +-----------+------+
-- | name      | age  |
-- +-----------+------+
-- | dream     |   18 |
-- | dream_one |   18 |
-- | dream_two |   28 |
-- +-----------+------+
```

## 6.2 查询数据（SELECT）

```sql
-- 查看表中所有字段的所有数据
SELECT * FROM 表名;

-- 查看指定字段的数据
SELECT 字段名1, 字段名2 FROM 表名;
```

**示例：**

```sql
-- 只查询name字段
SELECT name FROM t2;
-- +-----------+
-- | name      |
-- +-----------+
-- | dream     |
-- | dream_one |
-- | dream_two |
-- +-----------+
```

## 6.3 修改数据（UPDATE）

```sql
-- 修改满足条件的数据
UPDATE 表名 SET 字段名1 = 新值1, 字段名2 = 新值2 WHERE 筛选条件;
```

> **重要提示**：执行UPDATE语句时，**务必带上WHERE条件**，否则会修改表中所有数据！

**示例：**

```sql
-- 将姓名为dream_one的人的年龄改为38
UPDATE t2 SET age = 38 WHERE name = 'dream_one';
-- Query OK, 1 row affected (0.00 sec)

SELECT name, age FROM t2;
-- +-----------+------+
-- | name      | age  |
-- +-----------+------+
-- | dream     |   18 |
-- | dream_one |   38 |
-- | dream_two |   28 |
-- +-----------+------+
```

## 6.4 删除数据（DELETE）

```sql
-- 删除满足条件的数据
DELETE FROM 表名 WHERE 筛选条件;
```

> **重要提示**：执行DELETE语句时，**务必带上WHERE条件**，否则会删除表中所有数据！

**示例：**

```sql
-- 删除年龄为38岁的人
DELETE FROM t2 WHERE age = 38;
-- Query OK, 1 row affected (0.00 sec)

SELECT name, age FROM t2;
-- +-----------+------+
-- | name      | age  |
-- +-----------+------+
-- | dream     |   18 |
-- | dream_two |   28 |
-- +-----------+------+
```

---

# 第七部分：数据类型详解

## 7.1 创建表时的字段宽度说明

```sql
CREATE TABLE 表名 (
    字段名1 类型(宽度) 约束条件,
    字段名2 类型(宽度) 约束条件,
    字段名3 类型(宽度) 约束条件
);
```

- 宽度和约束条件是**可选的**
- 对于**整型**：宽度表示显示宽度，配合`zerofill`使用
- 对于**字符型**：宽度表示能存储的**字符个数**

## 7.2 整型

### 7.2.1 整型分类

| 整数类型 | 字节数 | 有符号范围 | 无符号范围 |
|----------|--------|------------|------------|
| TINYINT | 1 | -128 ~ 127 | 0 ~ 255 |
| SMALLINT | 2 | -32768 ~ 32767 | 0 ~ 65535 |
| MEDIUMINT | 3 | -8388608 ~ 8388607 | 0 ~ 16777215 |
| INT | 4 | -2147483648 ~ 2147483647 | 0 ~ 4294967295 |
| BIGINT | 8 | -2^63 ~ 2^63-1 | 0 ~ 2^64-1 |

### 7.2.2 有符号与无符号

```sql
-- 默认有符号 TINYINT
CREATE TABLE t2 (age TINYINT);

INSERT INTO t2 VALUES (-128);  -- 成功
INSERT INTO t2 VALUES (127);   -- 成功
INSERT INTO t2 VALUES (-129);  -- 错误：超出范围
INSERT INTO t2 VALUES (128);   -- 错误：超出范围

-- 无符号 TINYINT（使用UNSIGNED约束）
CREATE TABLE t3 (age TINYINT UNSIGNED);

INSERT INTO t3 VALUES (0);     -- 成功
INSERT INTO t3 VALUES (255);   -- 成功
INSERT INTO t3 VALUES (-1);    -- 错误：无符号不能为负
INSERT INTO t3 VALUES (256);   -- 错误：超出范围
```

### 7.2.3 显示宽度与ZEROFILL

```sql
-- 对于整型，括号中的数字表示显示宽度（不是存储宽度）
CREATE TABLE t4 (age INT(8));

-- 默认不填充0
INSERT INTO t4 VALUES (1234567);
SELECT * FROM t4;
-- +----------+
-- | age      |
-- +----------+
-- |  1234567 |
-- +----------+

-- 使用ZEROFILL约束，不足宽度用0填充
ALTER TABLE t4 MODIFY age INT(8) UNSIGNED ZEROFILL;

INSERT INTO t4 VALUES (1234567);
SELECT * FROM t4;
-- +----------+
-- | age      |
-- +----------+
-- | 01234567 |
-- +----------+
```

### 7.2.4 整型小结

```sql
-- 整型：TINYINT SMALLINT MEDIUMINT INT BIGINT
-- 整型后面的数字：限制显示长度
-- UNSIGNED：无符号约束，调整数值区间为0~正数
-- ZEROFILL：0填充约束，不足宽度时用0填充
```

## 7.3 浮点型

### 7.3.1 浮点型分类

| 数据类型 | 字节数 | 精度 | 说明 |
|----------|--------|------|------|
| FLOAT | 4 | 单精度 | 约7位有效数字 |
| DOUBLE | 8 | 双精度 | 约15位有效数字 |
| DECIMAL | 可变 | 定点精确 | 65位整数+30位小数 |

### 7.3.2 浮点型精度对比

```sql
-- 语法：FLOAT(M,D) / DOUBLE(M,D) / DECIMAL(M,D)
-- M：总位数（整数+小数）
-- D：小数位数

CREATE TABLE t5 (id FLOAT(255, 30));
CREATE TABLE t6 (id DOUBLE(255, 30));
CREATE TABLE t7 (id DECIMAL(65, 30));

-- 插入相同的小数（22位小数）
INSERT INTO t5 VALUES (1.1111111111111111111111);
INSERT INTO t6 VALUES (1.1111111111111111111111);
INSERT INTO t7 VALUES (1.1111111111111111111111);

-- 查询结果：
-- FLOAT：   1.111111164093017600000000000000  (前7位准确)
-- DOUBLE：  1.111111111111111200000000000000  (前15位准确)
-- DECIMAL： 1.111111111111111111111100000000  (全22位准确)
```

**结论**：精度比较 `FLOAT < DOUBLE < DECIMAL`
- 一般计算用`DOUBLE`
- 金额等精确数值用`DECIMAL`

## 7.4 字符型

### 7.4.1 CHAR 与 VARCHAR

| 特性 | CHAR | VARCHAR |
|------|------|---------|
| 默认长度 | 有默认值1 | 必须指定长度 |
| 存储方式 | 固定长度，不足用空格填充 | 变长，只存实际数据 |
| MySQL显示 | 自动去除末尾空格 | 保留原样 |
| 空间效率 | 浪费空间 | 节省空间 |
| 存取速度 | 快（无需计算长度） | 稍慢（需读取长度头） |

### 7.4.2 CHAR 与 VARCHAR 示例

```sql
-- CHAR有默认长度1，VARCHAR必须指定长度
CREATE TABLE t8 (name CHAR);         -- 相当于 CHAR(1)
CREATE TABLE t9 (name VARCHAR(1));   -- 必须指定长度

-- 插入测试
INSERT INTO t8 VALUES ('a');    -- 成功
INSERT INTO t8 VALUES ('ab');   -- 错误：数据过长

INSERT INTO t9 VALUES ('a');    -- 成功
INSERT INTO t9 VALUES ('ab');   -- 错误：数据过长

-- 修改长度为4
ALTER TABLE t8 MODIFY name CHAR(4);
ALTER TABLE t9 MODIFY name VARCHAR(4);

-- 统计字符长度
SELECT CHAR_LENGTH(name) FROM t8;  -- 1（MySQL自动去除空格）
SELECT CHAR_LENGTH(name) FROM t9;  -- 1
```

### 7.4.3 CHAR空格填充的严格模式

```sql
-- 查看当前严格模式
SHOW VARIABLES LIKE '%mode%';

-- PAD_CHAR_TO_FULL_LENGTH模式：恢复CHAR的空格填充
SET SESSION sql_mode = '...现有模式...,PAD_CHAR_TO_FULL_LENGTH';

-- 此时查询CHAR字段的字符长度就是填充后的长度
SELECT CHAR_LENGTH(name) FROM t8;  -- 4（空格被保留）
SELECT CHAR_LENGTH(name) FROM t9;  -- 1
```

### 7.4.4 CHAR vs VARCHAR 选择

- **CHAR**：适合存储固定长度的数据（如身份证号、手机号），存取速度快
- **VARCHAR**：适合存储变长的数据（如姓名、地址、描述），节省空间
- **目前趋势**：VARCHAR使用更广泛

## 7.5 日期时间类型

```sql
-- 四种日期时间类型
-- DATE      : 年月日（格式：YYYY-MM-DD）
-- DATETIME  : 年月日时分秒（格式：YYYY-MM-DD HH:MM:SS）
-- TIME      : 时分秒（格式：HH:MM:SS）
-- YEAR      : 年份（格式：YYYY）
```

**示例：**

```sql
CREATE TABLE t10 (
    id INT,
    born_year YEAR,
    birth DATE,
    study_time TIME,
    register_time DATETIME
);

-- 插入数据，分隔符可以使用 - / + : 等符号
INSERT INTO t10 VALUES
(1, '2000', '2000-3-6', '11:11:11', '2024-9-6 11:50:50');

INSERT INTO t10 VALUES
(2, '2000', '2000/3/6', '11:11:11', '2024-9-6 11:50:50');

INSERT INTO t10 VALUES
(3, '2000', '2000:3:6', '11:11:11', '2024-9-6 11:50:50');

-- 插入的数据会被自动格式化为统一格式
-- DATE:     2000-03-06
-- DATETIME: 2024-09-06 11:50:50
```

## 7.6 枚举类型（ENUM）

枚举类型用于**多选一**的场景：

```sql
CREATE TABLE user (
    id INT,
    name VARCHAR(25),
    gender ENUM('male', 'female', 'other')
);

INSERT INTO user VALUES (1, 'dream', 'male');     -- 成功
INSERT INTO user VALUES (2, 'hope', 'male,female'); -- 错误：只能选一个
```

## 7.7 集合类型（SET）

集合类型用于**多选多**的场景：

```sql
CREATE TABLE teacher (
    id INT,
    name VARCHAR(16),
    gender ENUM('male', 'female', 'others'),
    hobby SET('read books', 'listen music', 'play games')
);

-- 单选
INSERT INTO teacher VALUES (1, 'dream', 'male', 'read books');

-- 多选（多个值之间用逗号分隔）
INSERT INTO teacher VALUES (2, 'hope', 'male', 'read books,listen music');
```

---

# 第八部分：约束条件

## 8.1 NULL 与 NOT NULL

约束当前字段在插入数据时是否允许为空：

```sql
CREATE TABLE t1 (
    name VARCHAR(25) NULL,      -- 允许为空（默认）
    age INT NOT NULL             -- 不允许为空
);

-- age为NOT NULL，插入时必须提供age值
INSERT INTO t1 (age) VALUES (18);           -- 成功，name为NULL
INSERT INTO t1 (name, age) VALUES ('dream', 28); -- 成功
INSERT INTO t1 (name) VALUES ('dream');     -- 错误：age不能为空
```

## 8.2 UNIQUE（唯一性约束）

约束字段值在表中必须唯一，不能重复：

```sql
CREATE TABLE user (
    id INT,
    name VARCHAR(25) UNIQUE
);

INSERT INTO user VALUES (1, 'dream');  -- 成功
INSERT INTO user VALUES (2, 'dream');  -- 错误：Duplicate entry 'dream' for key 'name'
```

## 8.3 PRIMARY KEY（主键约束）

主键约束 = NOT NULL + UNIQUE，用于唯一标识表中的每一行数据：

```sql
-- 方式一：NOT NULL + UNIQUE
CREATE TABLE new_user (
    id INT NOT NULL UNIQUE
);

-- 方式二：直接使用PRIMARY KEY
CREATE TABLE new_user_one (
    id INT PRIMARY KEY
);

-- 以上两种方式等价，DESC查看都是 PRI 键
```

**主键核心概念：**
- **主键约束**：给字段加上`PRIMARY KEY`限制的规则
- **主键字段**：加上主键约束的字段
- **主键值**：主键字段对应的值

**主键的作用：**
- 主键值作为当前行数据的**唯一标识**（相当于身份证号）
- 主键字段会自动添加**索引（Index）**，提高查询速度
- 一张表**只能有一个主键**，但可以是复合主键

## 8.4 AUTO_INCREMENT（主键自增）

```sql
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25)
);

-- 不指定id插入，id自动递增
INSERT INTO user (name) VALUES ('dream');  -- id=1
INSERT INTO user (name) VALUES ('hope');   -- id=2
INSERT INTO user (name) VALUES ('opp');    -- id=3

-- 可以手动指定id
INSERT INTO user VALUES (10, 'test');      -- id=10

-- 再次自增插入，会在最大值基础上递增
INSERT INTO user (name) VALUES ('new');    -- id=11
```

**自增主键的特点：**
- 每次插入时如果不指定主键值，自动在上一个最大值基础上+1
- 中间断层的数据不影响后续自增（如1,2,5之后插入是6）
- 删除某条数据后，可以再次插入相同的主键值（该ID没有被占用）
- `TRUNCATE`会重置自增，`DELETE`不会

**修改自增起始值：**

```sql
ALTER TABLE user AUTO_INCREMENT = 20;

-- 只能修改为比当前最大值大的值才生效
-- 修改后会从指定值开始递增
```

## 8.5 FOREIGN KEY（外键约束）

外键用于建立两张表之间的关联关系。

**外键核心概念：**
- **外键约束**：给字段加上`FOREIGN KEY`限制的规则
- **外键字段**：加上外键约束的字段
- **外键值**：外键字段对应的值

**创建外键的基本语法：**

```sql
-- 先创建被关联表（目标表）
CREATE TABLE 目标表 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    其他字段...
);

-- 再创建关联表（包含外键的表）
CREATE TABLE 关联表 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    其他字段...,
    FOREIGN KEY (外键字段名) REFERENCES 目标表(目标主键字段名)
);
```

---

# 第九部分：外键关系

## 9.1 一对多关系

### 9.1.1 场景分析

以**员工表**和**部门表**为例：
- 从员工视角：一个员工可以有多个部门吗？**不能**，一个员工只能属于一个部门
- 从部门视角：一个部门可以有多个员工吗？**可以**，一个部门可以有多个员工
- 结论：员工和部门之间是**一对多**关系（部门是"一"，员工是"多"）

**外键建在"多"的一方（员工表）更合理。**

### 9.1.2 创建一对多关系表

```sql
-- 先创建被关联的部门表
CREATE TABLE dep (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '部门编号',
    dep_name VARCHAR(32) COMMENT '部门名称',
    dep_desc VARCHAR(32) COMMENT '部门描述'
);

-- 再创建员工表（外键在员工表）
CREATE TABLE emp (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '员工编号',
    name VARCHAR(32) COMMENT '员工姓名',
    age INT COMMENT '员工年龄',
    dep_id INT COMMENT '部门编号',
    FOREIGN KEY (dep_id) REFERENCES dep(id)
);
```

**创建表的先后顺序**：先创建被关联表（部门表），再创建关联表（员工表）。

## 9.2 一对一关系

### 9.2.1 场景分析

以**用户表**和**用户详情表**为例：
- 从用户视角：一个用户可以有多个详情吗？**不能**
- 从详情视角：一个详情可以有多个用户吗？**不能**
- 结论：用户和用户详情之间是**一对一**关系

### 9.2.2 创建一对一关系表

```sql
CREATE TABLE user_detail (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户详情编号',
    phone VARCHAR(11) COMMENT '用户手机号',
    age INT COMMENT '用户年龄'
);

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户编号',
    name VARCHAR(32) COMMENT '用户姓名',
    gender ENUM('male', 'female', 'other') COMMENT '用户性别',
    hobby SET('sing', 'dance', 'draw') COMMENT '用户爱好',
    detail_id INT UNIQUE,   -- 加UNIQUE确保一对一
    FOREIGN KEY (detail_id) REFERENCES user_detail(id)
);
```

> **提示**：一对一关系通常在关联字段上额外加`UNIQUE`约束。

## 9.3 多对多关系

### 9.3.1 场景分析

以**图书表**和**作者表**为例：
- 从图书视角：一本书可以有多个作者吗？**可以**
- 从作者视角：一个作者可以写多本书吗？**可以**
- 结论：图书和作者之间是**多对多**关系

### 9.3.2 创建多对多关系表

多对多关系需要借助**第三张中间表**来实现：

```sql
-- 创建图书表
CREATE TABLE book (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '图书编号',
    title VARCHAR(32) COMMENT '图书名称',
    price DECIMAL(5, 2) COMMENT '图书价格'
);

-- 创建作者表
CREATE TABLE author (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '作者编号',
    name VARCHAR(32) COMMENT '作者姓名',
    age INT COMMENT '作者年龄'
);

-- 创建中间表（关联图书和作者）
CREATE TABLE author_book (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '编号',
    book_id INT COMMENT '图书编号',
    author_id INT COMMENT '作者编号',
    FOREIGN KEY (book_id) REFERENCES book(id),
    FOREIGN KEY (author_id) REFERENCES author(id)
);
```

**中间表的数据示例：**

```
# 作者表
# id=1, name='dream'
# id=2, name='opp'

# 图书表
# id=1, title='西游记', price=99
# id=2, title='水浒传', price=88

# 中间表 author_book
# id=1, book_id=1, author_id=1  --> dream写了西游记
# id=2, book_id=1, author_id=2  --> opp写了西游记
# id=3, book_id=2, author_id=2  --> opp写了水浒传
```

通过中间表可以灵活地表达多对多关系。

## 9.4 级联更新与级联删除

在创建外键时，可以指定当被关联表数据发生变化时，关联表数据的处理方式：

```sql
CREATE TABLE emp (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32),
    dep_id INT,
    FOREIGN KEY (dep_id) REFERENCES dep(id)
        ON DELETE CASCADE   -- 级联删除
        ON UPDATE CASCADE   -- 级联更新
);
```

- **ON DELETE CASCADE**：当部门表中的某条数据被删除时，员工表中关联该部门的所有员工也会被删除
- **ON UPDATE CASCADE**：当部门表中的主键值被修改时，员工表中对应的外键值也会同步更新
- 这两种级联操作要写在`FOREIGN KEY`同一句中，不用逗号分隔

---

# 第十部分：查询语句详解

本章使用以下示例数据：

```sql
-- 准备数据库和表
DROP DATABASE IF EXISTS emp_data;
CREATE DATABASE emp_data;
USE emp_data;

CREATE TABLE emp (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    sex ENUM('male', 'female') NOT NULL DEFAULT 'male',
    age INT(3) UNSIGNED NOT NULL DEFAULT 28,
    hire_date DATE NOT NULL,
    post VARCHAR(50),
    post_comment VARCHAR(100),
    salary DOUBLE(15, 2),
    office INT,
    depart_id INT
);

INSERT INTO emp (name, sex, age, hire_date, post, salary, office, depart_id) VALUES
('dream', 'male', 78, '2022-03-06', '陌夜痴梦久生情', 730.33, 401, 1),
('mengmeng', 'female', 25, '2022-01-02', 'teacher', 12000.50, 401, 1),
('xiaomeng', 'male', 35, '2019-06-07', 'teacher', 15000.99, 401, 1),
('xiaona', 'female', 29, '2018-09-06', 'teacher', 11000.80, 401, 1),
('xiaoqi', 'female', 27, '2022-08-06', 'teacher', 13000.70, 401, 1),
('suimeng', 'male', 33, '2023-03-06', 'teacher', 14000.62, 401, 1),
('娜娜', 'female', 69, '2010-03-07', 'sale', 300.13, 402, 2),
('芳芳', 'male', 45, '2014-05-18', 'sale', 400.45, 402, 2),
('小明', 'male', 34, '2016-01-03', 'sale', 350.80, 402, 2),
('亚洲', 'female', 42, '2017-02-27', 'sale', 320.99, 402, 2),
('华华', 'female', 55, '2018-03-19', 'sale', 380.75, 402, 2),
('田七', 'male', 44, '2023-08-08', 'sale', 420.33, 402, 2),
('大古', 'female', 66, '2018-05-09', 'operation', 630.33, 403, 3),
('张三', 'male', 51, '2019-10-01', 'operation', 410.25, 403, 3),
('李四', 'male', 47, '2020-05-12', 'operation', 330.62, 403, 3),
('王五', 'female', 39, '2021-02-03', 'operation', 370.98, 403, 3),
('赵六', 'female', 36, '2022-07-24', 'operation', 390.15, 403, 3);
```

## 10.1 WHERE（条件筛选）

`WHERE`子句用于在查询时过滤数据。在执行顺序上：`FROM -> WHERE -> SELECT`。

```sql
-- 基本语法
SELECT */字段名 FROM 表名 WHERE 筛选条件;
```

### 10.1.1 比较运算与AND条件

```sql
-- 查询id大于等于3且小于等于6的数据
SELECT * FROM emp WHERE id >= 3 AND id <= 6;

-- 等价写法：BETWEEN ... AND ...
SELECT * FROM emp WHERE id BETWEEN 3 AND 6;
```

### 10.1.2 OR条件与IN运算

```sql
-- 查询薪资为指定值的数据
-- 方式一：OR连接
SELECT * FROM emp WHERE salary = 12000.50 OR salary = 13000.70 OR salary = 410.25;

-- 方式二：IN运算（类似Python中的集合判断）
SELECT * FROM emp WHERE salary IN (12000.50, 13000.70, 410.25);
```

### 10.1.3 模糊查询（LIKE）

```sql
-- % 表示任意多个字符
-- 查询姓名中包含字母"o"的员工姓名和薪资
SELECT name, salary FROM emp WHERE name LIKE '%o%';
-- +----------+----------+
-- | name     | salary   |
-- +----------+----------+
-- | xiaomeng | 15000.99 |
-- | xiaona   | 11000.80 |
-- | xiaoqi   | 13000.70 |
-- +----------+----------+

-- _ 表示任意一个字符
-- 查询姓名由6个字符组成的员工
SELECT name, salary FROM emp WHERE name LIKE '______';

-- 等价写法：使用CHAR_LENGTH函数
SELECT name, salary FROM emp WHERE CHAR_LENGTH(name) = 6;
```

### 10.1.4 NOT（取反）

```sql
-- 查询id不在3到6之间的数据
SELECT * FROM emp WHERE NOT id BETWEEN 3 AND 6;
```

### 10.1.5 NULL值判断

```sql
-- 错误写法（查不到数据）
SELECT name, post FROM emp WHERE post_comment = NULL;

-- 正确写法
SELECT name, post FROM emp WHERE post_comment IS NULL;

-- 查询不为空
SELECT name, post FROM emp WHERE post_comment IS NOT NULL;
```

## 10.2 GROUP BY（分组）

分组关键字：当出现"每个"、"平均"、"最高"、"最低"等词时，通常需要分组。

```sql
-- 基本语法
SELECT */字段名 FROM 表名 GROUP BY 分组字段;
```

### 10.2.1 解决GROUP BY的严格模式问题

```sql
-- 查看当前严格模式
SHOW VARIABLES LIKE '%mode%';

-- 临时关闭only_full_group_by（重新登录后失效）
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- 然后执行分组查询
SELECT * FROM emp GROUP BY post;
```

### 10.2.2 聚合函数与分组

聚合函数**必须在分组之后使用**：

```sql
-- 1. 每个部门的最高薪资
SELECT post, MAX(salary) AS "最高薪资" FROM emp GROUP BY post;

-- 2. 每个部门的最低薪资
SELECT post, MIN(salary) AS "最低薪资" FROM emp GROUP BY post;

-- 3. 每个部门的平均薪资
SELECT post, AVG(salary) AS "平均薪资" FROM emp GROUP BY post;

-- 4. 每个部门的薪资总和
SELECT post, SUM(salary) AS "薪资总和" FROM emp GROUP BY post;

-- 5. 每个部门的人数
SELECT post, COUNT(id) AS "部门人数" FROM emp GROUP BY post;
```

### 10.2.3 GROUP_CONCAT（分组拼接）

```sql
-- 查询每个部门下的所有员工姓名
SELECT post, GROUP_CONCAT(name) FROM emp GROUP BY post;
-- +-----------------------+-------------------------------------------+
-- | post                  | GROUP_CONCAT(name)                        |
-- +-----------------------+-------------------------------------------+
-- | operation             | 大古,张三,李四,王五,赵六                   |
-- | sale                  | 娜娜,芳芳,小明,亚洲,华华,田七              |
-- | teacher               | mengmeng,xiaomeng,xiaona,xiaoqi,suimeng    |
-- | 陌夜痴梦久生情         | dream                                     |
-- +-----------------------+-------------------------------------------+

-- 拼接时添加前缀
SELECT post, GROUP_CONCAT('员工_', name) FROM emp GROUP BY post;

-- 拼接多个字段
SELECT post, GROUP_CONCAT(name, ':', salary) FROM emp GROUP BY post;
```

### 10.2.4 CONCAT（字段拼接）

`CONCAT`不需要分组即可使用：

```sql
-- 拼接每个员工的姓名和薪资
SELECT CONCAT(name, ':', salary) FROM emp;
```

> **注意**：`WHERE`关键字必须在`GROUP BY`之前，且`WHERE`中不能使用聚合函数。

## 10.3 HAVING（分组后过滤）

`HAVING`用于在分组之后对数据进行再次筛选，且支持聚合函数：

```sql
-- 查询各部门年龄在30岁以上的员工的平均薪资，
-- 并保留平均薪资大于10000的部门
SELECT post, AVG(salary) AS "avg_salary"
FROM emp
WHERE age > 30
GROUP BY post
HAVING AVG(salary) > 10000;

-- +---------+--------------+
-- | post    | avg_salary   |
-- +---------+--------------+
-- | teacher | 14500.805000 |
-- +---------+--------------+
```

**WHERE vs HAVING：**
| 特性 | WHERE | HAVING |
|------|-------|--------|
| 作用阶段 | 分组前过滤 | 分组后过滤 |
| 能否使用聚合函数 | 不能 | 能 |
| 执行顺序 | 先于GROUP BY | 后于GROUP BY |

## 10.4 DISTINCT（去重）

```sql
-- 查询公司都有哪些不同的部门编号
SELECT DISTINCT office FROM emp;
-- +--------+
-- | office |
-- +--------+
-- |    401 |
-- |    402 |
-- |    403 |
-- +--------+
```

> **注意**：`DISTINCT`不能对主键字段去重（因为主键本身就不为空且唯一）。

## 10.5 ORDER BY（排序）

```sql
-- 升序排序（默认）
SELECT * FROM emp ORDER BY salary ASC;

-- 降序排序
SELECT * FROM emp ORDER BY salary DESC;

-- 多字段排序：先按部门降序，同一部门内按年龄升序
SELECT * FROM emp ORDER BY office DESC, age ASC;
```

**综合示例：**

```sql
-- 统计各部门年龄在30岁以上的员工的平均薪资，
-- 保留平均薪资大于500的部门，按平均薪资降序排列
SELECT post, AVG(salary) AS avg_salary
FROM emp
WHERE age > 30
GROUP BY post
HAVING AVG(salary) > 500
ORDER BY AVG(salary) DESC;

-- +-----------------------+--------------+
-- | post                  | avg_salary   |
-- +-----------------------+--------------+
-- | teacher               | 14500.805000 |
-- | 陌夜痴梦久生情         |   730.330000 |
-- +-----------------------+--------------+
```

## 10.6 LIMIT（限制条数）

```sql
-- 获取前10条数据
SELECT * FROM emp LIMIT 10;

-- 从索引0开始，获取5条数据（第一页）
SELECT * FROM emp LIMIT 0, 5;

-- 从索引5开始，获取5条数据（第二页）
SELECT * FROM emp LIMIT 5, 5;

-- 从索引6开始，获取5条数据
SELECT * FROM emp LIMIT 6, 5;
```

**LIMIT语法说明：**
- `LIMIT n`：获取前n条数据
- `LIMIT m, n`：从索引m开始（第一条数据索引为0），获取n条数据

### 10.6.1 完整查询语句的执行顺序

```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

## 10.7 REGEXP（正则表达式查询）

MySQL支持简单的正则匹配：

| 符号 | 说明 | 示例 | 匹配值示例 |
|------|------|------|-----------|
| `^` | 匹配文本开始 | `'^b'` | book、big |
| `$` | 匹配文本结束 | `'st$'` | test、persist |
| `.` | 匹配任意单个字符 | `'b.t'` | bit、bat |
| `*` | 匹配前面字符0次或多次 | `'f*n'` | fn、faan |
| `+` | 匹配前面字符1次或多次 | `'ba+'` | ba、bay |
| `?` | 匹配前面字符0次或1次 | `'sa?'` | sa、s |
| `[字符集合]` | 匹配集合中任意字符 | `'[xz]'` | x-ray、zebra |
| `[^]` | 匹配不在集合中的字符 | `'[^abc]'` | desk、fox |
| `{n}` | 匹配前面字符n次 | `'b{2}'` | bbb |
| `{n,m}` | 匹配前面字符n到m次 | `'b{2,4}'` | bbb、bbbb |

**示例：**

```sql
-- 查询name字段以'j'开头的记录
SELECT * FROM person WHERE name REGEXP '^j';

-- 查询name字段以'y'结尾的记录
SELECT * FROM person WHERE name REGEXP 'y$';

-- 查询name字段包含'a'和'y'且两字母之间只有一个字符的记录
SELECT * FROM person WHERE name REGEXP 'a.y';

-- 查询name字段包含'T'且后面有字母'h'的记录
SELECT * FROM person WHERE name REGEXP 'Th*';

-- 查询name字段包含'T'且后面至少有一个'h'的记录
SELECT * FROM person WHERE name REGEXP 'Th+';
```

---

# 第十一部分：聚合函数汇总

| 函数 | 作用 | 说明 |
|------|------|------|
| `COUNT()` | 统计行数 | 不会对NULL计数 |
| `SUM()` | 求和 | 忽略NULL值 |
| `AVG()` | 求平均值 | 忽略NULL值 |
| `MAX()` | 求最大值 | |
| `MIN()` | 求最小值 | |

```sql
-- 基本用法
SELECT COUNT(*) FROM emp;                    -- 总行数
SELECT COUNT(post_comment) FROM emp;         -- 不含NULL的行数
SELECT SUM(salary) FROM emp;                 -- 薪资总和
SELECT AVG(salary) FROM emp;                 -- 平均薪资
SELECT MAX(salary) FROM emp;                 -- 最高薪资
SELECT MIN(salary) FROM emp;                 -- 最低薪资

-- 结合分组使用
SELECT post, COUNT(id), SUM(salary), AVG(salary), MAX(salary), MIN(salary)
FROM emp
GROUP BY post;
```

---

# 第十二部分：联表查询

## 12.1 子查询 vs 联表查询

| 方式 | 思路 |
|------|------|
| **子查询** | 将一条SQL语句的结果作为另一条SQL语句的条件，分步解决 |
| **联表查询** | 将多张表的数据先拼接成一张大表，再在新表中查询 |

## 12.2 准备测试数据

```sql
CREATE DATABASE dep_emp_data;
USE dep_emp_data;

-- 部门表
CREATE TABLE dep (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20)
);

INSERT INTO dep VALUES
(200, '技术部'),
(201, '人力资源'),
(202, '销售部'),
(203, '运营部'),
(204, '售后部');

-- 员工表（使用逻辑外键，不设物理外键约束）
CREATE TABLE emp (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20),
    sex ENUM('male', 'female') NOT NULL DEFAULT 'male',
    age INT,
    dep_id INT
);

INSERT INTO emp (name, sex, age, dep_id) VALUES
('dream', 'male', 18, 200),
('chimeng', 'female', 18, 201),
('menmgneg', 'male', 38, 202),
('hope', 'male', 18, 203),
('own', 'male', 28, 204),
('thdream', 'male', 18, 205);
```

## 12.3 子查询

```sql
-- 示例1：获取员工dream所在的部门名称

-- 步骤分解：
-- (1) 先查询dream的部门ID
SELECT dep_id FROM emp WHERE name = 'dream';  -- 结果：200

-- (2) 根据部门ID查询部门名称
SELECT name FROM dep WHERE id = 200;  -- 结果：技术部

-- (3) 合并为一条子查询语句
SELECT name FROM dep WHERE id = (
    SELECT dep_id FROM emp WHERE name = 'dream'
);
-- +-----------+
-- | name      |
-- +-----------+
-- | 技术部     |
-- +-----------+

-- 示例2：查询部门是技术或人力资源的员工信息
SELECT * FROM emp WHERE dep_id IN (
    SELECT id FROM dep WHERE name = '技术部' OR name = '人力资源'
);
```

## 12.4 联表查询（笛卡尔积）

### 12.4.1 什么是笛卡尔积

笛卡尔积是两个集合之间所有可能元素组合的数量。如集合A有n个元素，集合B有m个元素，则笛卡尔积为n*m。

在MySQL中，当两张表进行连接时，结果集行数 = 表1行数 * 表2行数。

```sql
-- 直接拼接产生笛卡尔积（5*6=30行）
SELECT * FROM dep, emp;

-- 通过WHERE过滤获得有效数据
SELECT * FROM dep, emp WHERE emp.dep_id = dep.id;
-- 结果：只保留dep_id匹配的行（5行，因为有一个员工的dep_id=205无对应部门）
```

### 12.4.2 四种连接方式

```sql
-- 1. INNER JOIN（内连接）：取交集
SELECT * FROM emp INNER JOIN dep ON emp.dep_id = dep.id;
-- 结果：5行（emp中有匹配部门的数据）

-- 2. LEFT JOIN（左连接）：左表全部保留
SELECT * FROM emp LEFT JOIN dep ON emp.dep_id = dep.id;
-- 结果：6行（emp全部数据，dep中无匹配则为NULL）

-- 3. RIGHT JOIN（右连接）：右表全部保留
SELECT * FROM emp RIGHT JOIN dep ON emp.dep_id = dep.id;
-- 结果：5行（dep全部数据，emp中无匹配则为NULL）

-- 4. UNION（全连接）：两张表数据全部保留
SELECT * FROM emp LEFT JOIN dep ON emp.dep_id = dep.id
UNION
SELECT * FROM emp RIGHT JOIN dep ON emp.dep_id = dep.id;
-- 结果：6行（两张表所有数据，无匹配处为NULL）
```

### 12.4.3 联表查询综合示例

```sql
-- 查询平均年龄在25岁以上的部门名称
-- 步骤：
-- 1. 内连接拼接两表
-- 2. 按部门分组
-- 3. 计算平均年龄
-- 4. 过滤出大于25岁
SELECT dep.name, AVG(age) AS avg_age
FROM emp
INNER JOIN dep ON dep.id = emp.dep_id
GROUP BY dep.name
HAVING AVG(age) > 25;

-- +-----------+---------+
-- | name      | avg_age |
-- +-----------+---------+
-- | 售后部     | 28.0000 |
-- | 销售部     | 38.0000 |
-- +-----------+---------+
```

## 12.5 EXISTS 关键字

`EXISTS`用于判断子查询结果是否存在：

```sql
-- 若子查询有结果，则外层查询返回数据
SELECT * FROM emp WHERE EXISTS (
    SELECT id FROM dep WHERE id > 201
);
-- 结果：返回emp所有数据（因为子查询有结果）

-- 若子查询无结果，则外层查询返回空
SELECT * FROM emp WHERE EXISTS (
    SELECT id FROM dep WHERE id > 300
);
-- 结果：Empty set（因为子查询无结果）
```

---

# 第十三部分：存储引擎

## 13.1 什么是存储引擎

存储引擎是数据库管理系统中用于存储、处理和保护数据的核心服务。针对不同类型的数据，有不同的存储和处理机制。

## 13.2 MySQL主要存储引擎

| 存储引擎 | 说明 | 特点 |
|----------|------|------|
| **InnoDB** | MySQL 5.5之后的默认引擎 | 支持事务、行锁、外键，数据安全性高 |
| **MyISAM** | MySQL 5.5之前的默认引擎 | 查询速度快，数据安全性较弱 |
| **MEMORY** | 内存引擎 | 数据全部存在内存中，速度快但断电丢失 |
| **BLACKHOLE** | 黑洞引擎 | 任何写入的数据都会消失 |

## 13.3 查看存储引擎

```sql
SHOW ENGINES;
-- +--------------------+---------+----------------------------------------------------+
-- | Engine             | Support | Comment                                            |
-- +--------------------+---------+----------------------------------------------------+
-- | InnoDB             | DEFAULT | Supports transactions, row-level locking, ...      |
-- | MRG_MYISAM         | YES     | Collection of identical MyISAM tables              |
-- | BLACKHOLE          | YES     | /dev/null storage engine                           |
-- | CSV                | YES     | CSV storage engine                                 |
-- | MyISAM             | YES     | MyISAM storage engine                              |
-- | MEMORY             | YES     | Hash based, stored in memory                       |
-- +--------------------+---------+----------------------------------------------------+
```

## 13.4 不同引擎的文件结构

```sql
CREATE TABLE t1 (id INT) ENGINE = InnoDB;
CREATE TABLE t2 (id INT) ENGINE = MyISAM;
CREATE TABLE t3 (id INT) ENGINE = BLACKHOLE;
CREATE TABLE t4 (id INT) ENGINE = MEMORY;
```

各引擎在磁盘上的文件：

| 引擎 | 生成的文件 | 说明 |
|------|-----------|------|
| InnoDB | `.frm` + `.ibd` | frm存表结构，ibd存数据 |
| MyISAM | `.frm` + `.MYD` + `.MYI` | frm表结构，MYD数据，MYI索引 |
| BLACKHOLE | `.frm` | 只有表结构，数据不保存 |
| MEMORY | `.frm` | 只有表结构，数据在内存中 |

```sql
-- 测试写入数据
INSERT INTO t1 VALUES (1);
INSERT INTO t2 VALUES (1);
INSERT INTO t3 VALUES (1);
INSERT INTO t4 VALUES (1);

SELECT * FROM t1;  -- 数据存在（InnoDB）
SELECT * FROM t2;  -- 数据存在（MyISAM）
SELECT * FROM t3;  -- 空（BLACKHOLE，数据消失）
SELECT * FROM t4;  -- 数据存在（MEMORY），但重启MySQL后消失
```

## 13.5 引擎选择建议

- **InnoDB**：绝大多数场景的默认选择，支持事务和行锁
- **MyISAM**：适用于只读或读多写少的场景（如日志、报表）
- **MEMORY**：适用于临时表、缓存表
- **BLACKHOLE**：适用于主从复制中的中继日志

---

# 第十四部分：严格模式

## 14.1 什么是严格模式

严格模式（SQL Mode）是MySQL中用来约束数据存储格式的一组规则，确保数据的正确性和安全性。不恰当的严格模式设置可能导致数据错乱。

## 14.2 查看严格模式

```sql
SHOW VARIABLES LIKE '%mode%';

-- sql_mode常见值：
-- ONLY_FULL_GROUP_BY：SELECT中的列必须在GROUP BY中出现或使用聚合函数
-- STRICT_TRANS_TABLES：严格事务模式
-- NO_ZERO_IN_DATE：不允许日期中的月或日为0
-- NO_ZERO_DATE：不允许'0000-00-00'这样的日期
-- ERROR_FOR_DIVISION_BY_ZERO：除以0报错
-- PAD_CHAR_TO_FULL_LENGTH：CHAR类型不自动去除尾部空格
```

## 14.3 修改严格模式

```sql
-- 临时性修改（重新登录后失效）
SET SESSION sql_mode = '模式列表';

-- 永久性修改（重启客户端不失效）
SET GLOBAL sql_mode = '模式列表';
```

**注意事项**：
- 修改严格模式时一定要在**原有基础上**进行增减，不能直接覆盖
- 例如原来有5个模式，想关闭1个模式，需要在sql_mode中保留其他4个

**修改示例：**

```sql
-- 查看当前模式
SHOW VARIABLES LIKE '%mode%';
-- sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,...'

-- 如果要去除ONLY_FULL_GROUP_BY，保留其他模式
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- 如果要添加PAD_CHAR_TO_FULL_LENGTH
SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,PAD_CHAR_TO_FULL_LENGTH';
```

---

# 第十五部分：PyMySQL使用

## 15.1 DB-API介绍

DB-API是Python标准的数据库规范（PEP 249），定义了一系列必须的对象和数据库操作方式，为各种数据库提供一致的访问接口。

**Python操作MySQL的常用模块：**

| 模块 | 说明 |
|------|------|
| MySQL-python | MySQL官方提供，基本不用 |
| mysqlclient | MySQL-python的fork，Django推荐使用 |
| **PyMySQL** | 纯Python实现，兼容性好，最常用 |

## 15.2 安装PyMySQL

```bash
pip install PyMySQL
```

## 15.3 数据库连接

```python
import pymysql
from pymysql.cursors import Cursor, DictCursor

# 创建数据库连接
conn = pymysql.connect(
    user='root',            # 数据库用户名
    password='你的密码',     # 数据库密码
    host='127.0.0.1',       # 数据库服务器IP
    port=3306,              # 端口号
    database='user_data',   # 要连接的数据库名
    charset='utf8mb4',      # 编码格式
    cursorclass=DictCursor, # 返回数据格式
    autocommit=False        # 是否自动提交事务
)

# 创建游标对象
cursor = conn.cursor()
```

**cursorclass参数说明：**
- `Cursor`（默认）：返回的数据是**元组**类型，不带字段名
- `DictCursor`：返回的数据是**字典**类型，包含字段名和值的映射

**autocommit参数说明：**
- `False`（默认）：需要手动调用`conn.commit()`提交事务
- `True`：自动提交事务

## 15.4 查询操作

```python
def search_database_option(self):
    sql = 'SELECT * FROM user;'
    self.cursor.execute(sql)

    # 方法1：fetchone() - 查询单条数据（每次读取一条，游标后移）
    result = self.cursor.fetchone()
    # {'id': 1, 'username': 'dream', 'password': '521521'}
    result = self.cursor.fetchone()
    # {'id': 2, 'username': 'hope', 'password': '369369'}

    # 方法2：fetchall() - 查询所有数据
    result = self.cursor.fetchall()
    # [{'id': 1, 'username': 'dream', 'password': '521521'},
    #  {'id': 2, 'username': 'hope', 'password': '369369'}]

    # 方法3：fetchmany(size=n) - 查询指定数量的数据（类似LIMIT）
    result = self.cursor.fetchmany(size=2)
    # [{'id': 1, ...}, {'id': 2, ...}]

    # 方法4：scroll(value, mode) - 移动游标
    # mode='relative'：相对当前位置移动
    self.cursor.scroll(1, 'relative')
    # mode='absolute'：相对于起始位置移动
    self.cursor.scroll(0, 'absolute')
```

## 15.5 插入操作

```python
def insert_data_option(self):
    # 【方式一】原生SQL（注意数据不会自动提交）
    sql = "INSERT INTO user(username, password) VALUES ('dream_one', '369369');"
    self.cursor.execute(sql)
    self.conn.commit()  # 必须提交事务

    # 【方式二】使用%s占位符（按位置传参，推荐！）
    sql = 'INSERT INTO user(username, password) VALUES (%s, %s);'
    self.cursor.execute(sql, ['dream_two', '369369'])
    self.conn.commit()

    # 【方式三】使用%(name)s占位符（按关键字传参）
    sql = 'INSERT INTO user(username, password) VALUES (%(name)s, %(pwd)s);'
    self.cursor.execute(sql, {'name': 'dream_three', 'pwd': '369369'})
    self.conn.commit()
```

## 15.6 批量插入

```python
def insert_many_data_option(self):
    # 按位置批量插入
    sql = 'INSERT INTO user(username, password) VALUES (%s, %s);'
    self.cursor.executemany(sql, [
        ('user1', 'pwd1'),
        ('user2', 'pwd2'),
        ('user3', 'pwd3'),
    ])
    self.conn.commit()

    # 按关键字批量插入
    sql = 'INSERT INTO user(username, password) VALUES (%(username)s, %(password)s);'
    self.cursor.executemany(sql, [
        {'username': 'user4', 'password': 'pwd4'},
        {'username': 'user5', 'password': 'pwd5'},
    ])
    self.conn.commit()
```

## 15.7 更新操作

```python
def update_data_option(self):
    # 按关键字传参
    sql = 'UPDATE user SET username = %(new_username)s WHERE username = %(old_username)s;'
    self.cursor.execute(sql, {
        'new_username': 'dream_new',
        'old_username': 'dream_old'
    })
    self.conn.commit()
```

## 15.8 删除操作

```python
def delete_data_option(self):
    sql = 'DELETE FROM user WHERE username = %(del_name)s;'
    self.cursor.execute(sql, {'del_name': 'dream_4'})
    self.conn.commit()
```

## 15.9 SQL注入问题与防范

### 15.9.1 什么是SQL注入

SQL注入是利用SQL语句的漏洞，通过输入特殊字符来绕过正常的查询逻辑，从而获取或破坏数据库数据。

```python
# 【危险示例】字符串拼接导致SQL注入
username = input('请输入用户名: ').strip()
password = input('请输入密码: ').strip()

sql = f"SELECT * FROM user WHERE username='{username}' AND password='{password}';"
cursor.execute(sql)
```

**攻击演示：**
- 正常输入：`用户名=dream, 密码=521521`
  - SQL：`SELECT * FROM user WHERE username='dream' AND password='521521';`
  - 结果：登陆成功

- 攻击输入：`用户名=dream' -- xxx, 密码=xxx`
  - SQL：`SELECT * FROM user WHERE username='dream' -- xxx' AND password='xxx';`
  - SQL中的`--`表示注释，后面的密码验证被注释掉了
  - 结果：**无需密码即可登录**

### 15.9.2 防范SQL注入

**解决方案：使用参数化查询**

```python
# 【安全示例】使用%s占位符，PyMySQL会自动过滤特殊字符
username = input('请输入用户名: ').strip()
password = input('请输入密码: ').strip()

sql = 'SELECT * FROM user WHERE username = %(username)s AND password = %(password)s;'
cursor.execute(sql, {'username': username, 'password': password})
result = cursor.fetchall()

if result:
    print('登陆成功!')
else:
    print('用户名和密码错误!')
```

**PyMySQL的execute方法会自动对参数进行转义和过滤**，防止SQL注入攻击。

## 15.10 完整数据库操作类

```python
import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler:
    """MySQL数据库操作封装类"""
    
    def __init__(self):
        self.conn = pymysql.connect(
            user='root',
            password='你的密码',
            database='user_data',
            host='127.0.0.1',
            port=3306,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=False
        )
        self.cursor = self.conn.cursor()

    def search(self, username=None):
        """查询用户数据"""
        if username:
            sql = 'SELECT * FROM user WHERE username = %(username)s;'
            self.cursor.execute(sql, {'username': username})
        else:
            sql = 'SELECT * FROM user;'
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, username, password):
        """插入用户数据"""
        sql = 'INSERT INTO user(username, password) VALUES (%(username)s, %(password)s);'
        self.cursor.execute(sql, {'username': username, 'password': password})
        self.conn.commit()
        return self.cursor.rowcount  # 影响的行数

    def insert_many(self, user_list):
        """批量插入用户数据"""
        sql = 'INSERT INTO user(username, password) VALUES (%(username)s, %(password)s);'
        self.cursor.executemany(sql, user_list)
        self.conn.commit()
        return self.cursor.rowcount

    def update(self, old_username, new_username):
        """更新用户名"""
        sql = 'UPDATE user SET username = %(new)s WHERE username = %(old)s;'
        self.cursor.execute(sql, {'new': new_username, 'old': old_username})
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, username):
        """删除用户"""
        sql = 'DELETE FROM user WHERE username = %(username)s;'
        self.cursor.execute(sql, {'username': username})
        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        """关闭连接"""
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


# 使用示例
if __name__ == '__main__':
    db = MysqlHandler()

    # 查询
    users = db.search()
    print(users)

    # 插入
    db.insert('test_user', '123456')

    # 更新
    db.update('test_user', 'new_user')

    # 删除
    db.delete('new_user')

    db.close()
```

---

# 第十六部分：Navicat可视化工具

## 16.1 什么是Navicat

Navicat是一款强大的数据库管理和开发工具，提供直观的图形用户界面（GUI），支持MySQL、PostgreSQL、SQLite、SQL Server等多种数据库。

## 16.2 Navicat的主要功能

- 数据库连接管理
- 数据表可视化管理（创建、修改、删除）
- 数据浏览与编辑
- SQL编辑器（语法高亮、自动补全）
- 数据导入导出
- 数据库备份与还原
- 数据模型设计（ER图）
- 用户与权限管理
- SSH/HTTP隧道连接

## 16.3 Navicat版本说明

- **Navicat Premium**：付费版，功能完整，支持多种数据库
- **Navicat for MySQL**：付费版，专为MySQL设计
- **Navicat Premium Lite**（2024年后）：官方免费版，功能有所精简

对于开发学习使用，免费版已足够满足基本需求。

## 16.4 Navicat常用操作

1. **新建连接**：填写主机名(127.0.0.1)、端口(3306)、用户名(root)、密码
2. **新建数据库**：右键连接 -> 新建数据库 -> 设置数据库名和字符集
3. **新建数据表**：右键数据库 -> 新建表 -> 添加字段、设置类型和约束
4. **执行SQL**：打开查询编辑器 -> 编写SQL -> 点击运行
5. **数据操作**：直接在表格中双击编辑、右键插入/删除行
6. **导入导出**：右键表名 -> 导入向导/导出向导

---

# 第十七部分：MySQL进阶知识

## 17.1 视图（View）

### 17.1.1 什么是视图

视图是一种**虚拟表**，其内容是一个或多个基本表的查询结果。视图不存储实际数据，每次查询时动态计算。

**视图的优点：**
- 简化复杂查询
- 隐藏敏感数据，控制访问权限
- 实现逻辑数据独立性
- 可创建物化视图优化查询性能

### 17.1.2 视图操作

```sql
-- 创建视图
CREATE VIEW 视图名 AS (SELECT * FROM 表名 WHERE 条件);

-- 示例：创建只包含id>202的部门视图
CREATE VIEW emp_dep(id, name) AS (
    SELECT * FROM dep WHERE id > 202
);
-- 视图会出现在SHOW TABLES的结果中

-- 查询视图（和使用普通表一样）
SELECT * FROM emp_dep;

-- 更新视图数据（注意：会影响到原表！）
UPDATE emp_dep SET id = 206 WHERE id = 204;

-- 删除视图
DROP VIEW 视图名;
```

> **注意**：视图一般只用于**查询**，不建议对视图数据进行修改，因为修改视图会影响原表数据。过多的视图也会让表结构变得复杂。

## 17.2 触发器（Trigger）

### 17.2.1 什么是触发器

触发器是在满足对表数据进行**增删改**操作时，**自动触发**执行的一段SQL逻辑。用于实现日志记录、数据验证、数据同步等功能。

### 17.2.2 触发器的六种场景

| 时机 | INSERT | UPDATE | DELETE |
|------|--------|--------|--------|
| BEFORE | 插入前触发 | 修改前触发 | 删除前触发 |
| AFTER | 插入后触发 | 修改后触发 | 删除后触发 |

### 17.2.3 创建触发器

```sql
-- 基本语法
DELIMITER $$
CREATE TRIGGER 触发器名字
    BEFORE/AFTER INSERT/UPDATE/DELETE
    ON 表名
    FOR EACH ROW
BEGIN
    SQL语句;
END$$
DELIMITER ;
```

### 17.2.4 触发器示例

```sql
-- 1. 创建命令表
CREATE TABLE cmd (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    username VARCHAR(32) COMMENT '执行用户',
    group_id VARCHAR(32) COMMENT '用户分组',
    cmd VARCHAR(32) COMMENT '执行的命令',
    sub_time DATETIME COMMENT '执行时间',
    success ENUM('success', 'failure') COMMENT '执行成功或失败'
);

-- 2. 创建错误日志表
CREATE TABLE error_log (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    error_cmd VARCHAR(255) COMMENT '执行错误的命令',
    error_time DATETIME COMMENT '记录日志的时间'
);

-- 3. 创建触发器：当cmd表插入失败记录时自动写入error_log
DELIMITER $$
CREATE TRIGGER trigger_after_insert_cmd
    AFTER INSERT ON cmd
    FOR EACH ROW
BEGIN
    IF NEW.success = 'failure' THEN
        INSERT INTO error_log(error_cmd, error_time)
        VALUES (NEW.cmd, NEW.sub_time);
    END IF;
END$$
DELIMITER ;

-- 4. 测试触发器
INSERT INTO cmd(username, group_id, cmd, sub_time, success)
VALUES ('dream', '0755', 'ls -l', NOW(), 'success');
-- 不会触发（success = success）

INSERT INTO cmd(username, group_id, cmd, sub_time, success)
VALUES ('dream', '0755', 'lss', NOW(), 'failure');
-- 触发！error_log表中自动插入一条错误记录
```

**NEW关键字**：代表当前插入或更新的数据行对象，存储了所有字段值。

### 17.2.5 查看和删除触发器

```sql
-- 查看所有触发器
SHOW TRIGGERS;
-- 或 格式化查看
SHOW TRIGGERS \G;

-- 删除触发器
DROP TRIGGER 触发器名字;
```

## 17.3 事务（Transaction）

### 17.3.1 什么是事务

事务是指一系列相关操作的集合，这些操作被视为一个**不可分割的工作单元**。事务中的操作要么全部成功执行，要么全部失败回滚。

### 17.3.2 事务的四大特性（ACID）

| 特性 | 说明 |
|------|------|
| **原子性（Atomicity）** | 事务是不可分割的最小单元，要么全做，要么全不做 |
| **一致性（Consistency）** | 事务执行前后，数据必须保持一致状态，满足所有完整性约束 |
| **隔离性（Isolation）** | 并发事务之间相互隔离，互不干扰 |
| **持久性（Durability）** | 事务一旦提交，结果是永久性的，即使系统故障也不会丢失 |

### 17.3.3 事务操作

```sql
-- 开启事务
START TRANSACTION;

-- 执行SQL操作...
INSERT INTO ...
UPDATE ...
DELETE FROM ...

-- 提交事务（确认所有操作）
COMMIT;

-- 回滚事务（撤销所有操作）
ROLLBACK;
```

### 17.3.4 Python中操作事务

```python
# conn.autocommit = False  # 默认不自动提交

# 执行SQL操作
cursor.execute(sql)
# ...

# 手动提交
conn.commit()

# 或手动回滚
conn.rollback()
```

## 17.4 存储过程（Stored Procedure）

### 17.4.1 什么是存储过程

存储过程类似于编程语言中的**自定义函数**，内部包含一系列可执行的SQL语句，存储在MySQL服务端，通过调用存储过程来触发内部的SQL执行。

### 17.4.2 存储过程的特点

- **预编译**：首次创建时编译优化，后续执行无需再编译
- **数据库端执行**：减少网络传输开销
- **代码重用**：可被多个应用程序共享
- **安全性**：可限制数据库访问权限
- **事务支持**：可包含事务处理逻辑

### 17.4.3 创建和调用存储过程

```sql
-- 基本语法
DELIMITER $$
CREATE PROCEDURE 存储过程名(参数列表)
BEGIN
    SQL语句;
END$$
DELIMITER ;

-- 调用存储过程
CALL 存储过程名(参数值);

-- 查看存储过程创建语句
SHOW CREATE PROCEDURE 存储过程名;

-- 查看所有存储过程
SHOW PROCEDURE STATUS;

-- 删除存储过程
DROP PROCEDURE 存储过程名;
```

### 17.4.4 存储过程示例

```sql
-- 创建一个根据ID范围查询员工的存储过程
DELIMITER $$
CREATE PROCEDURE search_info(
    IN m INT,       -- 输入参数：起始ID
    IN n INT        -- 输入参数：结束ID
)
BEGIN
    SELECT * FROM emp WHERE id BETWEEN m AND n;
END$$
DELIMITER ;

-- 调用存储过程
CALL search_info(3, 6);
-- 返回id在3到6之间的员工数据
```

**参数类型说明：**
- `IN`：输入参数（默认）
- `OUT`：输出参数（返回值）
- `INOUT`：既是输入也是输出参数

### 17.4.5 数据库操作三种开发方式

| 方式 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| 存储过程 | MySQL端预编写，应用调用 | 效率高 | 扩展性差，跨部门沟通困难 |
| 手写SQL | 应用端自己编写SQL | 扩展性好 | 开发效率低，需考虑优化 |
| ORM框架 | 使用框架封装数据库操作 | 开发效率最高 | 语句扩展性差，可能效率低 |

## 17.5 MySQL内置函数

### 17.5.1 字符串函数

```sql
-- 字符串连接
SELECT CONCAT('Hello', ' ', 'World');  -- 'Hello World'

-- 截取子串
SELECT SUBSTRING('Hello World', 1, 5);  -- 'Hello'

-- 大小写转换
SELECT UPPER('hello world');  -- 'HELLO WORLD'
SELECT LOWER('HELLO WORLD');  -- 'hello world'

-- 字符串长度
SELECT LENGTH('Hello World');  -- 11

-- 去除空格
SELECT TRIM('   hello   ');    -- 'hello'
SELECT LTRIM('   hello   ');   -- 'hello   '
SELECT RTRIM('   hello   ');   -- '   hello'

-- 获取左右字符
SELECT LEFT('Hello World', 5);   -- 'Hello'
SELECT RIGHT('Hello World', 5);  -- 'World'
```

### 17.5.2 日期时间函数

```sql
SELECT NOW();              -- 当前日期时间：2024-09-06 11:50:50
SELECT CURDATE();          -- 当前日期：2024-09-06
SELECT CURTIME();          -- 当前时间：11:50:50
SELECT DATE_FORMAT(NOW(), '%Y年%m月%d日');  -- 格式化日期
```

### 17.5.3 数值函数

```sql
SELECT ROUND(3.14159, 2);   -- 3.14（四舍五入）
SELECT FLOOR(3.9);          -- 3（向下取整）
SELECT CEILING(3.1);        -- 4（向上取整）
SELECT ABS(-5);             -- 5（绝对值）
SELECT RAND();              -- 随机数 0~1
```

### 17.5.4 条件函数

```sql
-- IF：条件判断
SELECT IF(age > 18, '成年', '未成年') FROM emp;

-- CASE WHEN：多条件判断
SELECT name,
    CASE
        WHEN salary < 500 THEN '低薪'
        WHEN salary < 1000 THEN '中薪'
        ELSE '高薪'
    END AS '薪资等级'
FROM emp;
```

## 17.6 流程控制

MySQL支持在存储过程和触发器中使用流程控制语句：

```sql
-- IF语句
IF 条件 THEN
    语句;
ELSEIF 条件 THEN
    语句;
ELSE
    语句;
END IF;

-- WHILE循环
DECLARE num INT DEFAULT 0;
WHILE num < 10 DO
    SET num = num + 1;
END WHILE;
```

## 17.7 索引（Index）

### 17.7.1 索引的概念

索引（也叫"键"）是存储引擎用于快速找到记录的**数据结构**。类似于书的目录，通过索引可以快速定位数据，而不需要全表扫描。

**索引的作用**：
- 大幅提高查询速度
- 数据量越大，索引的效果越明显
- 是查询性能优化最有效的手段

**索引的代价**：
- 占用额外的磁盘空间
- 插入、更新、删除操作需要同时维护索引，会降低写操作速度

### 17.7.2 索引类型

| 索引类型 | 创建方式 | 说明 |
|----------|----------|------|
| **主键索引** | `PRIMARY KEY` | 自动创建，唯一且不为空 |
| **唯一索引** | `UNIQUE` | 值必须唯一 |
| **普通索引** | `CREATE INDEX` | 最通用的索引 |
| **全文索引** | `FULLTEXT INDEX` | 用于文本搜索 |

### 17.7.3 索引操作

```sql
-- 查看表中的索引
SHOW INDEX FROM 表名;

-- 创建普通索引
CREATE INDEX 索引名 ON 表名(字段名);

-- 创建唯一索引
CREATE UNIQUE INDEX 索引名 ON 表名(字段名);

-- 删除索引
DROP INDEX 索引名 ON 表名;
```

**示例：**

```sql
-- 在emp表的name字段上创建索引
CREATE INDEX index_name ON emp(name);

-- 查看索引
SHOW INDEX FROM emp;
-- +-------+------------+------------+--------------+-------------+...
-- | Table | Non_unique | Key_name   | Seq_in_index | Column_name |...
-- +-------+------------+------------+--------------+-------------+...
-- | emp   |          0 | PRIMARY    |            1 | id          |...
-- | emp   |          1 | index_name |            1 | name        |...
-- +-------+------------+------------+--------------+-------------+...

-- 删除索引
DROP INDEX index_name ON emp;
```

### 17.7.4 索引的数据结构（B+树）

MySQL索引底层使用**B+树**数据结构：

**B+树的特点：**
- **平衡性**：所有叶子节点在同一层级，查询复杂度O(log n)
- **多路搜索**：每个节点可存储多个关键字
- **顺序访问**：叶子节点形成有序链表，支持范围查询
- **高存储利用率**：内部节点只存关键字不存数据

**在B+树中：**
- 只有叶子节点存放真实数据
- 根节点和内部节点只存索引信息
- 查询次数由树的层级决定，层级越低查询越快

### 17.7.5 聚集索引 vs 辅助索引（二级索引）

| 特性 | 聚集索引（主键索引） | 辅助索引（普通索引） |
|------|---------------------|---------------------|
| 数量 | 一个表只能有一个 | 一个表可以有多个 |
| 数据存储 | 叶子节点存储完整数据行 | 叶子节点存储主键值 |
| 物理顺序 | 决定数据的物理存储顺序 | 不影响物理存储顺序 |
| 查询方式 | 找到索引即找到数据 | 找到主键后再回表查询 |
| 自动创建 | 主键自动创建 | 需手动创建 |

> **InnoDB 主键选取规则**：①若显式定义了 `PRIMARY KEY`，则用它作为聚簇索引；②否则选择第一个非空 `UNIQUE` 索引；③仍没有时，InnoDB 会生成一个隐藏的 6 字节 `ROW_ID` 作为聚簇索引。
>
> **为什么主键推荐自增整型？** 自增主键能保证新行始终追加到 B+ 树的最右端，避免页分裂；而 UUID/字符串主键随机分布，会频繁触发页分裂和回表，写入性能差。

#### 回表（Bookmark Lookup）示意

```
查询语句：SELECT * FROM emp WHERE name = '张三';

1. 在 idx_name（辅助索引）的 B+ 树中查找 '张三' → 拿到主键 id = 100
2. 拿 id = 100 回到聚簇索引（主键 B+ 树）中查找完整行 → 得到 *
   ↑ 这一步就是"回表"
```

### 17.7.6 覆盖索引（Covering Index）

如果一个查询所需的全部字段都能从某个索引的叶子节点直接取得，**无需回表**，这种现象称为**覆盖索引**。是 SQL 优化中最重要的技巧之一。

```sql
-- 假设有联合索引 idx_name_age ON emp(name, age)

-- 案例 1：覆盖索引，EXPLAIN 中 Extra 显示 "Using index"
SELECT name, age FROM emp WHERE name = '张三';

-- 案例 2：需要回表，EXPLAIN 中 Extra 不会显示 "Using index"
SELECT * FROM emp WHERE name = '张三';

-- 案例 3：经典优化——避免 SELECT *，只 SELECT 需要的字段
-- 慢：SELECT * FROM emp ORDER BY age LIMIT 100000, 10;
-- 快：SELECT * FROM emp WHERE id IN (
--        SELECT id FROM emp ORDER BY age LIMIT 100000, 10
--      );
```

### 17.7.7 联合索引与最左前缀原则

联合索引（Composite Index）指多列组成一个索引，B+ 树按"列1 → 列2 → 列3"依次排序。

```sql
-- 创建联合索引
CREATE INDEX idx_multi ON emp(name, age, dep_id);
```

**最左前缀原则**：查询能否命中联合索引，取决于 WHERE 条件是否从最左列开始连续使用：

| WHERE 条件 | 是否命中 idx_multi | 说明 |
|---|---|---|
| `WHERE name = ?` | ✅ 命中 (name) | 最左列 |
| `WHERE name = ? AND age = ?` | ✅ 命中 (name, age) | 连续 |
| `WHERE name = ? AND age = ? AND dep_id = ?` | ✅ 完全命中 | 三列全部使用 |
| `WHERE age = ?` | ❌ 不命中 | 跳过了 name |
| `WHERE name = ? AND dep_id = ?` | ⚠️ 仅命中 (name) | dep_id 部分不走索引 |
| `WHERE name LIKE '张%'` | ✅ 命中 | 前缀模糊 |
| `WHERE name LIKE '%张'` | ❌ 不命中 | 后缀模糊导致全表扫描 |

> **优化器顺序无关**：`WHERE age = 18 AND name = '张三'` 与 `WHERE name = '张三' AND age = 18` 等价，优化器会自动调整顺序。但**索引中字段的物理顺序**必须从左到右连续使用。

### 17.7.8 索引失效的常见场景

```sql
-- 1. 对索引列使用函数 / 表达式 → 失效
SELECT * FROM emp WHERE YEAR(create_time) = 2025;     -- ❌
SELECT * FROM emp
 WHERE create_time >= '2025-01-01'
   AND create_time <  '2026-01-01';                   -- ✅ 改写

-- 2. 隐式类型转换 → 失效
-- name 是 VARCHAR，下式会把整个列转 INT 比较
SELECT * FROM emp WHERE name = 123;                   -- ❌

-- 3. 前导模糊查询 → 失效
SELECT * FROM emp WHERE name LIKE '%张%';             -- ❌（全文索引或 ES 解决）

-- 4. OR 连接的字段中有未建索引的列 → 整体失效
SELECT * FROM emp WHERE name = '张三' OR remark = 'x';-- ❌（remark 未建索引）

-- 5. != 、 <> 、 NOT IN 等否定条件通常无法用 B+ 树定位
SELECT * FROM emp WHERE age != 30;                    -- ❌

-- 6. IS NULL / IS NOT NULL 在不同 MySQL 版本表现不同，5.7+ 大多可走索引

-- 7. 索引列上做计算
SELECT * FROM emp WHERE age + 1 = 30;                 -- ❌
SELECT * FROM emp WHERE age = 29;                     -- ✅
```

### 17.7.9 EXPLAIN 执行计划

`EXPLAIN` 是 SQL 调优必须掌握的工具，它显示 MySQL 优化器如何执行查询：

```sql
EXPLAIN SELECT * FROM emp WHERE name = '张三';
```

输出关键列说明：

| 列名 | 含义 | 关注点 |
|------|------|--------|
| `id` | 查询的序列号 | 多表 / 子查询时表示执行顺序 |
| `select_type` | 查询类型 | SIMPLE / PRIMARY / SUBQUERY / DERIVED |
| `table` | 涉及的表 | — |
| `type` | **访问类型（最重要）** | system > const > eq_ref > ref > range > index > **ALL（全表扫描，需优化）** |
| `possible_keys` | 可能用到的索引 | — |
| `key` | **实际使用的索引** | NULL 表示未走索引 |
| `key_len` | 索引使用的字节数 | 越短越好，可判断联合索引用了几列 |
| `rows` | 预计扫描行数 | 越少越好 |
| `Extra` | 附加信息 | `Using index`（覆盖索引，✅好）<br>`Using where`（用 WHERE 过滤）<br>`Using filesort`（额外排序，⚠️）<br>`Using temporary`（临时表，⚠️） |

**type 列的优劣（从优到劣）**：

```
system → const → eq_ref → ref → range → index → ALL
  ↑ 最快                                          ↑ 全表扫描，性能最差
```

### 17.7.10 PyMySQL 配合 EXPLAIN 示例

```python
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='123456', database='test', charset='utf8mb4')
cursor = conn.cursor(pymysql.cursors.DictCursor)

# 用 EXPLAIN 分析查询
cursor.execute("EXPLAIN SELECT * FROM emp WHERE name = %s", ('张三',))
plan = cursor.fetchall()
for row in plan:
    print(f"type={row['type']}, key={row['key']}, "
          f"rows={row['rows']}, Extra={row['Extra']}")

# 如果 type=ALL 或 key=None，提示考虑加索引
if plan and (plan[0]['type'] == 'ALL' or plan[0]['key'] is None):
    print("⚠️ 该 SQL 未走索引，建议优化")

cursor.close()
conn.close()
```

### 17.7.11 索引设计原则

1. **为高频 WHERE / JOIN / ORDER BY 字段建索引**
2. **区分度低的字段不建索引**（如性别只有 2 个值，扫描代价≈全表）
3. **写多读少的表慎加索引**（每个索引都会拖慢 INSERT/UPDATE/DELETE）
4. **优先使用联合索引覆盖多条件查询**，比建多个单列索引更高效
5. **联合索引把区分度高的列放左边**
6. **字符串字段过长时使用前缀索引**：`CREATE INDEX idx_email ON user(email(20))`
7. **定期检查并删除冗余索引**：`(a)` 与 `(a, b)` 同时存在时 `(a)` 是冗余的

## 17.8 事务隔离级别

### 17.8.1 事务的 ACID 特性回顾

| 特性 | 含义 |
|------|------|
| **A** Atomicity（原子性） | 事务内所有操作要么全成功、要么全回滚，不存在中间状态 |
| **C** Consistency（一致性） | 事务执行前后数据库都处于一致状态（业务约束不被破坏） |
| **I** Isolation（隔离性） | 并发事务之间相互隔离，不应互相干扰 |
| **D** Durability（持久性） | 事务一旦提交，对数据库的修改是永久的（依赖 redo log） |

> 隔离级别就是**对 I（Isolation）做出不同强度的承诺**——隔离性越强，并发性越差。

### 17.8.2 数据库三大读现象

在高并发场景下，多个事务同时执行可能产生以下问题：

| 现象 | 说明 | 示例 |
|------|------|------|
| **脏读（Dirty Read）** | 读到其他事务**未提交**的数据 | 事务A改了数据，事务B读到，事务A回滚，B读到的数据是无效的 |
| **不可重复读（Non-Repeatable Read）** | 同一事务内两次**单行读取**结果不同 | 事务A读取后，事务B修改并提交，事务A再次读取结果变化 |
| **幻读（Phantom Read）** | 同一**范围查询**两次执行返回的行集合不同 | 事务A查询后，事务B插入新数据并提交，事务A再次查询发现多了行 |

**不可重复读 vs 幻读区别**：
- 不可重复读 = 同一行的"值"变了（UPDATE 引起）
- 幻读 = 同一范围的"行数"变了（INSERT/DELETE 引起）

### 17.8.3 四种隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 并发性能 |
|----------|------|-----------|------|----------|
| **READ UNCOMMITTED**（读未提交） | ❌ 可能 | ❌ 可能 | ❌ 可能 | 最高 |
| **READ COMMITTED**（读已提交） | ✅ 不会 | ❌ 可能 | ❌ 可能 | 较高 |
| **REPEATABLE READ**（可重复读，**MySQL InnoDB 默认**） | ✅ 不会 | ✅ 不会 | ⚠️ 标准协议中可能，InnoDB 通过 Next-Key Lock 已解决 | 中等 |
| **SERIALIZABLE**（串行化） | ✅ 不会 | ✅ 不会 | ✅ 不会 | 最低 |

> **重要差异**：Oracle / PostgreSQL 默认 `READ COMMITTED`；MySQL InnoDB 默认 `REPEATABLE READ`，这是因为早期 MySQL 主从复制基于 statement-based binlog，RR 才能保证主从一致。

### 17.8.4 查看和设置隔离级别

```sql
-- 查看当前会话的隔离级别（MySQL 8.0+）
SELECT @@transaction_isolation;
-- MySQL 5.7 用：SELECT @@tx_isolation;

-- 查看全局隔离级别
SELECT @@global.transaction_isolation;

-- 设置当前会话的隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- 设置全局隔离级别（需 SUPER 权限）
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 17.8.5 三大读现象的复现演示

打开两个 MySQL 客户端窗口（分别记为会话 A 和会话 B），准备数据：

```sql
CREATE TABLE account (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    balance DECIMAL(10,2)
) ENGINE=InnoDB;

INSERT INTO account VALUES (1, '张三', 1000);
```

**(1) 复现脏读（隔离级别设为 READ UNCOMMITTED）**：

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
SELECT balance FROM account WHERE id = 1;  -- 1000

-- 会话 B（不提交！）
START TRANSACTION;
UPDATE account SET balance = 500 WHERE id = 1;

-- 会话 A 再读
SELECT balance FROM account WHERE id = 1;  -- 500 ← 脏读！B 还没提交

-- 会话 B
ROLLBACK;  -- 会话 A 读到的 500 是无效数据
```

**(2) 复现不可重复读（READ COMMITTED 下）**：

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM account WHERE id = 1;  -- 1000

-- 会话 B
START TRANSACTION;
UPDATE account SET balance = 800 WHERE id = 1;
COMMIT;

-- 会话 A
SELECT balance FROM account WHERE id = 1;  -- 800 ← 同一事务内两次读取不同！
```

**(3) REPEATABLE READ 下不可重复读消失**：

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT balance FROM account WHERE id = 1;  -- 1000

-- 会话 B 修改并提交
START TRANSACTION;
UPDATE account SET balance = 600 WHERE id = 1;
COMMIT;

-- 会话 A 再读
SELECT balance FROM account WHERE id = 1;  -- 仍是 1000！MVCC 保证可重复读
```

### 17.8.6 MVCC（多版本并发控制）简介

InnoDB 在 `READ COMMITTED` 和 `REPEATABLE READ` 下通过 **MVCC**（Multi-Version Concurrency Control）实现"非阻塞读"。

**核心思想**：每行数据维护**多个历史版本**，事务读取时看到的是某个时间点的"快照"，而不是最新值。

**实现要素**：

| 元素 | 作用 |
|------|------|
| `DB_TRX_ID`（6字节）| 隐藏字段：最后一次修改该行的事务 ID |
| `DB_ROLL_PTR`（7字节）| 隐藏字段：回滚指针，指向 undo log 中的历史版本 |
| `undo log` | 存放数据的历史版本链 |
| `Read View` | 事务开启时生成的"快照视图"，决定哪些版本可见 |

**两种隔离级别下 Read View 的生成时机不同**：
- `READ COMMITTED`：**每次 SELECT 都生成新的 Read View** → 因此能看到其他已提交事务的最新数据 → 出现不可重复读
- `REPEATABLE READ`：**事务的第一次 SELECT 生成 Read View，之后整个事务复用** → 因此整个事务内读到的都是同一份快照 → 不可重复读消失

**可见性规则**（简化版）：对某行的某个版本，如果其 `DB_TRX_ID`：
- 小于 Read View 中的最小活跃事务 ID → 可见（已提交且早于当前事务）
- 大于等于最大事务 ID → 不可见（在当前 Read View 之后才出现）
- 处于活跃事务集合中 → 不可见（未提交）
- 否则 → 可见（已提交）

### 17.8.7 InnoDB 如何解决幻读：Next-Key Lock

按 SQL 标准，REPEATABLE READ 不能防止幻读。但 **InnoDB 在 RR 级别下通过锁机制额外解决了幻读**：

| 锁类型 | 锁定范围 |
|--------|----------|
| **Record Lock**（记录锁） | 锁定**索引上的一条记录** |
| **Gap Lock**（间隙锁） | 锁定**索引记录之间的间隙**，防止其他事务在间隙中 INSERT |
| **Next-Key Lock** | Record Lock + Gap Lock 的组合，锁住一条记录及其前面的间隙 |

**示例**：表中有 id = 10, 20, 30 三行。

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM account WHERE id BETWEEN 10 AND 25 FOR UPDATE;
-- 此时 InnoDB 会锁住 (−∞, 10], (10, 20], (20, 30) 这些区间

-- 会话 B
INSERT INTO account VALUES (15, '李四', 500);
-- ⛔ 会被阻塞！因为 (10, 20] 被 Next-Key Lock 锁住了
```

> **注意**：
> - Next-Key Lock 仅在**当前读**（SELECT ... FOR UPDATE / LOCK IN SHARE MODE / UPDATE / DELETE）下生效。
> - 普通 `SELECT` 是**快照读**，靠 MVCC 解决幻读问题。
> - 这是 InnoDB 比标准 SQL 协议更强的承诺。

### 17.8.8 当前读 vs 快照读

| 类型 | 触发语句 | 数据来源 |
|------|---------|----------|
| **快照读** | 普通 `SELECT` | MVCC 历史版本 |
| **当前读** | `SELECT ... LOCK IN SHARE MODE`<br>`SELECT ... FOR UPDATE`<br>`UPDATE` / `DELETE` / `INSERT` | 最新已提交版本 + 加锁 |

理解这两种读的区别是判断"是否会出现幻读"的关键：
- RR 级别下普通 SELECT 永远看不到幻行 → 由 MVCC 保证
- RR 级别下当前读 + Next-Key Lock 防止其他事务插入 → 也看不到幻行

## 17.9 锁机制

### 17.9.1 什么是锁

当多个事务同时操作同一份数据时，锁机制确保同一时间只有一个事务能操作数据，保证数据安全性。锁会降低并发效率，但保证了数据的安全。

### 17.9.2 锁的分类

**按粒度分：**
| 类型 | 锁定范围 | 并发度 |
|------|----------|--------|
| 行级锁 | 锁定一行 | 高 |
| 表级锁 | 锁定整张表 | 低 |
| 页级锁 | 锁定一个数据页 | 中 |

InnoDB支持行级锁和表级锁，MyISAM只支持表级锁。

**按级别分：**
| 类型 | 说明 |
|------|------|
| 共享锁（S锁/读锁） | 多个事务可同时读，但不能写 |
| 排他锁（X锁/写锁） | 只能一个事务持有，其他事务不能读写 |

**按使用方式分：**
| 类型 | 策略 | 实现方式 |
|------|------|----------|
| 乐观锁 | 认为冲突少，更新时检查 | 版本号机制 |
| 悲观锁 | 认为冲突多，操作前加锁 | SELECT ... FOR UPDATE |

## 17.10 数据库三大范式

### 17.10.1 第一范式（1NF）

**要求**：确保**原子性**，每个字段的值不可再分割。

```sql
-- 不符合1NF（student字段包含多个信息）
+----------------------+--------+-------+
| student              | course | score |
+----------------------+--------+-------+
| 蚩梦，男，185cm       | 语文   |    95 |
+----------------------+--------+-------+

-- 符合1NF（拆分为独立字段）
+--------------+-------------+----------------+--------+-------+
| student_name | student_sex | student_height | course | score |
+--------------+-------------+----------------+--------+-------+
| 蚩梦          | 男          | 185cm          | 语文   |    95 |
+--------------+-------------+----------------+--------+-------+
```

### 17.10.2 第二范式（2NF）

**要求**：在满足1NF的基础上，确保**唯一性**，一张表只描述一种业务属性。所有非主键列必须完全依赖于主键。

```sql
-- 不符合2NF：学生信息和成绩混在一起，course和score不直接依赖student主键
-- 拆分为：学生表 + 课程表 + 成绩表

-- 学生表
+----+--------------+-------------+----------------+
| id | student_name | student_sex | student_height |
+----+--------------+-------------+----------------+

-- 课程表
+-----------+-------------+
| course_id | course_name |
+-----------+-------------+

-- 成绩表
+----+------------+-----------+-------+
| id | student_id | course_id | score |
+----+------------+-----------+-------+
```

### 17.10.3 第三范式（3NF）

**要求**：在满足2NF的基础上，确保**独立性**。非主键列之间不能存在传递依赖，必须和主键直接相关。

```sql
-- 不符合3NF：dean（系主任）与student_id无直接关系，
-- dean依赖于department而非student_id
+------------+--------+------+--------+--------------+--------------+
| student_id | name   | sex  | height | department   | dean         |
+------------+--------+------+--------+--------------+--------------+

-- 符合3NF：拆分出独立的部门表

-- 学生表
+------------+--------+------+--------+---------------+
| student_id | name   | sex  | height | department_id |
+------------+--------+------+--------+---------------+

-- 部门表
+---------------+-----------------+-----------------+
| department_id | department_name | department_dean |
+---------------+-----------------+-----------------+
```

### 17.10.4 三范式总结

| 范式 | 核心要求 | 解决问题 |
|------|----------|----------|
| 第一范式（1NF） | 字段原子性，不可再分 | 数据冗余 |
| 第二范式（2NF） | 一张表只描述一件事 | 数据冗余和更新异常 |
| 第三范式（3NF） | 非主键列之间无传递依赖 | 数据冗余和更新异常 |

**遵循三范式的好处：**
- 减少数据冗余
- 避免更新异常（修改一处即可）
- 表结构更清晰优雅
- 灵活性和扩展性更强

**反范式化（适度冗余）：**
在实际开发中，有时为了查询性能，会适当地做一些冗余设计（以空间换时间），但核心结构仍应遵循范式原则。

---

# 第十八部分：快速参考

## 18.1 数据库操作速查

```sql
-- 数据库操作
CREATE DATABASE IF NOT EXISTS 库名 CHARSET utf8mb4;   -- 创建
SHOW DATABASES;                                        -- 查看所有
SHOW CREATE DATABASE 库名;                             -- 查看创建语句
ALTER DATABASE 库名 CHARSET 'utf8mb4';                 -- 修改编码
DROP DATABASE IF EXISTS 库名;                          -- 删除
USE 库名;                                              -- 切换
SELECT DATABASE();                                     -- 查看当前库
```

## 18.2 表操作速查

```sql
-- 表操作
CREATE TABLE 表名 (字段定义...);                        -- 创建
SHOW TABLES;                                           -- 查看所有表
SHOW CREATE TABLE 表名;                                -- 查看创建语句
DESC 表名;                                             -- 查看结构
ALTER TABLE 表名 ADD/MODIFY/DROP/CHANGE ...;           -- 修改
DROP TABLE IF EXISTS 表名;                             -- 删除
TRUNCATE TABLE 表名;                                   -- 清空数据
```

## 18.3 数据操作速查

```sql
-- 数据操作
INSERT INTO 表名 (字段...) VALUES (值...);             -- 插入
SELECT 字段 FROM 表名 WHERE 条件;                      -- 查询
UPDATE 表名 SET 字段=值 WHERE 条件;                    -- 更新
DELETE FROM 表名 WHERE 条件;                           -- 删除
```

## 18.4 查询子句速查

```sql
SELECT [DISTINCT] 字段名
FROM 表名
[INNER/LEFT/RIGHT JOIN 表名 ON 条件]
[WHERE 条件]
[GROUP BY 分组字段]
[HAVING 分组后条件]
[ORDER BY 排序字段 ASC/DESC]
[LIMIT 起始索引, 条数];
```

## 18.5 聚合函数速查

```sql
COUNT(字段)    -- 计数（忽略NULL）
SUM(字段)      -- 求和
AVG(字段)      -- 平均值
MAX(字段)      -- 最大值
MIN(字段)      -- 最小值
```

## 18.6 PyMySQL速查

```python
# 连接
conn = pymysql.connect(user='root', password='pwd', host='127.0.0.1',
                       port=3306, database='db', charset='utf8mb4',
                       cursorclass=DictCursor, autocommit=False)
cursor = conn.cursor()

# CRUD
cursor.execute(sql, params)       # 执行单条
cursor.executemany(sql, params)   # 批量执行
cursor.fetchone()                 # 获取一条
cursor.fetchall()                 # 获取全部
cursor.fetchmany(size=n)          # 获取n条
conn.commit()                     # 提交事务
conn.rollback()                   # 回滚事务

# 关闭
cursor.close()
conn.close()
```

---

# 附录：综合实践案例

## A.1 员工管理系统（PyMySQL + MySQL）

以下是一个完整的员工管理系统示例，整合了数据库设计、PyMySQL操作、SQL查询等知识点：

### A.1.1 数据库准备

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS emp_system CHARSET utf8mb4;
USE emp_system;

-- 部门表
CREATE TABLE department (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '部门编号',
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '部门名称',
    create_time DATETIME DEFAULT NOW() COMMENT '创建时间'
);

-- 员工表
CREATE TABLE employee (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '员工编号',
    name VARCHAR(32) NOT NULL COMMENT '员工姓名',
    age TINYINT UNSIGNED NOT NULL COMMENT '员工年龄',
    gender ENUM('male', 'female') NOT NULL COMMENT '员工性别',
    phone VARCHAR(11) COMMENT '手机号',
    salary DECIMAL(10, 2) NOT NULL DEFAULT 0 COMMENT '薪资',
    hire_date DATE NOT NULL COMMENT '入职日期',
    dept_id INT COMMENT '所属部门',
    FOREIGN KEY (dept_id) REFERENCES department(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 管理员表
CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

-- 插入测试数据
INSERT INTO department (name) VALUES ('技术部'), ('市场部'), ('人事部'), ('财务部');

INSERT INTO employee (name, age, gender, phone, salary, hire_date, dept_id) VALUES
('张三', 28, 'male', '13800138001', 15000.00, '2020-03-15', 1),
('李四', 32, 'male', '13800138002', 18000.00, '2019-07-01', 1),
('王五', 25, 'female', '13800138003', 12000.00, '2021-06-20', 2),
('赵六', 30, 'female', '13800138004', 14000.00, '2018-11-10', 2),
('孙七', 35, 'male', '13800138005', 20000.00, '2017-01-05', 1),
('周八', 27, 'female', '13800138006', 10000.00, '2022-09-01', 3),
('吴九', 29, 'male', '13800138007', 13000.00, '2020-05-18', 3),
('郑十', 33, 'male', '13800138008', 16000.00, '2019-12-25', 4);

INSERT INTO admin (username, password) VALUES ('admin', '123456');
```

### A.1.2 Python代码实现

```python
"""
员工管理系统 - 基于PyMySQL和MySQL数据库实现
功能：
  1. 管理员登录
  2. 员工信息增删改查
  3. 部门信息管理
  4. 统计报表
"""
import pymysql
from pymysql.cursors import DictCursor
from datetime import date
import hashlib


class EmployeeSystem:
    """员工管理系统核心类"""

    def __init__(self):
        """初始化数据库连接"""
        self.conn = pymysql.connect(
            user='root',
            password='你的密码',
            host='127.0.0.1',
            port=3306,
            database='emp_system',
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=False
        )
        self.cursor = self.conn.cursor()
        self.current_user = None

    # ==================== 管理员登录 ====================

    def login(self, username, password):
        """管理员登录验证（使用参数化查询防止SQL注入）"""
        sql = 'SELECT id, username FROM admin WHERE username = %(username)s AND password = %(password)s;'
        self.cursor.execute(sql, {'username': username, 'password': password})
        result = self.cursor.fetchone()
        if result:
            self.current_user = result
            return True
        return False

    # ==================== 员工管理 ====================

    def get_all_employees(self):
        """查询所有员工（联合部门表）"""
        sql = '''
            SELECT e.id, e.name, e.age, e.gender, e.phone,
                   e.salary, e.hire_date, d.name AS dept_name
            FROM employee e
            LEFT JOIN department d ON e.dept_id = d.id
            ORDER BY e.id;
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_employee_by_id(self, emp_id):
        """根据ID查询员工"""
        sql = '''
            SELECT e.id, e.name, e.age, e.gender, e.phone,
                   e.salary, e.hire_date, d.name AS dept_name
            FROM employee e
            LEFT JOIN department d ON e.dept_id = d.id
            WHERE e.id = %(id)s;
        '''
        self.cursor.execute(sql, {'id': emp_id})
        return self.cursor.fetchone()

    def search_employees(self, keyword):
        """模糊搜索员工（按姓名或手机号）"""
        sql = '''
            SELECT e.id, e.name, e.age, e.gender, e.phone,
                   e.salary, e.hire_date, d.name AS dept_name
            FROM employee e
            LEFT JOIN department d ON e.dept_id = d.id
            WHERE e.name LIKE %(keyword)s OR e.phone LIKE %(keyword)s
            ORDER BY e.id;
        '''
        self.cursor.execute(sql, {'keyword': f'%{keyword}%'})
        return self.cursor.fetchall()

    def add_employee(self, name, age, gender, phone, salary, hire_date, dept_id=None):
        """添加员工"""
        sql = '''
            INSERT INTO employee (name, age, gender, phone, salary, hire_date, dept_id)
            VALUES (%(name)s, %(age)s, %(gender)s, %(phone)s, %(salary)s, %(hire_date)s, %(dept_id)s);
        '''
        self.cursor.execute(sql, {
            'name': name, 'age': age, 'gender': gender,
            'phone': phone, 'salary': salary,
            'hire_date': hire_date, 'dept_id': dept_id
        })
        self.conn.commit()
        return self.cursor.lastrowid  # 返回新插入的ID

    def update_employee(self, emp_id, **kwargs):
        """更新员工信息"""
        allowed_fields = ['name', 'age', 'gender', 'phone', 'salary', 'hire_date', 'dept_id']
        updates = []
        params = {'id': emp_id}

        for field in allowed_fields:
            if field in kwargs and kwargs[field] is not None:
                updates.append(f'{field} = %({field})s')
                params[field] = kwargs[field]

        if not updates:
            return 0

        sql = f"UPDATE employee SET {', '.join(updates)} WHERE id = %(id)s;"
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount

    def delete_employee(self, emp_id):
        """删除员工"""
        sql = 'DELETE FROM employee WHERE id = %(id)s;'
        self.cursor.execute(sql, {'id': emp_id})
        self.conn.commit()
        return self.cursor.rowcount

    # ==================== 部门管理 ====================

    def get_all_departments(self):
        """查询所有部门"""
        sql = 'SELECT * FROM department ORDER BY id;'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_department(self, name):
        """添加部门"""
        sql = 'INSERT INTO department (name) VALUES (%(name)s);'
        self.cursor.execute(sql, {'name': name})
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_department(self, dept_id):
        """删除部门（级联将员工dept_id设为NULL）"""
        sql = 'DELETE FROM department WHERE id = %(id)s;'
        self.cursor.execute(sql, {'id': dept_id})
        self.conn.commit()
        return self.cursor.rowcount

    # ==================== 统计报表 ====================

    def get_dept_statistics(self):
        """部门人数和平均薪资统计"""
        sql = '''
            SELECT d.name AS dept_name,
                   COUNT(e.id) AS emp_count,
                   IFNULL(AVG(e.salary), 0) AS avg_salary,
                   IFNULL(SUM(e.salary), 0) AS total_salary
            FROM department d
            LEFT JOIN employee e ON d.id = e.dept_id
            GROUP BY d.id, d.name
            ORDER BY emp_count DESC;
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_gender_statistics(self):
        """性别统计"""
        sql = '''
            SELECT gender,
                   COUNT(*) AS count,
                   AVG(salary) AS avg_salary
            FROM employee
            GROUP BY gender;
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_salary_ranking(self, top_n=10):
        """薪资排名"""
        sql = '''
            SELECT name, salary, d.name AS dept_name
            FROM employee e
            LEFT JOIN department d ON e.dept_id = d.id
            ORDER BY salary DESC
            LIMIT %(n)s;
        '''
        self.cursor.execute(sql, {'n': top_n})
        return self.cursor.fetchall()

    # ==================== 工具方法 ====================

    def md5(self, text):
        """MD5加密"""
        return hashlib.md5(text.encode()).hexdigest()

    def close(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


# ==================== 主程序 ====================

def print_menu():
    """打印功能菜单"""
    print('\n' + '=' * 50)
    print('  员工管理系统')
    print('=' * 50)
    print('  1. 查看所有员工')
    print('  2. 搜索员工')
    print('  3. 添加员工')
    print('  4. 修改员工')
    print('  5. 删除员工')
    print('  6. 部门管理')
    print('  7. 统计报表')
    print('  0. 退出系统')
    print('=' * 50)


def main():
    """主程序入口"""
    system = EmployeeSystem()

    # 登录验证
    print('欢迎使用员工管理系统')
    for i in range(3):  # 最多3次登录机会
        username = input('用户名: ').strip()
        password = input('密  码: ').strip()
        if system.login(username, password):
            print('登录成功!')
            break
        else:
            print(f'用户名或密码错误，还有{2 - i}次机会')
    else:
        print('登录失败次数过多，系统退出')
        system.close()
        return

    # 主循环
    while True:
        print_menu()
        choice = input('请选择操作: ').strip()

        if choice == '1':
            # 查看所有员工
            employees = system.get_all_employees()
            print(f'\n共找到 {len(employees)} 名员工:')
            print('-' * 80)
            print(f'{"ID":<5}{"姓名":<10}{"年龄":<6}{"性别":<8}{"电话":<15}{"薪资":<12}{"部门":<12}{"入职日期":<12}')
            print('-' * 80)
            for emp in employees:
                print(f'{emp["id"]:<5}{emp["name"]:<10}{emp["age"]:<6}{emp["gender"]:<8}'
                      f'{emp["phone"] or "N/A":<15}{emp["salary"]:<12.2f}'
                      f'{emp["dept_name"] or "未分配":<12}{str(emp["hire_date"]):<12}')
            print('-' * 80)

        elif choice == '2':
            # 搜索员工
            keyword = input('请输入搜索关键词(姓名/电话): ').strip()
            results = system.search_employees(keyword)
            print(f'\n搜索结果: 找到 {len(results)} 条记录')
            for emp in results:
                print(f'  [{emp["id"]}] {emp["name"]} - {emp["phone"]} - {emp["dept_name"]}')

        elif choice == '3':
            # 添加员工
            print('\n--- 添加新员工 ---')
            name = input('姓名: ').strip()
            age = int(input('年龄: ').strip())
            gender = input('性别(male/female): ').strip()
            phone = input('手机号: ').strip()
            salary = float(input('薪资: ').strip())
            hire_date = input('入职日期(YYYY-MM-DD): ').strip()
            dept_id = input('部门ID(可选): ').strip()
            dept_id = int(dept_id) if dept_id else None

            new_id = system.add_employee(name, age, gender, phone, salary, hire_date, dept_id)
            print(f'添加成功! 新员工ID: {new_id}')

        elif choice == '4':
            # 修改员工
            emp_id = int(input('请输入要修改的员工ID: ').strip())
            emp = system.get_employee_by_id(emp_id)
            if not emp:
                print('员工不存在!')
                continue

            print(f'当前信息: {emp}')
            print('请输入新值(直接回车保留原值):')

            name = input(f'姓名 [{emp["name"]}]: ').strip()
            age = input(f'年龄 [{emp["age"]}]: ').strip()
            phone = input(f'手机号 [{emp["phone"]}]: ').strip()
            salary = input(f'薪资 [{emp["salary"]}]: ').strip()

            kwargs = {}
            if name: kwargs['name'] = name
            if age: kwargs['age'] = int(age)
            if phone: kwargs['phone'] = phone
            if salary: kwargs['salary'] = float(salary)

            if kwargs:
                system.update_employee(emp_id, **kwargs)
                print('修改成功!')

        elif choice == '5':
            # 删除员工
            emp_id = int(input('请输入要删除的员工ID: ').strip())
            confirm = input(f'确认删除员工ID={emp_id}? (yes/no): ').strip()
            if confirm.lower() == 'yes':
                count = system.delete_employee(emp_id)
                print(f'删除成功! 影响了 {count} 条数据')

        elif choice == '6':
            # 部门管理
            print('\n--- 部门列表 ---')
            depts = system.get_all_departments()
            for d in depts:
                print(f'  ID:{d["id"]} - {d["name"]}')

            sub = input('\n1.添加部门 2.删除部门: ').strip()
            if sub == '1':
                name = input('部门名称: ').strip()
                system.add_department(name)
                print('添加成功!')
            elif sub == '2':
                dept_id = int(input('部门ID: ').strip())
                confirm = input(f'确认删除? 该部门下员工将变为未分配 (yes/no): ').strip()
                if confirm.lower() == 'yes':
                    system.delete_department(dept_id)
                    print('删除成功!')

        elif choice == '7':
            # 统计报表
            print('\n--- 部门统计 ---')
            for row in system.get_dept_statistics():
                print(f'  {row["dept_name"]}: {row["emp_count"]}人, '
                      f'平均薪资 {row["avg_salary"]:.2f}, 总薪资 {row["total_salary"]:.2f}')

            print('\n--- 性别统计 ---')
            for row in system.get_gender_statistics():
                gender = '男' if row['gender'] == 'male' else '女'
                print(f'  {gender}: {row["count"]}人, 平均薪资 {row["avg_salary"]:.2f}')

            print('\n--- 薪资TOP5 ---')
            for i, row in enumerate(system.get_salary_ranking(5), 1):
                print(f'  {i}. {row["name"]} - {row["salary"]:.2f} ({row["dept_name"]})')

        elif choice == '0':
            print('感谢使用，再见!')
            break

    system.close()


if __name__ == '__main__':
    main()
```

## A.2 常用SQL面试题与解答

### 1. 查询每个部门薪资最高的员工信息

```sql
-- 方法一：子查询
SELECT e.*, d.name AS dept_name
FROM employee e
INNER JOIN department d ON e.dept_id = d.id
WHERE e.salary = (
    SELECT MAX(salary)
    FROM employee
    WHERE dept_id = e.dept_id
);

-- 方法二：联表 + 分组
SELECT e.*, d.name AS dept_name
FROM employee e
INNER JOIN department d ON e.dept_id = d.id
INNER JOIN (
    SELECT dept_id, MAX(salary) AS max_salary
    FROM employee
    GROUP BY dept_id
) t ON e.dept_id = t.dept_id AND e.salary = t.max_salary;
```

### 2. 查询薪资高于部门平均薪资的员工

```sql
SELECT e.name, e.salary, d.name AS dept_name,
       ROUND(t.avg_salary, 2) AS dept_avg
FROM employee e
INNER JOIN department d ON e.dept_id = d.id
INNER JOIN (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employee
    GROUP BY dept_id
) t ON e.dept_id = t.dept_id
WHERE e.salary > t.avg_salary
ORDER BY e.salary DESC;
```

### 3. 查询入职超过3年的员工（使用日期函数）

```sql
SELECT name, hire_date,
       DATEDIFF(NOW(), hire_date) AS work_days,
       TIMESTAMPDIFF(YEAR, hire_date, NOW()) AS work_years
FROM employee
WHERE TIMESTAMPDIFF(YEAR, hire_date, NOW()) > 3
ORDER BY hire_date;
```

### 4. 分页查询员工列表（每页5条，第2页）

```sql
-- 第N页 = LIMIT (N-1)*pageSize, pageSize
SELECT e.id, e.name, e.salary, d.name AS dept_name
FROM employee e
LEFT JOIN department d ON e.dept_id = d.id
ORDER BY e.id
LIMIT 5, 5;  -- 第2页：(2-1)*5=5 作为起始索引
```

### 5. 批量更新 - 给入职超过5年的员工涨薪10%

```sql
UPDATE employee
SET salary = salary * 1.1
WHERE TIMESTAMPDIFF(YEAR, hire_date, NOW()) > 5;
```

### 6. 查询没有分配部门的员工

```sql
SELECT * FROM employee WHERE dept_id IS NULL;
```

### 7. 查询每个部门的男女员工数量（行转列）

```sql
SELECT d.name AS dept_name,
       SUM(CASE WHEN e.gender = 'male' THEN 1 ELSE 0 END) AS male_count,
       SUM(CASE WHEN e.gender = 'female' THEN 1 ELSE 0 END) AS female_count
FROM department d
LEFT JOIN employee e ON d.id = e.dept_id
GROUP BY d.id, d.name;
```

## A.3 PyMySQL 事务使用示例（转账场景）

```python
def transfer_money(self, from_user, to_user, amount):
    """
    转账操作 - 演示事务的原子性
    要么两边都成功，要么都回滚
    """
    try:
        # 开启事务（autocommit=False时默认已开启）

        # 1. 检查转出方余额
        sql_check = 'SELECT balance FROM account WHERE username = %(username)s FOR UPDATE;'
        self.cursor.execute(sql_check, {'username': from_user})
        result = self.cursor.fetchone()

        if not result or result['balance'] < amount:
            raise Exception('余额不足或用户不存在')

        # 2. 转出方扣款
        sql_out = 'UPDATE account SET balance = balance - %(amount)s WHERE username = %(username)s;'
        self.cursor.execute(sql_out, {'amount': amount, 'username': from_user})

        # 3. 转入方收款
        sql_in = 'UPDATE account SET balance = balance + %(amount)s WHERE username = %(username)s;'
        self.cursor.execute(sql_in, {'amount': amount, 'username': to_user})

        # 4. 记录转账日志
        sql_log = '''INSERT INTO transfer_log (from_user, to_user, amount, time)
                      VALUES (%(from)s, %(to)s, %(amount)s, NOW());'''
        self.cursor.execute(sql_log, {'from': from_user, 'to': to_user, 'amount': amount})

        # 5. 所有操作成功，提交事务
        self.conn.commit()
        print(f'转账成功: {from_user} -> {to_user}, 金额: {amount}')
        return True

    except Exception as e:
        # 任何一步失败，回滚所有操作
        self.conn.rollback()
        print(f'转账失败，已回滚: {e}')
        return False
```

## A.4 MySQL 慢查询优化示例

```sql
-- 1. 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- 超过2秒的查询记录
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- 2. 使用EXPLAIN分析查询计划
EXPLAIN SELECT e.name, d.name
FROM employee e
LEFT JOIN department d ON e.dept_id = d.id
WHERE e.salary > 10000
ORDER BY e.salary DESC;

-- EXPLAIN输出关键字段解读：
-- type:    ALL(全表扫描) < index < range < ref < eq_ref < const(最优)
-- key:     实际使用的索引
-- rows:    预估扫描行数
-- Extra:   Using filesort(需要优化), Using index(覆盖索引, 好)

-- 3. 优化建议：
-- (1) 在WHERE/ORDER BY/JOIN字段上创建索引
CREATE INDEX idx_salary ON employee(salary);
CREATE INDEX idx_dept_id ON employee(dept_id);

-- (2) 避免SELECT *，只查询需要的字段
-- (3) 用EXISTS替代IN（当子查询结果集较大时）
-- (4) 分页时使用覆盖索引 + 延迟关联
```

---

> **文档说明**：本文档系统地整理了MySQL数据库从基础到进阶的全部知识点，包括数据库概念、SQL语句操作、数据类型、约束条件、查询语句、存储引擎、PyMySQL使用以及进阶知识。文档中包含大量可直接执行的SQL示例代码和一个完整的PyMySQL员工管理系统实战项目。建议配合实际操作练习，循序渐进地掌握MySQL数据库的各个方面。
