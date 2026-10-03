## ORM拓展







## 查询优化

表数据

```python
class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    avatar = models.FileField(verbose_name='头像',upload_to = 'avatar/',default="/avatar/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
 
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))
 
    def __str__(self):
        return self.username
 
class UserFans(models.Model):
    """
    互粉关系表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')
 
class Blog(models.Model):
 
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')
    def __str__(self):
        return self.title
 
class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
 
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
 
class Article(models.Model):
 
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0)
    comment_count= models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)
    create_time = models.DateField(verbose_name='创建时间')
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
)
 
 
class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )
 
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')
 
 
class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
 
    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
 
    up_count = models.IntegerField(default=0)
 
    def __str__(self):
        return self.content
 
class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)
    models.BooleanField(verbose_name='是否赞')
 
class CommentUp(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    comment = models.ForeignKey("Comment", null=True)
 
 
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
 
 
 
class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')
```





### select_related

#### 简单使用

对于一对一字段（OneToOneField）和外键字段（ForeignKey），可以使用select_related 来对QuerySet进行优化。

select_related 返回一个`QuerySet`，当执行它的查询时它沿着外键关系查询关联的对象的数据。它会生成一个复杂的查询并引起性能的损耗，但是在以后使用外键关系时将不需要数据库查询。

简单说，在对QuerySet使用select_related()函数后，Django会获取相应外键对应的对象，从而在之后需要的时候不必再查询数据库了。

下面的例子解释了普通查询和`select_related()` 查询的区别。

查询id=2的文章的分类名称,下面是一个标准的查询：

```
# Hits the database.
article=models.Article.objects.get(nid=2)
 
# Hits the database again to get the related Blog object.
print(article.category.title)

```



```
'''
 
SELECT
    "blog_article"."nid",
    "blog_article"."title",
    "blog_article"."desc",
    "blog_article"."read_count",
    "blog_article"."comment_count",
    "blog_article"."up_count",
    "blog_article"."down_count",
    "blog_article"."category_id",
    "blog_article"."create_time",
     "blog_article"."blog_id",
     "blog_article"."article_type_id"
             FROM "blog_article"
             WHERE "blog_article"."nid" = 2; args=(2,)
 
SELECT
     "blog_category"."nid",
     "blog_category"."title",
     "blog_category"."blog_id"
              FROM "blog_category"
              WHERE "blog_category"."nid" = 4; args=(4,)
 
 
'''

```



 如果我们使用select_related()函数：

```
articleList=models.Article.objects.select_related("category").all()
 
 
    for article_obj in articleList:
        #  Doesn't hit the database, because article_obj.category
        #  has been prepopulated in the previous query.
        print(article_obj.category.title)

```



```
SELECT
     "blog_article"."nid",
     "blog_article"."title",
     "blog_article"."desc",
     "blog_article"."read_count",
     "blog_article"."comment_count",
     "blog_article"."up_count",
     "blog_article"."down_count",
     "blog_article"."category_id",
     "blog_article"."create_time",
     "blog_article"."blog_id",
     "blog_article"."article_type_id",
 
     "blog_category"."nid",
     "blog_category"."title",
     "blog_category"."blog_id"
 
FROM "blog_article"
LEFT OUTER JOIN "blog_category" ON ("blog_article"."category_id" = "blog_category"."nid");

```



#### 多外键查询

这是针对category的外键查询，如果是另外一个外键呢？让我们一起看下：

```
article=models.Article.objects.select_related("category").get(nid=1)
print(article.articledetail)

```



 观察logging结果，发现依然需要查询两次，所以需要改为：

```
article=models.Article.objects.select_related("category","articledetail").get(nid=1)
print(article.articledetail)

```



 或者：

```
article=models.Article.objects　　　　　　　　　　　　　.select_related("category")　　　　　　　　　　　　　.select_related("articledetail")　　　　　　　　　　　　　.get(nid=1)  # django 1.7 支持链式操作
print(article.articledetail)
```

 ```
SELECT
 
    "blog_article"."nid",
    "blog_article"."title",
    ......
 
    "blog_category"."nid",
    "blog_category"."title",
    "blog_category"."blog_id",
 
    "blog_articledetail"."nid",
    "blog_articledetail"."content",
    "blog_articledetail"."article_id"
 
   FROM "blog_article"
   LEFT OUTER JOIN "blog_category" ON ("blog_article"."category_id" = "blog_category"."nid")
   LEFT OUTER JOIN "blog_articledetail" ON ("blog_article"."nid" = "blog_articledetail"."article_id")
   WHERE "blog_article"."nid" = 1; args=(1,)

 ```





