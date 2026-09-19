##### 介绍一下try except的用法和作用？
* 主要用来处理异常
* 完整用法如下：
```python
try:
     Normal execution block
except A:
     Exception A handle
except B:
     Exception B handle
except:
     Other exception handle
else:
     if no exception,get here
finally:
     print("finally")   
```

---

##### 写出以下代码的输出结果：
```python
def test():
    try:
        raise ValueError('something wrong')
    except ValueError as e:
        print('error occured')
        return
    finally:
        print('ok')
test()
```
* 结果(finally无论怎样都会执行)
>error occured
>ok

---

##### 什么是断言(assert)?应用场景？
[断言的参考](https://blog.csdn.net/shujuanyaning/article/details/47184541)

* assert是用来检查一个条件，如果它为真，就不做任何事。如果它为假，则会抛出AssertError并且包含错误信息。
* 应用场景：
    1. 防御型编程
    2. 运行时检查程序逻辑
    3. 检查约定
    4. 程序常量
    5. 检查文档
