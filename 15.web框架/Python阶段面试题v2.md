# 第十一章 api

> 来源：Python阶段面试题v2.md

1. 什么是webservice？

2. 什么是rpc？

3. 谈谈你对restfull 规范的认识？

4. 什么是接口的幂等性？

5. 为什么要使用django rest framework框架？

6. django rest framework框架中都有那些组件？

7. 使用django rest framework框架编写视图时都继承过哪些类？

8. django rest framework框架如何对Queryset进行序列化？

9. 简述 django rest framework框架的认证流程。

10. django rest framework如何实现的用户访问频率控制？（匿名用户和注册用户）

---

# 第八章 django

> 来源：Python阶段面试题v2.md

1. 简述http协议及常用请求头。

2. 列举常见的请求方法。

3. 列举常见的状态码。

4. http和https的区别？

5. 简述websocket协议及实现原理。

6. django中如何实现websocket？

7. Python web开发中, 跨域问题的解决思路是?

8. 请简述http缓存机制。

9. 谈谈你所知道的Python web框架。

10. Http和Https的区别？

11. django、flask、tornado框架的比较？

12. 什么是wsgi？

13. 列举django的内置组件？

14. 简述django下的(內建的)缓存机制

15. django中model的SlugField类型字段有什么用途

16. django中想要验证表单提交是否格式正确需要用到form中的那个方法

    ```
    A.  form.save()
    B.  form.save(commit=False)
    C.  form.verify()
    D.  form.is_valid()
    ```

17. django常见的线上部署方式有哪几种？

18. django对数据查询结果排序怎么做, 降序怎么做？

19. 下面关于http协议中的get和post方式的区别, 那些是错误的?(多选)

    ```
    A.  他们都可以被收藏, 以及缓存
    B.  get请求参数放在url中
    C.  get只用于查询请求, 不能用于数据请求
    D.  get不应该处理敏感数据的请求
    ```

20. django中使用memcached作为缓存的具体方法? 优缺点说明?

21. django的orm中如何查询 id 不等于5的元素？

22. 使用Django中model filter条件过滤方法,把下边sql语句转化成python代码

    ```
    select * from company where title like "%abc%" or mecount>999
    order by createtime desc;
    ```

23. 从输入http://www.baidu.com/到页面返回, 中间都是发生了什么？

24. django请求的生命周期？

25. django中如何在model保存前做一定的固定操作,比如写一句日志？

26. 简述django中间件及其应用场景？

27. 简述django FBV和CBV？

28. 如何给django CBV的函数设置添加装饰器？

29. django如何连接多个数据库并实现读写分离？

30. 列举django orm 中你了解的所有方法？

31. django中的F的作用？

32. django中的Q的作用？

33. django中如何执行原生SQL？

34. only和defer的区别？

35. select_related和prefetch_related的区别？

36. django中filter和exclude的区别

37. django中values和values_list的区别？

38. 如何使用django orm批量创建数据？

39. django的Form和ModeForm的作用？

40. django的Form组件中，如果字段中包含choices参数，请使用两种方式实现数据源实时更新。

41. django的Model中的ForeignKey字段中的on_delete参数有什么作用？

42. django中csrf的实现机制？

43. django如何实现websocket？

44. 基于django使用ajax发送post请求时，有哪种方法携带csrf token？

45. django缓存如何设置？

46. django的缓存能使用redis吗？如果可以的话，如何配置？

47. django路由系统中name的作用？

48. django的模板中filter、simple_tag、inclusion_tag的区别？

49. django-debug-toolbar的作用？

50. django中如何实现单元测试？

51. 解释orm中 db first 和 code first的含义？

52. django中如何根据数据库表生成model类？

53. 使用orm和原生sql的优缺点？

54. 简述MVC和MTV

55. django的contenttype组件的作用？

56. 使用Django中model filter条件过滤方法,把下边sql语句转化成python代码

    ```
    select * from company where title like "%abc%" or mecount>999
    order by createtime desc;
    ```

---

# 第九章 Flask

> 来源：Python阶段面试题v2.md

1. 请手写一个flask的 Hello World。

2. Flask框架的优势？

3. Flask框架依赖组件？

4. Flask蓝图的作用？

5. 列举使用过的Flask第三方组件？

6. 简述Flask上下文管理流程?

7. Flask中的g的作用？

8. 如何编写flask的离线脚本？

9. Flask中上下文管理主要涉及到了那些相关的类？并描述类主要作用？

10. 为什么要Flask把Local对象中的的值stack 维护成一个列表？

11. Flask中多app应用如何编写？

12. 在Flask中实现WebSocket需要什么组件？

13. wtforms组件的作用？

14. Flask框架默认session处理机制？

15. 解释Flask框架中的Local对象和threadinglocal对象的区别？

16. SQLAlchemy中的 session和scoped_session 的区别？

17. SQLAlchemy如何执行原生SQL？

18. ORM的实现原理？

19. DBUtils模块的作用？

20. 以下SQLAlchemy的字段是否正确？如果不正确请更正.

21. SQLAchemy中如何为表设置引擎和字符编码？

22. SQLAchemy中如何设置联合唯一索引？

23. 简述tornado框架特点及应用场景。

---

# 第十章 tornado

> 来源：Python阶段面试题v2.md

1. tornado中的gen.coroutine的作用？

2. tornado框架中Future对象的作用？

3. tornado框架中如何编写webSocket程序？

4. tornado中静态文件是如何处理的？

5. tornado操作MySQL使用的模块？

6. tornado操作redis使用的模块？

7. ni
