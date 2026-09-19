## 1 Redis 高频面试题

### Q1: 什么是 Redis？为什么用它？

**答：** Redis（Remote Dictionary Server）是开源的、基于内存的键值存储数据库。

**核心特点：**
- 基于内存，读写速度极快（10万+ QPS）
- 支持多种数据结构（String、Hash、List、Set、Sorted Set）
- 支持持久化（RDB/AOF）
- 支持主从复制、哨兵、集群（高可用）
- 单线程模型，无锁竞争（注：Redis 6.0+ 网络 I/O 已支持多线程，但**命令执行依然由单一主线程串行处理**，无并发安全问题）
- 支持发布订阅、Lua 脚本、事务、Pipeline

**主要应用场景：**
- 缓存：减少数据库压力，提高访问速度
- 分布式锁：SETNX 实现
- 计数器/排行榜：Sorted Set
- 消息队列：List、Stream
- 会话存储：Session 集中管理
- 社交：共同好友（Set 交集）、UV 统计（HyperLogLog）

---

### Q2: 什么是缓存穿透？如何解决？

**答：** 缓存穿透是指查询一个**根本不存在的数据**，缓存和数据库都没有，导致每次请求都穿透缓存直接打到数据库。

**解决方案：**

| 方案 | 说明 | 优缺点 |
|------|------|--------|
| **缓存空值** | 将不存在的 key 也缓存，value 设为 null 或空，设置较短过期时间 | 实现简单，但消耗内存 |
| **布隆过滤器（Bloom Filter）** | 在缓存前加一层布隆过滤器，先把所有存在的 key 存入，请求先过布隆过滤器判断 | 内存占用小，但存在误判（说不存在一定不存在，说存在可能不存在） |
| **参数校验** | 在接口层做参数合法性校验，过滤掉明显非法的请求 | 基础防护，无法完全解决 |

```python
# 缓存空值示例
def get_data(key):
    data = cache.get(key)
    if data is not None:
        return data  # None 也表示缓存了空值

    data = db.query(key)
    if data:
        cache.set(key, data, timeout=3600)
    else:
        cache.set(key, None, timeout=60)  # 空值短时间缓存
    return data
```

---

### Q3: 什么是缓存击穿？如何解决？

**答：** 缓存击穿是指**某个热点 key 过期**的瞬间，大量并发请求同时打到数据库，造成数据库压力激增。

**解决方案：**

| 方案 | 说明 |
|------|------|
| **互斥锁（Mutex）** | 获取缓存失败时，加锁，只让一个线程去查数据库，其他线程等待 |
| **逻辑过期** | 热点 key 永不过期，但 value 中存一个逻辑过期时间，发现过期后异步更新，旧值继续用 |
| **热点数据永不过期** | 对已知热点 key 不设置过期时间，通过后台任务定期更新 |

```python
# 互斥锁方案
import threading

lock = threading.Lock()

def get_hot_data(key):
    data = cache.get(key)
    if data:
        return data

    if lock.acquire(blocking=False):  # 尝试获取锁
        try:
            # 双重检查
            data = cache.get(key)
            if data:
                return data
            data = db.query(key)
            cache.set(key, data, timeout=3600)
            return data
        finally:
            lock.release()
    else:
        time.sleep(0.1)  # 等待后再试
        return cache.get(key)
```

---

### Q4: 什么是缓存雪崩？如何解决？

**答：** 缓存雪崩是指**大量 key 在同一时刻过期**，或者 Redis 服务器宕机，导致大量请求直接打到数据库，造成数据库崩溃。

**解决方案：**

| 方案 | 说明 |
|------|------|
| **过期时间加随机值** | 避免同时过期，在基础过期时间上加随机偏移量 |
| **Redis 高可用** | 主从复制 + 哨兵 + 集群，保证 Redis 不宕机 |
| **限流/降级** | 对数据库访问做限流，当缓存不可用时返回默认值或提示"系统繁忙" |
| **多级缓存** | 本地缓存（进程内）+ Redis + 数据库，层层缓存 |

```python
import random

# 设置过期时间时加随机偏移
base_timeout = 3600
cache.set(key, value, timeout=base_timeout + random.randint(0, 300))
```

---

### Q5: 什么是布隆过滤器？

**答：** 布隆过滤器（Bloom Filter）是一种**空间效率极高的概率型数据结构**，用于判断一个元素是否在一个集合中。

**特点：**
- **如果判断不存在，则一定不存在**
- **如果判断存在，则可能存在（有一定误判率）**
- 使用多个哈希函数和位图实现
- 不支持删除操作

