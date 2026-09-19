# 第四章 面向对象

> 来源：Python阶段面试题v2.md

1. 简述面向对象的三大特性。

2. 什么是鸭子模型？

3. super的作用？

4. mro是什么？

5. 什么是c3算法？

6. 列举面向对象中带双下划线的特殊方法。

7. 双下划线和单下划线的区别？

8. 实例变量和类变量的区别？

9. 静态方法和类方法区别？

10. isinstance和type的作用？

11. 有用过with statement（语句）吗？它的好处是什么？

12. 下列数据结构中,哪一种是不可迭代的

    ```
    A.  dict
    B.  object
    C.  set
    D.  str
    ```

13. 实现一个Singleton单例类, 要求遵循基本语言编程规范（用尽量多的方式）。

14. 请描述with的用法, 如果自己的类需要支持with语句, 应该如何书写?

15. python中如何判断一个对象是否可调用? 那些对象可以是可调用对象?如何定义一个类, 使其对象本身就是可调用对象?

16. 请实现一个栈。

17. 关于Python类的继承不正确的说法是?(多选)

    ```python
    A.  Python类无法继承
    B.  可以继承, 无法执行父类的构造函数
    C.  可以有多个父类
    D.  只能有一个父类
    ```

18. 实现一个hashtable类, 对外暴露的有add和get方法, 满足以下测试代码

    ```
    def test():
        import uuid
        name = {"name", "web", "python"}
        ht = HashTable()
        for key in names:
            value = uuid.uuid4()
            ht.add(key,value)
            print("add元素",key,value)
    
        for key in names:
            v = ht.get(key)
            print("get 元素",key, v)
    ```

19. 请用两个队列来实现一个栈(给出伪代码即可)

20. 已知如下链表类, 请实现单链表逆置

    ```
    class Node:
        def __init__(self, value, next):
            self.value = value
            self.next = next
    ```

21. 类的加载顺序(类中有继承有构造有静态)？

22. 参考下面代码片段

    ```
    class Context:
        pass
    
    with Content() as ctx:
        ctx.do_something()
    请在Context类下添加代码完成该类的实现
    ```

23. 以下代码输出是什么? 请给出答案并解释。

    ```
    class Parent(object):
        x = 1
    
    class Child1(Parent):
        pass
    
    class Child2(Parent):
        pass
    
    print Parent.x, Child1.x, Child2.x
    
    Child1.x = 2
    print Parent.x, Child1.x, Child2.x
    
    Parent.x = 3
    print Parent.x, Child1.x, Child2.x
    ```

24. 函数del_node(self,data)的功能: 在根节点指针为root的二叉树(又称二叉排序树)上排除数值为K的节点,若删除成功,返回0,否则返回-1, 概述节点的定义类型为

    ```
    class Node(object):
        def __init__(self,data):
            self.data = data # 节点的数值
            self.left_child = Node # 指向左右子树的指针
            self.right_child = Node
    
        def set_data(self,data):
            self.data = data
    
    
    ```

25. 请给出下面代码片段的输出，请简述上面代码需要改进的地方？

    ```
    class Singleton:
        _instance = None
        def __new__(cls, *args, **kwargs)
            print("New")
            if cls._instance is None:
                print("Create")
                cls._instance = super().__new__(cls,*args, **kwargs)
            return cls._instance
    
        def __init__(self):
            print("Initalize")
            self.prop  = None
    
    s1 = Singleton()
    s2 = singleton()
    ```

26. 请简单解释Python中的static method(静态方法)和class method(类方法),并将以下代码填写完整。

    ```
    class A(object):
        def foo(self,x)
            print 'executing foo(%s, %s)'%(self,x)
    
        @classmethod
        def class_foo(cls,x):
            print 'executing class_foo(%s, %s)'%(cls,x)
    
        @staticmethod
        def static_foo(x):
            print 'executing static_foo(%s)'%(x)
    
    a= A()
    # 调用foo函数,参数传入1
    ____________________
    # 调用class_foo函数,参数传入1
    ____________________
    # 调用static_foo函数,参数传入1
    ____________________
    
    ```

27. 已知一个订单对象（tradeOrder）有如下字段：

    | 字段英文名   | 中文名       | 字段类型               | 取值                                                 |
    | ------------ | ------------ | ---------------------- | ---------------------------------------------------- |
    | Id           | 主键         | Long                   | 123456789                                            |
    | Name         | 姓名         | String                 | 张三                                                 |
    | Items        | 商品列表集合 | List<商品>（关联商品） | 查找商品对象，一个订单有两个商品。商品字段任意取值。 |
    | IsMember     | 是否是会员   | Boolean                | True                                                 |
    | CouponAmount | 优惠券金额   | Bigdecimal             | Null                                                 |

    商品对象

    | 字段英文名称 | 中文名   | 字段类型 | 取值      |
    | ------------ | -------- | -------- | --------- |
    | Id           | 主键     | Long     | 987654321 |
    | Name         | 商品名称 | String   | 手机      |

    问题：若将订单对象转成JSON格式，请书写出转换后的JSON字符串。

28. 写代码(栈与队列)

    编程实现一个先进先出的队列类, 能指定初始化时的队列大小, 以及enqueue,dequeue,is_empty, is_full四种方法

    使用方法如下

    ```
    s = Queue(2) # 初始化一个大小为2的队列
    s.is_empty() # 初始化后, 队列为空, 返回True
    s.enqueue(1) # 将1加入队列
    s.enqueue(2) # 将2加入队列
    s.isfull() # 加入了两个元素, 队列已满, 返回True
    s.dequeue() # 移除一个元素, 返回1
    s.dequeue() # 移除一个元素, 返回2
    s.is_empty() # 队列已经为空, 返回True
    ```

29. 编程实现一个后进先出的栈类, 能指定初始化时的队列大小, 以及push, pull ,is_empty, is_full四种方法

    使用方法如下

    ```
    s = Stack(2) # 初始化一个大小为2的队列
    s.is_empty() # 初始化后, 队列为空, 返回True
    s.push(1) # 将1加入栈
    s.push(2) # 将2加入栈
    s.isfull() # 加入了两个元素, 队列已满, 返回True
    s.pull() # 移除一个元素, 返回2
    s.pull() # 移除一个元素, 返回1
    s.is_empty() # 队列已经为空, 返回True
    ```
