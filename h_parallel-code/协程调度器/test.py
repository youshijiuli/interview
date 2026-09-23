# 编写协程测试用例

# 求等差数列
import random
import string
import time
from queue import deque
from loop import coroutine, YieldLoop

@coroutine
def test1():
    sum = 0
    # 1-10000 所有奇数的和
    for i in range(1, 10001, 2):
        sum += yield i

    print('sum = ', sum)

YieldLoop.instance().add_coroutine(test1())
# YieldLoop.instance().run_until_complete()



# 生产者消费者模型

@coroutine
def producer(q):
    while True:
        good = ''.join(random.sample(string.ascii_letters+string.digits, 8))
        q.append(good)
        cnt = len(q)
        print('producer produce good. cnt = ',cnt)
        if cnt > 0:
            yield 

@coroutine
def consumer(q):
    while True:
        while len(q) <= 0:
            print("q is empty!")
            yield
        good = q.popleft()
        print('consumer consum good = {}, cnt = {}'.format(good, len(q))) 
        time.sleep(1)

# 产品队列， 作用于生产者 和 消费者
q = deque()
# 可以多个生产者，多个消费者调度
YieldLoop.instance().add_coroutine(producer(q))
YieldLoop.instance().add_coroutine(producer(q))
YieldLoop.instance().add_coroutine(producer(q))
YieldLoop.instance().add_coroutine(consumer(q))
YieldLoop.instance().add_coroutine(consumer(q))
YieldLoop.instance().run_until_complete()




