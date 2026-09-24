# HttpServer
一个简易的HTTP服务器的实现 (Python)

source link:
> https://blog.csdn.net/hxxjxw/article/details/105805478


---

<br>



## 开发环境
* Python 3.7
* IDE：Pycharm

<br>



## 功能
* 能访问 127.0.0.1:9999

* 能访问 127.0.0.1:9999/index.html

* 能够用用户名和密码登录127.0.0.1:9999/index.html，然后页面会自动跳转到另一个页面

  <br>

* 自定义实现了GET和POST方法

* 多线程

<br>



## 运行方式
   运行test.py

<br>



## 文件说明

* socket_server.py是TCP server

* base_handler.py是TCP协议封装字节流网络请求处理

  <br>

* base_http_server是基础http服务器，继承socket_server
* base_http_handler是基础处理http请求的类，继承base_handler

<br>

* simple_http_handler，继承base_http_server
* simple_http_server，继承base_http_handler
* 是在基础http服务器和处理类的基础上，自定义实现了GET和POST方法

<br>

test.py直接运行是跑simple.http.server的
其main函数中还有个SocketServerTest().run()，运行它可以测试TCPServer

<br>



## 项目具体过程

https://blog.csdn.net/hxxjxw/article/details/105805478

