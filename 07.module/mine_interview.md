## Python

##### Python常用模块及其对应方法

time 模块

- time.time() 返回当前时间戳
- time.localtime([secs]) 将一个时间戳转换为当前时区的struct_time。secs参数未提供，则以当前时间为准。
- time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime()) 接收时间元组 返回可读的字符串表示当地时间
- time.sleep([secs]) 执行阻塞

os模块

- os.path.join() 拼接路径信息
- os.mkdir 创建目录
- os.path.split 将path分割成目录和文件名，元组返回
- os.path.isfile 判断是否是文件
- os.path.isdir  判断是否是目录

sys模块

- sys.path.insert() 添加目录进解释器环境，可以直接导包

json模块

- json.dumps() 使字典转换为json格式
- json.loads() 将json解码为字典

##### re 模块正则匹配一个邮箱（手写具体代码）

```python
import re  
text = input("Please input your Email address：\n")  

re.match(r'^\w{0,19}@\w{1,13}.\w{1,10}$',text)
```

##### re 模块的常用方法

search: 扫描整个字符串并返回第一个pattern模式的成功匹配 匹配失败返回None(包含即可)，匹配一次

math: match 必须第一位就开始匹配，否则匹配失败，匹配一次

- search是在要匹配的字符串中  包含正则表达式的内容就可以

findall: 扫描整个字符串，并返回所有pattern所匹配的结果，匹配多次

split: 拆分字符串

sub: 对字符串进行匹配替换

subn: 对字符串进行匹配替换，返回替换后的次数

##### 计算程序运行的时间差

time.time 进行时间戳的相减

time.clock 计算 cpu 处理的时间

##### 说一下Unittest

TestCase：用户自定义的测试 case 的[基类](https://so.csdn.net/so/search?q=基类&spm=1001.2101.3001.7020)，调用 run () 方法，会依次调用 setUp 方法、执行用例的方法、tearDown 方法。

TestSuite：[测试用例](https://so.csdn.net/so/search?q=测试用例&spm=1001.2101.3001.7020)集合，可以通过 addTest () 方法手动增加 Test Case，也可以通过 TestLoader 自动添加 Test Case，TestLoader 在添加用例时，会没有顺序。

TestRunner：运行测试用例的驱动类，可以执行 TestCase，也可以执行 TestSuite，执行后 TestCase 和 TestSuite 会自动管理 TESTResult。

TestFixture：简单来说就是做一些测试过程中需要准备的东西，比如创建临时的数据库，文件和目录等，其中 setUp () 和 setDown () 是最常用的方法

整个的流程就是首先要写好 TestCase，然后由 TestLoader 加载 TestCase 到 TestSuite，然后由 TestTestRunner 来运行 TestSuite，运行的结果保存在 TextTestReusult 中，整个过程集成在 unittest.main 模块中。
