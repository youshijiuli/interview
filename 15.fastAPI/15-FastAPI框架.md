# FastAPI 框架快速入门

## 目录

1. [FastAPI 介绍与安装](#1-fastapi-介绍与安装)
2. [第一个 FastAPI 应用](#2-第一个-fastapi-应用)
3. [路由与请求方法](#3-路由与请求方法)
4. [路径参数与查询参数](#4-路径参数与查询参数)
5. [请求体（Pydantic 模型）](#5-请求体pydantic-模型)
6. [响应模型](#6-响应模型)
7. [自动 API 文档（Swagger/ReDoc）](#7-自动-api-文档swaggerredoc)
8. [依赖注入](#8-依赖注入)
9. [数据库操作（SQLAlchemy 异步）](#9-数据库操作sqlalchemy-异步)
10. [认证与授权（OAuth2、JWT）](#10-认证与授权oauth2jwt)
11. [中间件与 CORS](#11-中间件与-cors)
12. [后台任务](#12-后台任务)
13. [WebSocket 支持](#13-websocket-支持)
14. [项目上线部署](#14-项目上线部署)

---

## 1. FastAPI 介绍与安装

### 1.1 FastAPI 简介

FastAPI 是一个用于构建 API 的现代、高性能 Web 框架，基于 Python 3.8+ 的类型提示，遵循 OpenAPI 和 JSON Schema 标准。

**核心特性：**

- **极高性能**：与 NodeJS 和 Go 相当的并发性能（基于 Starlette 和 Pydantic）
- **高效编码**：开发效率提升 200%~300%
- **更少 Bug**：减少约 40% 的人为错误
- **智能提示**：处处自动补全，减少调试时间
- **自动文档**：自动生成交互式 Swagger UI 和 ReDoc 文档
- **标准化**：完全兼容 OpenAPI 和 JSON Schema

**技术架构：**

| 层级 | 组件 | 说明 |
|------|------|------|
| Web 框架 | FastAPI | 整合 Starlette + Pydantic |
| Web 工具包 | Starlette | 轻量级 ASGI 框架/工具包 |
| 数据验证 | Pydantic | Python 数据验证库，基于类型注解 |
| ASGI 服务器 | Uvicorn / Hypercorn | 异步 Web 服务器 |

### 1.2 WSGI 与 ASGI

```python
# WSGI (Web Server Gateway Interface)
# - 同步接口标准，适用于 Flask、Django（旧版）
# - 基于 HTTP 协议，不支持 WebSocket
# - Web 服务器：uWSGI、Gunicorn

# ASGI (Asynchronous Server Gateway Interface)
# - 异步接口标准，适用于 FastAPI、Starlette、Sanic
# - 支持 HTTP、HTTP2、WebSocket 等协议
# - Web 服务器：Uvicorn、Daphne、Hypercorn

# 对比：
# Flask    : Werkzeug (WSGI 工具包) + uWSGI/Gunicorn (WSGI 服务器)
# FastAPI  : Starlette (ASGI 工具包) + Uvicorn/Daphne (ASGI 服务器)
```

### 1.3 安装

```bash
# Python 3.8+，推荐 3.11 及以上

# 安装 FastAPI
pip install fastapi

# 安装 ASGI 服务器
pip install uvicorn

# 完整安装（含所有可选依赖）
pip install "fastapi[all]"
```

### 1.4 Pydantic 简介

Pydantic 是 Python 使用最广泛的数据验证库，FastAPI 用它来做请求体的自动校验和序列化：

```python
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: int
    name: str = '默认用户名'
    signup_ts: datetime | None = None
    tastes: dict[str, PositiveInt]  # key为字符串，value为正整数


# 校验成功
external_data = {
    'id': 123,
    'signup_ts': '2026-06-01 12:22',
    'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
user = User(**external_data)
print(user.id)                    # 123
print(user.model_dump())          # 导出为字典


# 校验失败示例
try:
    User(**{'id': 'not_number', 'tastes': {}})
except ValidationError as e:
    print(e.errors())  # 输出详细错误信息


# 更多类型示例
from typing import Annotated, Dict, List, Literal, Tuple
from annotated_types import Gt


class Fruit(BaseModel):
    name: str
    color: Literal['red', 'green']               # 枚举类型
    weight: Annotated[float, Gt(0)]               # 必须大于0
    bazam: Dict[str, List[Tuple[int, bool, float]]]  # 复杂嵌套类型


fruit = Fruit(name='Apple', color='red', weight=1.1,
              bazam={'foobar': [(1, True, 0.1)]})
```

---

## 2. 第一个 FastAPI 应用

### 2.1 最小应用

```python
from fastapi import FastAPI

# 创建 FastAPI 实例
app = FastAPI()


@app.get("/")
def read_root():
    """同步视图函数"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """异步视图函数，支持路径参数和查询参数"""
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
```

### 2.2 运行方式

```bash
# 方式一：命令行启动
# uvicorn main:app --reload --host 0.0.0.0 --port 8080

# 命令说明：
# main       : main.py 文件（Python 模块）
# app        : FastAPI() 实例对象名
# --reload   : 代码变更时自动重启（仅开发环境）
# --host     : 监听地址
# --port     : 监听端口

# 方式二：代码中启动
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
```

### 2.3 同步与异步的选择

FastAPI 同时支持同步和异步视图函数，但两者的执行方式有本质区别：

```python
import asyncio
import time
from fastapi import FastAPI

app = FastAPI()


# 同步视图函数 -- Uvicorn 会在线程池中运行，支持并发
@app.get('/sync')
def sync_view():
    time.sleep(3)  # 同步 IO
    return {'msg': '同步视图'}


# 异步 + 同步 IO -- 最差的选择！会阻塞整个事件循环
@app.get('/async_bad')
async def async_bad_view():
    time.sleep(3)  # 同步 IO 在异步函数中会阻塞！
    return {'msg': '不推荐'}


# 异步 + 异步 IO -- 最佳实践
@app.get('/async_good')
async def async_good_view():
    await asyncio.sleep(3)  # 异步 IO
    return {'msg': '推荐写法'}


# 总结：
# 1. 同步视图 + 同步IO  -> 在线程池中运行，支持并发（性能好）
# 2. 异步视图 + 同步IO  -> 阻塞事件循环，效率最低（禁止使用）
# 3. 异步视图 + 异步IO  -> 单线程协程并发，效率最高（推荐）
```

**异步生态替换表：**

| 同步库 | 异步替代库 | 用途 |
|--------|-----------|------|
| `requests` | `httpx` / `aiohttp` | HTTP 客户端 |
| `pymysql` | `aiomysql` | MySQL 数据库 |
| `redis-py` | `aioredis` / `redis.asyncio` | Redis 操作 |
| `time.sleep` | `asyncio.sleep` | 延时等待 |

```python
# 异步 HTTP 请求示例
import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get('/fetch')
async def fetch_external():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/data')
        return response.json()
```

---

## 3. 路由与请求方法

### 3.1 路由装饰器

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
def get_items():
    return {"method": "GET"}


@app.post("/items")
def create_item():
    return {"method": "POST"}


@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"method": "PUT", "item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"method": "DELETE", "item_id": item_id}


@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"method": "PATCH", "item_id": item_id}


@app.options("/items")
def options_items():
    return {"method": "OPTIONS"}


@app.head("/items")
def head_items():
    return {"method": "HEAD"}


# 自定义多个请求方法
@app.api_route("/custom", methods=["GET", "POST", "DELETE"])
def custom_handler():
    return {"msg": "支持多种请求方法"}
```

### 3.2 路由分组（APIRouter）

FastAPI 使用 `APIRouter` 进行路由分发，类似于 Flask 的 Blueprint：

```python
# ========== routers/users.py ==========
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_users():
    return {"users": ["Alice", "Bob", "Charlie"]}


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": f"用户{user_id}"}


@router.post("/")
async def create_user(name: str):
    return {"msg": f"用户 {name} 已创建"}


# ========== routers/orders.py ==========
from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["订单管理"])


@router.get("/")
async def list_orders():
    return {"orders": []}


@router.get("/{order_id}")
async def get_order(order_id: int):
    return {"order_id": order_id}
```

```python
# ========== main.py ==========
from fastapi import FastAPI
from routers import users, orders

app = FastAPI()

# 注册路由
app.include_router(users.router, prefix="/api/v1/users", tags=["用户管理"])
app.include_router(orders.router, prefix="/api/v1")  # 使用路由器自带的 prefix

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
```

### 3.3 大项目目录结构

```
project/
├── main.py                 # 应用入口
├── config/
│   ├── __init__.py
│   └── settings.py         # 配置信息
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── users.py        # 用户相关路由
│       ├── orders.py       # 订单相关路由
│       └── products.py     # 产品相关路由
├── models/
│   ├── __init__.py
│   ├── user.py             # 用户模型
│   └── order.py            # 订单模型
├── schemas/
│   ├── __init__.py
│   ├── user.py             # 请求/响应 Pydantic 模型
│   └── order.py
├── services/
│   ├── __init__.py
│   ├── user_service.py     # 业务逻辑层
│   └── order_service.py
├── core/
│   ├── __init__.py
│   ├── security.py         # 认证授权
│   └── dependencies.py     # 公共依赖
├── .env                    # 环境变量
└── requirements.txt
```

---

## 4. 路径参数与查询参数

### 4.1 路径参数

```python
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


# 基本路径参数
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}


# 路径参数类型转换（自动校验）
@app.get("/articles/{article_id}")
async def get_article(article_id: int):  # 自动将字符串转为 int
    return {"article_id": article_id, "type": type(article_id)}


# 枚举类型路径参数
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN"}

    return {"model_name": model_name, "message": "Have some residuals"}


# 路径转换器（含斜杠的文件路径）
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    # 匹配 /files/home/user/myfile.txt
    return {"file_path": file_path}
```

### 4.2 查询参数

```python
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

# 模拟数据
items_db = [{"name": f"Item {i}"} for i in range(100)]


# 基本查询参数（不在路径中的参数自动成为查询参数）
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """skip 和 limit 都是查询参数：/items/?skip=0&limit=10"""
    return items_db[skip: skip + limit]


# 可选查询参数
@app.get("/items/search")
async def search_items(q: str | None = None, page: int = 1):
    """q 为可选参数，不传则为 None"""
    if q:
        return {"query": q, "page": page}
    return {"page": page, "items": items_db[:10]}


# 路径参数 + 查询参数
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int,
    item_id: str,
    q: str | None = None,
    short: bool = False
):
    """参数自动识别：路径中有声明的为路径参数，其余为查询参数"""
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item["q"] = q
    if not short:
        item["description"] = "这是一段很长的描述"
    return item


# 必选查询参数（不设默认值即为必选）
@app.get("/items/required")
async def read_required_items(q: str):
    """q 是必选的查询参数：/items/required?q=hello"""
    return {"q": q}


# 查询参数列表（多值）
@app.get("/items/tags")
async def read_by_tags(tags: list[str] = Query(default=[])):
    """多值查询：/items/tags?tags=python&tags=fastapi"""
    return {"tags": tags}
```

### 4.3 查询参数校验

```python
from fastapi import FastAPI, Query

app = FastAPI()


# 长度限制
@app.get("/items/")
async def read_items(
    q: str | None = Query(default=None, min_length=3, max_length=50)
):
    return {"q": q}


# 正则表达式
@app.get("/items/regex")
async def read_items_regex(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^fixedquery$"
    )
):
    return {"q": q}


# 默认值
@app.get("/items/default")
async def read_items_default(q: str = Query(default="固定查询", min_length=3)):
    return {"q": q}


# 声明为必需参数（使用 ... 省略号）
@app.get("/items/mandatory")
async def read_items_mandatory(q: str = Query(default=..., min_length=3)):
    """省略号 ... 表示必须提供此参数"""
    return {"q": q}


# 别名参数（URL 中的参数名与 Python 变量名不同）
@app.get("/items/alias")
async def read_items_alias(
    q: str | None = Query(default=None, alias="item-query")
):
    """URL: /items/alias?item-query=hello  (item-query 不是合法的 Python 变量名)"""
    return {"q": q}


# 弃用参数
@app.get("/items/deprecated")
async def read_items_deprecated(
    q: str | None = Query(
        default=None,
        alias="item-query",
        title="查询字符串",
        description="用于在数据库中搜索的查询字符串",
        deprecated=True,
    )
):
    return {"q": q}


# 元数据（title、description）
@app.get("/items/meta")
async def read_items_meta(
    q: str | None = Query(
        default=None,
        title="查询字符串",
        description="用于在数据库中搜索匹配项的字符串",
        min_length=3,
    )
):
    return {"q": q}
```

### 4.4 路径参数校验

```python
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


# 数值校验
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="物品ID", ge=1, le=1000)],
    q: str | None = None,
):
    """
    ge=1 : greater than or equal  (大于等于1)
    le=1000 : less than or equal  (小于等于1000)
    gt=0 : greater than           (大于0)
    lt=1000 : less than           (小于1000)
    """
    return {"item_id": item_id, "q": q}


# 不使用 Annotated 的写法（兼容 Python 3.8）
@app.get("/legacy/items/{item_id}")
async def read_items_legacy(
    item_id: int = Path(title="物品ID", ge=1),
    q: str | None = Query(default=None, alias="item-query"),
):
    return {"item_id": item_id, "q": q}
```

---

## 5. 请求体（Pydantic 模型）

### 5.1 基本请求体模型

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 自动将 JSON 请求体反序列化为 Item 对象
@app.post("/items/")
async def create_item(item: Item):
    """请求体 JSON 自动转为 Item 对象"""
    print(f"物品名: {item.name}, 价格: {item.price}")
    # 返回 Pydantic 对象，自动序列化为 JSON
    return item


# 访问模型属性
@app.post("/items/with_tax/")
async def create_item_with_tax(item: Item):
    item_dict = item.model_dump()  # 转为字典
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### 5.2 请求体 + 路径参数 + 查询参数

FastAPI 能自动识别参数类型：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,           # 路径参数（路径中有同名声明）
    item: Item,             # 请求体（Pydantic 模型类型）
    q: str | None = None,   # 查询参数（单类型 + 非路径参数）
):
    """
    参数识别规则：
    - 路径中声明的参数 -> 路径参数
    - Pydantic 模型类型 -> 请求体
    - 基础类型（int/str/bool 等）-> 查询参数
    """
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result["q"] = q
    return result
```

### 5.3 多个请求体参数

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# 多个请求体模型
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
):
    """请求体 JSON 格式：
    {
        "item": {"name": "Foo", "price": 50.5},
        "user": {"username": "alice", "full_name": "Alice"}
    }
    """
    return {"item_id": item_id, "item": item, "user": user}


# 单个值作为请求体
@app.put("/items/{item_id}/importance")
async def update_importance(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],  # 单一值作为请求体字段
    q: str | None = None,                    # 查询参数
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
        "q": q,
    }


# 嵌入单个请求体（嵌套在 key 中）
@app.put("/items/{item_id}/embed")
async def update_item_embed(
    item_id: int,
    item: Annotated[Item, Body(embed=True)],
):
    """embed=True 后的 JSON 格式：
    {
        "item": {
            "name": "Foo",
            "price": 50.5
        }
    }
    """
    return {"item_id": item_id, "item": item}
```

### 5.4 请求体字段校验

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="物品描述",
        max_length=300
    )
    price: float = Field(gt=0, description="价格必须大于零")
    tax: float | None = Field(default=None, ge=0, le=30)

    # 模型级配置：示例数据
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "示例物品",
                    "description": "这是一个示例",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

### 5.5 请求体嵌套

```python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Set, Dict

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl    # Pydantic 的 URL 类型，自动校验
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: Set[str] = set()                     # Set 去重
    image: Image | None = None                  # 嵌套模型
    images: List[Image] | None = None           # 嵌套模型列表


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}


# 纯列表请求体
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    """请求体直接是一个列表：[{...}, {...}]"""
    return images


# 字典类型请求体
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    """key 为整数，value 为浮点数"""
    return weights


# 深度嵌套
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: List[Item]  # Offer 包含 Item 列表，Item 又包含 Image 列表


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
```

---

## 6. 响应模型

### 6.1 response_model 参数

使用 `response_model` 可以控制返回给客户端的数据结构（过滤敏感字段）：

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# 输入模型（包含密码等敏感字段）
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# 输出模型（排除密码等敏感字段）
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# 指定 response_model 后，返回时会自动过滤掉密码字段
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    """即使返回了密码，response_model 也会过滤掉"""
    return user  # 返回对象中实际包含 password，但客户端看不到


# 不指定 response_model（会返回所有字段，包括密码）
@app.post("/user-unsafe/")
async def create_user_unsafe(user: UserIn):
    return user  # 危险：password 也会返回给客户端
```

### 6.2 响应过滤参数

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tags": []},
}


# response_model_exclude_unset：仅返回实际设置的值
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    """
    item_id=foo 时返回：{"name": "Foo", "price": 50.2}  (不含 tax)
    item_id=bar 时返回：{"name": "Bar", "description": "The Bartenders", "price": 62, "tax": 20.2}
    """
    return items[item_id]


# response_model_exclude：排除指定字段
@app.get("/items/{item_id}/safe", response_model=Item,
         response_model_exclude={"tax", "description"})
async def read_item_safe(item_id: str):
    """返回不含 tax 和 description"""
    return items[item_id]


# response_model_include：只包含指定字段
@app.get("/items/{item_id}/brief", response_model=Item,
         response_model_include={"name", "price"})
async def read_item_brief(item_id: str):
    """只返回 name 和 price"""
    return items[item_id]


# response_model_exclude_none：排除值为 None 的字段
@app.get("/items/{item_id}/nonull", response_model=Item,
         response_model_exclude_none=True)
async def read_item_none(item_id: str):
    return items[item_id]
```

### 6.3 响应状态码

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    """201 表示资源已创建"""
    return {"name": name, "id": 123}


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """204 表示成功但无返回内容"""
    return None  # 不会返回任何内容


# 使用 Response 对象动态设置状态码
from fastapi import Response


@app.get("/conditional")
async def conditional(response: Response, create: bool = False):
    if create:
        response.status_code = status.HTTP_201_CREATED
    return {"msg": f"created={create}"}
```

---

## 7. 自动 API 文档（Swagger/ReDoc）

### 7.1 自动生成的文档

FastAPI 基于 OpenAPI 标准自动生成交互式 API 文档，无需任何额外配置：

```python
from fastapi import FastAPI

app = FastAPI(
    title="我的 API",
    description="这是一个示例 API 的描述",
    version="1.0.0",
)


@app.get("/items/{item_id}", tags=["物品管理"],
         summary="获取物品详情",
         description="根据物品 ID 返回物品的详细信息",
         response_description="物品的详细信息")
async def read_item(item_id: int):
    """获取物品详情

    - **item_id**: 物品的唯一标识符
    """
    return {"item_id": item_id}


@app.post("/items/", tags=["物品管理"],
          summary="创建新物品",
          status_code=201)
async def create_item(name: str, price: float):
    return {"name": name, "price": price}
```

**访问地址（启动服务后）：**
- Swagger UI（交互式文档）：`http://127.0.0.1:8080/docs`
- ReDoc（备选文档）：`http://127.0.0.1:8080/redoc`
- OpenAPI JSON Schema：`http://127.0.0.1:8080/openapi.json`

### 7.2 文档配置

```python
from fastapi import FastAPI

app = FastAPI(
    title="电商平台 API",
    description="""
    这是一个电商平台的后端 API 系统。

    ## 功能模块
    * **用户管理**
    * **商品管理**
    * **订单管理**
    """,
    version="2.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API 支持团队",
        "url": "https://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    # 禁用文档（生产环境可关闭）
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,
)
```

### 7.3 标签分组与示例

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(examples=["手机"])
    description: str | None = Field(default=None, examples=["最新款智能手机"])
    price: float = Field(gt=0, examples=[5999.00])
    tax: float | None = Field(default=None, examples=[599.00])


@app.put("/items/{item_id}", tags=["物品管理"])
async def update_item(
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "笔记本电脑",
                "description": "高性能办公笔记本",
                "price": 7999.00,
                "tax": 799.00,
            }
        ]
    ),
):
    return {"item_id": item_id, "item": item}


