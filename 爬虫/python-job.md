## 爬虫相关知识

### Scrapy需要了解的类  
去重 RepeatFilter()类  
序列化 Pipeline()类  
终止 DropItem()类  
信号 - 预留钩子扩展 sinals  

### Scrapy框架数据流（重要！面试官一般问：说说Scrapy原理）  
Scrapy中的数据流由执行引擎控制，其过程如下：  
* 引擎从Spiders中获取到的最初的要爬取的请求(Requests)。  
* 引擎安排请求(Requests)到调度器中，并向调度器请求下一个要爬取的请求(Requests)。  
* 调度器返回下一个要爬取的请求(Request)给请求。  
* 引擎从上步中得到的请求(Requests)通过下载器中间件(Downloader Middlewares)发送给下载器(Downloader),这个过程中下载器中间件(Downloader Middlerwares)中的 process\_request() 函数就会被调用。  
* 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(Downloader Middlewares)中的 process\_response() 函数，最后返回给引擎  
* 引擎从下载器中得到上步中的Response并通过Spider中间件(Spider Middewares)发送给Spider处理，这个过程中Spider中间件(Spider Middlewares)中的 process\_spider\_input() 函数会被调用到。  
* Spider处理Response并通过Spider中间件(Spider Middlewares)返回爬取到的Item及(跟进的)新的Request给引擎，这个过程中Spider中间件(Spider Middlewares)的 process\_spider\_output() 函数会被调用到。  
* 上步中Spider处理的结果可能是Item和Request，引擎将其爬取到的Item给Item管道(Piplline),将Requests发送给调度器，并向调度器请求可能存在的下一个要爬取的请求(Requests)  
* (从第二步)重复知道调度器中没有更多的请求(Requests)。  

