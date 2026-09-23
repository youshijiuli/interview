# 协程调度器实现
from queue import deque
from wrapper import CoroutineWrapper

import functools
import inspect


def coroutine(func):
    """
        将一个 普通的生成器，封装为 CoroutineWrapper对象
    """
    # 这个工具的作用是 ，原函数调用 __name__ 返回的将是原来的函数名， 而不是wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        # 判断是否为一个生成器
        if inspect.isgenerator(gen):
            coro = CoroutineWrapper(YieldLoop(), gen)
            return coro
        else:
            raise RuntimeError("不是一个生成器")
    return wrapper

class YieldLoop():

    current = None 
    # 任务队列
    runnables = deque()

    def __new__(cls, *args, **kwargs):
        """ 单例模式 """
        if not hasattr(YieldLoop, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        
        return cls._instance


    def __init__(self):
        pass

    @classmethod
    def instance(self):
        return YieldLoop()

    # def instance(cls):
    #     """ 单例模式 """
    #     if not YieldLoop.current:
    #         YieldLoop.current = YieldLoop()
    #     return YieldLoop.current

    def add_runnables(self, coro):
        self.runnables.append(coro)


    def add_coroutine(self, coro):
        """ 添加协程到队列 """
        # TODO 对类型进行判断
        assert isinstance(coro, CoroutineWrapper), 'isinstance(coro) != CoroutineWrapper'
        self.add_runnables(coro)
    

    def run_coroutine(self, coro):
        """ 执行协程 """
        try:
            coro.send(coro.context)
        except StopIteration as e:
            print("coroutine {} stop.".format(coro))

    
    def run_until_complete(self):
        """ ，从队列里面取协程去调度，去执行 """
        while YieldLoop.runnables:
            coro = YieldLoop.runnables.popleft()
            self.run_coroutine(coro)
   
