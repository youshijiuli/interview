# 生成器适配器

class CoroutineWrapper():
    """ 生成器协程适配器
    重写生成器的方法： send， next
    使生成器可以在调度器loop里面去执行
    """

    def __init__(self, loop, gen):
        # YieldLoop
        self.loop = loop
        # 生成器
        self.gen = gen
        # 生成器上下文
        self.context = None  
        pass

    def throw(self, tp, *rest):
        """ 抛出异常 """
        return self.gen.throw(tp, *rest)

    def close(self):
        return self.gen.close()
    
    def send(self, val):
        """ 重写生成器的send方法
            就是驱动 生成器执行完之后，再次添加到队列中
        """
        val = self.gen.send(val)
        self.context = val
        self.loop.add_runnables(self)

    def __next__(self):
        val = next(self.gen)
        self.context = val
        self.loop.add_runnables(self)

    def __getattr__(self, name):
        return getattr(self.gen, name)

    def __str__(self):
        """ 程序结束后，出现 Iteration异常，返回对象，就调用这个方法，返回 """
        return ('coroutinewarpper: {}, context: {}'.format(self.gen, self.context))
