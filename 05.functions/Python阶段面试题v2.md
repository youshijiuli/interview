# 第二章 函数

> 来源：Python阶段面试题v2.md

1. 通过代码实现如下转换：

   ```python
   二进制转换成十进制：v = “0b1111011”
   十进制转换成二进制：v = 18
   八进制转换成十进制：v = “011”
   十进制转换成八进制：v = 30
   十六进制转换成十进制：v = “0x12”
   十进制转换成十六进制：v = 87
   ```

2. Python递归的最大层数？

3. 列举常见的内置函数？

4. filter、map、reduce的作用？

5. 一行代码实现9\*9乘法表

6. 什么是闭包？

7. 简述 生成器、迭代器、装饰器以及应用场景？

8. 使用生成器编写fib函数, 函数声明为fib(max), 输入一个参数max值, 使得该函数可以这样调用。

   ```python
   for i in range(0,100):
       print fib(1000)
   
   并产生如下结果(斐波那契数列),1,1,2,3,5,8,13,21...
   ```

9. 一行代码, 通过filter和lambda函数输出以下列表索引为基数对应的元素。

   ```python
   list_a=[12,213,22,2,2,2,22,2,2,32]
   ```

10. 写一个base62encode函数, 62进制。

    ```python
    即:0123456789AB..Zab..z(10个数字+26个大写字母+26个小写字母)。
    	base62encode(1)=1
    	base62encode(61) = z 
    	base62encode(62)=10
    ```

11. 请实现一个装饰器, 限制该函数被调用的频率, 如10秒一次

12. 请实现一个装饰器, 通过一次调用使函数重复执行5次。

13. python一行print出1~100偶数的列表, (列表推导式, filter均可)

14. 解释生成器与函数的不同, 并实现和简单使用generator.

15. 列表推导式和生成器表达式 [i % 2 for i in range(10)] 和 (i % 2 for i in range(10)) 输出结果分别是什么？

16. map(str,[1,2,3,4,5,6,7,8,9]) 输出是什么？

17. python中定义函数时如何书写可变参数和关键字参数?

18. Python3.5中enumerate的意思是什么？

19. 说说Python中的装饰器,迭代器的用法:描述下dict的item方法与iteritems方法的不同

20. 是否使用过functools中的函数？其作用是什么？

21. 如何判断一个值是函数还是方法？

22. 请编写一个函数实现将IP地址转换成一个整数。

    ```
    如 10.3.9.12 转换规则为：
            10            00001010
             3            00000011
             9            00001001
            12            00001100
            
    再将以上二进制拼接起来计算十进制结果：00001010 00000011 00001001 00001100 = ？
    ```

23. lambda表达式格式以及应用场景？

24. pass的作用？

25. *arg和**kwarg作用?

26. 如何在函数中设置一个全局变量 ?

27. 请写出打印结果：

    ```
    # 例 1
    def func(a,b=[]):
      b.append(a)
        print(b)
    func(1)
    func(1)
    func(1)
    func(1)
    
    
    # 例 2
    def func(a,b={}):
      b[a] = 'v'
      print(b)
    func(1)
    func(2)
    
    ```

28. 求结果： lambda

    ```
    def num():
      return [lambda x:i*x for i in range(4)]
    print([m(2) for m in num()])
    
    ```

29. 简述 yield和yield from关键字。

30. 有processFunc变量 ,初始化为processFunc = collapse and (lambda s:" ".join(s.split())) or (lambda s:s)

    调用上下文如下

    ```
    collapse = True
    processFunc = collapse and (lambda s:" ".join(s.split())) or (lambda s:s)
    print processFunc("i\tam\ntest\tobject !")
    
    collapse = False
    processFunc = collapse and (lambda s:" ".join(s.split())) or (lambda s:s)
    print processFunc("i\tam\ntest\tobject !")
    
    ```

    以上代码会在控制台输出什么?

31. 请给出下面代码的输出结果

    ```
    a = 1
    def fun(a):
        a = 2
    
    fun(a)
    print a
    
    a = []
    def fun(a):
        a.append(1)
    
    fun(a)
    print a
    
    ```

32. 全局变量和局部变量的区别, 如何给function里面的一个全局变量赋值

