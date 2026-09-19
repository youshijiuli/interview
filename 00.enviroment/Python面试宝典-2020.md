## Python面试宝典 - 基础篇 - 2020
> 来源：Python面试宝典-2020.md

#### 题目30：说一下Python 2和Python 3的区别。

> **点评**：这种问题千万不要背所谓的参考答案，说一些自己最熟悉的就足够了。

1. Python 2中的`print`和`exec`都是关键字，在Python 3中变成了函数。
2. Python 3中没有`long`类型，整数都是`int`类型。
3. Python 2中的不等号`<>`在Python 3中被废弃，统一使用`!=`。
4. Python 2中的`xrange`函数在Python 3中被`range`函数取代。
5. Python 3对Python 2中不安全的`input`函数做出了改进，废弃了`raw_input`函数。
6. Python 2中的`file`函数被Python 3中的`open`函数取代。
7. Python 2中的`/`运算对于`int`类型是整除，在Python 3中要用`//`来做整除除法。
8. Python 3中改进了Python 2捕获异常的代码，很明显Python 3的写法更合理。
9. Python 3生成式中循环变量的作用域得到了更好的控制，不会影响到生成式之外的同名变量。
10. Python 3中的`round`函数可以返回`int`或`float`类型，Python 2中的`round`函数返回`float`类型。
11. Python 3的`str`类型是Unicode字符串，Python 2的`str`类型是字节串，相当于Python 3中的`bytes`。
12. Python 3中的比较运算符必须比较同类对象。
13. Python 3中定义类的都是新式类，Python 2中定义的类有新式类（显式继承自`object`的类）和旧式类（经典类）之分，新式类和旧式类在MRO问题上有非常显著的区别，新式类可以使用`__class__`属性获取自身类型，新式类可以使用`__slots__`魔法。
14. Python 3对代码缩进的要求更加严格，如果混用空格和制表键会引发`TabError`。
15. Python 3中字典的`keys`、`values`、`items`方法都不再返回`list`对象，而是返回`view object`，内置的`map`、`filter`等函数也不再返回`list`对象，而是返回迭代器对象。
16. Python 3标准库中某些模块的名字跟Python 2是有区别的；而在三方库方面，有些三方库只支持Python 2，有些只能支持Python 3。
