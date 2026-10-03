# python面试题带答案







## py2和py3的区别



- print成为函数 【print语句没有了，取而代之的是print\(\)函数】

- 编码问题。python3不再有unicode对象，默认str就是unicode

- 除法变化。python3除号返回浮点数，如果要返回整数，应使用//

- 类型注解。帮助IDE实现类型检查

- 优化的super\(\)方便直接调用父类函数。Python3\.x 和 Python2\.x 的一个区别是: Python 3 可以使用直接使用 super\(\)\.xxx 代替 super\(Class, self\)\.xxx :

- 高级解包操作。a, b, \*rest = range\(10\)

- keyword only arguments。限定关键字参数

- chained exceptions。python3重新抛出异常不会丢失栈信息

- 一切返回迭代器。range, zip, map, dict\.values, etc\. are all iterators

- 性能优化等。。。



2. unicode

Python 2 有 ASCII str\(\) 类型，unicode\(\) 是单独的，不是 byte 类型。

现在， 在 Python 3，我们最终有了 Unicode \(utf\-8\) 字符串，以及一个字节类：byte 和 bytearrays。

Python3\.X 源码文件默认使用utf\-8编码

Python2

1. `str` = **字节串\(bytes\)**，存原始二进制字节，默认ASCII编码，不直接支持中文。

2. `unicode` = **真正的字符串**，存储Unicode字符。

```Plain Text
# Python2
s = "中文"       # str，一堆gbk/utf‑8字节，不是字符
u = u"中文"     # unicode类型，真正的文本
```

坑：直接打印、拼接很容易乱码，要频繁 `decode` / `encode` 来回转换。

> Python2源码文件默认编码不是utf‑8，如果写中文，必须顶部写 `# -*- coding:utf-8 -*-`，否则直接报错。
> 
> 

---

Python3

1. `str` 全部是**Unicode字符串**，我们日常写的字符串，全部存字符，内部用Unicode，默认utf‑8展示。

2. 二进制单独分出两种类型：`bytes`、`bytearray`，专门存原始字节。

```Python
# Python3
s = "中文"    # str(Unicode)，文本
b = b"abc"   # bytes，原始字节
```

- `str` ↔ `bytes` 必须显式转换：

    - `str.encode("utf‑8")` → bytes 字符串转字节

    - `bytes.decode("utf‑8")` → str 字节转回字符串

> Python3 **源码文件默认编码就是 UTF‑8**，代码里写中文注释、中文字符串，不用再加编码声明，不会报编码错误。
> 
> 

---

## 一句话总结

1. **Py2：str是字节，unicode才是文本；源码默认不是utf‑8。**

2. **Py3：str就是Unicode文本，bytes专门管二进制；源码默认utf‑8。**

### 高频面试考点

- Py2：`str` ≠ 文本；Py3：`str` = Unicode文本

- Py3去掉了`unicode()`这个类型，统一用`str`；二进制交给`bytes`

- Py3脚本不用写`# -*- coding:utf‑8 -*-`，默认就是utf‑8

### 记忆

> 文本用str，网络/文件二进制用bytes；二者不能直接拼接，必须encode/decode。
> 
> 







**参考资料**

python2和python3中调用父类方法

https://cloud\.tencent\.com/developer/article/1365782

https://www\.runoob\.com/python/python\-func\-super\.html

