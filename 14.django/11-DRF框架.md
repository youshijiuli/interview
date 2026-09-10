# Django REST Framework 从入门到精通

---

## 目录

1. [前后端开发模式](#一前后端开发模式)
2. [API接口](#二api接口)
3. [RESTful API设计规范](#三restful-api设计规范)
4. [序列化与反序列化概念](#四序列化与反序列化概念)
5. [DRF介绍与安装](#五drf介绍与安装)
6. [Request对象与Response对象](#六request对象与response对象)
7. [序列化器 Serializer](#七序列化器-serializer)
8. [序列化器校验](#八序列化器校验)
9. [定制返回格式](#九定制返回格式)
10. [多表关联序列化与反序列化](#十多表关联序列化与反序列化)
11. [ModelSerializer](#十一modelserializer)
12. [请求与响应深入](#十二请求与响应深入)
13. [视图层](#十三视图层)
14. [路由层](#十四路由层)
15. [认证组件](#十五认证组件)
16. [权限组件](#十六权限组件)
17. [频率限制（限流）](#十七频率限制限流)
18. [过滤与排序](#十八过滤与排序)
19. [分页](#十九分页)
20. [全局异常处理](#二十全局异常处理)
21. [接口文档生成](#二十一接口文档生成)
22. [JWT认证](#二十二jwt认证)
23. [权限控制模型 (ACL/RBAC)](#二十三权限控制模型-aclrbac)
24. [源码分析](#二十四源码分析)

---

## 一、前后端开发模式

### 1.1 混合开发模式

在混合开发模式下，后端与前端紧密耦合。后端框架（如 Django、Flask、Java JSP、Go Gin）使用模板语法在服务器端渲染 HTML 页面。

**执行流程：**

```
1. 后端拿到模板文件（如 index.html）
2. 使用模板语法（DTL、Jinja2 等）将变量渲染到模板中
3. 生成纯 HTML/CSS/JS 字符串
4. 将字符串返回给浏览器
5. 浏览器解析 HTML、应用 CSS、执行 JS
```

**关键特点：**
- 模板渲染在后端完成
- 前端代码和后端代码耦合在一起
- 适用于小型项目或内容型网站
- 各语言有自己的模板语法：Django 用 DTL、Flask 用 Jinja2、Java 用 JSP、Go 用 .tpl

**示例（Django 混合开发）：**

```python
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'name': '张三', 'books': book_list})
```

```html
<!-- index.html -->
<h1>欢迎 {{ name }}</h1>
<ul>
    {% for book in books %}
        <li>{{ book.name }} - ¥{{ book.price }}</li>
    {% endfor %}
</ul>
```

### 1.2 前后端分离开发模式

前后端分离是现代 Web 开发的主流模式，前端和后端完全独立开发和部署。

**架构特点：**

```
前端（大前端）：
  - Web 前端：Vue、React、Angular
  - 微信小程序
  - 移动 App（iOS/Android）
  - 桌面应用（Electron）

后端（接口服务）：
  - 提供 RESTful API 接口
  - 返回 JSON/XML 格式数据
  - 专注于业务逻辑和数据处理
```

**交互流程：**

```
1. 前端通过 AJAX/Fetch 请求后端接口
2. 后端处理请求，返回 JSON 数据
3. 前端收到数据后，通过 JS 动态渲染页面
```

**优点：**
- 前后端独立开发，提高开发效率
- 后端接口可复用（Web、App、小程序共用）
- 前后端可以独立部署和扩展
- 技术选型灵活

---

## 二、API接口

### 2.1 什么是API接口

API（Application Programming Interface）接口是前后端信息交互的媒介，规定了前后台信息交互规则。

**API接口的组成部分：**

| 组成部分 | 说明 | 示例 |
|---------|------|------|
| URL | 链接地址 | `http://127.0.0.1:8080/api/v1/books/` |
| 请求方式 | GET、POST、PUT、DELETE等 | `GET` |
| 请求参数 | key-value类型数据 | `?name=红楼梦&price=50` |
| 请求体 | JSON/XML/表单数据 | `{"name":"红楼梦","price":50}` |
| 响应结果 | JSON/XML格式数据 | `{"code":100,"msg":"成功"}` |

### 2.2 HTTP请求协议

```
请求首行：协议版本、请求地址、请求方式
请求头：key-value 键值对
请求体：不同编码格式的数据

编码格式（Content-Type）：
- urlencoded：  name=lqz&age=19          （form表单默认格式）
- json：        {"name":"lqz","age":19}   （最常用）
- form-data：   文件+数据的混合格式        （用于文件上传）
```

### 2.3 Django中获取请求数据

```python
# Django 原生 request 的限制：
request.POST    # 只能获取 POST 请求的 urlencoded 和 form-data 数据
request.GET     # 获取 URL 中的查询参数
request.body    # 原始请求体（所有请求方式、所有编码格式都在这里）

# 问题：PUT 请求的 JSON 数据需要通过 request.body 手动解析
```

```python
# jQuery AJAX 不同编码格式示例

# 1. urlencoded 格式
$.ajax({
    url: '/api/books/',
    method: 'POST',
    contentType: 'application/x-www-form-urlencoded',
    data: {name: 'lqz', password: '123'},  // 请求体: name=lqz&password=123
    success: function(data) { console.log(data); }
});

# 2. form-data 格式（上传文件）
$.ajax({
    url: '/api/upload/',
    method: 'POST',
    processData: false,
    contentType: false,
    data: formDataObj,
    success: function(data) { console.log(data); }
});

# 3. JSON 格式
$.ajax({
    url: '/api/books/',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({name: 'lqz', password: '123'}),
    success: function(data) { console.log(data); }
});
```

### 2.4 接口测试工具

常用的接口测试工具有：

- **Postman**：最主流的接口测试工具（收费）
- **Apifox**：Postman + Swagger + Mock + JMeter
- **Postwoman**：开源替代方案
- **Python requests 模块**：代码方式测试

---

## 三、RESTful API设计规范

### 3.1 什么是RESTful规范

RESTful 是一种定义 Web API 接口的设计风格，尤其适用于前后端分离的应用模式。它不是标准，而是约定俗成的规范，共有 10 条建议。

### 3.2 十条规范详解

**1. 数据安全保障 —— URL使用HTTPS**

```
http://api.example.com   （不安全）
https://api.example.com  （安全，推荐）
```

**2. 接口中带API标识**

```
https://api.example.com/v1/books
https://www.example.com/api/v1/books
```

**3. 接口中带版本标识**

```
https://api.example.com/v1/books
https://api.example.com/v2/books
```

**4. 数据即资源，使用名词（可用复数）**

```
https://api.example.com/v1/users
https://api.example.com/v1/books
```

**5. 通过请求方式决定资源操作**

| 请求方式 | URL | 操作 | 对应SQL |
|---------|-----|------|---------|
| GET | /books/ | 获取所有书 | SELECT * |
| POST | /books/ | 新增一本书 | INSERT |
| GET | /books/1/ | 获取主键为1的书 | SELECT WHERE id=1 |
| PUT | /books/1/ | 整体修改主键为1的书 | UPDATE WHERE id=1 |
| PATCH | /books/1/ | 局部修改主键为1的书 | UPDATE 部分字段 |
| DELETE | /books/1/ | 删除主键为1的书 | DELETE WHERE id=1 |

**6. 请求地址中带过滤条件**

```
https://api.example.com/v1/books?name=红楼梦
https://api.example.com/v1/books?ordering=-price&search=红
```

**7. 响应中带状态码**

```json
// HTTP 状态码
200 OK             // 成功
201 Created        // 创建成功
204 No Content     // 删除成功（无响应体）
400 Bad Request    // 请求错误
401 Unauthorized   // 未认证
403 Forbidden      // 无权限
404 Not Found      // 资源不存在
500 Server Error   // 服务器错误

// 自定义业务状态码
{
    "code": 100,
    "msg": "成功"
}
```

**8. 响应中带错误信息**

```json
{
    "code": 101,
    "msg": "用户名或密码错误"
}
```

**9. 不同操作返回不同结果格式**

```
GET /books/     -> [{...}, {...}]           // 返回列表
GET /books/1/   -> {...}                   // 返回单个对象
POST /books/    -> {...}                   // 返回新创建的对象
PUT /books/1/   -> {...}                   // 返回修改后的完整对象
DELETE /books/1/ -> ""                      // 返回空文档
```

**10. 返回数据中带URL链接（HATEOAS）**

```json
{
    "id": 1,
    "name": "红楼梦",
    "url": "https://api.example.com/v1/books/1/"
}
```

---

## 四、序列化与反序列化概念

### 4.1 基本概念

在 API 接口开发中，序列化是最核心的过程。

**序列化（Serialization）：**
将程序中的数据结构（字典、列表、对象）转换成指定格式（JSON字符串、XML、二进制等），以便传输或存储。

```
Python对象/QuerySet  -->  JSON字符串  -->  前端使用
```

**反序列化（Deserialization）：**
将传输过来的数据（JSON字符串等）还原成程序中的数据结构。

```
前端JSON数据  -->  数据校验  -->  Python对象  -->  保存到数据库
```

### 4.2 在Django中的应用场景

```python
# 序列化场景：数据库查出的模型对象 -> 序列化为JSON -> 返回给前端
students = Student.objects.all()           # QuerySet对象
# 序列化后 -> [{"name":"张三","age":18}, ...]

# 反序列化场景：前端提交的JSON -> 数据校验 -> 保存到数据库
{"name":"张三","age":18}  ->  校验通过  ->  Student.objects.create(name="张三", age=18)
```

---

## 五、DRF介绍与安装

### 5.1 什么是DRF

Django REST Framework（DRF）是 Django 的一个第三方应用，用于快速构建符合 RESTful 规范的 Web API。它本质上是 Django 的一个 app，构建在 Django 之上，提供了大量开箱即用的功能。

**DRF封装的核心功能：**

- 新的请求对象（Request）
- 新的响应对象（Response）
- 序列化器（Serializer/ModelSerializer）
- 丰富的视图类（APIView、GenericAPIView、ViewSet等）
- 路由自动生成
- 认证组件（Authentication）
- 权限组件（Permission）
- 频率限制（Throttling）
- 过滤与排序（Filtering/Ordering）
- 分页（Pagination）
- 全局异常处理（Exception Handler）
- JWT 认证支持
- 接口文档自动生成

### 5.2 环境要求与安装

```bash
# 环境要求
# Django >= 3.2
# Python >= 3.8
# MySQL >= 8.0（如果使用MySQL）

# 安装 DRF
pip install djangorestframework

# 安装最新版
pip install djangorestframework --upgrade
```

### 5.3 配置DRF

```python
# settings.py
INSTALLED_APPS = [
    '14.django.contrib.admin',
    '14.django.contrib.auth',
    '14.django.contrib.contenttypes',
    '14.django.contrib.sessions',
    '14.django.contrib.messages',
    '14.django.contrib.staticfiles',
    'rest_framework',        # 注册 DRF
    'app01',                 # 你自己的应用
]

# DRF 全局配置（可选）
REST_FRAMEWORK = {
    # 全局解析器
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # 全局渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### 5.4 快速体验：5个基本接口

DRF 最基本的使用场景是为一数据表快速生成增删改查的 5 个接口。

```python
# models.py
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()

# serializer.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# views.py
from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializer import BookSerializer

class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookView

router = SimpleRouter()
router.register('books', BookView, 'books')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

访问上述配置后，自动生成 5 个接口：

| 请求方式 | URL | 功能 |
|---------|-----|------|
| GET | /api/v1/books/ | 查询所有图书 |
| POST | /api/v1/books/ | 新增一本图书 |
| GET | /api/v1/books/1/ | 查询单本图书 |
| PUT | /api/v1/books/1/ | 修改单本图书 |
| DELETE | /api/v1/books/1/ | 删除单本图书 |

---

## 六、Request对象与Response对象

### 6.1 新的Request对象

当视图类继承 `APIView` 后，`request` 对象会变成 DRF 提供的新 Request 对象。

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class DemoView(APIView):
    def post(self, request):
        # request 现在是 rest_framework.request.Request 对象
        # 原来的 request 是 14.django.core.handlers.wsgi.WSGIRequest
        pass
```

**新老Request对比：**

```python
# 老Request的属性/方法，新Request依然兼容
request.method              # 请求方式
request.GET                 # URL查询参数
request.POST                # POST数据
request.FILES               # 上传的文件
request.body                # 原始请求体
request.get_full_path()     # 完整路径
request.META                # 请求头元数据（HTTP_USER_AGENT, REMOTE_ADDR等）

# 新Request新增的属性
request.data                # 所有请求体数据（无论什么编码格式、什么请求方式）
request.query_params        # URL查询参数（等同于 request.GET，语义更清晰）
request._request            # 原来的老 Request 对象
```

**request.data 详解：**

```python
class StudentView(APIView):
    def post(self, request):
        # request.data 自动解析不同编码格式
        # - JSON格式：返回普通 dict
        # - urlencoded/form-data：返回 QueryDict 对象
        # 但无论是哪种，都可以当字典使用
        name = request.data.get('name')
        age = request.data.get('age')
        return Response({'name': name, 'age': age})
```

### 6.2 Response对象

DRF 提供了统一的 Response 对象用于返回响应，等同于 `HttpResponse` + `JsonResponse` 的合体。

```python
from rest_framework.response import Response

# 基本使用
Response('ok')
Response({'code': 100, 'msg': '成功'})
Response([1, 2, 3])

# 指定状态码
Response({'code': 100, 'msg': '创建成功'}, status=201)

# 指定响应头
Response('ok', status=200, headers={'X-Custom': 'value'})
```

**Response 的参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| data | dict/list/str | 响应体数据 |
| status | int | HTTP 状态码，DRF 封装了常量如 `status.HTTP_200_OK` |
| headers | dict | 响应头 |
| content_type | str | 响应编码格式，默认 application/json |
| template_name | str | 浏览器访问时使用的模板 |

**重要提示：**
如果使用浏览器访问 DRF 接口返回的 Response，可能遇到模板错误。解决方法是在 `INSTALLED_APPS` 中注册 `rest_framework`：

```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # 必须注册，否则浏览器访问会报模板错误
]
```

---

## 七、序列化器 Serializer

### 7.1 Serializer 简介

序列化器有三个核心作用：
1. **序列化**：将模型对象/QuerySet 转换为 JSON 数据
2. **反序列化**：将 JSON 数据校验后保存到数据库
3. **数据校验**：对前端传入的数据进行验证

### 7.2 Serializer 基本使用

**定义模型：**

```python
# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    school = models.CharField(max_length=32)
```

**定义序列化类：**

```python
# serializer.py
from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    school = serializers.CharField()
```

**序列化（查询）操作：**

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from .serializer import StudentSerializer

class StudentView(APIView):
    def get(self, request):
        # 1. 获取所有数据
        students = Student.objects.all()
        # 2. 序列化（多条数据必须传 many=True）
        serializer = StudentSerializer(instance=students, many=True)
        # 3. 返回 JSON 数据
        return Response(serializer.data)

class StudentDetailView(APIView):
    def get(self, request, pk):
        # 1. 获取单条数据
        student = Student.objects.filter(pk=pk).first()
        # 2. 序列化（单条数据不需要 many）
        serializer = StudentSerializer(instance=student)
        # 3. 返回 JSON 数据
        return Response(serializer.data)
```

**路由配置：**

```python
# urls.py
from django.urls import path
from .views import StudentView, StudentDetailView

urlpatterns = [
    path('students/', StudentView.as_view()),
    path('students/<int:pk>/', StudentDetailView.as_view()),
]
```

### 7.3 常用字段类

序列化器的字段类与 Django 模型的字段类一一对应：

| 序列化字段类 | 对应模型字段 | 说明 |
|------------|------------|------|
| CharField | CharField | 字符串 |
| IntegerField | IntegerField | 整数 |
| FloatField | FloatField | 浮点数 |
| DecimalField | DecimalField | 精确小数 |
| BooleanField | BooleanField | 布尔值 |
| DateTimeField | DateTimeField | 日期时间 |
| DateField | DateField | 日期 |
| TimeField | TimeField | 时间 |
| EmailField | EmailField | 邮箱 |
| URLField | URLField | URL |
| FileField | FileField | 文件 |
| ImageField | ImageField | 图片 |
| ChoiceField | - | 选项 |
| ListField | - | 列表（特殊） |
| DictField | - | 字典（特殊） |
| SerializerMethodField | - | 自定义方法字段（特殊） |

**技巧：** 如果不确定使用哪个字段类型，可以统一使用 `CharField`。

### 7.4 常用字段参数

```python
# CharField 专用参数
max_length       # 最大长度
min_length       # 最小长度
allow_blank      # 是否允许为空
trim_whitespace  # 是否截断空白字符

# IntegerField 专用参数
max_value        # 最大值
min_value        # 最小值

# DateTimeField 专用参数
format           # 格式化输出，如 'Y年m月d日'

# 所有字段通用参数
required         # 是否必填，默认 True
default          # 默认值
allow_null       # 是否允许 None，默认 False
read_only        # 只读（仅用于序列化输出），默认 False
write_only       # 只写（仅用于反序列化输入），默认 False
```

---

## 八、序列化器校验

### 8.1 反序列化校验概述

反序列化校验分为两层：
1. **字段自身校验**：通过字段类的参数控制（max_length、min_value、required 等）
2. **钩子函数校验**：
   - **局部钩子**：`validate_字段名(self, value)` —— 校验单个字段
   - **全局钩子**：`validate(self, attrs)` —— 校验多个字段

### 8.2 字段自身校验

```python
from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=110)
    name = serializers.CharField(max_length=8, min_length=3)
    school = serializers.CharField(max_length=8, min_length=3)
```

### 8.3 局部钩子校验

局部钩子用于对单个字段进行自定义校验，方法名必须为 `validate_字段名`。

```python
from rest_framework.exceptions import ValidationError

class StudentSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=110)
    name = serializers.CharField(max_length=8, min_length=3)
    school = serializers.CharField(max_length=8, min_length=3)

    # 局部钩子：校验 name 字段
    def validate_name(self, value):
        # value 是前端传入、经过字段自身校验后的值
        if value.startswith('刘'):
            raise ValidationError('你不配姓刘')
        # 校验通过必须返回 value
        return value

    # 局部钩子：校验 school 字段
    def validate_school(self, value):
        if 'sb' in value:
            raise ValidationError('学校名不能包含敏感词')
        return value
```

### 8.4 全局钩子校验

全局钩子用于对多个字段进行联合校验，方法名必须为 `validate`。

```python
class StudentSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=110)
    name = serializers.CharField(max_length=8, min_length=3)
    school = serializers.CharField(max_length=8, min_length=3)

    # 全局钩子：校验多个字段的关系
    def validate(self, attrs):
        # attrs 是前端传入、经过字段自身校验和局部钩子校验后的所有数据
        name = attrs.get('name')[:2]
        school = attrs.get('school')[:2]
        if name == school:
            raise ValidationError('人名和学校的前两个字符不能一样')
        # 校验通过必须返回 attrs
        return attrs
```

### 8.5 完整的校验代码示例

```python
# models.py
class Student(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=32)
    school = models.CharField(max_length=32)

# serializer.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Student

class StudentSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=110)
    name = serializers.CharField(max_length=8, min_length=3)
    school = serializers.CharField(max_length=8, min_length=3)

    # 局部钩子
    def validate_name(self, value):
        if value.startswith('刘'):
            raise ValidationError('你不配姓刘')
        return value

    # 全局钩子
    def validate(self, attrs):
        name = attrs.get('name')[:2]
        school = attrs.get('school')[:2]
        if name == school:
            raise ValidationError('人名和学校的前两个字符不能一样')
        return attrs

    # 新增
    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    # 修改
    def update(self, instance, validated_data):
        for key in validated_data:
            setattr(instance, key, validated_data.get(key))
        instance.save()
        return instance

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import StudentSerializer

class StudentView(APIView):
    def post(self, request):
        # 实例化时传入 data 参数表示反序列化
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # 校验通过，保存数据
            serializer.save()
            return Response(serializer.data)
        else:
            # 校验失败，返回错误信息
            return Response(serializer.errors)

# urls.py
from django.urls import path
from .views import StudentView

urlpatterns = [
    path('students/', StudentView.as_view()),
]
```

---

## 九、定制返回格式

### 9.1 使用 source 定制字段

当序列化的字段名与模型字段名不一致，或需要跨表获取字段时，使用 `source` 参数。

```python
# 模型
class Student(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=32)
    school = models.CharField(max_length=32)

    @property
    def new_school(self):
        return "NB_" + self.school

# 序列化类
class StudentSerializer(serializers.Serializer):
    # 基础使用：source 指定模型中的字段
    sch = serializers.CharField(source='school')

    # 跨表使用：获取关联表的字段
    publish_name = serializers.CharField(source='publish.name')

    # 使用模型方法
    new_school_name = serializers.CharField(source='new_school')
```

**注意：** 使用 `source` 时，序列化类中的字段名不能与 source 的值相同。

### 9.2 表模型中写方法

在模型中定义方法（或 `@property`），然后在序列化类中使用 `DictField` 或 `ListField` 接收。

```python
# models.py
class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey('Publish', on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField('Author')

    # 一对多关系的定制返回
    @property
    def publish_detail(self):
        return {
            'name': self.publish.name,
            'addr': self.publish.addr,
            'city': self.publish.city
        }

    # 多对多关系的定制返回
    @property
    def author_list(self):
        result = []
        for author in self.authors.all():
            result.append({'name': author.name, 'age': author.age, 'addr': author.addr})
        return result

# serializer.py
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    # 接收模型方法的返回值
    publish_detail = serializers.DictField()
    author_list = serializers.ListField()
```

### 9.3 序列化类中使用 SerializerMethodField

在序列化类中定义一个 `SerializerMethodField` 字段，并配合 `get_字段名` 方法使用。

```python
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.IntegerField()

    # 一对多定制
    publish_detail = serializers.SerializerMethodField()
    def get_publish_detail(self, obj):
        # obj 是当前正在序列化的 Book 对象
        return {
            'name': obj.publish.name,
            'addr': obj.publish.addr,
            'city': obj.publish.city
        }

    # 多对多定制
    author_list = serializers.SerializerMethodField()
    def get_author_list(self, obj):
        result = []
        for author in obj.authors.all():
            result.append({'name': author.name, 'age': author.age, 'addr': author.addr})
        return result

    # 自定义拼接字段
    new_name = serializers.SerializerMethodField()
    def get_new_name(self, obj):
        return obj.name + '_明星'
```

### 9.4 子序列化

通过嵌套另一个序列化器来实现关联对象的序列化。

```python
# 子序列化器
class PublishSerializer(serializers.Serializer):
    name = serializers.CharField()
    addr = serializers.CharField()
    city = serializers.CharField()

class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    addr = serializers.CharField()

# 主序列化器
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.IntegerField()

    # 一对多：直接嵌套
    publish = PublishSerializer()

    # 多对多：嵌套时必须加 many=True
    authors = AuthorSerializer(many=True)
```

---

## 十、多表关联序列化与反序列化

### 10.1 多表关联反序列化 — 新增

```python
# models.py
class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    addr = models.CharField(max_length=32)

class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey('Publish', on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField('Author')

# serializer.py
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    # 外键字段使用 _id 结尾
    publish_id = serializers.IntegerField()
    # 多对多使用 ListField
    authors = serializers.ListField()

    def validate_publish_id(self, value):
        # 校验出版社是否存在
        if not Publish.objects.filter(pk=value).exists():
            raise ValidationError('出版社不存在')
        return value

    def create(self, validated_data):
        # validated_data: {"name":"三国演义","price":88,"publish_id":1,"authors":[1,2]}
        authors = validated_data.pop('authors')  # 取出多对多数据
        # 创建图书（一对多关系）
        book = Book.objects.create(**validated_data)
        # 设置作者（多对多关系）
        book.authors.add(*authors)
        return book

# views.py
class BookView(APIView):
    def post(self, request):
        # 前端传入的数据格式：{"name":"三国演义","price":88,"publish_id":1,"authors":[1,2]}
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 100, 'msg': '创建成功'})
        else:
            return Response(serializer.errors)
```

### 10.2 多表关联反序列化 — 修改

```python
# serializer.py
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    publish_id = serializers.IntegerField()
    authors = serializers.ListField()

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        book.authors.add(*authors)
        return book

    def update(self, instance, validated_data):
        # 处理多对多字段（如果有）
        authors = validated_data.pop('authors', None)
        # 更新基础字段
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # 更新多对多关联
        if authors is not None:
            instance.authors.set(authors)
        return instance

# views.py
class BookDetailView(APIView):
    def put(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 100, 'msg': '修改成功'})
        else:
            return Response(serializer.errors)
```

---

## 十一、ModelSerializer

### 11.1 ModelSerializer 简介

`ModelSerializer` 是 `Serializer` 的子类，它能够自动根据模型生成序列化字段，大大减少代码量。

**ModelSerializer 的优势：**
- 自动根据模型字段生成序列化字段
- 自动实现 `create()` 和 `update()` 方法（包含多对多关系处理）
- 通过 `Meta` 类来配置

### 11.2 基本使用

```python
# models.py
class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey('Publish', on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField('Author')

    @property
    def publish_detail(self):
        return {'name': self.publish.name, 'addr': self.publish.addr, 'city': self.publish.city}

    @property
    def author_list(self):
        return [{'name': author.name, 'age': author.age} for author in self.authors.all()]

# serializer.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = '__all__'  # 所有字段
        fields = ['id', 'name', 'price', 'publish', 'authors', 'publish_detail', 'author_list']
        # extra_kwargs 给字段传递额外参数
        extra_kwargs = {
            'publish': {'write_only': True},
            'authors': {'write_only': True},
            'publish_detail': {'read_only': True},
            'author_list': {'read_only': True},
        }
```

### 11.3 extra_kwargs 详解

`extra_kwargs` 用于给 `Meta` 中自动生成的字段传递额外参数。

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'max_length': 10,
                'min_length': 2,
                'required': True,
                'error_messages': {
                    'max_length': '书名不能超过10个字符',
                    'required': '书名不能为空'
                }
            },
            'price': {
                'max_value': 10000,
                'min_value': 0
            },
            'publish': {'write_only': True},
            'authors': {'write_only': True},
        }
```

### 11.4 read_only 与 write_only

```python
# read_only：仅用于序列化输出，反序列化时忽略此字段
# write_only：仅用于反序列化输入，序列化时不输出此字段

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'price', 'publish', 'authors', 'publish_detail']

        extra_kwargs = {
            # 前端新增/修改时需要传入出版社ID（反序列化用）
            'publish': {'write_only': True},
            # 前端新增/修改时需要传入作者ID列表（反序列化用）
            'authors': {'write_only': True},
            # 出版社详情只返回给前端（序列化用）
            'publish_detail': {'read_only': True},
        }
```

### 11.5 ModelSerializer 完整示例

```python
# serializer.py
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # 字段列表：包含序列化字段和反序列化字段
        fields = ['id', 'name', 'price', 'publish', 'authors', 'publish_detail', 'author_all']
        extra_kwargs = {
            'publish': {'write_only': True},
            'authors': {'write_only': True},
            'publish_detail': {'read_only': True},
            'author_all': {'read_only': True},
        }

    # ModelSerializer 同样支持局部钩子和全局钩子
    def validate_name(self, value):
        if 'sb' in value:
            raise ValidationError('书名不能包含敏感词汇')
        return value

    def validate(self, attrs):
        if attrs.get('price') and attrs.get('price') > 10000:
            raise ValidationError('价格不能超过10000')
        return attrs

# views.py
class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(instance=books, many=True)
        return Response({'code': 100, 'msg': '成功', 'results': serializer.data})

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        # raise_exception=True 可以替代 if serializer.is_valid() 判断
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 100, 'msg': '新增成功', 'result': serializer.data})
```

---

## 十二、请求与响应深入

### 12.1 请求解析器（Parser）

DRF 的 Request 对象默认支持三种编码格式：`JSON`、`urlencoded`、`form-data`。可以通过解析器配置来控制支持的编码格式。

```python
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

# 方式一：局部使用（在视图类上配置）
class BookView(APIView):
    parser_classes = [JSONParser]  # 只接受 JSON 格式

# 方式二：全局配置（settings.py）
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# 方式三：局部禁用（覆盖全局配置）
class BookView(APIView):
    parser_classes = [JSONParser]  # 只接受 JSON
```

**解析器使用顺序（优先级）：**
1. 视图类上配置的 `parser_classes`
2. 项目配置文件中 `REST_FRAMEWORK` 的 `DEFAULT_PARSER_CLASSES`
3. DRF 内置默认配置（三种都支持）

### 12.2 响应渲染器（Renderer）

控制响应数据的输出格式（JSON 还是浏览器可浏览的 HTML 页面）。

```python
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

# 局部使用：只返回 JSON（浏览器也不会显示好看页面）
class BookView(APIView):
    renderer_classes = [JSONRenderer]

# 全局配置
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# 局部禁用
class BookView(APIView):
    renderer_classes = [JSONRenderer]
```

---

## 十三、视图层

### 13.1 视图层总览

DRF 提供了多层次的视图类封装，代码量从多到少：

```
APIView                    （最灵活，代码最多）
  |
GenericAPIView              （封装了 queryset 和 serializer_class）
  |
5个视图扩展类（Mixin）       （封装了增删改查方法）
  |
9个视图子类                 （组合了 GenericAPIView + Mixin）
  |
ViewSet/ModelViewSet        （最简洁，路由需映射）
```

### 13.2 APIView

`APIView` 是 DRF 最基础的视图类，继承自 Django 的 `View`。使用它需要手写所有逻辑。

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializer import BookSerializer

class BookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 100, 'msg': '成功', 'result': serializer.data})

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(instance=books, many=True)
        return Response({'code': 100, 'msg': '成功', 'results': serializer.data})

class BookDetailView(APIView):
    def put(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        serializer = BookSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 100, 'msg': '修改成功', 'result': serializer.data})

    def get(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        serializer = BookSerializer(instance=book)
        return Response({'code': 100, 'msg': '成功', 'results': serializer.data})

    def delete(self, request, pk):
        Book.objects.filter(pk=pk).delete()
        return Response({'code': 100, 'msg': '删除成功'})
```

### 13.3 GenericAPIView

`GenericAPIView` 继承自 `APIView`，增加了类属性和辅助方法，减少重复代码。

**核心类属性：**

| 属性/方法 | 说明 |
|----------|------|
| `queryset` | 数据查询集 |
| `serializer_class` | 序列化类 |
| `lookup_field` | 获取单条时的查找字段，默认 'pk' |
| `get_queryset()` | 获取查询集 |
| `get_object()` | 获取单条数据 |
| `get_serializer()` | 获取序列化类实例 |
| `get_serializer_class()` | 获取序列化类（可重写以动态选择） |

```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Book
from .serializer import BookSerializer

class BookView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request):
        # self.get_serializer() 等同于 BookSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 100, 'msg': '成功', 'result': serializer.data})

    def get(self, request):
        # self.get_queryset() 等同于 Book.objects.all()
        books = self.get_queryset()
        serializer = self.get_serializer(instance=books, many=True)
        return Response({'code': 100, 'msg': '成功', 'results': serializer.data})

class BookDetailView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def put(self, request, pk):
        # self.get_object() 根据 pk 自动获取单条数据
        book = self.get_object()
        serializer = self.get_serializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 100, 'msg': '修改成功', 'result': serializer.data})

    def get(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(instance=book)
        return Response({'code': 100, 'msg': '成功', 'results': serializer.data})

    def delete(self, request, pk):
        self.get_object().delete()
        return Response({'code': 100, 'msg': '删除成功'})
```

### 13.4 5个视图扩展类（Mixin）

视图扩展类不是视图类，必须配合 `GenericAPIView` 使用，封装了增删改查的核心逻辑。

| Mixin类 | 方法 | 功能 |
|---------|------|------|
| ListModelMixin | list() | 获取列表 |
| CreateModelMixin | create() | 新增数据 |
| RetrieveModelMixin | retrieve() | 获取单条 |
| UpdateModelMixin | update() | 更新数据 |
| DestroyModelMixin | destroy() | 删除数据 |

```python
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.generics import GenericAPIView

class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

### 13.5 9个视图子类

DRF 将 `GenericAPIView` 与 5 个 Mixin 组合，形成了 9 个可以直接使用的视图子类。

| 视图子类 | 组合 | 支持方法 | 功能 |
|---------|------|---------|------|
| ListAPIView | GenericAPIView + ListModelMixin | GET | 查询所有 |
| CreateAPIView | GenericAPIView + CreateModelMixin | POST | 新增一条 |
| RetrieveAPIView | GenericAPIView + RetrieveModelMixin | GET | 查询单条 |
| UpdateAPIView | GenericAPIView + UpdateModelMixin | PUT/PATCH | 修改一条 |
| DestroyAPIView | GenericAPIView + DestroyModelMixin | DELETE | 删除一条 |
| ListCreateAPIView | +List +Create | GET, POST | 查所有 + 新增 |
| RetrieveUpdateAPIView | +Retrieve +Update | GET, PUT/PATCH | 查单条 + 修改 |
| RetrieveDestroyAPIView | +Retrieve +Destroy | GET, DELETE | 查单条 + 删除 |
| RetrieveUpdateDestroyAPIView | +Retrieve +Update +Destroy | GET, PUT/PATCH, DELETE | 查单条 + 修改 + 删除 |

```python
from rest_framework.generics import (
    ListAPIView, CreateAPIView, ListCreateAPIView,
    RetrieveAPIView, UpdateAPIView, DestroyAPIView,
    RetrieveUpdateDestroyAPIView
)

# 查询所有 + 新增
class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 查询单条 + 修改 + 删除
class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 13.6 ViewSet 视图集

视图集通过路由映射的方式，可以将多个视图逻辑集中在一个类中。

**ViewSet 相关类继承关系：**

```
ViewSetMixin                    （核心：改变路由写法为映射形式）
  |
  +-- ViewSet                   （ViewSetMixin + APIView）
  |
  +-- GenericViewSet            （ViewSetMixin + GenericAPIView）
       |
       +-- ModelViewSet         （GenericViewSet + 5个Mixin，5个接口齐全）
       |
       +-- ReadOnlyModelViewSet （GenericViewSet + ListMixin + RetrieveMixin，只读2个接口）
```

**ModelViewSet 使用：**

```python
from rest_framework.viewsets import ModelViewSet

class BookView(ModelViewSet):
    """
    继承 ModelViewSet 后自动拥有以下5个方法：
    - list()       -> GET    查询所有
    - create()     -> POST   新增
    - retrieve()   -> GET    查询单条
    - update()     -> PUT    修改
    - destroy()    -> DELETE 删除
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 路由（必须使用映射写法）
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('books', BookView, 'books')
urlpatterns += router.urls

# 等价于手动映射：
# path('books/', BookView.as_view({'get': 'list', 'post': 'create'})),
# path('books/<int:pk>/', BookView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
```

**ViewSetMixin 的强大之处：**

```python
from rest_framework.viewsets import ViewSetMixin, ViewSet
from rest_framework.views import APIView

# 方法名可以随意命名，通过路由映射关联
class UserView(ViewSet):
    def login(self, request):
        return Response('login')

    def register(self, request):
        return Response('register')

    def send_sms(self, request):
        return Response('send_sms')

# 路由映射
urlpatterns = [
    path('login/', UserView.as_view({'post': 'login'})),
    path('register/', UserView.as_view({'post': 'register'})),
    path('send_sms/', UserView.as_view({'post': 'send_sms'})),
]
```

### 13.7 视图层总结

```python
# 视图层选择指南

# 1. 只写登录/发送短信等不需要序列化的接口
#    -> 使用 ViewSet (ViewSetMixin + APIView) 或 APIView

# 2. 写完整的5个接口（最少代码）
#    -> 使用 ModelViewSet

# 3. 只写查询所有和查询单条接口（最少代码）
#    -> 使用 ReadOnlyModelViewSet

# 4. 只写5个接口中的部分
#    -> 使用 9个视图子类（如 ListCreateAPIView 等）

# 5. 需要灵活控制（如不同请求使用不同序列化类）
#    -> 使用 GenericAPIView + 5个视图扩展类

# 6. 最大灵活性
#    -> 使用 APIView（最底层）

# self.action 属性
# 在继承 ViewSetMixin 的视图类中，可以通过 self.action 获取当前执行的方法名
# 常用于 get_serializer_class() 中动态选择序列化类

class BookView(ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer    # 列表用简化的序列化类
        elif self.action == 'retrieve':
            return BookDetailSerializer  # 详情用详情的序列化类
        return BookSerializer
```

---

## 十四、路由层

### 14.1 路由写法演进

```python
# 1. 传统写法（APIView/GenericAPIView）
path('books/', BookView.as_view()),
path('books/<int:pk>/', BookDetailView.as_view()),

# 2. ViewSet 映射写法
path('books/', BookView.as_view({'get': 'list', 'post': 'create'})),
path('books/<int:pk>/', BookView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})),

# 3. 自动生成路由（推荐）
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('books', BookView, 'books')
urlpatterns += router.urls
```

### 14.2 自动生成路由

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookView, UserView

# 1. 实例化路由对象
router = SimpleRouter()

# 2. 注册路由
# 参数1：路径前缀
# 参数2：视图类
# 参数3：别名（一般与路径前缀同名）
router.register('books', BookView, 'books')
router.register('users', UserView, 'users')

# 3. 加入总路由
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
# 或者
urlpatterns += router.urls
```

**自动生成的路由规则：**

```
router.register('books', BookView, 'books')
# 自动生成：
# GET    /books/          -> list
# POST   /books/          -> create
# GET    /books/{pk}/     -> retrieve
# PUT    /books/{pk}/     -> update
# DELETE /books/{pk}/     -> destroy
```

### 14.3 action 装饰器

对于视图集中非标准的方法（不是 list/create/retrieve/update/destroy），使用 `@action` 装饰器来声明路由。

```python
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # detail=False：不需要带 pk 的路由  /users/login/
    # methods：支持的请求方式列表
    @action(methods=['POST'], detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # 登录逻辑...
        return Response({'code': 100, 'msg': '登录成功'})

    # detail=True：需要带 pk 的路由  /users/{pk}/set_password/
    @action(methods=['PUT'], detail=True)
    def set_password(self, request, pk):
        user = self.get_object()
        new_password = request.data.get('password')
        user.set_password(new_password)
        user.save()
        return Response({'code': 100, 'msg': '密码修改成功'})
```

**路由注册：**

```python
router.register('users', UserView, 'users')

# 自动生成：
# POST   /users/login/                     -> login
# PUT    /users/{pk}/set_password/          -> set_password
# GET    /users/                            -> list
# POST   /users/                            -> create
# ...其他标准路由
```

---

## 十五、认证组件

### 15.1 认证概述

在 DRF 中，`APIView` 的 `dispatch` 方法在执行视图方法之前会先执行三大认证：认证 -> 权限 -> 频率。

```python
# APIView.dispatch 中的关键代码
def dispatch(self, request, *args, **kwargs):
    request = self.initialize_request(request, *args, **kwargs)
    self.request = request
    try:
        self.initial(request, *args, **kwargs)
        # initial 中执行：
        #   self.perform_authentication(request)   # 认证
        #   self.check_permissions(request)        # 权限
        #   self.check_throttles(request)          # 频率
        # 然后才执行视图方法
        ...
    except Exception as exc:
        response = self.handle_exception(exc)
    ...
```

### 15.2 自定义认证类

```python
# auth.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserToken

class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. 从请求头中取出 token
        token = request.META.get('HTTP_TOKEN')
        # 2. 校验 token
        user_token = UserToken.objects.filter(token=token).first()
        if user_token:
            # 返回两个值：(当前登录用户, token)
            return (user_token.user, token)
        else:
            raise AuthenticationFailed('请您登录后操作')
```

### 15.3 使用认证类

```python
# 方式一：局部使用（视图类配置）
from .auth import LoginAuthentication

class BookView(CreateAPIView):
    authentication_classes = [LoginAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 方式二：全局使用（settings.py 配置）
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'app01.auth.LoginAuthentication'
    ],
}

# 方式三：局部禁用
class UserView(ViewSet):
    authentication_classes = []  # 登录接口不需要认证

    @action(methods=['POST'], detail=False)
    def login(self, request):
        ...
```

### 15.4 认证后的 request.user

认证通过后，`request.user` 就是当前登录用户对象，可以直接在视图中使用。

```python
class BookView(APIView):
    authentication_classes = [LoginAuthentication]

    def post(self, request):
        # 认证通过后，可以获取当前用户
        current_user = request.user
        print(f'当前登录用户: {current_user.username}')
        ...
```

---

## 十六、权限组件

### 16.1 权限概述

权限控制是认证之后执行的，用于判断当前登录用户是否有权限执行当前操作。

### 16.2 自定义权限类

```python
# permission.py
from rest_framework.permissions import BasePermission

class SuperPermission(BasePermission):
    def has_permission(self, request, view):
        # 认证通过后，request.user 就是当前登录用户
        if request.user.user_type == 3:  # 假设 user_type=3 是超级用户
            return True
        else:
            # self.message 用于自定义错误提示
            self.message = f'您不是超级用户，不能操作，您是：【{request.user.get_user_type_display()}】用户'
            return False
```

### 16.3 使用权限类

```python
# 局部使用
class BookView(CreateAPIView):
    permission_classes = [SuperPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 全局使用
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'app01.permission.SuperPermission',
    ],
}

# 局部禁用
class UserView(ViewSet):
    permission_classes = []  # 登录/注册接口不需要权限

# DRF 内置权限类
from rest_framework.permissions import (
    AllowAny,           # 允许所有
    IsAuthenticated,    # 必须登录
    IsAdminUser,        # 管理员
    IsAuthenticatedOrReadOnly,  # 登录用户可写，匿名用户只读
)
```

### 16.4 基于 action 的细粒度权限

```python
class SuperPermission(BasePermission):
    def has_permission(self, request, view):
        # 通过 view.action 判断当前操作
        if view.action in ['list', 'retrieve']:
            # 普通用户可查
            return True
        elif view.action in ['create', 'update', 'destroy']:
            # 超级用户才能增删改
            return request.user.user_type == 3
        return False
```

---

## 十七、频率限制（限流）

### 17.1 频率概述

频率限制用于控制用户对接口的访问频次，防止恶意请求。限制条件可以是：IP地址、用户ID、设备ID等。

### 17.2 使用 SimpleRateThrottle

```python
# throttle.py
from rest_framework.throttling import SimpleRateThrottle

class CommonThrottle(SimpleRateThrottle):
    # rate 格式：'次数/时间'，时间单位：s(秒) m(分钟) h(小时) d(天)
    rate = '3/m'  # 一分钟3次

    def get_cache_key(self, request, view):
        # 返回什么就以什么做限制

        # 方式1：按 IP 限制
        return request.META.get('REMOTE_ADDR')

        # 方式2：按用户 ID 限制（需要登录）
        # return request.user.id

        # 方式3：按 IP + 接口名限制（不同接口不同频次）
        # return f"{request.META.get('REMOTE_ADDR')}_{view.action}"
```

### 17.3 使用频率类

```python
# 局部使用
class BookView(CreateAPIView):
    throttle_classes = [CommonThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 全局使用
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'app01.throttle.CommonThrottle',
    ],
}

# 局部禁用
class UserView(ViewSet):
    throttle_classes = []
```

### 17.4 继承 BaseThrottle 自定义频率类

```python
from rest_framework.throttling import BaseThrottle
import time

class MyThrottle(BaseThrottle):
    # 存储不同 IP 的访问时间列表
    VISIT_RECORD = {}

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        ip = request.META.get('REMOTE_ADDR')
        ctime = time.time()

        # 第一次访问
        if ip not in self.VISIT_RECORD:
            self.VISIT_RECORD[ip] = [ctime]
            return True

        # 清理 60 秒以前的记录
        self.history = self.VISIT_RECORD.get(ip)
        while self.history and ctime - self.history[-1] > 60:
            self.history.pop()

        # 60 秒内小于 5 次则放行
        if len(self.history) < 5:
            self.history.insert(0, ctime)
            return True
        else:
            return False

    def wait(self):
        # 返回还需等待多少秒
        ctime = time.time()
        return 60 - (ctime - self.history[-1])
```

---

## 十八、过滤与排序

过滤和排序仅针对"查询所有"（list）接口。

### 18.1 排序（OrderingFilter）

```python
from rest_framework.filters import OrderingFilter

class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'id']

# 前端请求示例：
# GET /books/?ordering=price        # 按价格升序
# GET /books/?ordering=-price       # 按价格降序
# GET /books/?ordering=price,-id    # 按价格升序，id降序
```

### 18.2 内置搜索过滤（SearchFilter）

```python
from rest_framework.filters import SearchFilter

class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'publish__name']

# GET /books/?search=红   # 搜索名字中包含"红"的图书
```

### 18.3 DjangoFilterBackend 精确过滤

```bash
# 安装
pip install django-filter
```

```python
from django_filters.rest_framework import DjangoFilterBackend

class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'publish', 'price']

# GET /books/?name=红楼梦&publish=1
```

### 18.4 自定义过滤类

```python
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

class CommonFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        price = request.query_params.get('price')

        if name and price:
            # Q 查询：名字包含 name 或价格等于 price
            queryset = queryset.filter(Q(name__contains=name) | Q(price=price))
        elif name:
            queryset = queryset.filter(name__contains=name)
        elif price:
            queryset = queryset.filter(price=price)

        return queryset

# 使用
class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [CommonFilter]

# GET /books/?name=红&price=50
```

### 18.5 组合使用排序和过滤

```python
class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filter_backends 可以配置多个，按顺序依次执行
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['price', 'id']
    search_fields = ['name']
    filterset_fields = ['publish']

# GET /books/?search=红&ordering=-price
# GET /books/?publish=1&ordering=price
```

---

## 十九、分页

分页只针对"查询所有"接口。

### 19.1 三种分页方式

DRF 提供了三种分页方式：

**1. PageNumberPagination（基本分页，最常用）**

```python
from rest_framework.pagination import PageNumberPagination

class CommonPageNumberPagination(PageNumberPagination):
    page_size = 2                  # 每页默认显示 2 条
    page_query_param = 'page'      # 页码查询参数
    page_size_query_param = 'size' # 每页条数查询参数
    max_page_size = 5              # 每页最大条数

# GET /books/?page=2&size=3
```

**2. LimitOffsetPagination（偏移分页）**

```python
from rest_framework.pagination import LimitOffsetPagination

class CommonLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2              # 默认每页 2 条
    limit_query_param = 'limit'    # 每页条数参数
    offset_query_param = 'offset'  # 偏移量参数
    max_limit = 5                  # 最大条数

# GET /books/?limit=10&offset=20
# 从第 20 条开始，取 10 条
```

**3. CursorPagination（游标分页，性能最高）**

```python
from rest_framework.pagination import CursorPagination

class CommonCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'  # 游标参数
    page_size = 2                  # 每页条数
    ordering = 'id'                # 排序字段（必须是数据库字段，用于游标定位）

# GET /books/?cursor=cD0yMDI0LTA4LTAx
# 游标值由服务端返回，前端不能伪造，安全且性能高
```

### 19.2 使用分页

```python
class BookView(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CommonPageNumberPagination  # 配置分页类

# 分页后的响应格式：
# {
#     "count": 100,          // 总条数
#     "next": "...?page=2",  // 下一页链接
#     "previous": null,      // 上一页链接
#     "results": [...]       // 当前页数据
# }
```

---

## 二十、全局异常处理

### 20.1 DRF 异常处理机制

`APIView` 的 `dispatch` 方法中有一个 `try-except`，在三大认证和视图方法执行过程中，如果发生任何异常，都会被捕获并交给 `exception_handler` 函数处理。

**DRF 默认的异常处理函数只处理 DRF 自己的异常（继承自 APIException 的异常），对于 Python 原生的异常不处理。**

### 20.2 自定义全局异常处理函数

```python
# exception.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import (
    ValidationError, AuthenticationFailed, Throttled, APIException
)
import time

def common_exception_handler(exc, context):
    """
    自定义全局异常处理函数
    exc: 异常对象
    context: 上下文对象，包含 request 和 view
    """
    # 区分处理不同类型的异常
    if isinstance(exc, ValidationError):
        # 数据校验异常
        data = {'code': 103, 'msg': exc.detail}
    elif isinstance(exc, AuthenticationFailed):
        # 认证失败
        data = {'code': 104, 'msg': exc.detail}
    elif isinstance(exc, Throttled):
        # 频率限制
        data = {'code': 105, 'msg': exc.detail}
    elif isinstance(exc, IndexError):
        data = {'code': 106, 'msg': '数据越界异常'}
    elif isinstance(exc, ZeroDivisionError):
        data = {'code': 107, 'msg': '除数不能为零'}
    elif isinstance(exc, APIException):
        # 其他 DRF 异常
        data = {'code': 999, 'msg': exc.detail}
    else:
        # 其他 Python 异常
        data = {'code': 888, 'msg': '未知错误，请联系系统管理员'}

    # 记录错误日志
    request = context.get('request')
    view = context.get('view')
    print(f'''
    程序错误：
    错误原因：【{str(exc)}】
    时间：【{time.time()}】
    请求地址：【{request.get_full_path()}】
    请求方式：【{request.method}】
    用户：【{request.user.username if hasattr(request, 'user') else '未登录'}】
    视图类：【{str(view)}】
    ''')

    return Response(data)
```

### 20.3 配置全局异常处理

```python
# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'app01.exception.common_exception_handler',
}

# 配置后，无论什么错误，前端收到的都是统一格式：
# {"code": 103, "msg": "..."}
```

---

## 二十一、接口文档生成

### 21.1 接口文档实现方式

| 方式 | 说明 |
|------|------|
| Word/Markdown | 手动编写，放在公共平台 |
| ShowDoc | 第三方付费平台 |
| YAPI | 百度开源，支持搭建私有平台 |
| Swagger | 行业标准，FastAPI 自带支持 |
| 自动生成 | DRF + drf-spectacular / drf-yasg 等第三方库 |

> ⚠️ 早期教程常用的 `coreapi` 已于 DRF 3.12+ 被官方弃用，新项目请改用 [`drf-spectacular`](https://drf-spectacular.readthedocs.io)（OpenAPI 3 规范）或 [`drf-yasg`](https://drf-yasg.readthedocs.io)。

### 21.2 使用 coreapi 自动生成

```bash
# 安装
pip install coreapi
```

```python
# urls.py
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('docs/', include_docs_urls(title='项目接口文档')),
]
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```

```python
# views.py - 在视图类中添加注释
class BookView(ModelViewSet):
    """
    list:
    获取所有图书信息

    create:
    新增一本图书
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

```python
# serializer.py - 通过字段参数控制文档显示
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'required': True,       # 必填
                'help_text': '图书名称'  # 字段说明
            },
            'price': {
                'help_text': '图书价格',
                'min_value': 0
            }
        }
```

访问 `http://127.0.0.1:8000/docs/` 即可查看自动生成的接口文档。

---

## 二十二、JWT认证

### 22.1 JWT 是什么

JWT（JSON Web Token）是一种用于前后端分离项目中的登录认证方案。与传统的 Session 方案不同，JWT 不需要在服务端存储用户登录信息。

### 22.2 JWT 原理

**JWT Token 结构（三段式）：**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
       ↑ 头部（Header）           ↑ 荷载（Payload）                        ↑ 签名（Signature）
```

**签发阶段（登录时）：**
1. 生成头部：`{"alg":"HS256","typ":"JWT"}` -> Base64 编码
2. 生成荷载：`{"user_id":1,"name":"张三","exp":过期时间戳}` -> Base64 编码
3. 生成签名：`HMAC-SHA256(头部编码.荷载编码, 密钥)` -> Base64 编码
4. 拼接：`头部.荷载.签名` 即为 Token

**认证阶段（访问接口时）：**
1. 前端在请求头中携带 Token
2. 后端取出前两段，使用同样的算法和密钥重新签名
3. 比较新签名与 Token 的第三段是否一致
4. 一致则认证通过，不一致则 Token 被篡改

### 22.3 Base64 编码

```python
import base64
import json

# 编码
user_dic = {'name': 'lqz', 'age': 19, 'user_id': 99}
user_str = json.dumps(user_dic)
encoded = base64.b64encode(user_str.encode('utf-8'))
print(encoded)  # b'eyJuYW1lIjogImxxeiIsICJhZ2UiOiAxOSwgInVzZXJfaWQiOiA5OX0='

# 解码
decoded = base64.b64decode(encoded)
print(json.loads(decoded))  # {'name': 'lqz', 'age': 19, 'user_id': 99}

# Base64 特点：
# 1. 长度必须是4的倍数，不足用 = 补齐
# 2. = 不表示数据，只是占位符
# 3. Base64 不是加密，只是编码
```

### 22.4 使用 djangorestframework-simplejwt

```bash
pip install djangorestframework-simplejwt
```

**快速使用（基于 auth 的 User 表）：**

```python
# urls.py - 签发 token（登录）
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

urlpatterns = [
    path('login/', token_obtain_pair),   # 登录接口，返回 access 和 refresh
    path('refresh/', token_refresh),     # 刷新 access token
]

# views.py - 认证
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated

class BookView(APIView):
    # simple-jwt 提供的认证类 + 权限类
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 认证通过后，request.user 为当前用户
        return Response({'msg': 'success', 'user': request.user.username})
```

**前端携带 Token（请求头格式）：**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 22.5 双 Token 认证

双 Token 是为了解决 Token 泄露风险：

- **Access Token**：有效期短（如 5 分钟），用于访问受保护接口
- **Refresh Token**：有效期长（如 7 天），用于刷新 Access Token

```python
# settings.py 配置
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),   # Access Token 5分钟
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh Token 7天
}
```

### 22.6 定制登录返回格式

```python
# serializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 调用父类获取原始的 access 和 refresh
        data = super().validate(attrs)
        access = data.get('access')
        refresh = data.get('refresh')
        user = self.user
        # 自定义返回格式
        return {
            'code': 100,
            'msg': '登录成功',
            'username': user.username,
            'access': access,
            'refresh': refresh
        }

# settings.py 配置
SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "app01.serializer.MyTokenObtainPairSerializer",
}
```

### 22.7 定制令牌荷载

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 在荷载中添加自定义字段
        token['name'] = user.username
        token['email'] = user.email
        token['user_type'] = user.user_type
        return token
```

### 22.8 多方式登录

支持用户名+密码、手机号+密码、邮箱+密码等多种登录方式。

**前端传入格式：**

```json
{
    "username": "18912345678 或 zhangsan 或 zhangsan@qq.com",
    "password": "123456"
}
```

**序列化类实现：**

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
import re
from .models import UserInfo

class LoginSerializer(serializers.ModelSerializer):
    # 重写 username 字段，去除 unique 校验
    username = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # 正则匹配判断登录方式
        if re.match(r'^1[3-9][0-9]{9}$', username):
            user = UserInfo.objects.filter(mobile=username).first()
        elif re.match(r'^.+@.+$', username):
            user = UserInfo.objects.filter(email=username).first()
        else:
            user = UserInfo.objects.filter(username=username).first()

        # 校验密码
        if user and user.check_password(password):
            # 签发 Token
            refresh = RefreshToken.for_user(user)
            self.context['refresh'] = str(refresh)
            self.context['access'] = str(refresh.access_token)
        else:
            raise ValidationError('用户名或密码错误')

        return attrs

# 视图类
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.context.get('refresh')
        access = serializer.context.get('access')
        return Response({
            'code': 100,
            'msg': '登录成功',
            'refresh': refresh,
            'access': access
        })
```

### 22.9 自定义用户表签发与认证

```python
# serializer.py - 签发
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class MyLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # ⚠️ 演示用：下面是错误示例，明文匹配密码字段假设数据库存的就是明文
        # 生产中数据库应只存密码哈希，校验须改为：
        #   user = User.objects.filter(username=username).first()
        #   if not user or not user.check_password(password):
        #       raise serializers.ValidationError('用户名密码错误')
        user = User.objects.filter(username=username, password=password).first()
        if not user:
            raise serializers.ValidationError('用户名密码错误')

        # 签发 Token
        refresh = RefreshToken.for_user(user)
        self.context['refresh'] = str(refresh)
        self.context['access'] = str(refresh.access_token)
        return attrs

# auth.py - 认证
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

class CustomLoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[-1]
            try:
                validate_token = AccessToken(token)
                user = User.objects.filter(pk=validate_token.get('user_id')).first()
                return (user, token)
            except TokenError as e:
                raise AuthenticationFailed(str(e))
        else:
            raise AuthenticationFailed('Token未携带或格式不合法')

# 使用
class BookView(APIView):
    authentication_classes = [CustomLoginAuthentication]
```

### 22.10 JWT 配置项汇总

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # Access Token 有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Refresh Token 有效期
    'ROTATE_REFRESH_TOKENS': False,                    # 刷新时是否轮换 Refresh Token
    'BLACKLIST_AFTER_ROTATION': False,                 # 轮换时是否将旧 Token 加入黑名单
    'ALGORITHM': 'HS256',                              # 签名算法
    'SIGNING_KEY': None,                               # 签名密钥（默认使用 SECRET_KEY）
    'AUTH_HEADER_TYPES': ('Bearer',),                  # 请求头中认证类型
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',           # 请求头名称
    'USER_ID_FIELD': 'id',                             # 用户 ID 字段
    'USER_ID_CLAIM': 'user_id',                        # 荷载中用户 ID 键名
}
```

---

## 二十三、权限控制模型 (ACL/RBAC)

### 23.1 权限控制分类

**1. ACL（Access Control List）访问控制列表**

用户和权限直接建立多对多关系：

```
用户表              权限表              用户-权限中间表
id  name            id  权限名          id  user_id  perm_id
1   张三            1   开直播          1    1        1
2   李四            2   评论            2    1        2
                    3   发视频          3    2        1
                    4   打赏
```

**2. RBAC（Role-Based Access Control）基于角色的访问控制**

用户与角色关联，角色与权限关联：

```
用户 <--多对多--> 角色 <--多对多--> 权限

用户表          角色表          权限表
id  name        id  name        id  权限名
1   张三        1   总裁        1   开总裁会
2   李四        2   HR         2   开发代码
3   王五        3   开发        3   删除代码
                             4   发工资
```

**3. Django Admin 的权限模型（RBAC + ACL）**

Django 后台管理使用了 6 张表：

- auth_user（用户表）
- auth_group（组/角色表）
- auth_permission（权限表）
- auth_user_groups（用户-组中间表）
- auth_group_permissions（组-权限中间表）
- auth_user_user_permissions（用户-权限中间表）

这实现了 RBAC 权限控制，同时支持直接给用户分配权限（ACL），实现更细粒度的权限控制。

---

## 二十四、源码分析

### 24.1 APIView 执行流程

```python
# rest_framework/views.py
class APIView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs
        # 去除 CSRF 认证
        return csrf_exempt(view)

    def dispatch(self, request, *args, **kwargs):
        # 1. 包装新的 Request 对象
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request

        try:
            # 2. 执行三大认证（认证、权限、频率）
            self.initial(request, *args, **kwargs)

            # 3. 通过反射执行与请求方式同名的方法
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)

        except Exception as exc:
            # 4. 全局异常处理
            response = self.handle_exception(exc)

        # 5. 最终处理响应
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
```

**总结：**
- 继承 APIView 后，request 变成新的 DRF Request 对象
- 视图类对象中可以通过 `self.request` 获取当前请求
- 在执行视图方法之前，依次执行了认证、权限、频率
- 三大认证和视图方法中的异常都会被统一捕获处理
- 自动去除 CSRF 认证

### 24.2 序列化器 many=True 源码

```python
# rest_framework/serializers.py
class BaseSerializer:
    def __new__(cls, *args, **kwargs):
        # many=True 时走 many_init，否则正常创建对象
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def many_init(cls, *args, **kwargs):
        # 创建 ListSerializer 对象
        list_kwargs = {'child': cls(*args, **kwargs)}
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        return list_serializer_class(*args, **list_kwargs)

# 当 many=True 时，实际返回的是 ListSerializer 对象
# ListSerializer 内部包含多个子序列化器对象
# serializer.data 遍历所有子序列化器获取数据
```

### 24.3 序列化器校验源码

```python
# Serializer 类
def is_valid(self, raise_exception=False):
    if not hasattr(self, '_validated_data'):
        try:
            self._validated_data = self.run_validation(self.initial_data)
        except ValidationError as exc:
            self._validated_data = {}
            self._errors = exc.detail
        else:
            self._errors = {}
    return not bool(self._errors)

def run_validation(self, data=empty):
    (is_empty_value, data) = self.validate_empty_values(data)
    if is_empty_value:
        return data
    # 1. 执行字段校验和局部钩子
    value = self.to_internal_value(data)
    # 2. 执行全局钩子
    value = self.validate(value)
    return value

def to_internal_value(self, data):
    # 遍历所有字段
    for field in fields:
        # 反射查找 validate_字段名（局部钩子）
        validate_method = getattr(self, 'validate_' + field.field_name, None)
        # 执行字段自身校验
        validated_value = field.run_validation(primitive_value)
        # 如果存在局部钩子，执行它
        if validate_method is not None:
            validated_value = validate_method(validated_value)
    return ret
```

### 24.4 GenericAPIView 核心方法源码

```python
class GenericAPIView(APIView):
    queryset = None
    serializer_class = None
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class
```

---

## 二十五、版本控制

### 25.1 版本控制概述

在实际项目开发中，API 接口会不断迭代升级。版本控制用于管理不同版本的 API，确保老版本客户端不受新版本变更的影响。

常见的版本控制策略：

| 策略 | 示例 | 说明 |
|------|------|------|
| URL 路径 | `/api/v1/books/` | 最常用，直观 |
| 查询参数 | `/api/books/?version=1` | 简单但不 RESTful |
| 请求头 | `Accept: application/json; version=1` | 对 URL 无侵入 |
| 子域名 | `v1.api.example.com` | 适用于大型项目 |

### 25.2 DRF 中的版本控制

DRF 提供了内置的版本控制方案，通过配置 `DEFAULT_VERSIONING_CLASS` 来启用。

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',               # 默认版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],      # 允许的版本
    'VERSION_PARAM': 'version',            # 版本参数名
}
```

### 25.3 URL 路径版本控制（最常用）

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# urls.py
urlpatterns = [
    path('api/<str:version>/books/', BookView.as_view()),
]

# views.py
class BookView(APIView):
    def get(self, request, version):
        # request.version 可以获取当前请求的版本号
        print(f'当前API版本: {request.version}')
        if request.version == 'v1':
            # v1 版本逻辑
            books = Book.objects.all()
            serializer = BookSerializerV1(instance=books, many=True)
        elif request.version == 'v2':
            # v2 版本逻辑（可能返回更多字段）
            books = Book.objects.all()
            serializer = BookSerializerV2(instance=books, many=True)
        return Response(serializer.data)
```

### 25.4 其他版本控制方式

```python
# 方式1：查询参数版本控制
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'VERSION_PARAM': 'version',  # /api/books/?version=v1
}

# 方式2：请求头版本控制
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    # 请求头：Accept: application/json; version=1.0
}

# 方式3：命名空间版本控制
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}
# urls.py
urlpatterns = [
    path('v1/', include(('app01.urls', 'app01'), namespace='v1')),
    path('v2/', include(('app01.urls', 'app01'), namespace='v2')),
]
```

### 25.5 在视图中使用版本信息

```python
class BookView(APIView):
    def get(self, request, *args, **kwargs):
        # request.version：版本号字符串，如 'v1'
        # request.versioning_scheme：当前使用的版本控制类实例
        version = request.version
        return Response({'version': version})
```

---

## 二十六、实用设计模式与最佳实践

### 26.1 统一返回格式设计

在实际项目中，建议统一所有接口的返回格式，方便前端统一处理。

```python
# utils/response.py
from rest_framework.response import Response

class APIResponse(Response):
    """统一API响应格式"""
    def __init__(self, code=100, msg='成功', result=None, status=200,
                 headers=None, **kwargs):
        data = {
            'code': code,
            'msg': msg,
        }
        if result is not None:
            data['result'] = result if 'many' not in kwargs else kwargs.pop('many')
        data.update(kwargs)
        super().__init__(data=data, status=status, headers=headers)

# 使用示例
class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(instance=books, many=True)
        return APIResponse(msg='获取成功', result=serializer.data)
        # 返回：{"code":100,"msg":"获取成功","result":[...]}

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(msg='创建成功', result=serializer.data, status=201)
```

### 26.2 混合使用 Serializer 和 ModelSerializer

```python
# 序列化类可以混用，部分字段用 Serializer 方式定义，其余由 Meta 自动生成
class BookSerializer(serializers.ModelSerializer):
    # 自定义字段（不在 Meta 的 fields 中自动生成）
    publish_detail = serializers.SerializerMethodField()
    author_list = serializers.SerializerMethodField()

    # 重写模型字段以覆盖默认行为
    name = serializers.CharField(max_length=10, error_messages={
        'max_length': '书名不能超过10个字符'
    })

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'publish', 'authors', 'publish_detail', 'author_list']
        extra_kwargs = {
            'publish': {'write_only': True},
            'authors': {'write_only': True},
        }

    def get_publish_detail(self, obj):
        return {
            'id': obj.publish.id,
            'name': obj.publish.name,
            'city': obj.publish.city
        }

    def get_author_list(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data

    def validate_name(self, value):
        if 'sb' in value.lower():
            raise serializers.ValidationError('书名包含敏感词汇')
        return value
```

### 26.3 不同请求方式使用不同序列化类

```python
class BookView(GenericAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        """
        根据请求方式动态选择序列化类：
        - GET 请求：使用包含详情的序列化类
        - POST/PUT 请求：使用简洁的反序列化类
        """
        if self.request.method == 'GET':
            return BookDetailSerializer      # 返回字段多，包含关联对象详情
        return BookWriteSerializer           # 只返回必要字段，用于创建/修改

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

### 26.4 密码加密保存

当自定义用户表使用明文密码时需要手动处理密码加密。

```python
# models.py
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        # 如果密码被修改过，则重新加密
        if self._state.adding or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

# serializer.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, validated_data):
        # 使用 make_password 加密密码
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# 登录认证
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(username=username).first()
        # 使用 check_password 验证密码
        if user and check_password(password, user.password):
            self.context['user'] = user
            return attrs
        raise serializers.ValidationError('用户名或密码错误')
```

### 26.5 QueryDict 常用操作

```python
from django.http import QueryDict

# QueryDict 是 Django 处理 URL 编码数据的特殊字典类
# 一个 key 可以对应多个 value

# 创建 QueryDict
qd = QueryDict('name=lqz&age=19&hobby=篮球&hobby=足球')

# 获取单个值
print(qd.get('name'))        # 'lqz'
print(qd['age'])             # '19'

# 获取多个值
print(qd.getlist('hobby'))   # ['篮球', '足球']

# 修改（QueryDict 默认不可变，需要先复制）
qd = qd.copy()
qd['name'] = 'new_name'

# 添加
qd.appendlist('hobby', '乒乓球')

# URL 编码
print(qd.urlencode())        # 'name=new_name&age=19&hobby=篮球&hobby=足球&hobby=乒乓球'
```

### 26.6 断言（assert）在 DRF 中的应用

DRF 源码中大量使用断言来确保执行顺序和条件正确。

```python
# DRF 源码中的断言示例
class BaseSerializer:
    def save(self, **kwargs):
        # 必须调用 is_valid() 后才能调用 save()
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )
        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )
        ...

# 在项目中使用断言
class BookSerializer(serializers.Serializer):
    def validate_price(self, value):
        # 确保价格是正数
        assert value >= 0, '价格不能为负数'
        return value

# 特别注意：断言在 Python 优化模式（-O 参数）下会被跳过
# 因此不要用断言做业务逻辑校验，只用于开发阶段的约定检查
```

### 26.7 CBV 请求方式分发原理

```python
# Django View 基类的 dispatch 原理
class View:
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    @classonlymethod
    def as_view(cls, **initkwargs):
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            return self.dispatch(request, *args, **kwargs)
        return view

    def dispatch(self, request, *args, **kwargs):
        # 如果请求方式在允许列表中
        if request.method.lower() in self.http_method_names:
            # 通过反射找到同名方法
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

# 所以 CBV 的路由写法：
# path('books/', BookView.as_view())
# 当 GET 请求匹配成功时 -> BookView.as_view()(request) -> dispatch -> get(request)
# 当 POST 请求匹配成功时 -> BookView.as_view()(request) -> dispatch -> post(request)
```

---

## 附录：常用命令速查

```bash
# 安装
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install coreapi

# 创建 Django 项目
django-admin startproject project_name
cd project_name
python manage.py startapp app01

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 运行项目
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

---

## 附录：DRF 配置项汇总

```python
# settings.py
REST_FRAMEWORK = {
    # 解析器
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # 渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 权限
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 频率
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    # 分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 过滤
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # 全局异常
    'EXCEPTION_HANDLER': 'app01.exception.common_exception_handler',
    # 接口文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```

---

本文档涵盖了 Django REST Framework 从入门到精通的核心内容，包括前后端开发模式、RESTful 规范、序列化器、视图层、路由层、三大认证（认证/权限/频率）、过滤排序、分页、全局异常处理、接口文档和 JWT 认证。掌握这些内容后，您将能够高效构建符合 RESTful 规范的 Web API。