### 反爬的一般手段  
* 遵守robots 协议  
* 限制频率  
* 图像识别验证码  
* 多账号反爬  
* 代理池  
* 分布式爬虫  
* 保存cookies,带上cookie去访问，或某些场景不要带cookies访问  
* 一般来说移动端、app的页面反爬手段相对少  
* 使用PhantomJS，Selenium模拟浏览器  

  参考:[如何应对网站反爬虫策略？如何高效地爬大量数据?](https://www.zhihu.com/question/28168585)  

### 常见的反爬虫和应对方法？（爬虫与反爬虫的博弈）  

#### __通过Headers反爬虫__  
从用户请求的Headers反爬虫是最常见的反爬虫策略。很多网站都会对Headers的User-Agent进行检测，还有一部分网站会对Referer进行检测（如一些资源网站的防盗链、知乎）。如果遇到了这类反爬虫机制，可以直接在爬虫中添加Headers，构造随机UA和Refer等参数即可绕过。  

#### __基于用户行为反爬虫__  
还有一部分网站是通过检测用户行为，例如同一IP短时间内多次访问同一页面，或者同一账户短时间内多次进行相同操作。  
大多数网站都是前一种情况，对于这种情况，使用IP代理就可以解决。可以专门写一个爬虫，爬取网上公开的代理ip，检测后全部保存起来。  
对于第二种情况，可以在每次请求后随机间隔几秒再进行下一次请求。有些有逻辑漏洞的网站，可以通过请求几次，退出登录，重新登录来绕过。也可以采用多账号策略。  

  
#### __动态页面的反爬虫__  
上述的几种情况大多都是出现在静态页面，还有一部分网站，我们需要爬取的数据是通过ajax请求得到，或者通过JavaScript生成的。首先用Fiddler对网络请求进行分析。如果能够找到ajax请求返回的目标数据，就直接模拟ajax请求。  
但是有些网站把ajax请求的所有参数全部加密了。这种情况可以初步分析JS文件看是否能找到解密方法进行解密，有的网站会进行JS混淆，这种情况可以尝试单独执行js解密会比较困难，一般做法是使用selenium模拟人为操作爬取数据。  
用这套框架几乎能绕过大多数的反爬虫。利selenium+phantomJS能干很多事情，例如识别点触式（12306）或者滑动式的验证码，对页面表单进行暴力破解等。    

  
#### __通过前端CSS和HTML标签进行干扰混淆进行反爬__  
前端通过CSS和HTML标签进行干扰混淆关键数据，防止爬虫轻易获取数据  
__1 . font-face，自定义字体干扰__  
如列子：汽车之家论帖子，猫眼电影电影评分 [http://maoyan.com/films/342601](http://maoyan.com/films/342601)  
破解思路： 找到ttf字体文件地址，然后下载下来，使用font解析模块包对ttf文件进行解析，可以解析出一个字体编码的集合，与dom里的文字编码进行映射，然后根据编码在ttf里的序号进行映射出中文  
可以使用FontForge/FontCreator工具打开ttf文件进行分析  
__2 . 伪元素隐藏式__  
通过伪元素来显示重要数据内容  
如例子：[汽车之家](https://car.autohome.com.cn/config/series/3170.html)   
破解思路： 找到样式文件，然后根据HTML标签里class名称，匹配出CSS里对应class中content的内容进行替换  
__3 . backgroud-image__  
如例子：美团 价格显示  
通过背景图片的position位置偏移量，显示数字/符号，如：价格，评分等  
根据backgroud-postion值和图片数字进行映射  
__4 . html标签干扰__  
通过在重要数据的标签里加入一些有的没的隐藏内容的标签，干扰数据的获取  
如例子：[全网代理IP](http://www.goubanjia.com/)   
破解思路： 过滤掉干扰混淆的HTML标签，或者只读取有效数据的HTML标签的内容.通过移除干扰标签里有display:none隐藏标签，然后再获取text就不会有干扰的内容了  
__5 . 字体替换__  
去哪儿手机版酒店价格获取，如何通过 css 计算元素的绝对定位  
参考：[去哪儿 m 版酒店价格获取，如何通过 css 计算元素的绝对定位](https://www.v2ex.com/t/354305)  
你会发现一个问题，就是页面展示的数字和html文件里的数字不一致  
1240的价格在html里竟然是4230  
根据css你会发现他们用了一个字体，打开你就发现了一件事  
正常字体是0123456789，在去哪儿官方的字体里被替换成了图片里的  
然后你根据这个做一些对应解析，就可以爬出正确的数据了。    

#### __投毒，以及喂毒（蜜罐）__  
有些网站搞一些正常的url pattern 的页面 链接做成隐藏链接 正常用户看不到，但是大部分爬虫就爬进去了，然后监控这些页面被访问的ip就可以了，基本都是爬虫  
还有些平台发现爬虫后并不会进行限制封杀，而是给爬虫提供误导的数据，影响他们进行错误的决策，这就是喂毒  
为了防止被投毒喂毒，需要对数据进行抽样校验。另外需要分析其投毒逻辑以尽量避免自己的爬虫中陷阱被识别出来    

### 投毒反爬策略    
从链接发现下手可以搞一些正常的url pattern 的页面 链接做成隐藏链接 正常用户看不到（比如白底白字，或者被遮盖） 但是大部分爬虫就爬进去了 [然后就对这些ip做惩罚就行了比如www.xxx.com?id=12345](http://xn--ipwww-g31hye02mx7k98nfsggtafa520o6t2bw8rs48c0w7ae83a.xxx.com?id=12345) 大部分id参数是正常页面 把一些id做成只有隐藏链接的假id 监控这些页面被访问的ip 然后收割吧 基本都是爬虫  

青铜反爬：请求头上做点基本的检验  
白银反爬：限制访问频率，封 IP，跳图形验证码，infinite redirect loop，需要登录  
黄金反爬：前端 js script 实时计算 parameter 加给请求在后端进行验证  
铂金反爬：翻页使用 ajax ，没有 pagination ，数据以 json 形式在前端异步加载，验证参数不正确随机截断 html  
钻石反爬：异地登录需要手机短信验证，拖动、拼图等各类人机验证码  
王者反爬：我们公司的前端写的代码让你的爬虫在 parse html 阶段的难度上升为 nlp ：）   

### 为什么要做分布式爬虫    
分布式爬虫通常会有一些教材告诉你，为了爬取效率，需要把爬虫分布式部署到多台机器上。这完全是骗人的。  
分布式作用是：防止对方封IP，以及避免使用代理IP，因为一些实时性要求比较高的爬虫系统，使用代理IP响应时间太长  

[干货！分享一个调试 cookies 的东西，只要监控到 cookies 被改写，就自动跳断点](https://github.com/paulirish/break-on-access)