@app.get("/users/", tags=["用户管理"])
async def list_users():
    return [{"id": 1, "name": "Alice"}]


@app.get("/orders/", tags=["订单管理"])
async def list_orders():
    return [{"id": 1001, "amount": 199.00}]
```

---

## 8. 依赖注入

### 8.1 依赖注入基本概念

依赖注入（Dependency Injection）是 FastAPI 的核心特性之一，允许将共享逻辑（认证、数据库连接、参数校验等）抽取为可复用的依赖函数：

```python
from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()


# ============ 定义依赖 ============

def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """公共查询参数依赖 - 可被多个路由复用"""
    return {"q": q, "skip": skip, "limit": limit}


# ============ 使用依赖 ============

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

### 8.2 依赖作为认证器

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated

app = FastAPI()


def verify_token(x_token: Annotated[str, Header()]):
    """验证请求头中的 Token"""
    if x_token != "expected-token-value":
        raise HTTPException(status_code=400, detail="无效的 X-Token")
    return x_token


def verify_key(x_key: Annotated[str, Header()]):
    """验证请求头中的 Key"""
    if x_key != "expected-key-value":
        raise HTTPException(status_code=400, detail="无效的 X-Key")
    return x_key


# 链式依赖
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    """同时需要 Token 和 Key 验证"""
    return [{"item": "Foo"}, {"item": "Bar"}]