**实现原理：**
```
元素 "hello"
  → hash1("hello") = 3   → 位图第3位 置1
  → hash2("hello") = 8   → 位图第8位 置1
  → hash3("hello") = 12  → 位图第12位 置1

查询 "hello"：检查第3、8、12位是否都为1 → 是 → 可能存在
查询 "world"：检查对应位不全为1 → 否 → 一定不存在
```

**Redis 中使用布隆过滤器：**
```bash
# Redis Stack 自带，或通过 redisbloom 模块
BF.ADD myfilter item1
BF.EXISTS myfilter item1   # 返回 1
BF.MADD myfilter item2 item3 item4
BF.MEXISTS myfilter item1 item2 item5  # [1, 1, 0]
```

---

### Q6: Redis 有哪些数据结构？分别适用什么场景？

| 数据结构 | 底层实现 | 使用场景 | 常用命令 |
|---------|---------|---------|---------|
| **String** | SDS（简单动态字符串） | 缓存、计数器、分布式锁、Session | SET/GET/INCR/SETEX/SETNX |
| **Hash** | 哈希表 + 压缩列表 | 对象存储、购物车 | HSET/HGET/HGETALL/HINCRBY |
| **List** | 双向链表 + 压缩列表 | 消息队列、最新列表、时间线 | LPUSH/RPUSH/LPOP/RPOP/BLPOP |
| **Set** | 哈希表 + 整数集合 | 去重、标签、共同好友 | SADD/SMEMBERS/SINTER/SUNION |
| **Sorted Set** | 跳表 + 哈希表 | 排行榜、延迟队列、权重排序 | ZADD/ZRANGE/ZREVRANGE/ZINCRBY |
| **Bitmap** | String（位操作） | 签到、在线状态、布隆过滤器 | SETBIT/GETBIT/BITCOUNT |
| **HyperLogLog** | 基数统计算法 | UV 统计、大数据去重计数 | PFADD/PFCOUNT/PFMERGE |
| **GEO** | Sorted Set | 附近的人、距离计算 | GEOADD/GEODIST/GEORADIUS |
| **Stream** | 链表 + Rax 树 | 消息队列（支持消费者组） | XADD/XREAD/XGROUP |

---

### Q7: Redis 的 String 类型底层是如何实现的？

**答：** Redis 使用 **SDS（Simple Dynamic String）** 而不是 C 语言的字符串。

**SDS 结构的优势：**
- **O(1) 获取长度**：有 len 属性，直接读取，C 字符串需要遍历
- **二进制安全**：可以存任意二进制数据（图片、序列化对象等）
- **杜绝缓冲区溢出**：每次修改前检查空间是否足够
- **空间预分配**：扩展时多分配空间，减少内存重分配次数
- **惰性空间释放**：缩短字符串时不立即回收空间，留给后续使用

```c
struct sdshdr {
    int len;   // 已使用字节数
    int free;  // 未使用字节数
    char buf[]; // 实际字符串数据
};
```

---

### Q8: Redis 的 Sorted Set 底层实现是什么？

**答：** Sorted Set 底层根据元素数量和元素大小，采用两种数据结构：

**1. 压缩列表（ziplist）**：当元素数量 < 128 且每个元素 < 64 字节时使用，节省内存。

**2. 跳表（skiplist）+ 哈希表**：元素较多时使用：
- **跳表**：负责按分数排序和范围查找，时间复杂度 O(logN)
- **哈希表**：负责按成员快速查找分数，时间复杂度 O(1)

**跳表原理：**
跳表是一种多层链表结构，每一层都是下一层的"快速通道"，通过随机函数决定节点层数，实现平均 O(logN) 的查找效率。

```
Level 2: 1 ---------------> 7 ---------------> 15
Level 1: 1 ------> 4 ------> 7 ------> 10 ------> 15
Level 0: 1 -> 2 -> 4 -> 5 -> 7 -> 8 -> 10 -> 12 -> 15
```

---

### Q9: Redis 怎么做持久化？

**答：** Redis 提供三种持久化方式：

#### RDB（Redis Database）
- **原理**：在指定时间间隔内，将内存中的数据集快照写入磁盘
- **触发方式**：
  - 自动：`save 900 1`（900秒内至少1次修改）
  - 手动：`save`（阻塞）/ `bgsave`（fork 子进程，非阻塞）
- **优点**：文件紧凑，恢复速度快，适合备份
- **缺点**：可能会丢失最后一次快照后的数据

