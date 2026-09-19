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
