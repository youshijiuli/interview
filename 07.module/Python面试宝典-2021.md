## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目19：说说你用过Python标准库中的哪些模块。

> **点评**：Python标准库中的模块非常多，建议大家根据自己过往的项目经历来介绍你用过的标准库和三方库，因为这些是你最为熟悉的，经得起面试官深挖的。

| 模块名                       | 介绍                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| sys                          | 跟Python解释器相关的变量和函数，例如：`sys.version`、`sys.exit()` |
| os                           | 和操作系统相关的功能，例如：`os.listdir()`、`os.remove()`    |
| re                           | 和正则表达式相关的功能，例如：`re.compile()`、`re.search()`  |
| math                         | 和数学运算相关的功能，例如：`math.pi`、`math.e`、`math.cos`  |
| logging                      | 和日志系统相关的类和函数，例如：`logging.Logger`、`logging.Handler` |
| json / pickle                | 实现对象序列化和反序列的模块，例如：`json.loads`、`json.dumps` |
| hashlib                      | 封装了多种哈希摘要算法的模块，例如：`hashlib.md5`、`hashlib.sha1` |
| urllib                       | 包含了和URL相关的子模块，例如：`urllib.request`、`urllib.parse` |
| itertools                    | 提供各种迭代器的模块，例如：`itertools.cycle`、`itertools.product` |
| functools                    | 函数相关工具模块，例如：`functools.partial`、`functools.lru_cache` |
| collections / heapq          | 封装了常用数据结构和算法的模块，例如：`collections.deque`    |
| threading / multiprocessing  | 多线程/多进程相关类和函数的模块，例如：`threading.Thread`    |
| concurrent.futures / asyncio | 并发编程/异步编程相关的类和函数的模块，例如：`ThreadPoolExecutor` |
| base64                       | 提供BASE-64编码相关函数的模块，例如：`bas64.encode`          |
| csv                          | 和读写CSV文件相关的模块，例如：`csv.reader`、`csv.writer`    |
| profile / cProfile / pstats  | 和代码性能剖析相关的模块，例如：`cProfile.run`、`pstats.Stats` |
| unittest                     | 和单元测试相关的模块，例如：`unittest.TestCase`              |

#### 题目36：如何使用`random`模块生成随机数、实现随机乱序和随机抽样？

> **点评**：送人头的题目，因为Python标准库中的常用模块应该是Python开发者都比较熟悉的内容，这个问题回如果答不上来，整个面试基本也就砸锅了。

1. `random.random()`函数可以生成`[0.0, 1.0)`之间的随机浮点数。
2. `random.uniform(a, b)`函数可以生成`[a, b]`或`[b, a]`之间的随机浮点数。
3. `random.randint(a, b)`函数可以生成`[a, b]`或`[b, a]`之间的随机整数。
4. `random.shuffle(x)`函数可以实现对序列`x`的原地随机乱序。
5. `random.choice(seq)`函数可以从非空序列中取出一个随机元素。
6. `random.choices(population, weights=None, *, cum_weights=None, k=1)`函数可以从总体中随机抽取（有放回抽样）出容量为`k`的样本并返回样本的列表，可以通过参数指定个体的权重，如果没有指定权重，个体被选中的概率均等。
7. `random.sample(population, k)`函数可以从总体中随机抽取（无放回抽样）出容量为`k`的样本并返回样本的列表。

> **扩展**：`random`模块提供的函数除了生成均匀分布的随机数外，还可以生成其他分布的随机数，例如`random.gauss(mu, sigma)`函数可以生成高斯分布（正态分布）的随机数；`random.paretovariate(alpha)`函数会生成帕累托分布的随机数；`random.gammavariate(alpha, beta)`函数会生成伽马分布的随机数。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目41：说一下你对Python中模块和包的理解。

每个Python文件就是一个模块，而保存这些文件的文件夹就是一个包，但是这个作为Python包的文件夹必须要有一个名为`__init__.py`的文件，否则无法导入这个包。通常一个文件夹下还可以有子文件夹，这也就意味着一个包下还可以有子包，子包中的`__init__.py`并不是必须的。模块和包解决了Python中命名冲突的问题，不同的包下可以有同名的模块，不同的模块下可以有同名的变量、函数或类。在Python中可以使用`import`或`from ... import ...`来导入包和模块，在导入的时候还可以使用`as`关键字对包、模块、类、函数、变量等进行别名，从而彻底解决编程中尤其是多人协作团队开发时的命名冲突问题。

---

## Python面试宝典 - 基础篇 - 2021
> 来源：demo07.md

#### 题目31：谈谈你对“猴子补丁”（monkey patching）的理解。

“猴子补丁”是动态类型语言的一个特性，代码运行时在不修改源代码的前提下改变代码中的方法、属性、函数等以达到热补丁（hot patch）的效果。很多系统的安全补丁也是通过猴子补丁的方式来实现的，但实际开发中应该避免对猴子补丁的使用，以免造成代码行为不一致的问题。

在使用`gevent`库的时候，我们会在代码开头的地方执行`gevent.monkey.patch_all()`，这行代码的作用是把标准库中的`socket`模块给替换掉，这样我们在使用`socket`的时候，不用修改任何代码就可以实现对代码的协程化，达到提升性能的目的，这就是对猴子补丁的应用。

另外，如果希望用`ujson`三方库替换掉标准库中的`json`，也可以使用猴子补丁的方式，代码如下所示。

```Python
import json, ujson

json.__name__ = 'ujson'
json.dumps = ujson.dumps
json.loads = ujson.loads
```

单元测试中的`Mock`技术也是对猴子补丁的应用，Python中的`unittest.mock`模块就是解决单元测试中用`Mock`对象替代被测对象所依赖的对象的模块。