#### AOF（Append Only File）
- **原理**：将每条写命令追加记录到日志文件中
- **同步策略**：
  - `appendfsync always`：每次写都同步（最安全，最慢）
  - `appendfsync everysec`：每秒同步一次（推荐，最多丢1秒数据）
  - `appendfsync no`：由操作系统决定（最快，最不安全）
- **AOF 重写**：当文件过大时，自动重写为最小命令集
- **优点**：数据安全性高，丢失少
- **缺点**：文件比 RDB 大，恢复速度慢

#### 混合持久化（Redis 4.0+）
- 同时使用 RDB 和 AOF
- AOF 文件前半段是 RDB 格式的二进制数据，后半段是增量 AOF 命令
- 兼顾了恢复速度和数据安全性

```bash
# RDB 配置
save 900 1
save 300 10
save 60 10000

# AOF 配置
appendonly yes
appendfsync everysec

# 混合持久化
aof-use-rdb-preamble yes
```

---

### Q10: Redis 如何实现主从复制？

**答：** Redis 主从复制是指将一台 Redis（Master）的数据同步到多台 Redis（Slave）上。

**复制过程：**

```
① 从节点执行 replicaof 命令
② 从节点与主节点建立 Socket 连接
③ 从节点发送 PSYNC 命令
④ 主节点执行 BGSAVE，生成 RDB 文件，同时记录缓冲区新写命令
⑤ 主节点发送 RDB 文件给从节点
⑥ 从节点清空旧数据，加载 RDB 文件
⑦ 主节点发送缓冲区中的写命令
⑧ 之后主节点每执行写命令，都同步发送给从节点（异步复制）
```

**配置：**
```bash
# 从节点配置
replicaof 主节点IP 6379
# 如果主节点有密码
masterauth 密码

# 从节点默认只读
replica-read-only yes
```

**作用：**
- 数据备份，高可用基础
- 读写分离：主写从读，提升读性能
- 故障恢复

---

### Q11: Redis 哨兵（Sentinel）是什么？

**答：** 哨兵是 Redis 的高可用解决方案，能**自动完成故障发现和故障转移**。

**哨兵功能：**
- **监控（Monitoring）**：持续检查主从节点是否正常工作
- **通知（Notification）**：将故障信息通知给管理员
- **自动故障转移（Failover）**：主节点故障时，自动选举新的主节点
- **配置提供者**：客户端通过哨兵获取当前主节点地址

**工作原理：**
```
哨兵集群（至少3个哨兵，推荐奇数个）
    ↓ 监控
Redis Master（主节点）
    ↓ 同步
Redis Slave（从节点）
Redis Slave（从节点）

当 Master 故障时：
1. 哨兵中的大多数（quorum）确认 Master 客观下线
2. 哨兵领导者选举，选择一个 Slave 提升为 Master
3. 其他 Slave 改为从新的 Master 复制
4. 通知客户端新的 Master 地址
```

**配置示例：**
```bash
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2  # 2表示至少2个哨兵同意才下线
sentinel down-after-milliseconds mymaster 30000  # 30秒无响应判断下线
sentinel failover-timeout mymaster 180000
sentinel parallel-syncs mymaster 1
```

---

### Q12: Redis Cluster（集群）是什么？数据如何分片？

**答：** Redis Cluster 是 Redis 的**分布式方案**，解决了单机容量和性能瓶颈问题。

**核心概念：**

- **虚拟槽（Slot，槽位）**：Redis Cluster 将数据空间划分为 **16384 个槽**
- **槽分配**：每个 Master 节点负责一部分槽（如 3 个 Master 各负责约 5461 个槽）
- **数据定位**：`slot = CRC16(key) % 16384`，根据 slot 值路由到对应节点

**集群架构：**
```
┌─────────────────────────────────────┐
│         Redis Cluster (6节点)        │
│                                     │
│  Master A    Master B    Master C   │
│  Slot 0-5460 Slot 5461-10922 Slot... │
│     ↓           ↓           ↓       │
│  Slave A1   Slave B1   Slave C1    │
└─────────────────────────────────────┘
```

**特点：**
- 每个节点负责部分槽，节点间通过 Gossip 协议通信
- Master-Slave 模式，Master 故障时 Slave 自动提升
- 所有节点互联（全连接）
- 最小配置：6 个节点（3 Master + 3 Slave）

