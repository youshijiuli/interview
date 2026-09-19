# python-面试通关宝典

### **并发**

#### 151.举例说明 conccurent.future 的中线程池的用法。

```python
concurrent.futures模块的基础是Exectuor，Executor是一个抽象类，它不能被直接使用。但是它提供的两个子类ThreadPoolExecutor和ProcessPoolExecutor却是非常有用，顾名思义两者分别被用来创建线程池和进程池的代码。我们可以将相应的tasks直接放入线程池/进程池，不需要维护Queue来操心死锁的问题，线程池/进程池会自动帮我们调度。
example1.py


from
concurrent.futures
import
ThreadPoolExecutor


import
time


def
return_future_result(message):


    time.sleep(2)


    return
message


pool
=
ThreadPoolExecutor(max_workers=2)  #
 创建一个最大可容纳2个task的线程池


future1
=
pool.submit(return_future_result,
("hello"))  #
 往线程池里面加入一个task


future2
=
pool.submit(return_future_result,
("world"))  #
 往线程池里面加入一个task


print(future1.done())  #
 判断task1是否结束


time.sleep(3)


print(future2.done())  #
 判断task2是否结束


print(future1.result())  #
 查看task1返回的结果


print(future2.result())  #
 查看task2返回的结果
```

#### 152.说一说多线程，多进程 和 协程 的区别。

```
这个问题虽然被问烂了，但是还是可能会问，不过网上都是答案，搜搜看下就行
```

#### 153.简述 GIL。

```
在CPython解释器中，全局解释锁GIL是在于执行Python字节码时为了保护访问Python对象而阻止多个线程执行的一把互斥锁。这把锁的存在在主要是因为CPython解释器的内存管理不是线程安全的。然而直到今天GIL依旧存在，现在的很多功能已经习惯于依赖它作为执行的保证
由于GIL的存在，当线程被操作系统唤醒后，必须拿到GIL锁后才能执行代码，也就是说同一时刻永远只有一个线程在执行，这就导致如果我们的程序是CPU密集运算型的任务，那么使用Python多线程是不能提高效率的
```

#### 154.进程之间如何通信？

```
共享内存，信号量，互斥锁，消息队列等
```

#### 155.IO 多路复用的作用？

```
I/O多路复用就通过一种机制，可以监视多个描述符，一旦某个描述符就绪（一般是读就绪或者写就绪），能够通知程序进行相应的读写操作。但select，poll，epoll本质上都是同步I/O，因为他们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的，而异步I/O则无需自己负责进行读写，异步I/O的实现会负责把数据从内核拷贝到用户空间
```

#### 156.select、poll 和 epoll 模型的区别。

```
可参考这篇博文，https://www.cnblogs.com/Anker/p/3265058.html
```

#### 157.什么是并发和并行？

```
并发的实质是一个物理CPU(也可以多个物理CPU) 在若干道程序之间多路复用，并发性是对有限物理资源强制行使多用户共享以提高效率
并行”指两个或两个以上事件或活动在同一时刻发生。在多道程序环境下，并行性使多个程序同一时刻可在不同CPU上同时执行
```

#### 158.解释什么是异步非阻塞？

```
当一个异步过程调用发出后，调用者不会立刻得到结果。
实际处理这个调用的部件是在调用发出后，
通过状态、通知来通知调用者，或通过回调函数处理这个调用
非阻塞的意思是，不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回
```

#### 159.简述 threading.local 的作用。

```
Python提供了 threading.local 类，将这个类实例化得到一个全局对象，但是不同的线程使用这个对象存储的数据其它线程不可见(本质上就是不同的线程使用这个对象时为其创建一个独立的字典)
```

---

# python-面试通关宝典

### **网络编程**

#### 148.TCP 和 UDP 的区别有哪些？

```markdown
TCP协议和UDP协议特性区别总结：
     1. TCP协议在传送数据段的时候要给段标号；UDP协议不
     2. TCP协议可靠；UDP协议不可靠
     3. TCP协议是面向连接；UDP协议采用无连接
     4. TCP协议负载较高，采用虚电路；UDP采用无连接
     5. TCP协议的发送方要确认接收方是否收到数据段（3次握手协议）
     6. TCP协议采用窗口技术和流控制
```

#### 149.简要介绍三次握手和四次挥手。

```p
https://mp.weixin.qq.com/s/jLkhjM7wOpZuWgJdAXis1A
这篇博文讲的不错，可以参考一下

另外，time_wait状态的作用在面试中也是常问的，可以参考下面这篇，https://www.iteblog.com/archives/169.html
```

#### 150.什么是粘包？ socket 中造成粘包的原因是什么？ 哪些情况会发生粘包现象？

```
基于TCP的socket编程中，发送端为了将多个发往接收端的包，更有效的发到对方，使用了优化方法（Nagle算法），将多次间隔较小、数据量小的数据包，合并成一个大的数据包发送(把发送端的缓冲区填满一次性发送)

造成粘包的原因：
1 发送端需要等缓冲区满才发送出去，造成粘包
2 接收方不及时接收缓冲区的包，造成多个包接收

```
