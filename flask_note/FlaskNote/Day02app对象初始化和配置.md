## APP对象初始化和配置



### 1.flask应用用对象初始化参数说明

***

**______name__**:

前面提到，第一个程序里面

```

app = Flask(__name__)    # __name__ 就是当前模块的名字
```

__name__是当前模块的名字，在执行语句中

```

if __name__ == '__main__':
    # 运行本地服务器进行测试flask程序
    app.run()
```

**难道模板名字叫__main__吗？**我应该是我创建的py文件的文件名吗？其实这里有一个小知识点，当我们把某个模板当做启动模板时，那么这个模板的**______name__**会默认成为**______main__**，如果不是作为启动模板，也就是我们导入到启动模板当中的模板名称才会是文件的文件名![](D:\Code\FlaskNote\images\Day02_1.png)

上面这张图就是我们再demo.py文件中直接运行的，也就是说此时的demo.py模板作为了启动模板。![](D:\Code\FlaskNote\images\Day02_2.png)

这张图是我们将demo模板导入到app模板当中，我们可以看到打印出来的模板名称是demo自己本身的文件名。



### 2.静态文件目录与路由说明

***

**除了__name__这个参数，其实Flask的应用对象还可以放一些参数。**



**static_url_path**: 访问静态资源的url前缀

**static_folde****r:** 默认‘static’

**template_folder**: 默认‘templates’



目录：![](D:\Code\FlaskNote\images\Day02_3.png)



**static_url_path: 访问静态资源的url前缀**



这个参数大部分人会认为就是静态资源的路径，其实大错特错，他只是访问静态资源的一个url前缀，跟路径没有半毛钱关系。

- 

```
app = Flask(__name__, static_url_path="/python")   
```

例如上面，我把访问静态资源的url前缀改为python，然后我去static文件夹创建一个html文件



访问方式应该是这样的：

```html
http://127.0.0.1:5000/python/index.html
```

![](D:\Code\FlaskNote\images\Day02_4.png)

**static_folder:** 默认‘static’，其实这个参数才是真正的静态文件的路径，路径可以是绝对路径也可以是相对路径，他所对应的路径就是静态文件所在的地方。



**template_folder:** 默认‘templates’ ，这个参数非常容易理解，就是模板文件的目录。

### 3.flask的配置参数设置

***

**pycharm设置debug module 为on**:

```
app.run(Debug = True)
```



![](D:\Code\FlaskNote\images\Day02_5.png)

其它方法不考虑，失效

### 4.app的run使用

***

在app的run方法中含有两个参数



```
    app.run(host="127.0.0.1", port="5000")
```



第一个则是你要开启的ip地址，第二个则是你所打开的端口。

**设置端口好像不管用**