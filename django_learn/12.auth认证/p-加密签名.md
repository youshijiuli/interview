Web应用程序保持安全的黄金法则是永远不信任任何来自不可信源的数据。

但是，有时候我们不得不通过不受信任的通道传递数据。

加密签名的值可以通过一个不可信的通道安全地传递，因为对原数据的篡改都会被检测到。

加密签名常用于：

- 用于给丢失密码的用户发送恢复账号的URL

- 确保存储在隐藏表单字段中的数据未被篡改。

- 生成一次性的秘密URL，以允许临时访问受保护的资源，例如用户付费的可下载文件。

Django提供了一个用于签名的低级API，以及一个用于设置和读取签名cookie的高级API。

此外，你还必须知道，当你使用startproject命令创建一个Django项目后，默认的settings.py文件中会自动生成一个随机的`SECRET_KEY`。这个值被用于在整个项目中加密数据。我们的签名方法在内部就需要用到这个值。所以，在部署、共享、开源你的项目代码前，请务必修改`SECRET_KEY`。如果让恶意份子获取到了这个随机值，你的项目安全将受到极大威胁。

```
SECRET_KEY = '&1u4g68@a*@%sr*_-f#*5wnckyuzaw$685-cg1pio+td#n!m!&'
```

## Signer

> class Signer(key=None, sep=':', salt=None, algorithm=None)

Django的签名方法位于`django.core.signing`模块。要为一个值进行加密签名，使用`sign()`方法，如下操作即可：

```python
>>> from django.core.signing import Signer
>>> signer = Signer()
>>> value = signer.sign('My string')
>>> value
'My string:GdMGD6HNQ_qdgxYP8yBZAdAIV1w'
```

签名紧跟在原始值之后，中间以冒号分隔。

你可以通过`unsign()`方法获得原始值：

```python
>>> original = signer.unsign(value)
>>> original
'My string'
```

如果你传递的初始值不是字符串类型，那么在签名的时候会强制转换为字符串类型，并且使用`unsign()`方法返回的也是字符串类型：

```python
>>> signed = signer.sign(2.5)
>>> original = signer.unsign(signed)
>>> original
'2.5'
```

如果签名被任何手段修改过，将抛出一个`django.core.signing.BadSignature`异常：

```python
>>> from django.core import signing
>>> value += 'm'
>>> try:
...    original = signer.unsign(value)
... except signing.BadSignature:
...    print("数据被篡改了!")
```

默认情况下，`Singer`类使用我们签名说的`SECRET_KEY`生成签名。你也可以指定使用别的密码，将它传递给Singer的构造器即可：

```python
>>> signer = Signer('my-other-secret')
>>> value = signer.sign('My string')
>>> value
'My string:EkfQJafvGyiofrdGnuthdxImIJw'
```

## 加盐

根据Signer类的构造函数我们可以看出：

* key：指定使用的初始密码串
* sep：指定分隔符，默认为冒号
* salt：密码加盐
* algorithm：指定加密算法，默认为sha256，可以是任何hashlib中的算法。

加盐是最常见的密码复杂化操作之一：

```python
>>> signer = Signer()
>>> signer.sign('My string')
'My string:GdMGD6HNQ_qdgxYP8yBZAdAIV1w'
>>> signer = Signer(salt='extra')
>>> signer.sign('My string')
'My string:Ee7vGi-ING6n02gkcJ-QLHg6vFw'
>>> signer.unsign('My string:Ee7vGi-ING6n02gkcJ-QLHg6vFw')
'My string'
```

加盐会将不同的签名放入不同的命名空间中。来自一个命名空间（特定salt值）的签名不能用于验证使用不同salt设置的不同命名空间中的相同明文字符串。目的是防止攻击者使用在代码中某个位置生成的签名字符串作为另一段代码的输入，该代码使用不同的salt生成（并验证）签名。

不同于`SECRET_KEY`，盐参数不需要保密。

## 验证时间戳

`TimestampSigner` 是 `Signer` 的子类，在原来的基础上附加了一个时间戳签名。

它用于确保你的加密签名在有效的时间范围内。

```python
>>> from datetime import timedelta
>>> from django.core.signing import TimestampSigner
>>> signer = TimestampSigner()
>>> value = signer.sign('hello')
>>> value
'hello:1NMg5H:oPVuCqlJWmChm1rA2lyTUtelC-c'
>>> signer.unsign(value)
'hello'
>>> signer.unsign(value, max_age=10)
...
SignatureExpired: Signature age 15.5289158821 > 10 seconds
>>> signer.unsign(value, max_age=20)
'hello'
>>> signer.unsign(value, max_age=timedelta(seconds=20))
'hello'
```

其中的max_age单位为秒，值可以是正整数或者`datatime.timedelta`对象

超出时间范围后，签名验证将不通过。

## 保护复杂的数据结构

如果你想保护列表，元组或字典，则可以使用签名模块的`dumps`和`loads`功能来实现。它们模仿Python的pickle模块，但在后台使用JSON序列化。JSON可确保即使你的`SECRET_KEY`被盗，攻击者也无法利用pickle执行任意命令：

```python
>>> from django.core import signing
>>> value = signing.dumps({"foo": "bar"})
>>> value
'eyJmb28iOiJiYXIifQ:1NMg1b:zGcDE4-TCkaeGzLeW9UQwZesciI'
>>> signing.loads(value)
{'foo': 'bar'}
```

由于JSON的性质（列表和元组之间没有本质的区别），如果传入一个元组，返回的是一个列表 `signing.loads(object)`：

```python
>>> from django.core import signing
>>> value = signing.dumps(('a','b','c'))
>>> signing.loads(value)
['a', 'b', 'c']
```

