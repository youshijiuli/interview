# python-面试通关宝典

### **正则表达式**

#### 80.使用正则表达式匹配```<html><h1>www.baidu.com</html>```中的地址。

```python
import re
s = '<html><h1>www.baidu.com</html>'
p = re.compile(r'<html><h1>(.*?)</html>')
result = re.findall(p,s)[0]
```

a="张明 98 分"，用 re.sub，将 98 替换为 100

```python
import re
a="张明 98 分"
pa = re.compile(r'\d+')
re.sub(pa,'100',a)
```

#### 81.正则表达式匹配中 (.*) 和 (.**?) 匹配区别？

```
加？会将贪婪模式改成懒惰模式,如果有问号的话，则表示匹配0个或1个问号前面的表达式
```

#### 82.写一段匹配邮箱的正则表达式。

```python
r'[0-9a-zA-Z_]*@.+\.(com|cn|net)$'
```
