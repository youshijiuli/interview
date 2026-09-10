# Python 面向对象编程专题

---

## 一、面向对象基础

### 1.1 面向对象与面向过程

#### 什么是面向过程

面向过程的核心在于"过程"二字，将程序流程化，按照步骤来解决问题。先做什么、再做什么、最后做什么，每一步都按照既定的流程进行。

```python
# 面向过程：按步骤解决问题
# 步骤1：获取用户输入
# 步骤2：处理数据
# 步骤3：输出结果
```

**优点**：将复杂的问题流程化、简单化，一步接一步地解决问题。

**缺点**：一套流水线只能解决某一类确定的问题，扩展性较差。生产汽车的流水线无法用于生产可乐，想要修改功能就需要重新设计整个流程。

#### 什么是面向对象

面向对象的核心在于"对象"二字，对象就是容器，可以盛放数据和功能。面向对象将某一类事物的属性和行为封装在一起，形成一个整体。

```python
# 面向对象：将数据和功能封装在一起
# 对象 = 数据（属性） + 功能（方法）
```

**优点**：
- 解决了程序的扩展性问题
- 将某个类的属性和方法集合到一起
- 如果需要添加新功能，只需要修改这个类即可

**缺点**：
- 设计过程比较复杂，必须先理清类都有哪些属性和功能
- 没有面向过程那么流程化，设计时容易出现交叉和混乱

#### 程序的本质

```python
# 程序 = 数据 + 功能
# 编写程序的本质就是定义出一系列的数据，然后定义出一系列的功能来操作这些数据
```

### 1.2 类与对象

#### 什么是类

类就是类别、种类的意思，是面向对象的基石。如果多个对象有相似的功能和属性，那么它们就应该同属于一个类。类的好处就是将同一类对象中相同的数据和功能存放到一起，这样每个对象就不需要单独复制一份。

```python
# 类与对象的关系
# 对象是存放数据和功能的集合体
# 类是用来存放同一类多个对象相同数据和功能的集合体

# 在程序中，先有类才能有对象
# 在逻辑思考中，先有对象才能抽象出某一个类
```

#### 定义类的语法

```python
# 函数命名：小写字母 + 下划线
def get_student():
    pass

# 类命名：大驼峰，每个单词首字母大写
class Student:
    pass

# 类名后面的括号可以省略
class Student:
    # 数据属性（类变量）
    name = "Dream"
    school = "清华大学"
    age = 18
    gender = "男"

    # 功能属性（方法）
    # self 代表当前对象本身
    def run(self):
        print(f"{self.name} 正在跑步")

    def swim(self):
        print(f"{self.name} 正在游泳")

    def read(self):
        print(f"{self.name} 正在读书")
```

#### 实例化与属性访问

```python
class Student:
    name = "Dream"
    school = "清华大学"
    age = 18
    gender = "男"

    def run(self):
        print(f"{self.name} 正在跑步")


# 实例化：类名() 得到对象
student = Student()
print(student)  # <__main__.Student object at 0x...>

# 查看对象的属性和方法
print(dir(student))

# 查看对象的名称空间（对象独有的属性）
print(student.__dict__)  # {}

# 查看类的名称空间（类中定义的所有属性）
print(Student.__dict__)

# 通过 . 访问属性
print(student.name)     # Dream
print(student.school)   # 清华大学
student.run()           # Dream 正在跑步
```

#### 对象的独有属性初始化

当多个对象需要不同的属性值时，需要为每个对象初始化独有属性：

```python
class Student:
    school = "清华大学"  # 类属性，所有对象共享

    def run(self):
        print(f"正在跑步")


# 方式一：通过 __dict__ 直接赋值
student_one = Student()
student_one.__dict__.update({"name": "Dream", "age": 18, "gender": "男"})
print(student_one.name)  # Dream

student_two = Student()
student_two.__dict__.update({"name": "Opp", "age": 28, "gender": "女"})
print(student_two.name)  # Opp
```

### 1.3 `__init__` 初始化方法

#### 推导过程

为了更方便地初始化对象属性，可以将初始化代码封装到函数中：

```python
class Student:
    school = "清华大学"

    def run(self):
        print(f"正在跑步")


# 外部函数初始化对象属性
def init_obj(obj, name, age, gender):
    obj.__dict__.update({"name": name, "age": age, "gender": gender})


student = Student()
init_obj(student, name="Dream", age=18, gender="男")
print(student.__dict__)  # {'name': 'Dream', 'age': 18, 'gender': '男'}
```

将初始化函数放入类内部：

```python
class Student:
    school = "清华大学"

    def init_obj(self, name, age, gender):
        # self 就是当前对象
        self.__dict__.update({"name": name, "age": age, "gender": gender})

    def run(self):
        print(f"正在跑步")


student = Student()
student.init_obj(name="Dream", age=18, gender="男")
print(student.__dict__)  # {'name': 'Dream', 'age': 18, 'gender': '男'}
```

#### `__init__` 最终版

Python 提供了 `__init__` 方法，在实例化对象时自动调用，无需手动调用初始化方法：

```python
class Student:
    school = "清华大学"  # 类属性

    # __init__ 方法在实例化时自动触发
    def __init__(self, name, age, gender):
        # 通过 self.属性名 的方式初始化对象的独有属性
        self.name = name
        self.age = age
        self.gender = gender

    def run(self):
        print(f"{self.name} 正在跑步")

    def swim(self):
        print(f"{self.name} 正在游泳")


# 实例化时传入参数，自动完成初始化
student = Student(name="Dream", age=18, gender="男")
print(student.__dict__)  # {'name': 'Dream', 'age': 18, 'gender': '男'}
print(student.name)      # Dream
print(student.school)    # 清华大学（类属性）

# 对象允许通过 .属性名 取值，也支持 .属性名 = 属性值 修改属性
student.name = "Opp"
print(student.name)  # Opp

student.run()  # Opp 正在跑步
```

#### self 的含义

```python
class Student:
    def run(self):
        # self 就是调用该方法的对象本身
        print(f"self 的内存地址：{self}")


student = Student()
student.run()
# self 的内存地址：<__main__.Student object at 0x...>

# 谁实例化得到当前对象，在调用的时候 self 就是谁
# self 和实例化得到的对象，内存地址是一样的
```

### 1.4 类属性与对象属性

```python
class Student:
    """
    这是一个学生类
    """
    school = "清华大学"  # 类属性（数据属性）

    def __init__(self, name, age):
        self.name = name   # 对象属性
        self.age = age     # 对象属性

    def show(self):
        print(f"{self.name} 正在看电影!")


student = Student(name="Dream", age=18)

# 查看对象的名称空间（只有对象自己的属性）
print(student.__dict__)  # {'name': 'Dream', 'age': 18}

# 查看类的名称空间（类中定义的所有内容）
print(Student.__dict__)
# 包含：'school', '__init__', 'show' 等

# 对象可以访问类属性
print(student.school)  # 清华大学
```

### 1.5 类的补充方法

