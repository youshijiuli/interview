## 6 Django 读写分离实现

### Q31: Django 如何实现读写分离？

**答：** Django 通过多数据库配置和自定义数据库路由（DBRouter）实现读写分离。

**1. 配置多数据库（settings.py）：**
```python
DATABASES = {
    'default': {  # 写库（Master）
        'ENGINE': '14.django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.100',
        'PORT': 3306,
    },
    'slave': {  # 读库（Slave）
        'ENGINE': '14.django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.101',
        'PORT': 3306,
    },
}
```

**2. 自定义数据库路由（router.py）：**
```python
class DBRouter:
    """数据库读写分离路由"""

    def db_for_read(self, model, **hints):
        """读操作走 slave"""
        return 'slave'

    def db_for_write(self, model, **hints):
        """写操作走 default（Master）"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """允许同一个库的表之间建关联"""
        db_set = {'default', 'slave'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """只允许在 default 库上做迁移"""
        return db == 'default'
```

**3. 注册路由（settings.py）：**
```python
DATABASE_ROUTERS = ['myapp.router.DBRouter']
```

**4. 手动指定库（特殊场景）：**
```python
# 强制读 Master（刚写完就要读的场景，避免主从延迟）
User.objects.using('default').get(id=1)

# 保存时也可以指定
user.save(using='default')

# 事务中的操作自动走 default
with transaction.atomic():
    user.save()
```

---

### Q32: Django 如何使用多个 Redis？

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'password',
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'password',
        }
    },
    'celery': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/3',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'password',
        }
    },
}

# 使用指定 Redis
from django.core.cache import caches

caches['default'].set('key', 'value')
caches['session'].set('session_key', 'session_data')
caches['celery'].get('task_result')
```

---

---

## 14 Django 面试题补充

### Q66: Django 的请求生命周期？

**答：** Django 处理请求的完整流程：

```
1. 用户请求 → 浏览器发起 HTTP 请求
2. WSGI 服务器接收（如 uWSGI/Gunicorn）
3. 中间件处理（Middleware，process_request 正向）
4. URL 路由匹配（URLconf，找到对应 View）
5. 视图处理（View）：
   - 接收请求参数
   - 调用 Model 操作数据库
   - 渲染 Template 或返回 JSON
6. 中间件处理（process_response 反向）
7. 返回 HTTP 响应给客户端
```

**详细流程：**
```
请求 → WSGIHandler → 加载 settings.py
    → 中间件链（request 方向）
    → URL 解析 → 视图函数/类
    → 中间件链（response 方向）
    → HTTP Response
```

---

### Q67: Django ORM 中 select_related 和 prefetch_related 的区别？

**答：**

| 对比 | select_related | prefetch_related |
|------|---------------|-----------------|
| 查询方式 | JOIN 联表查询（1 次 SQL） | 分开查询（2 次 SQL），Python 层面拼接 |
| 适用关系 | 一对一、外键（正向） | 多对多、反向外键 |
| SQL 数量 | 1 | 1 + 1 |
| 性能 | 大数据 JOIN 性能差 | 大数据时比 JOIN 好 |

```python
# select_related（正向 ForeignKey）
# SQL: SELECT * FROM course INNER JOIN teacher ON ...
courses = Course.objects.select_related('teacher').all()
for c in courses:
    print(c.teacher.name)  # 不再额外查询数据库

# prefetch_related（多对多/反向外键）
# SQL1: SELECT * FROM course
# SQL2: SELECT * FROM chapter WHERE course_id IN (1,2,3,...)
courses = Course.objects.prefetch_related('chapters').all()
for c in courses:
    for ch in c.chapters.all():  # 不额外查询
        print(ch.name)
```

---

### Q68: F 对象和 Q 对象是什么？

```python
from django.db.models import F, Q

# F 对象：引用数据库中的字段值（避免竞争条件）
# 不安全的写法（有并发问题）
product = Product.objects.get(id=1)
product.stock += 1
product.save()

# 使用 F 对象（数据库层面原子操作）
Product.objects.filter(id=1).update(stock=F('stock') + 1)

# Q 对象：构建复杂的查询条件（OR、NOT）
# AND 查询
Product.objects.filter(name__icontains='Python', price__lt=100)

# OR 查询
Product.objects.filter(
    Q(name__icontains='Python') | Q(description__icontains='Python')
)

# NOT 查询
Product.objects.filter(~Q(price=0))  # 价格不为 0

# 混合使用
Product.objects.filter(
    Q(name__icontains='Python') | Q(name__icontains='Django'),
    is_deleted=False,  # AND 条件
    price__gt=0,
)
```

---

### Q69: CBV 和 FBV 的区别与选择？

| 对比 | FBV（Function-Based View） | CBV（Class-Based View） |
|------|---------------------------|------------------------|
| 定义方式 | 函数 | 类 |
| 代码复用 | 通过装饰器 | 通过继承 Mixin |
| 适用场景 | 简单逻辑 | 复杂逻辑、CRUD 操作 |
| 灵活性 | 高 | 较高（但需要理解继承链） |

```python
# FBV 方式
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        data = CourseSerializer(courses, many=True).data
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# CBV 方式（DRF）
class CourseListAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
```

**CBV 的执行流程：**
```
as_view() → view() → dispatch() → get()/post()/put()/delete()
```

---

### Q70: Django 中间件如何自定义？

```python
# middlewares.py
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ① 请求到达 view 之前
        print('请求到达前')

        response = self.get_response(request)

        # ② view 处理完毕后，返回响应前
        print('响应返回前')

        return response

# 也支持 process_view、process_exception、process_template_response 等钩子

# settings.py
MIDDLEWARE = [
    'myapp.middlewares.CustomMiddleware',
    ...
]
```

---
