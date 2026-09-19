# python-面试通关宝典

## **二.编码规范**

#### 7.什么是 PEP8？

```markdown
PEP是 Python Enhancement Proposal 的缩写，翻译过来就是 Python增强建议书
简单说就是一种编码规范，是为了让代码“更好看”，更容易被阅读
具体可参考：
https://www.python.org/dev/peps/pep-0008/
```

#### 8.了解 Python 之禅吗？

```markdown
import this
```

#### 9.了解 docstring 吗？

```markdown
Python有一个很奇妙的特性，称为 文档字符串 ，它通常被简称为 docstrings 。DocStrings是一个重要的工具，由于它帮助你的程序文档更加简单易懂，你应该尽量使用它。你甚至可以在程序运行的时候，从函数恢复文档字符串。
使用魔法方法'__doc__'可以打印docstring的内容
```

#### 10.了解类型注解吗？

```markdown
def add(x:int, y:int) -> int:
    return x + y
用 : 类型 的形式指定函数的参数类型，用 -> 类型 的形式指定函数的返回值类型
```

#### 11.例举你知道 Python 对象的命名规范，例如方法或者类等。

```
类名都使用首字母大写开头(Pascal命名风格)的规范；
全局变量全用大写字母，单词之间用 _分割；
普通变量用小写字母，单词之间用 _分割；
普通函数和普通变量一样；
私有函数以 __ 开头（2个下划线），其他和普通函数一样；

```

#### 12.Python 中的注释有几种？

```markdown
单行注释，多行注释，docstring注释
```

#### 13.如何优雅的给一个函数加注释？

```markdown
在函数逻辑行的首行使用""" xxx """给函数添加注释，注释中可包含函数参数的说明，返回值说明等
def foo(bar):
    """
    This is an example.
    :param bar: explain param bar
    """
    return bar
```

#### 14.如何给变量加注释？

```python
参数注释：以冒号（:）标记
返回值注释：以 -> 标记
示例：
def add(x:int, y:int) -> int:
    return x + y
```

#### 15.Python 代码缩进中是否支持 Tab 键和 空格 混用？

```markdown
支持，Python 并没有强制要求你用Tab缩进或者用空格缩进，但在 PEP8中，建议使用4个空格来缩进
```

#### 16.是否可以在一句 import 中导入多个库？

```python
可以的
import json,random,requests
```

#### 17.在给 Python 文件命名的时候需要注意什么？

```markdown
全小写，单词之间使用下划线分隔
```

#### 18.例举几个规范 Python 代码风格的工具。

```markdown
pylint,black,pycharm也带有pep8的代码规范工具
```