```python
class Student:
    """学生类文档注释"""

    school = "清华大学"

    def __init__(self, name):
        self.name = name


# 获取当前类的名称空间
print(Student.__dict__)

# 获取当前类的文档注释字符串
print(Student.__doc__)  # 学生类文档注释

# 获取当前类的名字
print(Student.__name__)  # Student

# 查看当前类所在的模块名
print(Student.__module__)  # __main__

# 查看当前类继承的所有父类（默认是 object）
print(Student.__bases__)  # (<class 'object'>,)

# 查看当前类继承的第一个父类
print(Student.__base__)  # <class 'object'>

# 查看产生当前类的类（即元类 type）
print(Student.__class__)  # <class 'type'>
```

---

## 二、封装

### 2.1 什么是封装

封装是面向对象的三大特性之一（封装、继承、多态），其核心思想是将某些数据保护和隐藏起来，不希望除了开发者以外的其他人可以随意访问当前的属性和方法。

```python
# 封装的作用是保护数据，防止外部代码随意修改对象内部的数据

class Student:
    school = "清华大学"


student = Student()
# 外部可以直接修改属性，缺乏保护
student.school = "北京大学"
print(student.school)  # 北京大学
```

### 2.2 如何进行封装

在 Python 中，通过在属性名前加双下划线 `__` 来实现封装：

```python
class Student:
    __school = "清华大学"  # 封装后的类属性
    # __school 在类初始化时自动变形为 _Student__school

    def __init__(self, name, age, gender):
        self.__name = name     # 封装后的对象属性
        self.__age = age
        self.__gender = gender

    def show_info(self):
        # 在类内部可以直接使用 __属性名 访问
        print(f"姓名：{self.__name}，年龄：{self.__age}，性别：{self.__gender}，学校：{self.__school}")

    def __read(self):  # 封装后的方法
        print(f"{self.__school} 的 {self.__name} 正在读书")


student = Student("张三", 18, "男")
student.show_info()  # 正常访问

# 外部无法直接访问封装属性
# print(student.__name)  # AttributeError: 'Student' object has no attribute '__name'

# 查看名称空间可以发现属性名已经变形
print(Student.__dict__)  # '_Student__school': '清华大学'
print(student.__dict__)  # {'_Student__name': '张三', '_Student__age': 18, '_Student__gender': '男'}
```

#### 封装属性的变形规则

```python
# 1. 在类内部，将变量名用双下划线声明
# 2. 在类初始化时，属性名自动从 __变量名 变形为 _类名__变量名
# 3. 在类内部使用时，直接写 __变量名 即可调用
# 4. 从外部访问时，需要使用 对象._类名__变量名
# 5. 变形只会发生一次，后续的 __变量名 赋值不会被自动变形

class Student:
    __school = "清华大学"  # 变形为 _Student__school


# 通过变形后的名称访问
print(Student._Student__school)  # 清华大学

# 这种赋值不会覆盖被封装的属性，而是新增了一个 __school 属性
Student.__school = "北京大学"    # 这是新的属性，没有发生变形
print(Student.__dict__)  # 同时存在 '_Student__school' 和 '__school'
```

### 2.3 封装的目的：开放接口

封装不是为了禁止访问，而是为了提供规范的操作接口，对数据进行校验和控制：

```python
class Student:
    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.__gender = gender

    def show_info(self):
        """查看信息（只读接口）"""
        print(f"{self.__name} 的年龄是 {self.__age}，性别是 {self.__gender}")

    def set_info(self, name, age):
        """修改信息的接口（带数据校验）"""
        if not name.startswith("nb_"):
            raise ValueError(f"名字必须以 nb_ 开头")
        if not age.isdigit():
            raise ValueError("年龄必须为数字")
        # 校验通过后才允许修改
        self.__name = name
        self.__age = age


student = Student(name="Dream", age=18, gender="男")
student.show_info()

# 必须通过规范接口修改，直接赋值无法修改封装的属性
# student.set_info(name="opp", age=18)  # ValueError: 名字必须以 nb_ 开头
student.set_info(name="nb_opp", age="28")
student.show_info()
```

### 2.4 @property 装饰器

#### 基本使用

`@property` 可以将函数属性伪装成数据属性，让方法的调用像访问属性一样自然：

```python
# BMI 计算示例
class BMI:
    def __init__(self, name, height, weight):
        self.__name = name
        self.__height = height
        self.__weight = weight

    @property  # 将函数属性伪装成数据属性
    def bmi(self):
        """
        BMI 本质上是一个计算得出的数值，应该像数据属性一样被访问
        计算公式：体重 / (身高 * 身高)
        """
        return self.__weight / (self.__height * self.__height)


bmi_tool = BMI(name="Dream", height=1.7, weight=65)
# 访问时不需要加括号，像访问数据属性一样
print(bmi_tool.bmi)  # 22.49134948096886
```

#### property 装饰器三件套（getter / setter / deleter）

```python
class Student:
    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.gender = gender

    @property
    def real_name(self):
        """获取属性（getter）"""
        return f"nb_{self.__name}"

    @real_name.setter
    def real_name(self, value):
        """设置属性（setter），可以加入校验逻辑"""
        if not len(value) <= 3:
            raise ValueError("名字必须是三个字及以下")
        self.__name = value

    @real_name.deleter
    def real_name(self, value):
        """删除属性（deleter）"""
        del self.__name


student = Student(name="Dream", age=18, gender="男")

# 获取：触发 @property
print(student.real_name)  # nb_Dream

# 设置：触发 @real_name.setter
student.real_name = "Opp"
print(student.real_name)  # nb_Opp

# 删除：触发 @real_name.deleter
del student.real_name
```

#### 使用 property() 内置函数

除了装饰器方式，也可以使用 `property()` 内置函数统一暴露接口：

```python
class Student:
    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.gender = gender

    # 定义三个处理方法
    def __get_real_name(self):
        return f"nb_{self.__name}"

    def __set_real_name(self, value):
        if not len(value) <= 3:
            raise ValueError("名字必须是三个字及以下")
        self.__name = value

    def __del_real_name(self):
        del self.__name

    # 使用 property() 内置函数统一包装
    # property(fget, fset, fdel)
    real_name = property(__get_real_name, __set_real_name, __del_real_name)


student = Student(name="Dream", age=18, gender="男")
print(student.real_name)      # 触发 __get_real_name
student.real_name = "Opp"     # 触发 __set_real_name
del student.real_name         # 触发 __del_real_name
```

---

## 三、继承

### 3.1 什么是继承

继承是面向对象的第二大特性。继承就是创建一个新的类，新类会继承父类里面的所有属性，并且可以添加自己的属性。

```python
# 继承分为两种：
# 1. 单继承：新类只继承一个父类
# 2. 多继承：新类继承多个父类
```

#### 单继承

```python
class Animal:
    category = "动物"

    def eat(self):
        print(f"动物可以吃饭")

    def speak(self):
        print("动物可以发出声音")


class Duck(Animal):
    category = "鸭子"  # 可以覆盖父类的类属性

    def swim(self):
        """鸭子独有的方法"""
        print(f"鸭子可以游泳!")


duck = Duck()
duck.eat()          # 继承了父类的 eat 方法
print(duck.category)  # 鸭子（覆盖了父类属性）
duck.swim()         # 自己的方法
```

#### 多继承

