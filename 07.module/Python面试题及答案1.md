### Python语言特性

#### 40 Python里面match()和search()的区别？
答：re模块中match(pattern,string[,flags]),检查string的开头是否与pattern匹配。
re模块中research(pattern,string[,flags]),在string搜索pattern的第一个匹配值。
>>>print(re.match(‘super’, ‘superstition’).span())
(0, 5)
>>>print(re.match(‘super’, ‘insuperable’))
None
>>>print(re.search(‘super’, ‘superstition’).span())
(0, 5)
>>>print(re.search(‘super’, ‘insuperable’).span())
(2, 7)

#### 41 用Python匹配HTML tag的时候，<.*>和<.*?>有什么区别？
答：术语叫贪婪匹配( <.*> )和非贪婪匹配(<.*?> )
例如:
test
<.*> :
test
<.*?> :

#### 42 Python里面如何生成随机数？
答：random模块
随机整数：random.randint(a,b)：返回随机整数x,a<=x<=b
random.randrange(start,stop,[,step])：返回一个范围在(start,stop,step)之间的随机整数，不包括结束值。
随机实数：random.random( ):返回0到1之间的浮点数
random.uniform(a,b):返回指定范围内的浮点数。

#### 48 如何用Python来进行查询和替换一个文本字符串？
可以使用sub()方法来进行查询和替换，sub方法的格式为：sub(replacement, string[, count=0])
replacement是被替换成的文本
string是需要被替换的文本
count是一个可选参数，指最大被替换的数量

#### 49 Python里面search()和match()的区别？
match()函数只检测RE是不是在string的开始位置匹配，search()会扫描整个string查找匹配, 也就是说match()只有在0位置匹配成功的话才有返回，如果不是开始位置匹配成功的话，match()就返回none

#### 50 用Python匹配HTML tag的时候，<.*>和<.*?>有什么区别？
前者是贪婪匹配，会从头到尾匹配 <a>xyz</a>，而后者是非贪婪匹配，只匹配到第一个 >。

#### 51 Python里面如何生成随机数？
import random
random.random()
它会返回一个随机的0和1之间的浮点数


# python-面试通关宝典





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



