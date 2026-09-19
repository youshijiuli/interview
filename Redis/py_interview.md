##### 什么是codis
* Codis 是一个分布式 Redis 解决方案, 对于上层的应用来说, 连接到 Codis Proxy 和连接原生的 Redis Server 没有明显的区别 (有一些命令不支持), 上层应用可以像使用单机的 Redis 一样使用, Codis 底层会处理请求的转发, 不停机的数据迁移等工作, 所有后边的一切事情, 对于前面的客户端来说是透明的, 可以简单的认为后边连接的是一个内存无限大的 Redis 服务，当然，前段时间redis官方的3.0出了稳定版，3.0支持集群功能，codis的实现原理和3.0的集群功能差不多。

---

##### redis和memcached的区别
1. 存储方式：
    * Memecache把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小。Redis有部份存在硬盘上，这样能保证数据的持久性。
2. 数据支持类型
    * Memcache对数据类型支持相对简单。Redis有复杂的数据类型。
3. 使用底层模型不同
    * 它们之间底层实现方式 以及与客户端之间通信的应用协议不一样。Redis直接自己构建了VM 机制 ，因为一般的系统调用系统函数的话，会浪费一定的时间去移动和请求。
4. value大小
    * redis最大可以达到1GB，而memcache只有1MB

---