```python
class TangDuck:
    def play(self):
        print(f"唐老鸭可以玩!")


class SmallDuck(TangDuck, Duck):
    def eat(self):
        """覆盖父类的 eat 方法"""
        print("小鸭子喜欢吃东西")


small_duck = SmallDuck()
small_duck.eat()           # 小鸭子喜欢吃东西（自己的方法）
small_duck.play()          # 唐老鸭可以玩!（继承自 TangDuck）
small_duck.swim()          # 鸭子可以游泳!（继承自 Duck）

# 查看类的父类
print(SmallDuck.__bases__)  # (<class '__main__.TangDuck'>, <class '__main__.Duck'>)
print(SmallDuck.__base__)   # <class '__main__.TangDuck'>（第一个父类）
print(Animal.__bases__)     # (<class 'object'>,)
```

### 3.2 新式类与经典类

```python
# 经典类：Python 2.x 中才有的概念
# 在 Python 2.x 中，没有显式继承 object 的类就是经典类
# 在 Python 2.x 中，显式继承 object 的类就是新式类

# Python 3.x 中已经移除了经典类，默认所有类都是新式类
# 所有类都隐式继承自 object

class Foo:     # 在 Python 3.x 中等价于 class Foo(object):
    pass
```

### 3.3 属性查找顺序

#### 未封装情况

```python
class Foo:
    def f1(self):
        print(f"当前是 Foo 的 f1")

    def f2(self):
        print(f"当前是 Foo 的 f2")
        # self 是 Bar 的实例，所以这里调用的是 Bar 的 f1
        self.f1()


class Bar(Foo):
    def f1(self):
        print(f"当前是 Bar 的 f1")


b_obj = Bar()
b_obj.f2()
# 当前是 Foo 的 f2
# 当前是 Bar 的 f1
# 原因：self 是 Bar 的实例，查找属性时从自己的类开始

# 未封装时的属性查找顺序：
# 对象自身 → 实例化当前对象的类 → 父类 → 更上层父类 → 报错
```

#### 封装情况

```python
class Foo:
    def __f1(self):  # 封装后变形为 _Foo__f1
        print(f"当前是 Foo 的 f1")

    def f2(self):
        print(f"当前是 Foo 的 f2")
        # 这里 __f1 在 Foo 类内部，调用的是 Foo 的 __f1
        self.__f1()


class Bar(Foo):
    def __f1(self):  # 封装后变形为 _Bar__f1
        print(f"当前是 Bar 的 f1")


b_obj = Bar()
b_obj.f2()
# 当前是 Foo 的 f2
# 当前是 Foo 的 f1
# 原因：封装后的属性在定义它的类内部调用时，使用的是该类的变形名称

# 封装时的属性查找顺序：
# 从当前执行该方法的类中找封装属性 → 找不到就报错
# 封装是为了隐藏和保护数据，不会跨类查找
```

### 3.4 菱形继承与 MRO

菱形继承是指一个类继承自两个父类，而这两个父类又继承自同一个基类，形成菱形结构。

```python
class A:
    def test(self):
        print('from A')


class B(A):
    def test(self):
        print('from B')


class C(A):
    def test(self):
        print('from C')


class D(B):
    def test(self):
        print('from D')


class E(C):
    def test(self):
        print('from E')


class F(D, E):
    pass


f = F()
f.test()  # from D
```

#### 经典类与新式类的查找顺序

```python
# 经典类（Python 2.x）：深度优先
# F → D → B → A → E → C
# 先一条道走到黑，没有再去开枝散叶

# 新式类（Python 3.x）：广度优先（C3 线性化算法）
# F → D → B → E → C → A
# 先剔除公共类 A，找完其他分支后再找公共类
```

#### 查看 MRO（Method Resolution Order）

```python
# MRO 只适用于新式类（Python 3.x 所有类都是新式类）
print(F.__mro__)
# (<class '__main__.F'>, <class '__main__.D'>, <class '__main__.B'>,
#  <class '__main__.E'>, <class '__main__.C'>, <class '__main__.A'>,
#  <class 'object'>)

print(F.mro())
# [<class '__main__.F'>, <class '__main__.D'>, <class '__main__.B'>,
#  <class '__main__.E'>, <class '__main__.C'>, <class '__main__.A'>,
#  <class 'object'>]
```

### 3.5 C3 线性化算法简述

Python 3 使用 C3 线性化算法来计算 MRO，核心原则：
1. 子类优先于父类
2. 父类的顺序按照声明顺序
3. 所有父类都遵循同样的规则

```python
# 对于 class F(D, E)，其中 D(B, A)，E(C, A)，B(A)，C(A)：
# L[F] = F + merge(L[D], L[E], DE)
# L[D] = D + merge(L[B], L[A], BA) = D B A object
# L[E] = E + merge(L[C], L[A], CA) = E C A object
# L[F] = F + merge(DBAO, ECAO, DE) = F D B E C A object
```

---

## 四、派生与抽象类

### 4.1 抽象与继承的关系

```python
# 抽象：从某一类事物中提取出公共的部分
# 奥巴马 + 梅西 → 人
# 麦兜 + 猪八戒 → 猪
# 史努比 + 史派克 → 狗
# 人 + 猪 + 狗 → 动物（抽象）

# 继承：将公共的部分赋予具体的类
# 动物 → 人 + 猪 + 狗
# 人 → 奥巴马 + 梅西
# 猪 → 麦兜 + 猪八戒
# 狗 → 史努比 + 史派克
```

### 4.2 派生

派生就是继承父类的所有属性之后，衍生出自己的独有属性。

```python
class People:
    school = "清华大学"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def eat(self):
        print(f"{self.name} 正在吃饭")


class Teacher(People):
    def __init__(self, course):
        # 重写了父类的 __init__，导致父类的 name/age/gender 没有被初始化
        self.course = course


teacher = Teacher(course="数学")
print(teacher.course)   # 数学
print(teacher.school)   # 清华大学（继承了类属性）
# print(teacher.name)   # AttributeError: 子类重写了 __init__，父类的属性丢失
```

### 4.3 继承父类属性的两种方式

#### 方式一：super()

```python
class People:
    school = "清华大学"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def eat(self, animal):
        print(f"{animal} 正在吃")


class Family:
    def __init__(self, role):
        self.role = role


class Teacher(Family, People):
    def __init__(self, name, age, gender, course, role):
        # super() 永远指向第一个父类（这里是 Family）
        super().__init__(role)
        # 第二个父类需要指名道姓调用
        People.__init__(self, name, age, gender)
        # 自己的独有属性
        self.course = course

    def eat(self, animal):
        # 调用父类的方法
        super().eat(animal)
        print(f"{self.name} 老师吃完了")


teacher = Teacher(name="Dream", age=18, gender=1, course="数学", role="讲师")
print(teacher.name)    # Dream
print(teacher.role)    # 讲师
print(teacher.course)  # 数学
teacher.eat("苹果")
```

#### 方式二：指名道姓调用

```python
class Teacher(People, Family):
    def __init__(self, name, age, gender, course, role):
        # 直接使用父类名调用，必须手动传入 self
        People.__init__(self, name, age, gender)
        Family.__init__(self, role)
        self.course = course


teacher = Teacher(name="Dream", age=18, gender=1, course="数学", role="讲师")
```

#### 小结

```python
# 当一个类继承多个父类时，想要继承父类的所有属性，必须重载父类的 __init__：
# 方式一：super().方法名(参数)
#   优点：写法简洁
#   缺点：super() 永远指向继承的第一个父类
#
# 方式二：父类名.方法名(self, 参数)
#   优点：可以精确指定调用哪个父类的方法
#   缺点：必须手动传入 self
```

