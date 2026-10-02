##### logging模块的作用以及应用场景
* logging模块定义的函数和类为应用程序和库的开发实现了一个灵活的事件日志系统。
* 记录日志

---

##### re的match和search的区别
* match()函数是在string的开始位置匹配，如果不匹配，则返回None
* search()会扫描整个string查找匹配；也就是说match()只有在0位置匹配成功的话才有返回，

---

##### sys.path.append('xxx')的作用
* 添加搜索路径

---

##### 什么是正则的贪婪匹配？贪婪模式和非贪婪模式的区别？
[参考文档](https://www.cnblogs.com/ILoke-Yang/p/8060003.html)

* 贪婪匹配:正则表达式一般趋向于最大长度匹配，也就是所谓的贪婪匹配。
* 非贪婪匹配：就是匹配到结果就好，就少的匹配字符。
* 区别：默认是贪婪模式；在量词后面直接加上一个问号？就是非贪婪模式。

---

##### python代码如何获取命令行参数
[获取命令行参数的方法参考](https://www.cnblogs.com/ouyangpeng/p/8537616.html)
1.使用sys模块
    * 通过sys.argv来获取
2. 使用getopt模块

---

##### 写出邮箱的正则表达式

```python
import re
pp=re.compile('[a-zA-Z0-9_-]+@[0-9A-Za-z]+(.[0-9a-zA-Z]+)+')
if pp.match('1403179190@qq.com'):
    print('ok')
```