# 在路由组中全局使用
@app.get("/users/", dependencies=[Depends(verify_token)])
async def read_users():
    return [{"username": "Alice"}, {"username": "Bob"}]
```

### 8.3 带数据库的依赖

```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
import asyncio

app = FastAPI()


# 模拟数据库连接
async def get_db():
    """数据库会话依赖 - 每次请求创建新的数据库会话"""
    print("打开数据库连接")
    db = {"connection": True}
    try:
        yield db  # yield 后面的代码会在请求结束后执行
    finally:
        print("关闭数据库连接")


# 模拟当前用户依赖
async def get_current_user(token: str = "test"):
    """获取当前用户"""
    # 实际应从 token 解析用户信息
    user = {"id": 1, "username": "Alice", "role": "admin"}
    return user


# 组合依赖
async def get_admin_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """需要管理员权限的依赖"""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


@app.get("/db-items/")
async def read_db_items(
    db: Annotated[dict, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    return {
        "user": current_user["username"],
        "data": [{"id": 1, "name": "Item from DB"}]
    }


@app.get("/admin/")
async def admin_endpoint(
    admin_user: Annotated[dict, Depends(get_admin_user)]
):
    """仅管理员可访问"""
    return {"msg": f"欢迎管理员 {admin_user['username']}"}
```

### 8.4 类作为依赖

```python
from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()


class Pagination:
    """分页依赖类"""
    def __init__(self, page: int = 1, size: int = 10, max_size: int = 100):
        self.page = page
        self.size = min(size, max_size)  # 限制最大页面大小

    @property
    def offset(self):
        return (self.page - 1) * self.size


class CommonFilters:
    """通用过滤依赖类"""
    def __init__(
        self,
        q: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):
        self.q = q
        self.sort_by = sort_by
        self.order = order


@app.get("/items/")
async def list_items(
    pagination: Annotated[Pagination, Depends()],
    filters: Annotated[CommonFilters, Depends()],
):
    """
    使用类作为依赖，可以方便地组合多个参数
    URL 示例：/items/?page=2&size=20&q=python&sort_by=name&order=desc
    """
    return {
        "page": pagination.page,
        "size": pagination.size,
        "offset": pagination.offset,
        "query": filters.q,
        "sort_by": filters.sort_by,
        "order": filters.order,
    }
```

---

## 9. 数据库操作（SQLAlchemy 异步）

### 9.1 使用 Tortoise ORM（推荐）

Tortoise ORM 是一个专为异步设计的 ORM 框架，适用于 FastAPI：

```bash
pip install tortoise-orm[asyncmy]
```

```python
# models.py
from tortoise import Model, fields


class Publish(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    addr = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    # 一对多：一个出版社对应多本书
    publish = fields.ForeignKeyField('models.Publish', related_name='books')
    # 多对多：一本书有多个作者
    authors = fields.ManyToManyField('models.Author', related_name='books',
                                     through='author_book')

    def __str__(self):
        return self.name
```

```python
# main.py - 快速集成
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    db_url="mysql://root:password@127.0.0.1:3306/fastapi_db?charset=utf8mb4",
    modules={"models": ["models"]},   # 模型文件路径
    generate_schemas=True,            # 自动生成表（仅开发环境）
    add_exception_handlers=True,      # 添加 Tortoise 异常处理
)
```

```python
# settings.py - 使用配置文件方式
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': 'password',
                'database': 'fastapi_db',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True,   # 打印 SQL 日志
            }
        },
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai',
}