#####  redis中sentinel的作用
[参考链接](https://blog.csdn.net/qq2430/article/details/80679439)

* Redis Sentinel是一个用来监控redis集群中节点的状态，不用来存储数据。当集群中的某个节点有故障时，可以自动的进行故障转移的操作。通常为了保证sentinel的高可用，sentinel也会部署多个

---

##### 什么是Twemproxy

* Twemproxy是一种代理分片机制，由Twitter开源。Twemproxy作为代理，可接受来自多个程序的访问，按照路由规则，转发给后台的各个Redis服务器，再原路返回。该方案很好的解决了单个Redis实例承载能力的问题。当然，Twemproxy本身也是单点，需要用Keepalived做高可用方案。通过Twemproxy可以使用多台服务器来水平扩张redis服务，可以有效的避免单点故障问题。虽然使用Twemproxy需要更多的硬件资源和在redis性能有一定的损失（twitter测试约20%），但是能够提高整个系统的HA也是相当划算的。不熟悉twemproxy的同学，如果玩过nginx反向代理或者mysql proxy，那么你肯定也懂twemproxy了。其实twemproxy不光实现了redis协议

---

##### redis中watch的作用

> watch 用于在进行事务操作的最后一步也就是在执行exec 之前对某个key进行监视
> 如果这个被监视的key被改动，那么事务就被取消，否则事务正常执行.
> 一般在MULTI 命令前就用watch命令对某个key进行监控.如果想让key取消被监控，可以用unwatch命令

---

##### 什么是一致性哈希
[参考链接](https://www.jianshu.com/p/49e3fbf41b9b)

* 一致性哈希简称DHT,是麻省理工学院提出的一种算法，目前主要应用于分布式缓存当中。一致性哈希可以有效地解决分布式存储结构下动态增加和删除节点所带来的问题。

---

##### redis如何实现主从复制？以及数据同步机制？
* redis从主从结构可以采用一主多从或者级联结构，主从复制可以根据是否全量分为全量同步和增量同步。
* 全量同步：redis全量复制一般发生在slave初始化阶段，这时slave需要将master上的所有数据都复制一份步骤如下：
    - 从服务器连接主服务器，发送SYNC命令； 
    - 主服务器接收到SYNC命名后，开始执行BGSAVE命令生成RDB文件并使用缓冲区记录此后执行的所有写命令； 
    - 主服务器BGSAVE执行完后，向所有从服务器发送快照文件，并在发送期间继续记录被执行的写命令； 
    - 从服务器收到快照文件后丢弃所有旧数据，载入收到的快照； 
    - 主服务器快照发送完毕后开始向从服务器发送缓冲区中的写命令； 
    - 从服务器完成对快照的载入，开始接收命令请求，并执行来自主服务器缓冲区的写命令；
* 增量同步：
    * Redis增量复制是指Slave初始化后开始正常工作时主服务器发生的写操作同步到从服务器的过程。 增量复制的过程主要是主服务器每执行一个写命令就会向从服务器发送相同的写命令，从服务器接收并执行收到的写命令。
* Redis主从同步策略
    * 主从刚刚连接的时候，进行全量同步；全同步结束后，进行增量同步。当然，如果有需要，slave 在任何时候都可以发起全量同步。redis 策略是，无论如何，首先会尝试进行增量同步，如不成功，要求从机进行全量同步

---

##### redis如何实现事务
[参考链接](https://blog.csdn.net/hxpjava1/article/details/79553073)

---

##### 如果redis中的某个列表中的数据量非常大，如何实现循环显示每一个值？
* 使用生成器一个一个取

---

##### redis是单进程单线程的吗？
* Redis采用的是基于内存的采用的是单进程单线程模型的KV数据库

---

##### 如何基于redis实现发布和订阅
[参考链接](https://www.jianshu.com/p/c4d7255425da)

```python
# 发布者
#coding:utf-8import time
import redis

number_list = ['300033', '300032', '300031', '300030']
signal = ['1', '-1', '1', '-1']

rc = redis.StrictRedis(host='***', port='6379', db=3, password='********')
for i in range(len(number_list)):
    value_new = str(number_list[i]) + ' ' + str(signal[i])
    rc.publish("liao", value_new)  #发布消息到liao
```
```python
# 订阅者
#coding:utf-8import time
import redis

rc = redis.StrictRedis(host='****', port='6379', db=3,     password='******')
ps = rc.pubsub()
ps.subscribe('liao')  #从liao订阅消息for item in ps.listen():        #监听状态：有消息发布了就拿过来
    if item['type'] == 'message':
        print item['channel']
        print item['data']
```

---

##### redis中默认有多少个哈希槽
* 2^14个
* Redis 集群没有使用一致性hash, 而是引入了哈希槽的概念。

---

##### [redis常见的面试问题参考](https://www.cnblogs.com/Survivalist/p/8119891.html)

---

##### 简述redis的有几种持久化策略以及比较？

* RDB 持久化可以在指定的时间间隔内生成数据集的时间点快照。
* AOF 持久化记录服务器执行的所有写操作命令，并在服务器启动时，通过重新执行这些命令来还原数据集。 AOF 文件中的命令全部以 Redis 协议的格式来保存，新命令会被追加到文件的末尾。 Redis 还可以在后台对 AOF 文件进行重写(rewrite)，使得 AOF 文件的体积不会超出保存数据集状态所需的实际大小。
* 区别：
    *     RDB持久化是指在指定的时间间隔内将内存中的数据集快照写入磁盘，实际操作过程是fork一个子进程，先将数据集写入临时文件，写入成功后，再替换之前的文件，用二进制压缩存储。
    * AOF持久化以日志的形式记录服务器所处理的每一个写、删除操作，查询操作不会记录，以文本的方式记录，可以打开文件看到详细的操作记录。

---

##### 如何保证redis中的数据都是热点数据

* redis 内存数据集大小上升到一定大小的时候，就会施行数据淘汰策略。redis 提供 6种数据淘汰策略：
    * volatile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
    * volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
    * volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
    * allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
    * allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
    * no-enviction（驱逐）：禁止驱逐数据

---

##### 如何高效的找到redis中所有以felix开头的key
* scan 0 match felix* count 5
* 表示从游标0开始查询felix开头的key，每次返回5条，但是这个5条不一定

---

##### 列举redis支持的过期策略
* 定时删除
    * 在设置key的过期时间的同时，为该key创建一个定时器，让定时器在key的过期时间来临时，对key进行删除
* 惰性删除
    * key过期的时候不删除，每次从数据库获取key的时候去检查是否过期，若过期，则删除，返回null。
* 定期删除
    * 每隔一段时间执行一次删除(在redis.conf配置文件设置hz，1s刷新的频率)过期key操作

---

##### 如何实现redis集群
[参考链接](https://blog.csdn.net/truelove12358/article/details/79612954)

1. Twitter开发的twemproxy
2. 豌豆荚开发的codis
3. redis官方的redis-cluster

---

##### redis默认多少个db
* 默认有16个数据库
