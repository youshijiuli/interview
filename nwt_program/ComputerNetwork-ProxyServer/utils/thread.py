import time

from threading import Thread, Event


class BaseThread(Thread):
    """线程基础类"""

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, target=self.target, args=args, kwargs=kwargs)
        self._not_pause = Event()
        self._not_pause.set()
        self._not_stop = Event()
        self._not_stop.set()

    def func(self):
        """功能函数"""
        pass

    def target(self):
        """线程函数"""
        while self._not_stop.is_set():
            self._not_pause.wait()
            self.func()

    def pause(self):
        """暂停"""
        self._not_pause.clear()

    def resume(self):
        """恢复"""
        self._not_pause.set()

    def stop(self):
        """退出函数。Thread不自带线程退出，新加一个退出函数用于线程退出"""
        self._not_pause.set()
        self._not_stop.clear()


class TestThread(BaseThread):
    def __init__(self, info):
        BaseThread.__init__(self)
        self.info = info

    def func(self):
        print("hello{}: {}".format(self.info, time.time()))
        time.sleep(0.1)


if __name__ == '__main__':
    tt1 = TestThread("xxx")
    tt1.start()
    tt2 = TestThread("yyy")
    tt2.start()

    time.sleep(1)
    tt1.pause()
    time.sleep(1)
    tt1.resume()
    time.sleep(1)
    tt2.stop()
    time.sleep(1)
    tt2.resume()
