# python-面试通关宝典

### **爬虫相关**

#### 130.在 requests 模块中，requests.content 和 requests.text 什么区别？

```
resp.text返回的是Unicode型的数据。

resp.content返回的是bytes型也就是二进制的数据。
也就是说，如果你想取文本，可以通过r.text。

如果想取图片，文件，则可以通过r.content。

（resp.json()返回的是json格式数据）
```

#### 131.简要写一下 lxml 模块的使用方法框架。

```markdown
Python 标准库中自带了 xml 模块，但是性能不够好，而且缺乏一些人性化的 API，相比之下，第三方库 lxml 是用 Cython 实现的，而且增加了很多实用的功能，可谓爬虫处理网页数据的一件利器。lxml 大部分功能都存在 lxml.etree中.
可以看一下官方文档，https://lxml.de/index.html
```

#### 132.说一说 scrapy 的工作流程。

![](http://ww4.sinaimg.cn/large/006tNc79gy1g5vk6vdn28j312w0q4dhd.jpg)

#### 133.简述 scrapy 的去重原理。

```Python
1.需要将dont_filter设置为False开启去重，默认是False，开启去重；

2.对于每一个url的请求，调度器都会根据请求得相关信息加密得到一个指纹信息，并且将指纹信息和set()集合中的指纹信息进行比对，如果set()集合中已经存在这个数据，就不在将这个Request放入队列中。如果set()集合中没有存在这个加密后的数据，就将这个Request对象放入队列中，等待被调度
```

#### 134.scrapy 中间件有几种类，你用过哪些中间件？

```
scrapy自带两种中间件，下载器中间件（DownloaderMiddleware）,爬虫中间件（spiderMiddleware）
DownloaderMiddleware的作用是在request之前或者response之后，对spider进行配置处理，例如动态更换ip，更换user-agent,更换cookie等
Spider中间件是介入到Scrapy的spider处理机制的钩子框架，您可以添加代码来处理发送给 Spiders 的response及spider产生的item和request。
```

#### 135.你写爬虫的时候都遇到过什么反爬虫措施，你是怎么解决的？

```
可以看看这篇博文https://blog.csdn.net/weixin_33768481/article/details/87273454
```

#### 136.为什么会用到代理？

```
单一ip频繁重复请求同一个网站会被封掉
```

#### 137.代理失效了怎么处理？

```
构建代理池，动态更换ip
```

#### 138.列出你知道 header 的内容以及信息。

```
user-agent
referer
content-type
content-length
.....
详情可以看这篇https://kb.cnblogs.com/page/92320/
```

#### 139.说一说如何打开浏览器访问 www.baidu.com 获取到结果，简述整个流程。

```
可参考这篇博文https://www.jianshu.com/p/d616d887953a
```

#### 140.爬取速度过快时，出现了验证码怎么处理？

```
比较简单的验证码，可以用Python的PIL库（from PIL import Image）,tesserocr模块；
比较复杂的话可以引入机器学习模型，但是成本会比较高，最好还是使用高质量的代理ip，避免触发验证码。
```

#### 141.scrapy 和 scrapy-redis 有什么区别？为什么选择 redis 数据库？

```
1) scrapy是一个Python爬虫框架，爬取效率极高，具有高度定制性，但是不支持分布式。而scrapy-redis一套基于redis数据库、运行在scrapy框架之上的组件，可以让scrapy支持分布式策略，Slaver端共享Master端redis数据库里的item队列、请求队列和请求指纹集合。

2) 为什么选择redis数据库，因为redis支持主从同步，而且数据都是缓存在内存中的，所以基于redis的分布式爬虫，对请求和数据的高频读取效率非常高。
```

#### 142.分布式爬虫主要解决什么问题？

```
1)ip

2)带宽

3）cpu

4）io
```

#### 143.写爬虫是用多进程好还是多线程好？ 为什么？

```
IO密集型代码(文件处理、网络爬虫等)，多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。在实际的数据采集过程中，既考虑网速和响应的问题，也需要考虑自身机器的硬件情况，来设置多进程或多线程
```

#### 144.解析网页的解析器使用最多的是哪几个？

```
xpath,css-selector,beautifulSoup
```

#### 145.需要登录的网页，如何在不使用动态爬取的情况下解决 ip、cookie 和 session（其中有一些是动态生成的）的同时限制？

```
解决限制IP可以使用代理IP地址池、服务器；

不适用动态爬取的情况下可以使用反编译JS文件获取相应的文件，或者换用其他平台（比如手机端）看看是否可以获取相应的json文件
```

#### 146.验证码的解决。

```
图形验证码：干扰、杂色不是特别多的图片可以使用开源库Tesseract进行识别，太过复杂的需要借助第三方打码平台

点击和拖动滑块验证码可以借助selenium、无图形界面浏览器（chromedirver或者phantomjs）和pillow包来模拟人的点击和滑动操作，pillow可以根据色差识别需要滑动的位置
```

#### 147.使用的最多的数据库（mysql，mongodb，redis 等）有哪些？并简述对它的理解？

```
这个自由发挥了，多看下MySQL和MongoDB的使用，了解Redis的基本数据结构
```
