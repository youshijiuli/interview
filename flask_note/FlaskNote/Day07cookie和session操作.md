## cookie和session操作



### 1.cookie使用

***

**按照顺序来**

**设置cookie:**

```python
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("success")

    #设置cookie,设置有效期单位s
    resp.set_cookie("ITcast","python",max_age=200)
    resp.set_cookie('Itcast1','python1',max_age=200)
    return resp
```

通过make_response方法创建response对象，然后调用这个对象的set_cookie方法，最后返回这个对象，就可以达到我们设置cookie的目的。

cookie的默认有效期是临时cookie，浏览器关闭就会失效，**那如何把cookie的有效期设成我们想要的期限呢？**

在set_cookie方法中有一个**max_age**的参数，这个参数可以设置我们想要的cookie的有效期，单位为秒。

**拿取cookie:**

```
@app.route("/get_cookie")
def get_cookie():
    c = request.cookies.get("ITcast")
    return c
```

**删除cookie：**

```
@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie('Itcast1')
    return resp
```

同样也是非常简单的！其实在删除cookie当中，并不是真正的删除，只是把当前需要删除的cookie的**有效期**设置为了创建时候的时间，所以相当于是删除了cookie。

### 2. session使用

***

session是一种**会话机制**，可以存放一些状态信息

```
#session的运用
app.config['SECRET_KEY'] = '123scdinieroinds'

@app.route('/login')
def login():
    #设置session
    session["name"] = "python"
    session["mobile"] = "12112341231"

    return "login success"

@app.route("/index")
def index():
    #获取session数据
    name = session.get("name")
    mobile = session.get("mobile")
    return "hello %s %s"%(name,mobile)
```





```

# Flask的session需要使用到的秘钥字符串
app.config["SECRET_KEY"] = "123FIISUODFNOSAIFNHASIJDdasd"
```



这一段代码到底干啥的，在Flask当中如果我们需要使用session，那么我们**必须配置app当中的SECRET_KEY参数**，否则程序会报错。**参数的值我们可以任意编写**