### 4.4 组合

组合就是在一个类中将另一个类的对象或方法包含进来，形成"大杂烩"。

```python
class Course:
    """课程类"""
    def __init__(self, name, period, price):
        self.name = name
        self.period = period
        self.price = price

    def show_info(self):
        return f"课程：{self.name}，周期：{self.period}，价格：{self.price}"


class Date:
    """日期类"""
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def show_birth(self):
        return f"{self.year} 年 {self.month} 月 {self.day} 日"


class People:
    school = "清华大学"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Teacher:
    def __init__(self, name, age, gender, year, month, day):
        # 继承 People 的属性
        People.__init__(self, name, age, gender)
        # 组合 Date 对象作为属性
        self.birthday = Date(year, month, day)
        # 组合课程列表
        self.course_list = []

    def teach(self):
        print(f"讲师 {self.name}，年龄 {self.age}，性别 {self.gender}")
        print(f"生日：{self.birthday.show_birth()}")
        for course in self.course_list:
            print(f"教授：{course.show_info()}")


teacher = Teacher(name="张三", age=30, gender="男", year=1990, month=1, day=1)

python_course = Course(name="Python", period=6, price=100)
go_course = Course(name="Go", period=9, price=200)
teacher.course_list.append(python_course)
teacher.course_list.append(go_course)

teacher.teach()
```

#### 组合与继承的区别

```python
# 继承：子类继承了父类的属性和方法，派生出自己的独有属性
#      表示 "is-a" 关系（狗是动物）

# 组合：将多个类的对象组合到一起，组合后的类拥有多个类中的属性和方法
#      表示 "has-a" 关系（人有生日）
```

### 4.5 抽象类（abc 模块）

#### 什么是抽象类

抽象类是一个特殊的类，它只能被继承，不能被实例化。抽象类用于限制子类必须实现某些方法。

```python
# 类是从一堆对象中抽取相同内容而来的
# 抽象类就是从一堆类中抽取相同内容而来的
# 香蕉、苹果、桃子 → 水果（抽象类）
# 你永远吃不到一个叫做"水果"的东西，只能吃到具体的香蕉、苹果
```

#### 使用 abc 模块实现抽象类

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    """抽象类：动物"""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        """抽象方法：子类必须实现"""
        ...

    @abstractmethod
    def speak(self):
        """抽象方法：子类必须实现"""
        ...

    def eat(self):
        """普通方法：子类可以不重写"""
        print(f"{self.name} 正在吃饭")


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        """必须实现父类的抽象方法"""
        print(f"{self.name} 正在跑...")

    def speak(self):
        """必须实现父类的抽象方法"""
        print(f"{self.name} 汪汪叫...")


class Cat(Animal):
    def run(self):
        print(f"{self.name} 正在跑...")

    def speak(self):
        print(f"{self.name} 喵喵叫...")


# animal = Animal("动物")  # TypeError: Can't instantiate abstract class Animal

dog = Dog(name="小黑")
dog.run()    # 小黑 正在跑...
dog.speak()  # 小黑 汪汪叫...
dog.eat()    # 小黑 正在吃饭

cat = Cat(name="小花")
cat.speak()  # 小花 喵喵叫...

# 抽象类的核心作用：限制子类必须重写父类的抽象方法
# 未实现所有抽象方法的子类也不能被实例化
```

---

## 五、多态与鸭子类型

### 5.1 多态

多态指的是一种事物的多种形态。在程序中，定义一个基类可以有多个子类，不同的子类对同一方法有不同的实现。

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    """所有动物的公共基类"""

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def speak(self):
        pass


# 第一种形态：人
class People(Animal):
    def run(self):
        print("人可以两条腿跑")

    def speak(self):
        print("人可以说各种语言")


# 第二种形态：猫
class Cat(Animal):
    def run(self):
        print("猫可以四条腿跑")

    def speak(self):
        print("猫喵喵叫")


# 第三种形态：鸭子
class Duck(Animal):
    def run(self):
        print("鸭子可以摇摆着跑")

    def speak(self):
        print("鸭子嘎嘎叫")


# 多态性：同一方法调用，不同对象表现出不同行为
def make_animal_run(animal):
    animal.run()


make_animal_run(People())  # 人可以两条腿跑
make_animal_run(Cat())     # 猫可以四条腿跑
make_animal_run(Duck())    # 鸭子可以摇摆着跑
```

#### 多态的好处

```python
# 1. 增加了程序的灵活性
#    可以根据父类衍生出很多子类，每个子类有自己的行为

# 2. 增强了程序的可扩展性
#    继承了父类之后，可以任意修改子类中的功能
#    父类中可以提前写好所有子类通用的方法
```

### 5.2 鸭子类型

鸭子类型是一种编程风格，不是真实存在的约束关系，而是一种普遍的规范。

```python
# 鸭子类型的核心理念：
# 叫起来像鸭子、看起来像鸭子、走起来像鸭子，那它就是鸭子
# 只要一个对象实现了某个接口所需的方法，就可以把它当作那个接口来使用


class NormalDuck:
    """正常的鸭子"""
    def eat(self):
        print("正常鸭子吃饭")

    def run(self):
        print("正常鸭子跑")


class RockDuck:
    """石头鸭子（玩具）"""
    def eat(self):
        print("石头鸭子不吃饭")

    def run(self):
        print("石头鸭子不能跑")


class Chicken:
    """鸡"""
    def eat(self):
        print("鸡吃饭")

    def run(self):
        print("鸡跑")


# 在鸭子类型中，不关心对象的具体类型，只关心它有没有需要的方法
def process_duck(duck_like):
    """只要对象有 eat 和 run 方法，就可以被处理"""
    duck_like.eat()
    duck_like.run()


process_duck(NormalDuck())  # 正常鸭子吃饭 / 正常鸭子跑
process_duck(RockDuck())    # 石头鸭子不吃饭 / 石头鸭子不能跑
process_duck(Chicken())     # 鸡吃饭 / 鸡跑

# Python 崇尚鸭子类型，这也是 Python 灵活性的重要来源
```

---

## 六、绑定方法与非绑定方法

### 6.1 概述

```python
# 绑定方法（动态方法）：绑给特定目标的方法
#   目标有两个：类 / 对象
#   - 绑定给对象的方法
#   - 绑定给类的方法

# 非绑定方法（静态方法）：不绑定给任何目标的方法
#   - 既不绑定给对象，也不绑定给类
```

### 6.2 绑定给对象的方法

```python
class Student:
    def __init__(self, name):
        self.name = name

    # 绑定给对象的方法：类内部定义的普通方法
    # 会自动补全 self 参数（代表当前对象）
    def run(self):
        print(f"{self.name} 正在跑步！")


student = Student(name="Dream")

# 对象调用绑定方法：不需要传入 self 参数
student.run()
# Dream 正在跑步！

# 类调用对象的绑定方法：必须主动传入一个对象作为 self
Student.run(student)
# Dream 正在跑步！

# 甚至可以传入任何对象（但不推荐在实际开发中这样做）
Student.run(None)
# 如果方法内有 self.xxx 则会报错

# 小结：
# - 绑定给对象的方法是在类内部直接定义的方法
# - 特点：会自动补全 self 参数
# - 对象调用时不需要传入 self
# - 类调用时需要传入 self（即当前对象）
```

