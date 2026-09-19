##### JavaScript(或者jQuery)如何选择一个id为main的容器

> jquery：$('#id')
> JavaScript：document.getElementById("id"))


##### css如何隐藏一个元素
* display：none

##### 前后端分离的基本原理
[参考链接](https://www.cnblogs.com/Kevin-ZhangCG/p/9501635.html)

* 前后端分离并非仅仅只是一种开发模式，而是一种架构模式（前后端分离架构）。前端项目与后端项目是两个项目，放在两个不同的服务器，需要独立部署，两个不同的工程，两个不同的代码库，不同的开发人员。前后端工程师需要约定交互接口，实现并行开发，开发结束后需要进行独立部署，前端通过Ajax来调用HTTP请求调用后端的restful api。前端只需要关注页面的样式与动态数据的解析&渲染，而后端专注于具体业务逻辑。

##### 如何保证api调用时数据的安全性
1. 通信使用https
2. 请求签名，防止参数被篡改
3. 身份确认机制，每次请求都要验证是否合法
4. app中使用ssl pinning防止抓包操作
5. 对所有的请求和响应都进行加解密操作

##### 如何实现响应式布局
1. 流体布局
    * 其实就是度量单位的改变。在响应式设计的布局中，不在把像素(px)作为唯一的单位，而是采用%或者是混合%、px为单位，设计出自己想要的布局方式。
2. 媒体查询
    * 媒体查询可以在你根据特定的环境下查询到各种属性---------比如设备类型，分辨率、屏幕物理尺寸以及色彩等。通过使用媒体查询，可以获得设备的一些特性，以及响应式的布局方案。
3. 弹性图片
    * 其实在做响应式布局时，大多用到的是弹性盒子进行布局，那么在设置图片的地方也应该具有一些变化以适应布局的变化。出了图片外，像图标啦！视频啦也应做一些调整用以适应布局的变化。

##### 曾经使用过哪些前端框架
* react，vue，bootstrap，elementUI，Echarts

##### 什么是ajax请求？手写一个ajax请求
* ajax（异步JavaScript和XML）是指一种创建交付式网页应用的网页开发技术。可以在不重新加载整个网页的情况下，对网页的某部分进行更新。
```javascript
// 不使用第三方
var xhr = new XMLHttpRequest();
xhr.open("GET", url, false);
xhr.onreadtstatechange = function () {
    if (xhr.readystate == 4) {
        //响应内容解析完成，可以在客户端调用了
        if (xhr.status == 200) {
            //客户端的请求成功了
            alert(xhr.responseText);
        }
    }
}
xhr.send(null);

// 使用ajax

$.ajax({
            type:"GET",
            url:"",
            dataType:"json",
            success:function(data){
            },
            error:function(jqXHR){
            }
        });

```

##### 什么是轮询和长轮询
* 轮询是在特定的的时间间隔（如每1秒），由浏览器对服务器发出HTTP request，然后由服务器返回最新的数据给客户端的浏览器。这种传统的HTTP request 的模式带来很明显的缺点 – 浏览器需要不断的向服务器发出请求，然而HTTP request 的header是非常长的，里面包含的有用数据可能只是一个很小的值，这样会占用很多的带宽。
```javascript
var xhr = new XMLHttpRequest();         
    setInterval(function(){
        xhr.open('GET','/user'); 
        xhr.onreadystatechange = function(){ }; 
        xhr.send();
    },1000)
```

* 长轮询是ajax实现:在发送ajax后,服务器端会阻塞请求直到有数据传递或超时才返回。 客户端JavaScript响应处理函数会在处理完服务器返回的信息后，再次发出请求，重新建立连接。

```javascript
 function ajax(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET','/user');
        xhr.onreadystatechange = function(){
              ajax();
        };
        xhr.send();
    }
```

##### vuex的作用

1. 组件之间的数据通信
2. 使用单向数据流的方式进行数据的去中心化管理

##### vue中的路由拦截器的作用

* 当某些页面需要访问权限时，可以使用路由拦截器对用户权限进行判断

##### axios的作用

* axios是基于promise的用于浏览器和nodejs的HTTP客户端，本身有以下特征：
  1. 从浏览器中创建XMLHttpRequest；
  2. 从nodejs发出http请求
  3. 支持promiseAPI
  4. 拦截 请求和响应
  5. 转换请求和响应数据
  6. 取消请求
  7. 自动转换JSON数据
  8. 客户端支持防止CSRF/XSRF攻击

##### 简述jsonp及其原理

* JSONP是JSON with Padding的略称。它是一个非官方的协议，它允许在服务器端集成Script tags返回至客户端，通过javascript callback的形式实现跨域访问（这仅仅是JSONP简单的实现形式）

* 原理：<script>标签的src属性并不被同源策略所约束，所以可以获取任何服务器上脚本并执行。

  ```javascript
  <script type="text/javascript" src="http://localhost:20002/test.js"></script>
  ```
