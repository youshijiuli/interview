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