### 6.3 绑定给类的方法（@classmethod）

```python
class Student:
    school = "清华大学"

    def __init__(self, name):
        self.name = name

    # 绑定给类的方法：使用 @classmethod 装饰
    # 会自动补全 cls 参数（代表当前类）
    @classmethod
    def get_school(cls):
        print(f"当前类 {cls.__name__} 的学校是：{cls.school}")

    @classmethod
    def create_student(cls, name):
        """工厂方法：创建并返回一个 Student 实例"""
        return cls(name)


student = Student("Dream")

# 对象调用类的绑定方法：不需要传入 cls，自动检测到类
student.get_school()
# 当前类 Student 的学校是：清华大学

# 类调用类的绑定方法：不需要传入 cls，自动传入当前类
Student.get_school()
# 当前类 Student 的学校是：清华大学

# 使用工厂方法创建对象
new_student = Student.create_student("Opp")
print(new_student.name)  # Opp

# 小结：
# - 绑定给类的方法必须用 @classmethod 装饰
# - 自动补全 cls 参数
# - 对象和类调用时都不需要传入额外的 cls 参数
```

### 6.4 非绑定方法 / 静态方法（@staticmethod）

```python
class Student:
    def __init__(self, name):
        self.name = name

    # 非绑定方法（静态方法）：使用 @staticmethod 装饰
    # 定义方式和普通函数完全一样，不会补全任何默认参数
    @staticmethod
    def is_valid_age(age):
        """工具方法：判断年龄是否合法"""
        if not isinstance(age, int):
            return False
        return 0 < age < 150

    @staticmethod
    def format_name(first, last):
        """工具方法：格式化名字"""
        return f"{first} {last}"


student = Student("Dream")

# 对象调用静态方法
print(student.is_valid_age(18))  # True
print(student.is_valid_age(-5))  # False

# 类调用静态方法
print(Student.is_valid_age(25))  # True
print(Student.format_name("Zhang", "San"))  # Zhang San

# 小结：
# - 在定义静态方法时必须用 @staticmethod 装饰
# - 装饰后的函数和普通函数定义一样
# - 对象和类调用静态方法时"有什么传什么"，与普通函数相同
```

### 6.5 三种方法的对比

```python
class Demo:
    # 类属性（所有实例共享）
    count = 0

    def __init__(self, name):
        self.name = name
        Demo.count += 1

    def instance_method(self):
        """实例方法：可以访问实例属性和类属性"""
        return f"实例方法：{self.name}，总数：{self.count}"

    @classmethod
    def class_method(cls):
        """类方法：可以访问类属性，不能直接访问实例属性"""
        return f"类方法：总数 {cls.count}"

    @staticmethod
    def static_method(x, y):
        """静态方法：不能访问实例属性，也不能访问类属性（除非通过类名）"""
        return f"静态方法：{x} + {y} = {x + y}"


obj = Demo("Dream")

# 实例方法调用
print(obj.instance_method())  # 实例方法：Dream，总数：1

# 类方法调用
print(Demo.class_method())    # 类方法：总数 1

# 静态方法调用
print(Demo.static_method(3, 5))  # 静态方法：3 + 5 = 8
```

---

## 七、反射

### 7.1 什么是反射

反射就是从某个对象中动态地获取或操作其属性。Python 提供了四个内置函数来实现反射机制：

```python
# 反射四大方法：
# setattr(obj, key, value)  -- 设置属性
# hasattr(obj, key)         -- 判断属性是否存在
# delattr(obj, key)         -- 删除属性
# getattr(obj, key, default) -- 获取属性
```

### 7.2 反射方法演示

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def run(self):
        print("这是绑定给对象的实例方法!")

    @classmethod
    def eat(cls):
        print("这是绑定给类的类方法!")

    @staticmethod
    def sleep():
        print("这是静态方法!")


student = Student(name="Dream", age=18)
```

#### hasattr(obj, name) -- 判断属性是否存在

```python
# hasattr(obj, name)：从对象中判断当前属性是否存在
# 有则返回 True，无则返回 False

print(hasattr(student, "name"))    # True
print(hasattr(student, "gender"))  # False
print(hasattr(student, "run"))     # True（也能判断方法属性）
print(hasattr(student, "sleep"))   # True（也能判断静态方法）
```

#### getattr(obj, name, default) -- 获取属性值

```python
# getattr(obj, name, default)：从对象中获取指定属性
# 属性存在则返回其值，不存在默认会抛出 AttributeError
# 可以指定 default 作为不存在时的默认值

print(getattr(student, "name"))           # Dream
# print(getattr(student, "gender"))       # AttributeError
print(getattr(student, "gender", None))   # None（指定了默认值）
print(getattr(student, "gender", "未知"))  # 未知
```

#### 获取方法属性

```python
# getattr 获取方法属性时，返回的是方法的内存地址
print(getattr(student, "sleep"))
# <function Student.sleep at 0x...>

# 获取后可以加括号调用
getattr(student, "sleep")()  # 这是静态方法!
getattr(student, "run")()    # 这是绑定给对象的实例方法!
```

#### setattr(obj, key, value) -- 设置属性

```python
def set_value(obj, key, value):
    """如果对象有该属性则返回原值，否则设置新值并返回"""
    if hasattr(obj, key):
        return getattr(obj, key)
    else:
        setattr(obj, key, value)
        return getattr(obj, key)


print(set_value(student, "name", "Opp"))    # Dream（已存在，返回原值）
print(set_value(student, "gender", "男"))    # 男（不存在，设置新值）

# 向对象中添加数据属性
print(student.__dict__)                     # {'name': 'Dream', 'age': 18}
setattr(student, "gender", "男")
print(student.__dict__)                     # {'name': 'Dream', 'age': 18, 'gender': '男'}

# 向类中添加方法属性
def speak():
    print("这是在类外部定义的方法!")

setattr(Student, "speak", speak)
print(Student.__dict__)  # 包含 'speak': <function speak at 0x...>
Student.speak()          # 这是在类外部定义的方法!

# 向对象中添加方法属性
setattr(student, "external_func", speak)
print(student.__dict__)  # 对象名称空间中包含 external_func
```

#### delattr(obj, key) -- 删除属性

```python
# 删除对象的数据属性
print(hasattr(student, "name"))  # True
delattr(student, "name")
print(hasattr(student, "name"))  # False

# 对象不允许删除类中的方法属性
# delattr(student, "eat")   # AttributeError
# delattr(student, "run")   # AttributeError
# delattr(student, "sleep") # AttributeError

# 但类允许删除自己的方法属性
delattr(Student, "sleep")  # 正常删除
```

### 7.3 反射的实际应用

```python
class UserController:
    """用户控制器：通过反射实现动态方法调用"""

    def login(self):
        return "登录成功"

    def register(self):
        return "注册成功"

    def logout(self):
        return "退出成功"


# 模拟根据用户输入动态调用方法
def dispatch(controller, action):
    """
    分发器：根据字符串调用对应方法
    这种方式在 Web 框架的路由系统中非常常见
    """
    if hasattr(controller, action):
        func = getattr(controller, action)
        return func()
    else:
        return f"方法 {action} 不存在"