#### 深层查询

```
# 查询id=1的文章的用户姓名
 
    article=models.Article.objects.select_related("blog").get(nid=1)
    print(article.blog.user.username)

```



 依然需要查询两次：

```
SELECT
    "blog_article"."nid",
    "blog_article"."title",
    ......
 
     "blog_blog"."nid",
     "blog_blog"."title",
 
   FROM "blog_article" INNER JOIN "blog_blog" ON ("blog_article"."blog_id" = "blog_blog"."nid")
   WHERE "blog_article"."nid" = 1;
 
 
 
 
SELECT
    "blog_userinfo"."password",
    "blog_userinfo"."last_login",
    ......
 
FROM "blog_userinfo"
WHERE "blog_userinfo"."nid" = 1;

```



 这是因为第一次查询没有query到userInfo表，所以，修改如下：

```
article=models.Article.objects.select_related("blog__user").get(nid=1)
print(article.blog.user.username)

```

```
SELECT
 
"blog_article"."nid", "blog_article"."title",
......
 
 "blog_blog"."nid", "blog_blog"."title",
......
 
 "blog_userinfo"."password", "blog_userinfo"."last_login",
......
 
FROM "blog_article"
 
INNER JOIN "blog_blog" ON ("blog_article"."blog_id" = "blog_blog"."nid")
 
INNER JOIN "blog_userinfo" ON ("blog_blog"."user_id" = "blog_userinfo"."nid")
WHERE "blog_article"."nid" = 1;

```



#### 总结

1. select_related主要针一对一和多对一关系进行优化。
2. select_related使用SQL的JOIN语句进行优化，通过减少SQL查询的次数来进行优化、提高性能。
3. 可以通过可变长参数指定需要select_related的字段名。也可以通过使用双下划线“__”连接字段名来实现指定的递归查询。
4. 没有指定的字段不会缓存，没有指定的深度不会缓存，如果要访问的话Django会再次进行SQL查询。
5. 也可以通过depth参数指定递归的深度，Django会自动缓存指定深度内所有的字段。如果要访问指定深度外的字段，Django会再次进行SQL查询。
6. 也接受无参数的调用，Django会尽可能深的递归查询所有的字段。但注意有Django递归的限制和性能的浪费。
7. Django >= 1.7，链式调用的select_related相当于使用可变长参数。Django < 1.7，链式调用会导致前边的select_related失效，只保留最后一个。

### prefetch_related()

对于多对多字段（ManyToManyField）和一对多字段，可以使用prefetch_related()来进行优化。

prefetch_related()和select_related()的设计目的很相似，都是为了减少SQL查询的数量，但是实现的方式不一样。后者是通过JOIN语句，在SQL查询内解决问题。但是对于多对多关系，使用SQL语句解决就显得有些不太明智，因为JOIN得到的表将会很长，会导致SQL语句运行时间的增加和内存占用的增加。若有n个对象，每个对象的多对多字段对应Mi条，就会生成Σ(n)Mi  行的结果表。

prefetch_related()的解决方法是，分别查询每个表，然后用Python处理他们之间的关系。

```
# 查询所有文章关联的所有标签
    article_obj=models.Article.objects.all()
    for i in article_obj:
 
        print(i.tags.all())  #4篇文章: hits database 5

改为prefetch_related：
# 查询所有文章关联的所有标签
    article_obj=models.Article.objects.prefetch_related("tags").all()
    for i in article_obj:
 
        print(i.tags.all())  #4篇文章: hits database 2





SELECT "blog_article"."nid",
               "blog_article"."title",
               ......
 
FROM "blog_article";
 
 
 
SELECT
  ("blog_article2tag"."article_id") AS "_prefetch_related_val_article_id",
  "blog_tag"."nid",
  "blog_tag"."title",
  "blog_tag"."blog_id"
   FROM "blog_tag"
  INNER JOIN "blog_article2tag" ON ("blog_tag"."nid" = "blog_article2tag"."tag_id")
  WHERE "blog_article2tag"."article_id" IN (1, 2, 3, 4);
```



 