# main.py
register_tortoise(app, config=TORTOISE_ORM)
```

### 9.2 Tortoise ORM 基本 CRUD

```python
from fastapi import FastAPI, HTTPException
from models import Book, Publish, Author

app = FastAPI()


# ============ 查询 ============

@app.get("/books")
async def list_books():
    """查询所有书籍"""
    books = await Book.all()
    return books


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    """查询单本书"""
    book = await Book.get_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    return book


@app.get("/books/search")
async def search_books(name: str = "", min_id: int = 0):
    """多种查询条件"""
    books = await Book.filter(
        name__icontains=name,   # 模糊查询（不区分大小写）
        id__gt=min_id           # ID 大于
    ).order_by('-id').limit(20)  # ID 降序，限制20条
    return books


@app.get("/books-by-publisher")
async def books_by_publisher(name: str):
    """连表查询：根据出版社名字查书籍"""
    books = await Book.filter(publish__name=name).values('name', 'id')
    return books


@app.get("/books-by-author")
async def books_by_author(author_name: str):
    """多对多连表查询"""
    books = await Book.filter(authors__name=author_name).values('name')
    return books


# ============ 新增 ============

@app.post("/books")
async def create_book(name: str, publish_id: int):
    """新增书籍"""
    book = await Book.create(name=name, publish_id=publish_id)
    return {"id": book.id, "name": book.name, "msg": "创建成功"}