controller = UserController()
print(dispatch(controller, "login"))     # 登录成功
print(dispatch(controller, "register"))  # 注册成功
print(dispatch(controller, "delete"))    # 方法 delete 不存在
```

---

## 八、魔法方法

### 8.1 什么是魔法方法

在类定义阶段定义的、根据特定条件自动触发的方法就叫魔法方法（Magic Methods），也称为内置方法或双下划线方法（dunder methods）。

```python
# 魔法方法的特点：
# 1. 以双下划线开头和结尾（如 __init__）
# 2. 在特定条件下自动触发，不需要手动调用
# 3. 可以自定义对象的行为
```

### 8.2 `__init__` -- 初始化方法

```python
class Person:
    def __init__(self, name, age):
        """在实例化对象时自动触发，用于初始化对象属性"""
        print("__init__ 被触发：对象正在初始化")
        self.name = name
        self.age = age


person = Person(name="Dream", age=18)
# __init__ 被触发：对象正在初始化
```

### 8.3 `__str__` -- 字符串表示（面向用户）

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        """在打印对象时自动触发，必须返回字符串"""
        return f"Person(name={self.name}, age={self.age})"


person = Person(name="Dream", age=18)
print(person)  # Person(name=Dream, age=18)

# 如果没有定义 __str__，print(person) 会输出：
# <__main__.Person object at 0x...>
```

### 8.4 `__repr__` -- 字符串表示（面向开发者）

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        """在交互式解释器中触发，或使用 repr() 函数时触发"""
        return f"Person('{self.name}', {self.age})"


person = Person(name="Dream", age=18)
print(repr(person))  # Person('Dream', 18)

# __str__ 和 __repr__ 的区别：
# - __str__：面向用户，返回易读的字符串，print() 时触发
# - __repr__：面向开发者，返回可用于重建对象的字符串，repr() 时触发
# - 如果只定义了 __repr__，print() 也会使用 __repr__
```

### 8.5 `__del__` -- 析构方法

```python
class Person:
    def __init__(self, name, age):
        print(f"__init__ 被触发")
        self.name = name
        self.age = age

    def __del__(self):
        """对象被删除时自动触发（程序结束、del 操作或被垃圾回收时）"""
        print(f"__del__ 被触发：{self.name} 被删除")


person = Person(name="Dream", age=18)
# __init__ 被触发
print(person.name)
# Dream
# __del__ 被触发：Dream 被删除

# 注意：__del__ 的触发时机由垃圾回收器决定，不是立即的
```

### 8.6 `__call__` -- 让对象可被调用

```python
class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add(self):
        return self.num1 + self.num2

    def __call__(self):
        """对象加括号时自动触发 obj()"""
        result = self.add()
        print(f"对象被调用，计算结果为：{result}")
        return result


cal = Calculator(9, 6)

# 对象加括号，触发 __call__
print(cal())
# 对象被调用，计算结果为：15
# 15

# 对象也可以像普通方法一样调用其他方法
print(cal.add())  # 15
```

### 8.7 `__new__` -- 构造方法（创建空对象）

```python
class Person:
    def __new__(cls, *args, **kwargs):
        """在 __init__ 之前被调用，用于创建并返回一个空对象"""
        print(f"__new__ 被触发：创建 {cls.__name__} 的实例")
        # 调用 object 的 __new__ 创建真正的空对象
        instance = super().__new__(cls)
        return instance

    def __init__(self, name, age):
        """在 __new__ 返回对象后调用，用于初始化对象属性"""
        print(f"__init__ 被触发：初始化 {name}")
        self.name = name
        self.age = age


person = Person(name="Dream", age=18)
# __new__ 被触发：创建 Person 的实例
# __init__ 被触发：初始化 Dream

# __new__ 和 __init__ 的关系：
# __new__：产生空对象（骨架）-- 相当于造人时的骨架
# __init__：初始化对象属性（血肉）-- 相当于填充血肉
# __new__ 先执行，__init__ 后执行
```

### 8.8 `__getattr__` -- 访问不存在的属性时触发

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getattr__(self, attr):
        """当访问的属性不存在时自动触发"""
        print(f"__getattr__ 被触发：属性 {attr} 不存在")
        if attr == "gender":
            # 为 gender 属性提供默认值
            return "male"
        # 其他不存在的属性直接报错
        raise AttributeError(f"'{self.__class__.__name__}' 没有属性 '{attr}'")


person = Person(name="Dream", age=18)
print(person.name)    # Dream（属性存在，不会触发 __getattr__）
print(person.gender)  # male（属性不存在，触发 __getattr__ 返回默认值）
# print(person.sex)   # AttributeError: 'Person' 没有属性 'sex'
```

### 8.9 `__setattr__` -- 设置属性时触发

```python
class Person:
    def __init__(self, name, age):
        # 注意：这里会触发 __setattr__
        self.name = name
        self.age = age

    def __setattr__(self, key, value):
        """对象设置属性（obj.属性名 = 属性值）时自动触发"""
        print(f"__setattr__ 被触发：{key} = {value}")
        if key == "age":
            # 对年龄进行类型校验
            if not isinstance(value, int):
                raise TypeError(f"{key} 必须是 int 类型")
        # 使用父类的 __setattr__ 方法正确设置属性
        super().__setattr__(key, value)


person = Person(name="Dream", age=18)
# __setattr__ 被触发：name = Dream
# __setattr__ 被触发：age = 18

person.age = 19
print(person.age)  # 19

# person.age = "19"  # TypeError: age 必须是 int 类型
```

### 8.10 `__delattr__` -- 删除属性时触发

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __delattr__(self, attr):
        """del 对象.属性名 时自动触发"""
        print(f"__delattr__ 被触发：准备删除 {attr}")
        if attr == "age":
            # 禁止删除 age 属性（但可以记录日志）
            print(f"不允许删除 {attr} 属性")
        else:
            # 其他属性正常删除
            super().__delattr__(attr)


person = Person(name="Dream", age=18)
del person.age    # 不允许删除 age 属性
del person.name   # 正常删除
```

### 8.11 `__getitem__` / `__setitem__` / `__delitem__` -- 索引操作

这三个方法让对象支持类似字典/列表的索引操作：

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # obj[key] 获取值
    def __getitem__(self, key):
        """对象[键] 获取值时触发"""
        print(f"__getitem__ 被触发：获取 {key}")
        return self.__dict__[key]

    # obj[key] = value 设置值
    def __setitem__(self, key, value):
        """对象[键] = 值 时触发"""
        print(f"__setitem__ 被触发：{key} = {value}")
        self.__dict__[key] = value

    # del obj[key] 删除值
    def __delitem__(self, key):
        """del 对象[键] 时触发"""
        print(f"__delitem__ 被触发：删除 {key}")
        del self.__dict__[key]


person = Person(name="Dream", age=18)

# 索引方式获取
print(person["name"])  # Dream

# 索引方式设置
person["gender"] = "男"
print(person.gender)   # 男

# 索引方式删除
del person["name"]
# print(person.name)   # AttributeError
```

### 8.12 `__enter__` 和 `__exit__` -- 上下文管理器

