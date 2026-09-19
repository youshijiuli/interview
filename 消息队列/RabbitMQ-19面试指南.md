## 4 消息队列 RabbitMQ

### Q23: 什么是消息队列？为什么要用消息队列？

**答：** 消息队列是在消息传输过程中保存消息的容器，遵循**生产者-消费者模型**。

**三大经典场景：**

| 场景 | 说明 | 示例 |
|------|------|------|
| **异步处理** | 耗时操作异步执行，不等待结果 | 用户注册后异步发邮件/短信 |
| **应用解耦** | 系统间通过消息通信，不直接调用 | 订单系统 → 库存系统 → 物流系统 |
| **流量削峰** | 应对突发高并发，平滑处理请求 | 秒杀系统，排队处理订单 |

```python
# 同步方式（耦合）
def register(username):
    user = save_user(username)     # 存到数据库
    send_email(username)           # 发邮件（耗时长）
    send_sms(username)             # 发短信
    return '注册成功'

# 异步方式（解耦）
def register(username):
    user = save_user(username)
    mq.send({'type': 'register', 'username': username})
    return '注册成功'
# 邮件和短信服务独立消费消息
```

---

### Q24: RabbitMQ 的核心架构是什么？

**答：** RabbitMQ 基于 **AMQP**（Advanced Message Queuing Protocol，高级消息队列协议）协议。

**核心概念：**

```
Producer ────→ Exchange ───→ Queue ───→ Consumer
  生产者       交换机(路由)   队列       消费者
                ↓
             Binding (绑定规则)
```

| 组件 | 说明 |
|------|------|
| **Producer** | 生产者，发送消息的应用 |
| **Consumer** | 消费者，接收消息的应用 |
| **Exchange** | 交换机，接收生产者消息，根据路由规则投递到对应队列 |
| **Queue** | 队列，存储消息的缓冲区 |
| **Binding** | 绑定，定义 Exchange 和 Queue 之间的路由关系 |
| **Routing Key** | 路由键，生产者发送消息时指定，用于路由匹配 |
| **Virtual Host** | 虚拟主机，类似命名空间，用于隔离不同应用 |

---

### Q25: RabbitMQ 的交换机类型有哪些？

| 类型 | 说明 | 路由规则 |
|------|------|---------|
| **Direct Exchange** | 直连交换机 | Routing Key 完全匹配 Binding Key |
| **Fanout Exchange** | 广播交换机 | 忽略 Routing Key，广播到所有绑定队列 |
| **Topic Exchange** | 主题交换机 | Routing Key 模式匹配（`*` 匹配一个词，`#` 匹配零个或多个词） |
| **Headers Exchange** | 头交换机 | 根据消息 Header 属性匹配（很少使用） |

```
Direct Exchange:
  routing_key = "error"  → Queue A（binding_key = "error"）
  routing_key = "info"   → Queue B（binding_key = "info"）

Fanout Exchange:
  无论什么 routing_key → 所有绑定的队列都收到

Topic Exchange:
  routing_key = "user.create"  → Queue A（binding_key = "user.*"）
  routing_key = "user.delete"  → Queue A
  routing_key = "order.pay"    → Queue B（binding_key = "order.#"）
```

---

### Q26: RabbitMQ 的消息确认机制是什么？

**答：** RabbitMQ 提供两种确认机制保证消息可靠投递：

#### 生产者确认（Publisher Confirm）
```python
# 开启确认模式
channel.confirm_delivery()

# 发送消息后等待确认
try:
    channel.basic_publish(exchange='', routing_key='queue', body='msg')
except Exception:
    print('消息发送失败')
```

#### 消费者确认（Consumer Ack）
```python
# 自动确认（不推荐，消息可能丢失）
channel.basic_consume(queue='queue', on_message_callback=callback, auto_ack=True)

# 手动确认（推荐）
def callback(ch, method, properties, body):
    try:
        process(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 确认
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # 拒绝并重新入队
        # 或 ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
```

---

### Q27: 如何保证消息不丢失？

**答：** 从三个环节保证：

| 环节 | 措施 |
|------|------|
| **生产者 → Exchange** | Publisher Confirm（发送方确认） |
| **Exchange → Queue** | 消息持久化（Delivery Mode=2），Queue 持久化 |
| **Queue → 消费者** | 消费者手动 ACK，处理完再确认 |
| **RabbitMQ 本身** | 队列、消息、交换机都持久化；使用镜像队列（高可用） |

---

### Q28: RabbitMQ 的安装

```bash
# Docker 安装（推荐）
docker run -d --name rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=admin \
    rabbitmq:3-management

# 访问管理界面：http://ip:15672
```

---