@app.post("/books/batch")
async def batch_create():
    """批量新增"""
    # 注意：bulk_create 接收的是未保存的实例列表，外键需用 _id 后缀（Tortoise 约定）
    books_data = [Book(name=f"书籍{i}", publish_id=1) for i in range(10)]
    await Book.bulk_create(books_data)
    return {"count": len(books_data), "msg": "批量创建成功"}


# ============ 更新 ============

@app.put("/books/{book_id}")
async def update_book(book_id: int, name: str):
    """更新书籍"""
    # 方式一：查询后修改属性
    book = await Book.get(id=book_id)
    book.name = name
    await book.save()

    # 方式二：批量更新
    # await Book.filter(id=book_id).update(name=name)

    return {"msg": "更新成功"}


# ============ 删除 ============

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """删除书籍"""
    book = await Book.get(id=book_id)
    await book.delete()
    # 或：await Book.filter(id=book_id).delete()
    return {"msg": "删除成功"}


# ============ 分页 ============

@app.get("/books/paginated")
async def paginated_books(page: int = 1, size: int = 10):
    """分页查询"""
    total = await Book.all().count()
    books = await Book.all().offset((page - 1) * size).limit(size)
    return {
        "total": total,
        "page": page,
        "size": size,
        "data": books,
    }
