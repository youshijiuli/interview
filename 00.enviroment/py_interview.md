##### 列举你所了解的所有Python2和Python3的区别
[python2和python3的区别](https://blog.csdn.net/weixin_41819299/article/details/81259721)
1. python2没有nonlocal关键字，要修改临时变量只能将其改成可变数据类型，如数组。b=[a]
2. print()函数代替print语句
3.  Python3加入 Unicode 字符串，用以编码存储字符串。比如用 utf-8可以用来输入中文
4.  Python3去掉long类型，新增了bytes。
5.  Python 3整数之间做除法可以得到浮点数的结果，不需要进行数据格式转换1/2=0.5 Python 2整数int间除法结果为把运算结果去尾的整数1/2=0，3/2.0=1.5
6.   Python3 中 range()，Python2 中 xrange()。
7.   python2中的不等于号可以是!=或者<>，python3只能是!=
8.   python2中raw_input()用来输入字符串，而python3中使用input()来输入字符串

##### py2项目如何迁移成py3
1. 先备份原文件，然后使用python3自带工具2to3.py将py2文件转换位py3文件
2. 手动将不兼容的代码改写成兼容py3的代码

##### 用一行代码实现数值交换
* a=1
* b=2
* 答案：a,b=b,a

##### python3和python2中int和long的区别
* python2中有long类型，python3中没有long类型，只有int类型。python3中的int类型包括了long类型。

##### xrange和range的区别
* xrange和range用法相同，但是xrange是一个生成器，range结果是一个列表。xrange做循环的时候性能比range好。

---

python-interview

[最新版本链接地址](https://github.com/wangyitao/python-interview)

##### 为什么学python

[为什么学python](https://blog.csdn.net/Darkman_EX/article/details/81101232)

* 答题路线：a、python的优点，b、python的应用领域广
* 具体：
    * 优点
        * 1、python语法非常优雅，简单易学
        *  2、免费开源
        *  3、跨平台，可以自由移植
        *  4、可扩展，可嵌入性强
        *  5、第三方库丰富

    * 应用领域
        * 1、在系统编程中应用广泛，比如说shell工具。
        * 2、在网络爬虫方面功能非常强大，常用的库如scrapy，request等
        * 3、在web开发中使用也很广泛，如很多大型网站都用python开发的，如ins，youtube等，常用的框架如django，flask等
        * 4、python在系统运维中应用广泛，尤其在linux运维方面，基本上都是自动化运维。
        * 5、在人工智能，云计算，金融等方面也应用非常广泛。


##### 通过什么途径学习python

* 通过看官方文档
* 通过哔哩哔哩上的视频教程
* 通过百度查资料
* 通过买python相关方面的书


##### 公司线上和开发环境使用的什么系统

* 线上用的centos和Ubuntu系统
* 开发环境用的windows，mac，还有Ubuntu。


##### python和java、php、c、c#、c++ 等其他语言对比？

* Java C# PHP Python (开发效率高)，这些语言本身不需要你去管理内存了。它们都有自己的虚拟机，对于开辟内存、释放内存都由这个虚拟机处理。
* C 和 Python、Java、C#等C语言： 代码编译得到 机器码 ，机器码在处理器上直接执行，每一条指令控制CPU工作其他语言： 代码编译得到 字节码 ，虚拟机执行字节码并转换成机器码再后在处理器上执行Python 和 C Python这门语言是由C开发而来　　
* 对于使用：Python的类库齐全并且使用简洁，如果要实现同样的功能，Python 10行代码可以解决，C可能就需要100行甚至更多.
* 对于速度：Python的运行速度相较与C，绝逼是慢了Python 和 Java、C#等　　
* 对于使用：Linux原装Python，其他语言没有；以上几门语言都有非常丰富的类库支持
* 对于速度：Python在速度上可能稍显逊色所以，Python和其他语言没有什么本质区别，其他区别在于：擅长某领域、人才丰富、先入为主


##### 简述解释型和编译型编程语言

* 解释型语言编写的程序不需要编译，在执行的时候，专门有一个解释器能够将VB语言翻译成机器语言，每个语句都是执行的时候才翻译。这样解释型语言每执行一次就要翻译一次，效率比较低。
* 用编译型语言写的程序执行之前，需要一个专门的编译过程，通过编译系统，把源高级程序编译成为机器语言文件，翻译只做了一次，运行时不需要翻译，所以编译型语言的程序执行效率高，但也不能一概而论，部分解释型语言的解释器通过在运行时动态优化代码，甚至能够使解释型语言的性能超过编译型语言。

##### python解释器种类以及特点

* CPython
    * c语言开发的 使用最广的解释器
* IPython
    * 基于cpython之上的一个交互式计时器 交互方式增强 功能和cpython一样
* PyPy
    * 目标是执行效率 采用JIT技术 对python代码进行动态编译，提高执行效率
* JPython
    * 运行在Java上的解释器 直接把python代码编译成Java字节码执行
* IronPython
    * 运行在微软 .NET 平台上的解释器，把python编译成. NET 的字节码

---

##### git的常见命令

[参考链接](https://www.cnblogs.com/my--sunshine/p/7093412.html)

* git init：在本地新建一个repo,进入一个项目目录,执行git init,会初始化一个repo,并在当前文件夹下创建一个.git文件夹.

* git clone：获取一个url对应的远程Git repo, 创建一个local copy.

* git status：查询repo的状态。

* git log：查看一个分支的提交历史。

* git diff：查看当前文件和暂存区域之间的差异

* git commit：提交已经被add进来的改动

* git reset：还原到某个提交状态

* git checkout：切换分支

* git merge：把一个分支merge进当前的分支

* git tag：在一个提交上建立一个书签

* git pull：更新本地

* git push：提交分支到远程服务器

* git stash：吧当前改动压入一个栈

---

##### 获取python解释器版本的方法
* 终端执行python -V
