##### json序列化时可以处理的数据类型有哪些？如何定制支持datetime类型？序列化时，遇到中文转成unicode，如何保持中文形式？
1. 可以处理的数据类型是 string、int、list、tuple、dict、bool、null
2. 通过自定义时间序列化转换器
```python
import json
from json import JSONEncoder
from datetime import datetime
class ComplexEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(‘%Y-%m-%d %H:%M:%S‘)
        else:
            return super(ComplexEncoder,self).default(obj)
d = { ‘name‘:‘alex‘,‘data‘:datetime.now()}
print(json.dumps(d,cls=ComplexEncoder))
# {"name": "alex", "data": "2018-05-18 19:52:05"}
```
3. 使用ensure_ascii=False参数

---

##### 文件操作时，xreadlines和readlines的区别

* xreadlines返回的是一个生成器
* readlines返回的是一个列表

---

##### 如何使用python删除一个文件或者文件夹？
```python
import os
import shutil
os.remove(path) # 删除文件
os.removedirs(path) # 删除空文件夹
shutil.rmtree(path) # 删除文件夹，可以为空也可以不为空
```

---

##### 一个大小为100G的文件etl_log.txt，要读取文件的内容，写出具体过程代码
```python
with open("etl_log.txt",'r',encoding='utf8') as f:
    for line in f:
        print(line,end='')
```

---

##### 写个函数接收一个文件夹名称作为参数，显示文件夹中文件的路径，以及其中包含的文件夹中文件的如今
```python
# 方法一
import os
def Test1(rootDir):
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print(os.path.join(root, d))
        for f in files:
            print(os.path.join(root, f))
Test1(r'C:\Users\felix\Desktop\aaa')
print('###################')
# 方法二
import os
def Test2(rootDir):
    paths=os.listdir(rootDir)
    for lis in paths:
        path=os.path.join(rootDir,lis)
        print(path)
        if os.path.isdir(path):
             Test2(path)
Test2(r'C:\Users\felix\Desktop\aaa')
```