```

### 9.3 数据库迁移（Aerich）

```bash
# 安装
pip install aerich

# 初始化配置
aerich init -t settings.TORTOISE_ORM

# 初始化数据库（仅首次）
aerich init-db

# 修改模型后，生成迁移文件
aerich migrate --name "添加新字段"

# 应用迁移
aerich upgrade

# 回滚到指定版本
aerich downgrade -v <version_number>

# 查看迁移历史
aerich history
```

### 9.4 使用 SQLAlchemy 异步

```bash
pip install sqlalchemy[asyncio] aiomysql
```

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, select

# 创建异步引擎
engine = create_async_engine(
    "mysql+aiomysql://root:password@127.0.0.1:3306/mydb?charset=utf8mb4",
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# 创建异步 Session 工厂
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    email = Column(String(64), unique=True)


# 在 FastAPI 中使用
from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@app.get("/users")
async def list_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@app.post("/users")
async def create_user(name: str, email: str,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    user = User(name=name, email=email)
    db.add(user)
    await db.flush()
    return {"id": user.id, "name": user.name}
```

---

## 10. 认证与授权（OAuth2、JWT）

### 10.1 JWT 认证实现

```bash
# ⚠️ python-jose 已数年未维护，并有公开 CVE，新项目推荐改用 pyjwt 或 authlib
# 教学保留 python-jose 仅为与官方文档示例兼容
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
# 推荐替代：pip install pyjwt[crypto] passlib[bcrypt] python-multipart
```

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ============ 配置 ============
SECRET_KEY = "your-secret-key-keep-it-secret-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============ 密码加密 ============
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============ OAuth2 密码流 ============
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# ============ 模拟用户数据 ============
fake_users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wang",
        "email": "alice@example.com",
        "hashed_password": pwd_context.hash("secret123"),
        "disabled": False,
    }
}


# ============ 数据模型 ============
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# ============ 工具函数 ============
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """从 Token 中解析当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """检查用户是否被禁用"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user


# ============ API 端点 ============

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """登录获取 Token"""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """获取当前用户信息（需要登录）"""
    return current_user


@app.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """获取当前用户的物品列表"""
    return [{"item_id": 1, "owner": current_user.username}]
```

### 10.2 简单的 Token 认证依赖

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated

app = FastAPI()


# 简单的 Token 验证依赖
async def verify_token(x_token: Annotated[str, Header()] = None):
    if x_token is None:
        raise HTTPException(status_code=401, detail="未提供认证 Token")
    if x_token != "my-secret-token":
        raise HTTPException(status_code=403, detail="Token 无效")
    return {"user_id": 1, "role": "user"}


# 角色验证依赖
def require_role(role: str):
    """工厂函数：生成特定角色的验证依赖"""
    async def role_checker(
        current_user: Annotated[dict, Depends(verify_token)]
    ):
        if current_user.get("role") != role:
            raise HTTPException(status_code=403, detail=f"需要 {role} 角色")
        return current_user
    return role_checker


@app.get("/protected")
async def protected_route(
    user: Annotated[dict, Depends(verify_token)]
):
    return {"msg": f"欢迎 {user['user_id']}"}


@app.get("/admin-only")
async def admin_only(
    admin: Annotated[dict, Depends(require_role("admin"))]
):
    return {"msg": "管理员专属页面"}
```

---

## 11. 中间件与 CORS

### 11.1 自定义中间件

```python
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """统计请求处理时间并添加到响应头"""
    start_time = time.time()

    # 调用下一个中间件或视图函数
    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """简单的 Token 验证中间件（不影响登录等公开接口）"""
    # 跳过不需要验证的路径
    public_paths = ["/docs", "/openapi.json", "/redoc", "/token", "/login"]
    if request.url.path in public_paths:
        return await call_next(request)

    # 检查 Token
    token = request.headers.get("Authorization")
    if token is None:
        return JSONResponse(
            status_code=401,
            content={"detail": "未提供认证 Token"}
        )

    # Token 有效时继续处理
    return await call_next(request)


@app.get("/")
async def index():
    return {"msg": "Hello World"}
```

**中间件执行顺序说明：**
- 多个中间件按照注册顺序从上往下执行（before 部分），返回时从下往上执行（after 部分）
- 可以将中间件定义为函数并添加到 app 上

### 11.2 CORS（跨域资源共享）

```bash
pip install fastapi  # CORS 中间件已包含在 FastAPI 中
```

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # 前端开发服务器
        "https://your-frontend.com", # 生产前端域名
    ],  # 也可使用 ["*"] 允许所有来源（仅开发环境）
    allow_credentials=True,          # 允许携带 Cookie
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的 HTTP 方法
    allow_headers=["*"],             # 允许的请求头
    expose_headers=["X-Process-Time"],  # 允许前端访问的响应头
    max_age=600,                     # 预检请求缓存时间（秒）
)


# 完整示例
@app.get("/data")
async def get_data():
    return {"data": "跨域请求成功"}


@app.post("/data")
async def create_data(payload: dict):
    return {"received": payload}