33. 什么是lambda函数, 下面这段代码的输出是什么

    ```
    nums = range(2,20)
    for i in nums:
        nums = filter(lambda x:x==i or x % i, nums)
    nums
    
    ```

34. 指出下面程序存在的问题

    ```
    def Lastllindextem(src, index):
        '''请返回传入src使用空格或者"\"切分后的倒数第index个子串'''
        return src.split("\")[-index]
    
    ```

35. 有一个数组[3,4,1,2,5,6,6,5,4,3,3] 请写一个函数, 找出该数组中没有重复的数的总和. (上面数据的么有重复的总和为1+2=3)

36. 求打印结果

    ```
    arr = [1,2,3]
    def bar():
        arr+=[5]
    
    bar()
    print arr
    ---------------------
    A.  error
    B.  [5]
    C.  [1,2,3]
    D.  [1,2,3,5]
    
    
    ```

37. 请写一个函数, 计算出如下几个字母代表的数字

    ```
    AB-CD=EF
    EF+GH = PPP
    ```

38. 请给出下面代码片段的输出

    ```python
    def say_hi(func):
        def wrapper(*args,**kwargs):
            print("HI")
            ret = func(*args,**kwargs)
            print("BYE")
            return ret
        return wrapper
    
    def say_yo(func):
        def wrapper(*args,**kwargs):
            print("YO")
            return func(*args,**kwargs)
        return wrapper
    
    @say_hi
    @say_yo
    def func():
        print("ROCK & ROLL")
    
    func()
    ```

39. 请简述标准库中functools.wraps的作用

40. 请给出下面代码片段的输出

    ```python
    def test():
        try:
            raise ValueError("something wrong")
        except ValueError as e:
            print("Error occurred")
            return
        finally:
            print("Done")
    
    test()
    ```