**集群搭建关键步骤：**
```bash
# 1. 配置每个节点的 redis.conf
cluster-enabled yes
cluster-config-file nodes-6379.conf
cluster-node-timeout 15000

# 2. 启动所有节点
redis-server redis-6379.conf
redis-server redis-6380.conf
# ...

# 3. 创建集群（分配槽）
redis-cli --cluster create \
    127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 \
    127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384 \
    --cluster-replicas 1

# 4. 连接集群
redis-cli -c -p 6379

# 5. 查看集群状态
cluster info
cluster nodes
```

**扩容/缩容：**
```bash
# 添加节点
redis-cli --cluster add-node 新节点IP:6379 已有节点IP:6379

# 重新分配槽
redis-cli --cluster reshard 任意节点IP:6379

# 添加从节点
redis-cli --cluster add-node 新节点IP:6380 主节点IP:6379 --cluster-slave

# 下线节点
redis-cli --cluster del-node 节点IP:6379 节点ID
```

**集群的限制：**
- 不支持多 key 跨槽操作（但可以用 Hash Tag：`{user}:1:name`）
- 不支持事务（multi/exec）
- 不支持 Lua 脚本跨槽
- Pipeline 只能在单节点内使用

---

### Q13: 缓存淘汰策略有哪些？

**答：** 当 Redis 内存使用达到 `maxmemory` 时，根据配置的淘汰策略移除数据。

| 策略 | 说明 |
|------|------|
| **noeviction** | 不淘汰，写入报错（默认） |
| **allkeys-lru** | 从所有 key 中淘汰最近最少使用的（推荐） |
| **volatile-lru** | 从设置了过期时间的 key 中淘汰 LRU |
| **allkeys-lfu** | 从所有 key 中淘汰最不经常使用的（4.0+） |
| **volatile-lfu** | 从设置了过期时间的 key 中淘汰 LFU |
| **allkeys-random** | 从所有 key 中随机淘汰 |
| **volatile-random** | 从设置了过期时间的 key 中随机淘汰 |
| **volatile-ttl** | 淘汰即将过期的 key |

**LRU vs LFU：**
- **LRU（Least Recently Used）**：最近最少使用，按**时间**判断
- **LFU（Least Frequently Used）**：最不经常使用，按**频率**判断

```bash
# 配置
maxmemory 2gb
maxmemory-policy allkeys-lru
```

---

### Q14: 什么是慢查询？

**答：** 慢查询用于记录执行时间超过指定阈值的命令。

```bash
# 配置慢查询
config set slowlog-log-slower-than 10000  # 超过 10ms 记录（单位微秒）
config set slowlog-max-len 128            # 最多记录128条
config rewrite                            # 持久化配置

# 查看慢查询
slowlog get 10        # 获取最近10条
slowlog len           # 慢查询数量
slowlog reset         # 清空慢查询

# 输出格式
# 1) 日志ID  2) 时间戳  3) 耗时(微秒)  4) 命令和参数
```

---

### Q15: 什么是 Pipeline？有什么作用？

**答：** Pipeline 可以将多个 Redis 命令打包在一起，一次性发送给 Redis 服务器执行，减少网络往返次数（RTT）。

```python
import redis

conn = redis.Redis(host='127.0.0.1', port=6379)

# 不使用 Pipeline
for i in range(10000):
    conn.set(f'key_{i}', i)  # 10000 次网络往返

# 使用 Pipeline
pipe = conn.pipeline()
for i in range(10000):
    pipe.set(f'key_{i}', i)
pipe.execute()  # 一次性发送，大幅提升性能
```

**注意事项：**
- Pipeline 不是原子的，中间可能穿插其他客户端的命令
- 如果设置 `transaction=True`，相当于在 MULTI/EXEC 事务中（但不完全等价）
- 集群模式下 Pipeline 只能用于同一节点的 key

---

### Q16: 什么是发布订阅（Pub/Sub）？

**答：** 发布订阅是一种消息通信模式，发布者发布消息后，所有订阅该频道的订阅者都能收到。

```bash
# 原生
# 终端1：订阅
subscribe channel1 channel2

# 终端2：发布
publish channel1 "hello"

# 终端1会自动收到：
# 1) "message"
# 2) "channel1"
# 3) "hello"
```

```python
import redis

r = redis.Redis(host='127.0.0.1', port=6379)

# 发布者
r.publish('channel', '广播消息')

# 订阅者
sub = r.pubsub()
sub.subscribe('channel')
for message in sub.listen():
    print(message)  # {'type': 'message', 'channel': b'channel', 'data': b'...'}
```

**适用场景：** 实时通知、聊天消息推送

**缺点：** 消息没有持久化，订阅者不在线时消息会丢失，没有消息确认机制

---