```

### 11.3 FastAPI 中间件与 Flask 请求扩展对比

| FastAPI 中间件 | Flask 请求扩展 | 说明 |
|---------------|---------------|------|
| `@app.middleware("http")` | `@app.before_request` + `@app.after_request` | 请求前后处理 |
| 自定义中间件函数 | `@app.before_request` | 请求前置处理 |
| `CORSMiddleware` | `Flask-CORS` 扩展 | 跨域处理 |
| `add_middleware()` | `app.wsgi_app = Middleware(app.wsgi_app)` | 添加中间件 |

---

## 12. 后台任务

### 12.1 使用 BackgroundTasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


# ============ 定义后台任务函数 ============

def write_log(message: str):
    """写入日志（模拟耗时操作）"""
    with open("app.log", "a") as f:
        f.write(f"[LOG] {message}\n")


def send_email(email: str, content: str = "欢迎注册"):
    """发送邮件（模拟）"""
    # 实际应调用邮件发送服务
    print(f"向 {email} 发送邮件: {content}")
    import time
    time.sleep(2)  # 模拟邮件发送耗时
    print(f"邮件已发送至 {email}")


def process_data(data_id: int):
    """处理数据"""
    print(f"开始处理数据 ID={data_id}")
    import time
    time.sleep(3)
    print(f"数据 ID={data_id} 处理完成")


# ============ 在路由中使用后台任务 ============

@app.post("/register")
async def register(email: str, background_tasks: BackgroundTasks):
    """用户注册 - 异步发送欢迎邮件"""
    # 1. 同步处理：创建用户
    user = {"id": 123, "email": email}

    # 2. 添加后台任务
    background_tasks.add_task(send_email, email, "欢迎注册我们的服务")
    background_tasks.add_task(write_log, f"新用户注册: {email}")

    # 3. 立即返回响应（不等待后台任务完成）
    return {"msg": "注册成功", "user_id": user["id"]}


@app.post("/data/{data_id}")
async def trigger_process(data_id: int, background_tasks: BackgroundTasks):
    """触发数据处理 - 后台处理数据，立即返回"""
    background_tasks.add_task(process_data, data_id)
    return {"msg": f"数据处理任务已提交，ID={data_id}"}


@app.get("/multi-task")
async def multi_task(background_tasks: BackgroundTasks):
    """添加多个后台任务"""
    for i in range(5):
        background_tasks.add_task(write_log, f"多任务日志 #{i}")
    return {"msg": "5个后台日志任务已添加"}
```

### 12.2 BackgroundTasks 注意事项

- 后台任务在响应返回之后执行
- 适合轻量级任务（写日志、发通知、简单计算等）
- 不适合长时间运行的任务（应使用 Celery 等分布式任务队列）
- 后台任务无法返回结果给客户端
- 不能直接在后台任务中使用 `await`（如需异步操作，使用 `asyncio` 创建任务）

### 12.3 使用 asyncio 后台任务

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()


async def async_background_work(task_id: str, duration: int):
    """异步后台工作"""
    await asyncio.sleep(duration)
    print(f"后台任务 {task_id} 完成（耗时 {duration}s）")


@app.post("/async-task/{task_id}")
async def create_async_task(task_id: str):
    """启动异步后台任务（不等待结果）"""
    asyncio.create_task(async_background_work(task_id, 5))
    return {"msg": f"异步任务 {task_id} 已启动", "status": "processing"}


# 如果需要等待所有任务完成
@app.get("/await-all")
async def await_all_tasks():
    """等待所有后台任务完成"""
    task1 = asyncio.create_task(async_background_work("task1", 2))
    task2 = asyncio.create_task(async_background_work("task2", 3))

    await asyncio.gather(task1, task2)
    return {"msg": "所有任务已完成"}
```

---

## 13. WebSocket 支持

### 13.1 WebSocket 简介

WebSocket 是一种应用层协议，建立连接后保持长连接，支持服务端主动向客户端推送消息，适用于实时聊天、实时数据推送、协作编辑等场景。

### 13.2 基本 WebSocket 端点

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板引擎
templates = Jinja2Templates(directory="templates")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """基本 WebSocket：服务端收到什么就返回什么（加后缀）"""
    # 接受 WebSocket 连接
    await websocket.accept()
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            # 发送消息给客户端
            await websocket.send_text(f"服务端回复: {data}")
    except WebSocketDisconnect:
        print("客户端断开连接")
```

### 13.3 多人聊天室

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # 存储所有活跃的 WebSocket 连接
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """移除断开连接"""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """发送私人消息"""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """向所有连接广播消息"""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{username}")
async def chat_websocket(websocket: WebSocket, username: str):
    """多人聊天 WebSocket 端点"""
    await manager.connect(websocket)

    # 通知其他人有新用户加入
    await manager.broadcast(f"系统消息: {username} 加入了聊天室")

    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            # 广播给所有人
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        # 处理断开连接
        manager.disconnect(websocket)
        await manager.broadcast(f"系统消息: {username} 离开了聊天室")
```

**前端 HTML 示例：**

```html
<!-- templates/chat.html -->
<!DOCTYPE html>
<html>
<head>
    <title>聊天室</title>
</head>
<body>
    <h1>多人聊天室</h1>
    <div id="messages"></div>
    <form onsubmit="sendMessage(event)">
        <input type="text" id="messageInput" autocomplete="off"/>
        <button>发送</button>
    </form>

    <script>
        const username = prompt("请输入你的名字:");
        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${username}`);

        ws.onmessage = function(event) {
            const messages = document.getElementById('messages');
            const message = document.createElement('div');
            message.textContent = event.data;
            messages.appendChild(message);
        };

        function sendMessage(event) {
            const input = document.getElementById('messageInput');
            ws.send(input.value);
            input.value = '';
            event.preventDefault();
        }
    </script>
</body>
</html>
```

### 13.4 WebSocket 认证

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Cookie, status

