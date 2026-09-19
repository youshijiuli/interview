# 第七章 前端

> 来源：Python阶段面试题v2.md

1. JavaScript(或jQuery)如何选择一个id为main的容器

2. JavaScript(或jQuery)如何选择一个class为menu的容器

3. 简述什么是浏览器时间流

4. 用css如何隐藏一个元素

5. 一行css实现padding上下左右分别为1px, 2px,3px, 4px

6. 前后端分离的基本原理。

7. 前后端分离的通信数据安全

8. 给ul设置样式为:背景色黑色,给ul下的ui设置样式为: 宽度30px, 背景红色

9. 用bootstrap写一个响应式栅格, 一个页面分左右两栏, 大屏情况下分6/6, 小屏情况下分为12/12 (大屏: 屏幕>=992px, 小屏;992px>=屏幕>=768px)

10. 写一个正则表达式获取HTML源码中的编码, 如下的编码是;utf-8怎么通过Python的热模块获得?

    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>404</title>
    </head>
    ```

11. 如何创建响应式布局？

12. 你曾经使用过哪些前端框架？

13. 什么是ajax请求？并使用jQuery和XMLHttpRequest对象实现一个ajax请求。

14. 如何在前端实现轮训？

15. 如何在前端实现长轮训？

16. vuex的作用？

17. vue中的路由的拦截器的作用？

18. axios的作用？

19. 列举vue的常见指令。

20. 简述jsonp及其原理？

21. 简述cors及其原理？

22. 看javascript代码写结果：

    ```javascript
    var name = '武沛齐';
    function func(){
    	var name = 'alex';
        function inner(){
            console.log(name);
        }
        return inner;
    }
    var ret = func();
    ret()
    ```

23. 看javascript代码写结果：

    ```javascript
    function main(){
        if(1==1){
            var name = "武沛齐";
        }
        console.log(name);
    }
    ```

24. 看javascript代码写结果：

    ```javascript
    var name = "武沛齐";
    function func(){
        var name = "alex";
        function inner(){
            var name = "老男孩";
            console.log(name);
        }
        return inner();
    }
    func();
    ```

25. 看javascript代码写结果：

    ```javascript
    function func(){
        console.log(name);
        var name = "武沛齐";
    }
    ```

26. 看javascript代码写结果：

    ```javascript
    var name = "武沛齐";
    function Foo(){
        this.name = "alex"；
        this.func = function(){
            console.log(this.name);
        }
    }
    var obj = new Foo();
    obj.func();
    ```

27. 看javascript代码写结果：

    ```javascript
    var name = "武沛齐";
    var info = {
        name: 'alex';
        func:function(){
            console.log(this.name);
            (function(){
    	        console.log(this.name);
            })()
        }
    }
    info.func();
    ```

28. 看javascript代码写结果：

    ```javascript
    var name = "武沛齐";
    var info = {
        name: 'alex';
        func:function(){
            console.log(this.name);
            var that = this;
            (function(){
    	        console.log(that.name);
            })()
        }
    }
    info.func();
    ```