## 四 extra

 extra(select=None, where=None, params=None, 

```
      tables=None, order_by=None, select_params=None)
```

有些情况下，Django的查询语法难以简单的表达复杂的 `WHERE` 子句，对于这种情况, Django 提供了 `extra()` `QuerySet`修改机制 — 它能在 `QuerySet`生成的SQL从句中注入新子句

extra可以指定一个或多个 `参数`,例如 `select`, `where` or `tables`. 这些参数都不是必须的，但是你至少要使用一个!要注意这些额外的方式对不同的数据库引擎可能存在移植性问题.(因为你在显式的书写SQL语句),除非万不得已,尽量避免这样做

### 参数之select

The `select` 参数可以让你在 `SELECT` 从句中添加其他字段信息，它应该是一个字典，存放着属性名到 SQL 从句的映射。

```
queryResult=models.Article　　　　　　　　　　　.objects.extra(select={'is_recent': "create_time > '2017-09-05'"})
```

结果集中每个 Entry 对象都有一个额外的属性is_recent, 它是一个布尔值，表示 Article对象的create_time 是否晚于2017-09-05.

练习：

```
# in sqlite:
    article_obj=models.Article.objects　　　　　　　　　　　　　　.filter(nid=1)　　　　　　　　　　　　　　.extra(select={"standard_time":"strftime('%%Y-%%m-%%d',create_time)"})　　　　　　　　　　　　　　.values("standard_time","nid","title")
    print(article_obj)
    # <QuerySet [{'title': 'MongoDb 入门教程', 'standard_time': '2017-09-03', 'nid': 1}]>
```



### 参数之`where` / `tables`

您可以使用`where`定义显式SQL `WHERE`子句 - 也许执行非显式连接。您可以使用`tables`手动将表添加到SQL `FROM`子句。

`where`和`tables`都接受字符串列表。所有`where`参数均为“与”任何其他搜索条件。

举例来讲：

```
queryResult=models.Article　　　　　　　　　　　.objects.extra(where=['nid in (1,3) OR title like "py%" ','nid>2'])
```



### 整体插入

创建对象时，尽可能使用bulk_create()来减少SQL查询的数量。例如：

```
Entry.objects.bulk_create([
    Entry(headline="Python 3.0 Released"),
    Entry(headline="Python 3.1 Planned")
])
```

...更优于：

```
Entry.objects.create(headline="Python 3.0 Released")
Entry.objects.create(headline="Python 3.1 Planned")
```

注意该方法有很多注意事项，所以确保它适用于你的情况。

这也可以用在ManyToManyFields中，所以：

```
my_band.members.add(me, my_friend)
```

...更优于：

```
my_band.members.add(me)
my_band.members.add(my_friend)
```

...其中Bands和Artists具有多对多关联。











#### （1）select_related()

对于一对一字段（OneToOneField）和外键字段（ForeignKey），可以使用select_related 来对QuerySet进行优化。

select_related 返回一个`QuerySet`，当执行它的查询时它沿着外键关系查询关联的对象的数据。它会生成一个复杂的查询并引起性能的损耗，但是在以后使用外键关系时将不需要数据库查询。

简单说，在对QuerySet使用select_related()函数后，Django会获取相应外键对应的对象，从而在之后需要的时候不必再查询数据库了。

下面的例子解释了普通查询和`select_related()` 查询的区别。

查询id=2的的书籍的出版社名称,下面是一个标准的查询：

```python
# Hits the database.
book= models.Book.objects.get(nid=2)
# Hits the database again to get the related Blog object.
print(book.publish.name)
```

如果我们使用select_related()函数：

```python
books=models.Book.objects.select_related("publish").all()
for book in books:
     #  Doesn't hit the database, because book.publish
     #  has been prepopulated in the previous query.
     print(book.publish.name)
```

##### 多外键查询

这是针对publish的外键查询，如果是另外一个外键呢？让我们一起看下：

```python
book=models.Book.objects.select_related("publish").get(nid=1)
print(book.authors.all())
```

 观察logging结果，发现依然需要查询两次，所以需要改为：

```python
book=models.Book.objects.select_related("publish","").get(nid=1)
print(book.publish)
```

 或者：

```python
book=models.Article.objects
　　　　　　　　　　　　　.select_related("publish")
　　　　　　　　　　　　　.select_related("")
　　　　　　　　　　　　　.get(nid=1)  # django 1.7 支持链式操作
print(book.publish)
```

#### （2）prefetch_related()

对于多对多字段（ManyToManyField）和一对多字段，可以使用prefetch_related()来进行优化。

prefetch_related()和select_related()的设计目的很相似，都是为了减少SQL查询的数量，但是实现的方式不一样。后者是通过JOIN语句，在SQL查询内解决问题。但是对于多对多关系，使用SQL语句解决就显得有些不太明智，因为JOIN得到的表将会很长，会导致SQL语句运行时间的增加和内存占用的增加。若有n个对象，每个对象的多对多字段对应Mi条，就会生成Σ(n)Mi 行的结果表。

prefetch_related()的解决方法是，分别查询每个表，然后用Python处理他们之间的关系。

```python
# 查询所有文章关联的所有标签
books=models.Book.objects.all()
for book in books:
  	print(book.authors.all())  #4篇文章: hits database 5
```

改为prefetch_related：

```python
# 查询所有文章关联的所有标签
books=models.Book.objects.prefetch_related("authors").all()
for book in books:
  	print(book.authors.all())  #4篇文章: hits database 2
```

#### （3）extra

```python
extra(select=None, where=None, params=None, 
      tables=None, order_by=None, select_params=None)
```

有些情况下，Django的查询语法难以简单的表达复杂的 `WHERE` 子句，对于这种情况, Django 提供了 `extra()` `QuerySet`修改机制 — 它能在 `QuerySet`生成的SQL从句中注入新子句

extra可以指定一个或多个 `参数`,例如 `select`, `where` or `tables`. 这些参数都不是必须的，但是你至少要使用一个!要注意这些额外的方式对不同的数据库引擎可能存在移植性问题.(因为你在显式的书写SQL语句),除非万不得已,尽量避免这样。

##### 参数之select

The `select` 参数可以让你在 `SELECT` 从句中添加其他字段信息，它应该是一个字典，存放着属性名到 SQL 从句的映射。

```
queryResult=models.Article
　　　　　　　　　　　.objects.extra(select={'is_recent': "create_time > '2017-09-05'"})
```

结果集中每个 Entry 对象都有一个额外的属性is_recent, 它是一个布尔值，表示 Article对象的create_time 是否晚于2017-09-05.

##### 参数之`where` / `tables`

您可以使用`where`定义显式SQL `WHERE`子句 - 也许执行非显式连接。您可以使用`tables`手动将表添加到SQL `FROM`子句。

`where`和`tables`都接受字符串列表。所有`where`参数均为“与”任何其他搜索条件。

举例来讲：

```python
queryResult=models.Article
　　　　　　　　　　　.objects.extra(where=['nid in (3，4) OR title like "py%" ','nid>2'])
```







## 优化访问

优化数据库访问，提高访问速度，降低内存消耗是必然的选择。

通常，最基本的优化手段是：

1. indexes：添加索引是最高优先级的优化手段。主要是通过为模型的定义添加`Meta.indexes`或者`Field.db_index `来实现。索引可以加速查询。为哪些字段添加索引，添加什么样的索引是个高级数据库话题，不在本文讨论范围之内。
1. 合理选择字段类型

下面我们介绍点别的优化手段。

### 1.缓存数据

首先我们要对QuerySet查询集有一定深度的理解，它有助于我们写出简单高效的查询语句。

为了避免性能问题，我们一定要知道：

* QuerySet是懒加载的
* 什么时候会真正提交QuerySet到数据库
* 数据是如何在内存中保持的

我们必须知道，那些不可调用的属性会被缓存。下面以我们一直使用的作者、博客和文章模型为例：

```python
>>> entry = Entry.objects.get(id=1)
>>> entry.blog   # 去数据库获取blog对象
>>> entry.blog   # 使用缓存的blog对象，不访问数据库
```

但是，可调用的属性不会缓存，每次都将访问数据库：

```python
>>> entry = Entry.objects.get(id=1)
>>> entry.authors.all()   # 访问数据库
>>> entry.authors.all()   # 再次访问
```

要注意，在Django的模板系统中，因为不允许使用圆括号，并且会自动调用可调用的属性，所以，为了让QuerySet能够被缓存，建议使用`with`模板标签，如下例子所示：

```python
{% with total=business.employees.count %}
    {{ total }} employee{{ total|pluralize }}
{% endwith %}
```

而对于你自定义的属性，则必须你自己决定是否使用缓存，怎么缓存。

当你有很多对象需要缓存的时候，会消耗很多的内存，此时可以使用`iterator()`方法，会比较高效，参考连接https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.iterator

另外一个建议是多使用`explain()`方法。这个方法能展示查询语句的具体SQL代码细节，包括索引和连接等内容。如果你的SQL语言掌握程度比较好的话，这能帮助你矫正ORM语句，提高查询效率。

### 2.在数据库中执行操作，而不是在 Python 代码中

其实在前面的章节中，我们已经介绍过这一点。

对于实例：

* 大多数情况下，请使用filter和exclude方法进行数据过滤
* 尽量使用F()表达式引用同模型内的其它字段
* 在数据库内使用注解进行数据聚合

如果上面的方法无法编写出满足需要的SQL语句，你还可以：

* 在查询参数中使用RawSQL()表达式
* 使用QuerySet的raw()方法，直接编写SQL语句。

### 3.使用唯一、索引列进行单个对象的获取

之所以在用get()方法获取单个对象的时候，建议使用具有`unique`、`db_index`属性的字段进行查询，有两个原因。第一，有索引的情况下会更加迅速，第二，唯一性约束可以保证不会检索到多个对象，再次提高查询速度。

下面的：

```python
>>> entry = Entry.objects.get(id=10)
```

将快过：

```python
>>> entry = Entry.objects.get(headline="News Item Title")
```

 `id` 是一个唯一并带索引的字段。

而下面的方法不但慢，还有bug：

```
>>> entry = Entry.objects.get(headline__startswith="News")
```

 `headline` 字段既没有索引，也不保证唯一。

### 4.有需求，全获取

假如你有一个Student模型，它有2个字段，name和sex。现在你马上要查询name字段的数据，并且你知道你很快也需要sex字段的内容。正确的做法是在检索name的时候就把sex一起检索出来，而不要分两次做。例子可能不太恰当，但就是这么个意思。

对于这一点，最常用的方式就是使用`select_related()` 和` prefetch_related()`方法，它们的用法在前面的章节有介绍。

### 5.无需求，不检索

当你明确只需要部分数据的时候，不要检索你不需要的数据。

#### QuerySet.values() 和 values_list()

当你只想得到字典或列表格式的值，并且不需要 ORM 模型对象时，可以适当使用 `values()` 。这对于替换模板代码中的模型对象非常有用——只要你提供的字典与模型对象有相同的属性就行。

#### QuerySet.defer() 和 only()

如果你明确不需要某列数据（或在大部分情况里不需要），可以使用 `defer()` 和 `only()` 来避免加载它们。

不要在没有分析的情况下过分使用延迟字段。当你不想加载许多文本数据，不想进行大量转换工作时， defer() 和 only() 方法最有用。总之，先分析，再优化。

#### QuerySet.count()

如果你只想计数，不要使用 `len(queryset)`，而是使用`count()`。

#### QuerySet.exists()

若你只想确认是否至少存在一个对象，请使用`exists()`，而不是 `if queryset`。

#### 不要过度使用 count() 和 exists()

count和exists会执行一次查询动作，所以不是任何时候都是最优解，比如下面的例子：

假设 Email 模型有一个 `body` 属性和一个与 User 模型的多对多关系 ，下面的模板代码是最佳的：

```python
{% if display_inbox %}
  {% with emails=user.emails.all %}
    {% if emails %}
      <p>You have {{ emails|length }} email(s)</p>
      {% for email in emails %}
        <p>{{ email.body }}</p>
      {% endfor %}
    {% else %}
      <p>No messages today.</p>
    {% endif %}
  {% endwith %}
{% endif %}
```

这是因为：

1. 因为查询集是懒加载，如果 `display_inbox` 是 False，就不会有数据库查询。
1. 使用 `with` 意味着我们在一个变量中存储 `user.emails.all` ，进行缓存，以供日后重复使用。
1. `{% if emails %}` 会调用 `QuerySet.__bool__()` ，由于emails已经缓存，所以不需要再次查询数据库。
1. `{{ emails|length }}` 会调用 `QuerySet.__len__()` ，使用缓存的数据，而不执行真实查询。
1. `for` 循环遍历已有的缓存。

总之，这个代码会执行一条或零条数据库查询。如果将`{% if emails %}`和`{{ emails|length }}`替换成`QuerySet.exists()` 与 `QuerySet.count()` ，会导致额外的查询动作。

#### QuerySet.update() 和 delete()

如果要设置一些值并单独保存它们，而不是检索对象，那么可以通过 `QuerySet.update()` 使用批量 SQL UPDATE 语句。类似地，尽可能使用批量删除（ bulk deletes ）。

注意，这些批量更新方法不会调用单独实例的 `save()` 或 `delete()` 方法，这意味着你为这些方法添加的任何自定义行为都不会执行，包括信号（ signals ）。

#### 直接使用外键值

如果只需要外键值，那么使用已有对象上的外键值，而不是检索出整个相关对象并获取它的主键。比如：

```
entry.blog_id
```

替换成：

```
entry.blog.id
```

#### 如无需要，不要对结果排序

排序是耗时的！如果模型有一个默认排序（ `Meta.ordering` ）并且你不需要它，那么可以通过在查询集上调用没有参数的 `order_by()` 方法来屏蔽排序动作。