app = FastAPI()


@app.websocket("/ws/auth")
async def authenticated_websocket(
    websocket: WebSocket,
    token: str = Query(...),  # 通过查询参数传递 token
):
    """带认证的 WebSocket 端点"""
    # 验证 token
    if token != "valid-token":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"认证用户: {data}")
    except WebSocketDisconnect:
        print("客户端断开连接")


# 客户端连接方式：ws://localhost:8000/ws/auth?token=valid-token
```

---

## 14. 项目上线部署

### 14.1 配置文件管理

```bash
pip install python-dotenv pydantic-settings
```

**.env 文件：**

```bash
# -------- 服务配置 --------
APP_HOST=0.0.0.0
APP_PORT=8080
APP_ENV=production
APP_DEBUG=false

# -------- 数据库配置 --------
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_DATABASE=fastapi_db

# -------- Redis 配置 --------
REDIS_URL=redis://127.0.0.1:6379/0

# -------- JWT 配置 --------
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# -------- CORS --------
CORS_ORIGINS=["https://your-frontend.com"]
```

```python
# config/settings.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # 服务配置
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    app_env: str = "development"
    app_debug: bool = False

    # 数据库配置
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_database: str = "fastapi_db"

    # Redis 配置
    redis_url: str = "redis://127.0.0.1:6379/0"

    # JWT 配置
    jwt_secret_key: str = "default-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # CORS
    cors_origins: list[str] = ["*"]

    @property
    def database_url(self) -> str:
        return (f"mysql+aiomysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_database}?charset=utf8mb4")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

```python
# main.py
from fastapi import FastAPI
from config.settings import settings

app = FastAPI(
    title="FastAPI 应用",
    version="1.0.0",
    debug=settings.app_debug,
    docs_url=None if settings.app_env == "production" else "/docs",
    redoc_url=None if settings.app_env == "production" else "/redoc",
)


@app.get("/")
async def root():
    return {"msg": "FastAPI 运行中", "env": settings.app_env}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
    )
```

### 14.2 使用 Uvicorn + Gunicorn 部署

```bash
# 安装 Gunicorn + Uvicorn worker
pip install gunicorn uvicorn

# 启动（4 个 Uvicorn worker，每个 worker 都是独立的进程）
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --log-level info
```

### 14.3 Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name api.example.com;

    # 代理到 FastAPI 后端
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 静态文件
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 14.4 Docker 部署

**Dockerfile：**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY .. .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml：**

```yaml
version: "3.8"

services:
  app:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - DB_HOST=mysql
      - DB_USER=root
      - DB_PASSWORD=password
      - DB_DATABASE=fastapi_db
    depends_on:
      - mysql
      - redis
    restart: always

  mysql:
    image: mysql:8.0
    container_name: fastapi_mysql
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: fastapi_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  redis:
    image: redis:7-alpine
    container_name: fastapi_redis
    ports:
      - "6379:6379"
    restart: always

  nginx:
    image: nginx:alpine
    container_name: fastapi_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app
    restart: always

volumes:
  mysql_data:
```

### 14.5 生产环境 Checklist

```python
# 生产配置检查清单
class ProductionSettings:
    # 1. 关闭调试模式
    APP_DEBUG = False

    # 2. 使用环境变量管理敏感信息
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 3. 限制文档访问（可选）
    # app = FastAPI(docs_url=None, redoc_url=None)

    # 4. 配置 HTTPS
    # uvicorn main:app --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem

    # 5. 配置请求大小限制
    # from starlette.middleware.base import BaseHTTPMiddleware
    # 或使用 Nginx client_max_body_size

    # 6. 配置日志
    LOG_LEVEL = "INFO"

    # 7. 配置数据库连接池
    DB_POOL_SIZE = 20
    DB_MAX_OVERFLOW = 40

    # 8. 配置 CORS 为具体域名
    CORS_ORIGINS = ["https://your-frontend.com"]
```

**部署检查清单：**

1. 关闭 `debug` 和 `reload` 模式
2. 使用强随机 SECRET_KEY，从环境变量读取
3. 启用 HTTPS，配置 SSL 证书
4. 配置 Uvicorn worker 数量 = (2 * CPU 核心数) + 1
5. 使用 Nginx 反向代理处理静态文件和 SSL 终端
6. 配置 Gunicorn + Uvicorn worker 进程管理
7. 使用 `supervisor` 或 `systemd` 管理进程
8. 配置日志轮转（RotatingFileHandler）
9. 添加健康检查接口 `/health`
10. 限制请求体大小（Nginx `client_max_body_size`）
11. 配置数据库连接池参数
12. 配置环境变量区分开发/生产环境

---

## 附录：FastAPI 请求参数速查表

| 参数来源 | Python 声明方式 | 示例 URL / 请求 |
|---------|---------------|----------------|
| 路径参数 | `item_id: int` | `/items/42` |
| 查询参数 | `q: str = None` | `/items/?q=hello` |
| 请求体 | `item: Item` (Pydantic模型) | `POST /items/` + JSON Body |
| 表单数据 | `username: str = Form()` | `POST /login/` + Form Data |
| 文件上传 | `file: UploadFile` | `POST /upload/` + Multipart |
| 请求头 | `user_agent: str = Header()` | 从请求头读取 |
| Cookie | `session_id: str = Cookie()` | 从 Cookie 读取 |

**关键参数类继承关系：**

```
Param (基类)
├── Path     (路径参数校验)
├── Query    (查询参数校验)
├── Header   (请求头校验)
├── Cookie   (Cookie 校验)
└── Body     (请求体校验)
```
