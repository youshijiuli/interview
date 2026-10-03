一定要区分QueryDict和QuerySet，前者是对HTTP请求数据包中携带的数据的封装，后者是对从数据库中查询出来的数据进行的封装。

在HttpRequest对象中，GET和POST属性都是一个`django.http.QueryDict`的实例。也就是说你可以按本文下面提供的方法操作request.POST和request.GET。

request.POST或request.GET的QueryDict都是不可变，只读的。如果要修改它，需要使用QueryDict.copy()方法，获取它的一个拷贝，然后在这个拷贝上进行修改操作。

```
<QueryDict: {'home': ['beijing'], 'age': ['30']}>
```


## 一、方法

QueryDict 实现了Python字典数据类型的所有标准方法，因为它是字典的子类。

不同之处在于下面：

###  `__init__(query_string=None, mutable=False, encoding=None)`

QueryDict实例化方法。**注意：QueryDict参数中的键值是可以重复的！**

```python
>>> QueryDict('a=1&a=2&c=3')
<QueryDict: {'a': ['1', '2'], 'c': ['3']}>
```

 如果需要实例化可以修改的对象，添加参数mutable=True。

### fromkeys(iterable, value='', mutable=False, encoding=None)

循环可迭代对象中的每个元素作为键值，并赋予同样的值（来至value参数）。

```python
>>> QueryDict.fromkeys(['a', 'a', 'b'], value='val')
<QueryDict: {'a': ['val', 'val'], 'b': ['val']}>
```

## `__getitem__(key)`

根据提供的key，返回对应的值。如果有多个值，返回最后那个。如果key不存在，弹出异常。

### `__setitem__(key, value)`

设置键值对。只能用于可变的QueryDict。

### `__contains__(key)`

如果QueryDict中有该key存在，返回True，否则False

### get(key, default=None)

和`QueryDict.__getitem__(key)`的作用一样，不同在于，如果key不存在，则返回default值。

### setdefault(key, default=None)

类似`__setitem__()`，字典的setdefault()方法。

### update(other_dict)


用新的QueryDict或字典更新当前QueryDict。类似`dict.update()`，但是追加内容，而不是更新并替换它们。 像这样：

```python
>>> q = QueryDict('a=1', mutable=True)
>>> q.update({'a': '2'})
>>> q.getlist('a')
['1', '2']
>>> q['a'] # returns the last
'2'
```

### items()

类似`dict.items()`，如果有重复项目，返回最近的一个，而不是都返回：

```python
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.items()
[('a', '3')]
```

### values()

类似`dict.values()`，但是只返回最近的值。 像这样：

```python
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.values()
['3']
```


### copy()

使用`copy.deepcopy()`返回QueryDict对象的副本。 此副本是可变的！

### getlist(key, default=None)

返回键对应的值列表。 如果该键不存在并且未提供默认值，则返回一个空列表。

### setlist(key, list_)

为`list_`设置给定的键。

### appendlist(key, item)

将键追加到内部与键相关联的列表中。

### setlistdefault(key, default_list=None)

类似setdefault()，除了它需要的是一个值的列表而不是单个值。

### lists()

类似items()，只是它将其中的每个键的值作为列表放在一起。 像这样：

```python
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.lists()
[('a', ['1', '2', '3'])]
```

### pop(key)

返回给定键的值的列表，并从QueryDict中移除该键。 如果键不存在，将引发KeyError。 像这样：

```python
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.pop('a')
['1', '2', '3']
```

### popitem()

删除QueryDict任意一个键，并返回二值元组，包含键和键的所有值的列表。在一个空的字典上调用时将引发KeyError。 像这样：

```python
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.popitem()
('a', ['1', '2', '3'])
```

### dict()

将QueryDict转换为Python的字典数据类型，并返回该字典。

如果出现重复的键，则将所有的值打包成一个列表，最为新字典中键的值。

```python
>>> q = QueryDict('a=1&a=3&a=5')
>>> q.dict()
{'a': '5'}
```

### urlencode(safe=None)

已url的编码格式返回数据字符串。 像这样：

```python
>>> q = QueryDict('a=2&b=3&b=5')
>>> q.urlencode()
'a=2&b=3&b=5'
```

使用safe参数传递不需要编码的字符。 像这样：

```python
>>> q = QueryDict(mutable=True)
>>> q['next'] = '/a&b/'
>>> q.urlencode(safe='/')
'next=/a%26b/'
```