```python
class FileManager:
    """自定义文件上下文管理器"""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """进入 with 语句块时触发"""
        print(f"__enter__ 被触发：打开文件 {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 语句块时触发（无论是否发生异常）"""
        print(f"__exit__ 被触发：关闭文件 {self.filename}")
        if self.file:
            self.file.close()
        # 返回 True 可以抑制异常，返回 False 或 None 则正常传播异常
        return False


# 使用自定义上下文管理器
with FileManager("test.txt", "w") as f:
    f.write("Hello World")
# __enter__ 被触发：打开文件 test.txt
# __exit__ 被触发：关闭文件 test.txt
```

### 8.13 `__iter__` 和 `__next__` -- 迭代器

```python
class RangeIterator:
    """自定义迭代器：生成指定范围内的数字"""

    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        """返回迭代器对象本身"""
        return self

    def __next__(self):
        """返回下一个值，没有更多值时抛出 StopIteration"""
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


# 使用自定义迭代器
for num in RangeIterator(0, 5):
    print(num, end=" ")  # 0 1 2 3 4
print()

# 也可以手动的使用 next()
iterator = RangeIterator(0, 3)
print(next(iterator))  # 0
print(next(iterator))  # 1
print(next(iterator))  # 2
# print(next(iterator))  # StopIteration
```

### 8.14 `__doc__` -- 文档注释

```python
class Person:
    """
    这是一个 Person 类
    用于表示一个人的基本信息
    """
    def __init__(self, name, age):
        """初始化人的属性"""
        self.name = name
        self.age = age


# 查看类的文档注释
print(Person.__doc__)
# 这是一个 Person 类
# 用于表示一个人的基本信息

# 查看方法的文档注释
print(Person.__init__.__doc__)
# 初始化人的属性
```

### 8.15 魔法方法汇总表

```python
# 常用魔法方法分类汇总：

# 【对象生命周期】
# __new__(cls, ...)      -- 创建对象时触发（在 __init__ 之前）
# __init__(self, ...)    -- 初始化对象时触发
# __del__(self)          -- 对象被销毁时触发

# 【字符串表示】
# __str__(self)          -- print() / str() 时触发，面向用户
# __repr__(self)         -- repr() / 交互式环境 时触发，面向开发者

# 【属性操作】
# __getattr__(self, name)     -- 访问不存在的属性时触发
# __setattr__(self, name, v)  -- 设置属性时触发
# __delattr__(self, name)     -- 删除属性时触发

# 【索引操作（将对象当字典/列表使用）】
# __getitem__(self, key)      -- obj[key] 获取值时触发
# __setitem__(self, key, v)   -- obj[key] = v 设置值时触发
# __delitem__(self, key)      -- del obj[key] 删除值时触发

# 【可调用对象】
# __call__(self, ...)         -- 对象加括号 obj() 时触发

# 【上下文管理】
# __enter__(self)             -- with 语句开始时触发
# __exit__(self, ...)         -- with 语句结束时触发

# 【迭代器】
# __iter__(self)              -- iter() / for 循环开始时触发
# __next__(self)              -- next() / 每次迭代时触发

# 【文档】
# __doc__                     -- 类/函数的文档字符串
```

---

## 九、元类

### 9.1 什么是元类

一切都源于一句话：**Python 中一切皆对象**。八大基本数据类型是对象，类实例化得到的对象也是对象，**类本身也是一种对象**。

```python
class Student:
    def __init__(self, name):
        self.name = name


# 实例化类得到对象
student = Student(name="Dream")

# 查看对象的数据类型
print(type(student))  # <class '__main__.Student'>
# 解释：student 是由 Student 类产生的对象

# 查看产生这个类的数据类型
print(type(Student))  # <class 'type'>
# 解释：Student 类本身也是一个对象，它是由 type 类产生的

# 类本身也是 type 的对象，type 就是"元类"
# 元类就是用来创建类的类，就像类是用来创建对象的模板一样
```

```python
# 验证：所有类都是由 type 创建的
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>
print(type(list))   # <class 'type'>
print(type(dict))   # <class 'type'>
print(type(object)) # <class 'type'>
print(type(type))   # <class 'type'>（type 本身也是 type 的实例）
```

### 9.2 产生类的两种方式

#### 方式一：使用 class 关键字（常规方式）

```python
class Student:
    school = "清华大学"

    def __init__(self, name):
        self.name = name

    def read(self):
        print(f"{self.name} 正在读书!")


# 查看创建当前类的类
print(type(Student))  # <class 'type'>

# 查看当前类的名称空间
print(Student.__dict__)
# {'__module__': '__main__', 'school': '清华大学',
#  '__init__': <function Student.__init__ at 0x...>,
#  'read': <function Student.read at 0x...>, ...}
```

#### 方式二：使用 type() 动态创建类

```python
# type() 的两种用法：
# 1. type(obj)             -- 查看对象的数据类型
# 2. type(name, bases, dict)  -- 动态创建新类

# type(name, bases, dict) 参数说明：
# name   -- 类名（字符串）
# bases  -- 父类元组
# dict   -- 类的属性字典（包含方法和类变量）


# 定义类的功能函数
def read(self):
    print(f"{self.name} 正在读书!")


def __init__(self, name):
    self.name = name


# 使用 type 动态创建类
Student = type("Student",       # 类名
               (object,),        # 父类
               {                 # 类的属性字典
                   "school": "清华大学",
                   "__init__": __init__,
                   "read": read,
               })

# 查看创建当前类的类
print(type(Student))  # <class 'type'>

# 使用动态创建的类
student = Student(name="Dream")
student.read()  # Dream 正在读书!
print(student.school)  # 清华大学

# 注意：通过 type() 动态创建时，传入的函数是普通函数
# 通过 class 关键字定义的方法会被包装成绑定方法（会带类名前缀）
# 但在 Python 3.x 中，通过 type() 创建也会自动处理这个问题
```

### 9.3 为什么要使用元类

元类可以控制类的创建过程，意味着我们可以高度定制类的具体行为。

```python
# 类比理解：
# - 类控制对象的创建过程（通过 __init__ 方法）
# - 元类控制类的创建过程（通过 __init__ 等方法）

# 掌握了食品的生产过程，就可以在里面动手脚
# 掌握了类的创建过程，就可以对类进行定制
```

### 9.4 元类的基本使用

#### 定义和使用自定义元类

```python
class MyMeta(type):
    """
    自定义元类，用于控制类的创建过程
    注意：元类必须继承自 type
    """

    def __init__(cls, class_name, class_bases, class_dict):
        """
        控制类的创建过程
        参数：
        - cls：正在创建的类
        - class_name：类名（字符串）
        - class_bases：父类元组
        - class_dict：类的属性字典
        """
        print(f"正在创建类：{class_name}")
        print(f"父类：{class_bases}")
        print(f"类属性：{list(class_dict.keys())}")
        # 调用父类的 __init__ 完成正常的初始化
        super().__init__(class_name, class_bases, class_dict)


# 使用 metaclass 关键字指定元类
# 这与继承不同——这里指定的是"创建这个类的类"
class MyClass(metaclass=MyMeta):
    name = "测试类"

    def show(self):
        print("show 方法")


# 输出：
# 正在创建类：MyClass
# 父类：(<class 'object'>,)
# 类属性：['__module__', '__qualname__', 'name', 'show']
```

#### 限制类名必须首字母大写

