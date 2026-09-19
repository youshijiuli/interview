# python-面试通关宝典

### **操作类题目**

#### 51.在 Python 中交换两个变量的值。

```python
a,b = b,a
```

#### 52.在读文件操作的时候会使用 read、readline 或者 readlines，简述它们各自的作用。

```python
read将整个文本都读取为一个字符串，占用内存大，readline读取为一个生成器，支持遍历和迭代，占用空间小。readlines将文本读取为列表，占用空间大
```

#### 53.json 序列化时，可以处理的数据类型有哪些？如何定制支持 datetime 类型？

```markdown
字符串、数字（整数和浮点数）、字典、列表、布尔值、None。使用strftime将datetime格式化为标准字符串类型即可。
```

#### 54.json 序列化时，默认遇到中文会转换成 unicode，如果想要保留中文怎么办？

```
使用json.dumps函数时，添加参数ensure_ascii=False，如果想显示的更美观，可以添加indent=2参数，会在每个key值前添加两个空格。
```

#### 55.有两个磁盘文件 A 和 B，各存放一行字母，要求把这两个文件中的信息合并（按字母顺序排列），输出到一个新文件 C 中。

```python
with open('A.txt','r') as f:
    a = f.readlines()[0]
with open('B.txt','r') as f:
    b = f.readlines()[0]
    a.extend(b).sort()
with open('C.txt','w') as f:
    for i in a:
        f.write(i)
```

#### 56.如果当前的日期为 20190530，要求写一个函数输出 N 天后的日期（比如 N 为 2，则输出 20190601)。

```python
import datetime
def getday(n):
    y,m,d = 2019,5,30
    the_date = datetime.datetime(y,m,d)
    result_date = the_date + datetime.timedelta(days=n)
    target_date = result_date.strftime('%Y%m%d')
    return target_date
```

#### 57.写一个函数，接收整数参数 n，返回一个函数。函数的功能是把函数的参数和 n 相乘并把结果返回。

```python
def mul(n):
  def wrapper(m):
    return n*m
  return wrapper
    
 # 闭包的基本操作
```

#### 58.下面的代码会存在什么问题，如何改进？

```Python
def strappend(num):
    str='first'
    for i in range(num):
        str+=str(i)
    return str
  # 将str(i)改为str[i]
```

#### 59.一行代码输出 1-100 之间的所有偶数。

```python
[x for x in range(101) if x %2 ==0]
```

#### 60.with 语句的作用，并用它写一段代码。

```python
# with语句用来管理资源，及时关闭文件等操作，避免资源的泄漏
with open('a.txt','r') as f:
    f.read()
```

#### 61.Python 字典和 json 字符串相互转化方法。

```python
json.dumps()   将Python中的对象转换为JSON中的字符串对象
json.loads()   将JSON中的字符串对象转换为Python中的对象
```

#### 62.请写一个 Python 逻辑，计算一个文件中的大写字母数量。

```python
import re
with open('a.txt','r') as f:
    f_content = f.read()
    len_cap = len(re.compile(r'[A-Z]').findall(f_content))
```
