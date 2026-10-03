# django 中的用户身份验证和 session 的关系

## Session

~~~
session的数据默认存在数据库中, 它在客户端是用cookie来识别的，作为一个票据。这个cookie的名称，默认就叫'sessionid'，但是可以通过settings.SESSION_COOKIE_NAME来修改。
~~~

~~~
sessionid这个cookie的值，在服务器就是session的session_key属性，同时数据库的django_session表中用它作为主键。
~~~

#### session的实现涉及下列几个主要的类

### 1.Session和SessionManager

~~~python
# 这两个是session的Model及其相应的Manager，它们负责
(1)session和数据库之间的持久化操作
(2)session_key的生成机制
(3)session内容(是一个字典)的序列化、反序列化工作
# 实际应用中，我们不会直接用这个类
~~~

### 2.SessionWrapper

~~~python
实现了 session 类似字典的一些功能，如设值、取值等。这个类是 request.session 对象的实际类型。
~~~

### 3.SessionMiddleware

~~~python
属于 django 自带的中间件之一，作用是在 request 中附加 session 属性，并可以在 response 的时候，适当的情况下保存 session 并发出相应的 cookie 到客户端。
# session 的几个可配置的参数：
* settings.SESSION_SAVE_EVERY_REQUEST
* settings.SESSION_EXPIRE_AT_BROWSER_CLOSE
* settings.SESSION_COOKIE_AGE
* settings.SESSION_COOKIE_SECURE
* settings.SESSION_COOKIE_DOMAIN
* settings.SESSION_COOKIE_NAME
~~~

## User

~~~python
用户的身份验证过程:
1. 首先通过 authenticate() 方法对传入的用户名、密码等信息进行验证，如果符合，则返回相应的 user 对象，同时，该方法会对 user 对象加以标注(该标记会在login方法时用到，如果没有该标记，则登录失败;authenticate与login要一起使用)，通过附加 user.backend 属性来记录验证是被哪个配置的 backend 通过的。默认只有一个 backend，是 django.contrib.auth.backends.ModelBackend.
2. login 方法调用
  login(request对象，user对象)
  如果上一步身份验证通过，则此方法中对 request.session 中简单的添加两个键值(使用SessionMiddleware将数据存入session当中):
  (1) "_auth_user_id"  这个是 user.id
  (2) "_auth_user_backend" 这个是 user.backend
# 可以用来判断用户是否已经成功登录
注意: 在用户还未登录的时候，也存在着匿名用户的Session，在其登陆之后，之前在匿名Session中保留的信息，都会保留下来。这两个方法要结合使用，而且必须要先调用authenticate()，因为该方法会User的一个属性上纪录该用户已经通过校验了，这个属性会被随后的login过程所使用。
3. 登录成功后，把user存入数据库的session表中
~~~

~~~
而实现 request.user 属性同样是通过 Middleware 来完成的，其中调用到一个 get_user 方法，该方法尝试读取上面在 session 中记录的 user.id 和 user.backend, 然后命令 backend 去查找相关 id 的 user 对象。如果没有找到，则返回一个 AnonymousUser. 而 AnonymousUser 是一个空实现，不具备 user 的任何功能。

可以通过 is_anonymous() 或 is_authenticated() 来判别是否为匿名用户。
~~~

## 小结

~~~
django 中 user 和 session 关系不大，仅仅是在其实现中利用 session 保存了 user.id 和 user.backend 两个值。
~~~

