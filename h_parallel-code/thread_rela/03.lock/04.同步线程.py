import threading

# from threading import Condition
"""
1.__enter__ 以及 __exit__ 上下文管理器 with
2.wait() --> 等待
3.notify() --> 唤醒
"""


class XiaoAi(threading.Thread):
    def __init__(self, mutex, cond):
        super().__init__(name="小爱同学")
        self.mutex = mutex
        self.cond = cond

    def run(self):
        # self.mutex.acquire()
        # print(f"{self.name}:在")
        # self.mutex.release()
        #
        # self.mutex.acquire()
        # print(f"{self.name}:你猜猜现在几点了")
        # self.mutex.release()

        # 加锁
        with self.cond:
            # 1.等待
            self.cond.wait()
            print(f"{self.name}:在")

            # 4.唤醒
            self.cond.notify()

            # 5.等待
            self.cond.wait()
            print(f"{self.name}:你猜猜现在几点了")

            # 9.唤醒
            self.cond.notify()


class TianMao(threading.Thread):
    def __init__(self, mutex, cond):
        super().__init__(name="天猫精灵")
        self.mutex = mutex
        self.cond = cond

    def run(self):
        # self.mutex.acquire()
        # print(f"{self.name}:小爱同学")
        # self.mutex.release()
        #
        # self.mutex.acquire()
        # print(f"{self.name}:现在几点了?")
        # self.mutex.release()

        # 加锁
        with self.cond:
            print(f"{self.name}:小爱同学")
            # 2.唤醒
            self.cond.notify()

            # 3.等待
            self.cond.wait()
            print(f"{self.name}:现在几点了?")

            # 6.唤醒
            self.cond.notify()

            # 8.等待
            self.cond.wait()


if __name__ == '__main__':
    # 1.加锁
    mutex = threading.RLock()

    # 2.线程同步
    cond = threading.Condition()

    xa = XiaoAi(mutex, cond)
    tm = TianMao(mutex, cond)

    xa.start()
    tm.start()