```python
class TitleMeta(type):
    """要求所有类名必须首字母大写"""

    def __init__(cls, class_name, class_bases, class_dict):
        # 检查类名是否首字母大写
        if not class_name.istitle():
            raise TypeError(f"类名 '{class_name}' 必须首字母大写！")
        super().__init__(class_name, class_bases, class_dict)


# 符合规范的类（首字母大写）
class Student(metaclass=TitleMeta):
    """正常创建"""
    pass


# 不符合规范的类 -- 直接报错
# class student(metaclass=TitleMeta):  # TypeError: 类名 'student' 必须首字母大写！
#     pass
```

### 9.5 元类的进阶使用

#### 类创建过程的完整生命周期

```python
class MyMeta(type):
    # 第一步：__new__ 创建空类（骨架）
    def __new__(cls, class_name, class_bases, class_dict):
        print(f"1. __new__ ：创建类 {class_name}")
        # 使用 type.__new__ 创建真正的类对象
        new_cls = type.__new__(cls, class_name, class_bases, class_dict)
        return new_cls

    # 第二步：__init__ 初始化类（血肉）
    def __init__(cls, class_name, class_bases, class_dict):
        print(f"2. __init__ ：初始化类 {class_name}")
        super().__init__(class_name, class_bases, class_dict)

    # 第三步：__call__ 在实例化类创建对象时触发
    def __call__(self, *args, **kwargs):
        print(f"3. __call__ ：实例化 {self.__name__}，参数：{args}, {kwargs}")
        # 调用父类的 __call__ 创建并初始化对象
        instance = super().__call__(*args, **kwargs)
        return instance


class MyClass(metaclass=MyMeta):
    def __init__(self, name):
        print(f"4. MyClass.__init__ ：初始化对象，name={name}")
        self.name = name


# 创建对象的过程
obj = MyClass(name="Dream")
print(f"创建的对象：{obj}, name={obj.name}")

# 输出：
# 1. __new__ ：创建类 MyClass
# 2. __init__ ：初始化类 MyClass
# 3. __call__ ：实例化 MyClass，参数：(), {'name': 'Dream'}
# 4. MyClass.__init__ ：初始化对象，name=Dream
# 创建的对象：<__main__.MyClass object at 0x...>, name=Dream
```

#### 定制对象的产生过程

```python
class StrictMeta(type):
    """要求对象只能通过关键字参数创建，不允许位置参数"""

    def __init__(cls, class_name, class_bases, class_dict):
        super().__init__(class_name, class_bases, class_dict)

    def __call__(self, *args, **kwargs):
        # 如果传入了位置参数，直接报错
        if args:
            raise TypeError(
                f"{self.__name__} 创建对象时仅支持关键字参数，"
                f"禁止使用位置参数！"
            )
        # 只允许关键字参数
        return super().__call__(*args, **kwargs)


class Person(metaclass=StrictMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age


# 正确：使用关键字参数
person = Person(name="Dream", age=18)
print(f"创建成功：{person.name}, {person.age}")

# 错误：使用位置参数
# person = Person("Dream", 18)
# TypeError: Person 创建对象时仅支持关键字参数，禁止使用位置参数！
```

### 9.6 元类总结

```python
# 元类属于面向对象中比较高阶的用法，无特殊需求不建议使用

# 元类的两个核心定制点：
# 1. 定制类的产生过程 → 编写元类的 __init__ 方法
#    - 可以校验类名、类属性
#    - 可以自动为类添加属性或方法
#    - 可以实现类似抽象类的约束

# 2. 定制对象的产生过程 → 编写元类的 __call__ 方法
#    - 可以限制对象的创建方式
#    - 可以实现单例模式
#    - 可以对创建的对象做额外处理


# 类创建的生命周期（使用元类时）：
# 1. 元类.__new__  →  创建空类（骨架）
# 2. 元类.__init__ →  初始化类（血肉）
# 3. 元类.__call__ →  创建类的实例时触发
#    - 内部会调用：类.__new__ → 类.__init__
```

### 9.7 单例模式（元类应用实例）

```python
class SingletonMeta(type):
    """使用元类实现单例模式"""

    # 存储每个类的唯一实例
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # 如果该类还没有实例，则创建一个
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        # 返回已有的实例
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        print(f"连接数据库：{host}:{port}")


# 无论创建多少次，都是同一个实例
db1 = Database("localhost", 3306)
db2 = Database("localhost", 3306)
db3 = Database("192.168.1.1", 5432)  # 仍然是同一个实例

print(db1 is db2)  # True
print(db1 is db3)  # True
print(f"db1.host = {db1.host}")  # localhost
print(f"db3.host = {db3.host}")  # localhost（不是 192.168.1.1）
```

---

## 十、面向对象知识总结

### 10.1 三大特性总结

```python
# 【封装】
# 将数据和方法包装在类内部，通过访问控制保护数据安全
# Python 中通过双下划线开头实现私有化
# 通过 @property 实现属性访问控制

# 【继承】
# 子类继承父类的属性和方法，实现代码复用
# 单继承、多继承、MRO（C3 线性化算法）
# super() 调用父类方法

# 【多态】
# 同一方法在不同类中有不同实现
# 鸭子类型：不关心对象类型，只关心对象有没有需要的方法
```

### 10.2 类的方法类型总结

```python
class Summary:
    class_var = "类属性"  # 所有实例共享

    def instance_method(self):
        """实例方法：第一个参数是 self（对象本身）"""
        pass

    @classmethod
    def class_method(cls):
        """类方法：第一个参数是 cls（类本身）"""
        pass

    @staticmethod
    def static_method():
        """静态方法：没有默认参数，和普通函数一样"""
        pass
```

### 10.3 魔法方法速查

| 魔法方法 | 触发场景 | 说明 |
|---------|---------|------|
| `__init__` | 实例化对象时 | 初始化对象属性 |
| `__new__` | 创建对象时（__init__之前） | 创建并返回空对象 |
| `__del__` | 对象被销毁时 | 析构方法，清理资源 |
| `__str__` | print() / str() | 面向用户的字符串表示 |
| `__repr__` | repr() / 交互环境 | 面向开发者的字符串表示 |
| `__call__` | obj() | 让对象可被调用 |
| `__getattr__` | 访问不存在的属性 | 属性访问的后备方法 |
| `__setattr__` | obj.attr = value | 控制属性设置行为 |
| `__delattr__` | del obj.attr | 控制属性删除行为 |
| `__getitem__` | obj[key] | 索引获取 |
| `__setitem__` | obj[key] = value | 索引设置 |
| `__delitem__` | del obj[key] | 索引删除 |
| `__enter__` | with 语句开始 | 上下文管理器入口 |
| `__exit__` | with 语句结束 | 上下文管理器出口 |
| `__iter__` | iter() / for循环 | 返回迭代器 |
| `__next__` | next() | 返回下一个值 |
| `__doc__` | 访问文档 | 类/函数的文档字符串 |

### 10.4 反射方法速查

| 方法 | 作用 | 示例 |
|-----|------|------|
| `hasattr(obj, name)` | 判断属性是否存在 | `hasattr(obj, "name")` |
| `getattr(obj, name, default)` | 获取属性值 | `getattr(obj, "name", None)` |
| `setattr(obj, name, value)` | 设置属性值 | `setattr(obj, "name", "Dream")` |
| `delattr(obj, name)` | 删除属性 | `delattr(obj, "name")` |
