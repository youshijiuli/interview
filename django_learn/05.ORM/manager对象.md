# manager对象



有很多人喜欢在模型的初始化上做文章，实现一些额外的业务需求，常见的做法是自定义`__init__`方法。这不好，容易打断Django源码的调用链，存在漏洞。更推荐的是下面两种方法。

第一种方法：为模型增加create类方法，在其中夹塞你的代码：

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)

    @classmethod
    def create(cls, title):
        book = cls(title=title)
        # 将你的个人代码放在这里
        print('测试一下是否工作正常')
        return book

book = Book.create("liujiangblog.com")   # 注意，改为使用created方法创建Book对象
book.save()           # 只有调用save后才能保存到数据库
```

第二种方法：自定义管理器，并在其中添加创建对象的方法，推荐！

```python
class BookManager(models.Manager):   # 继承默认的管理器
    def create_book(self, title):
        book = self.create(title=title)
        # 将你的个人代码放在这里
        print('测试一下是否工作正常')
        return book

class Book(models.Model):
    title = models.CharField(max_length=100)

    objects = BookManager()   # 赋值objects
 
book = Book.objects.create_book("liujiangblog.com")   #改为使用create_book方法创建对象
```