41. 下面的函数,那些会输出1,2,3三个数字

    ```
    for i in range(3):
        print i
    
    ```

    ```
    alist = [0,1,2]
    for i in alist:
        print i+1
    
    ```

    ```
    i = 1
    while i<3:
        print i
        i+=1
    ​```
    
    ​```
    for i in range(3):
        print i+1
    ​```
    
    ```

42. 以下函数需要在其中引用一个全局变量k, 请填写语句

    ```
    def fun():
       __________
       k = k+1
    
    ```

43. 请把以下函数转化为python lambda匿名函数

    ```
    def add(x,y):
        return x+y
    
    ```

44. 阅读以下代码, 并写出程序的输出结果

    ```
    my_dict = {"a":0,"b":1}
    
    def func(d):
        d["a"]=1
        return d
    
    func(my_dict)
    my_dict["c"]=2
    print my_dict
    
    ```

45. 填空题

    ```python
    # 有函数定义如下
    def calc(a,b,c,d=1,e=2):
        return (a+b)*(c-d)+e
    
    # 请分别写出以下标号代码的输出结果, 如果出错请写出Error
    print calc(1,2,3,4,5) # ____
    print calc(1,2,3) # ____
    print calc(1,2) # ____
    print calc(1,2,3,e=4) # ____
    print calc(e=4, c=5, a=2,b=3) # ____
    print calc(1,2,3, d=5,4) # ____
    ```

46. def(a, b=[])这种写法有什么陷阱？

47. 函数

    ```
    def add_end(l=[]):
        l.append("end")
        return l
    
    add_end() # 输出什么
    add_end() # 再次调用输出什么? 为什么
    
    ```

48. 函数参数 *args,**kwargs的作用是什么

    ```
    def func(a,b,c=0,*args,**kwargs):
        pass
    
    
    ```

49. 可变参数定义 `*args`,`**kwargs`的区别是什么?并且写出下边代码的输入内容

    ```
    def foo(*args,**kwargs):
    	print("args=",agrs)
    	print("kwargs=",kwargs)
    	print("-----------------")
    	
    if __name__ =='__main__':
    	foo(1,2,3,4)
    	foo(a=1,b=2,c=3)
    	foo(1,2,3,4,a=1,b=2,c=3)
    	foo("a",1,None,a=1,b="2",c=3)
    
    ```

50. 请写出log实现(主要功能时打印函数名)

    ```
    @log
    def now():
        print "2013-12-25"
    
    now()
    输出
    call now()
    2013-12-25
    
    ```

51. Python如何定义一个函数

    ```
    A.  class <name>(<Type> arg1, <type> arg2, ...)
    B.  function <name>(arg1,arg2,...)
    C.  def <name>(arg1, arg2,...)
    D.  def <name>(<type> arg1, <type> arg2...)
    
    ```

52. 选择代码运行结果

    ```
    country_counter ={}
    
    def addone(country):
        if country in country_counter:
            country_counter[country ]+=1
        else:
            country_counter[country ]= 1
    
    addone("China")
    addone("Japan")
    addone("china")
    print len(country_counter )
    
    
    A.  0
    B.  1
    C.  2
    D.  3
    E.  4
    
    ```

53. 选择输出结果

    ```
    def doff(arg1,*args):
        print type(args)
    
    doff("applea","bananas","cherry")
    
    
    A.  str
    B.  int
    C.  tuple
    D.  list
    E.  dict
    
    ```

54. 下面程序的输出结果是

    ```
    d = lambda p:p*2
    t = lambda p:p*3
    
    x = 2
    x = d(x)
    x = t(x)
    x = d(x)
    print x
    
    ```

55. 什么是lambda表达式？

56. 以下代码输出是什么,请给出答案并解释

    ```
    def multipliers():
        return [lambda x:x*i for i in range(4)]
    
    print([m(2) for m in multipliers()])
    请修改multipliers的定义来产生期望的结果
    ```

57. 有 0 < x <= 10, 10 < x <= 20, 20 < x <= 30, .，190 < x〈= 200,200 < x这样的21个区间分别对应1-21二十一个级别，请编写一个函数 level (x)根据输入数值返回对应级别。

58. 写函数

    有一个数据结构如下所示，请编写一个函数从该结构数据中返画由指定的 字段和对应的值组成的字典。如果指定字段不存在，则跳过该字段。

    ```python
    data:{
        "time":"2016-08-05T13:13:05",
        "some_id":"ID1234",
        "grp1":{"fld1":1, "fld2":2,},
        "xxx2":{"fld3":0, "fld4":0.4,},
        "fld6":11,
        "fld7": 7,
        "fld46":8
    }
    
    fields:由"|"连接的以fld开头的字符串, 如fld2|fld7|fld29
    
    def select(data,fields):
        return result
    ```

59. 补全代码

    ```
    若要将N个task分配给N个worker同时去完成, 每个worker分别都可以承担这N个task,但费用不同. 下面的程序用回溯法计算总费用最小的一种工作分配方案, 在该方案中, 为每个worker分配1个task.
    
    程序中,N个task从0开始顺序编号, N个worker也从0开始顺序编号, 主要的变量说明如下:
    
    - ci:将任务i分配给worker j的费用
    - task[i]: 值为0表示task i未分配, 值为j表示task i分配给worker j
    - worker[k] 值为0表示未分配task, 值为1表示worker k已分配task;
    - mincost: 最小总费用
    
    程序
    
        N=8
        mincosr = 65535
        worker = []
        task = []
        temp = []
        c = []
        def plan(k, cost):
            global  mincosr
            if __(1)__ and cost<mincosr:
                mincosr = cost
                for i in xrange(N):
                    temp[i] = task[i]
            else:
                for i in xrange(N):
                    if worker[i] ==0 and __(2)__:
                        worker[i] = 1
                        task[k] = __(3)__
                        plan(__(4)__,cost+c[k][i])
                        __(5)__
                        task[k] = 0
        def main():
            for i in xrange(N):
                worker.append(0)
                task.append(0)
                temp.append(0)
                c.append(0)
                for j in xrange(N):
                    print "请输入 worker"+str(i)+"完成 task" + str(j)+"的花费"
                    input_value = input()
                    c[i].append(int(input_value))
        plan(0,0)
        print('\n 最小费用: '+str(mincosr))
        for i in xrange(N):
            print "Task"+str(i)+"is assigned to Worker" + str(temp[i])
        if __name__ == "__main__":
            main()
    ```

60. 写个函数接收一个文件夹名称作为参数, 显示文件夹中文件的路径, 以及其中包含文件夹中文件的路径。
