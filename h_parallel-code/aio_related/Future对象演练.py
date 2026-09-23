# Future对象的实现原理

class Future():

    def __init__(self, loop):
        # 标记任务是否已经完成了
        self.done = False
        # 引用的协程 
        self.co = None
        self.loop = loop
        
    def set_coroutine(self, co):
        """ 添加协程 """
        self.co = co

    def set_done(self):
        """ 添加标记, 设置已完成 """
        self.done = True
    
    # await <可等待对象>
    def __await__(self):
        if not self.done:
            yield self
        return 


class SocketWrapper():
    """ 套接字协程适配器
        非阻塞 io
    """

    def __init__(self, sock, loop):
        sock.setblocking(False)
        # sock 套接字
        self.sock = sock
        # 事件循环
        self.loop = loop
    
    def fileno(self):
        return self.sock.fileno()

    def creat_future_for_events(self, events):
        """
        1. 为套接字创建future
        2. register_handler
        """
        future = self.loop.create_future()

        def handler():
            """ 可等待对象完成， 在epoll调用之后，事件就绪 """
            future.set_done()
            self.loop.unregister_handler(self.fileno())
            if future.co:
                self.loop.add_coroutine(future.co)

        self.loop.register_handler(self.fileno(), events, handler)
        return future


    async def accept(self): 
        while True:
            print("接收链接，创建套接字")
            try:
                sock, addr = self.sock.accept()
                return SocketWrapper(sock=sock, loop=self.loop), addr
            except BlockingIOError:
                future = self.creat_future_for_events(select.EPOLLIN)
                await future 

    async def recv(self, backlog):
        while True:
            try:
                return self.sock.recv(backlog)
            except BlockingIOError:
                future = self.creat_future_for_events(select.EPOLLIN)
                await future


    async def send(self, data):
        print(123123)
        while True:
            try:
                print("执行到这里了send")
                return self.sock.send(data)
            except BlockingIOError:
                future = self.creat_future_for_events(select.EPOLLOUT)
                await future 


import select
import socket
from queue import deque

class EventLoop():

    current = None
    runnables = deque()
    epoll = select.epoll()
    # 维护 文件描述符 到 回调处理函数的 关系
    handlers = {}


    def __new__(cls, *args, **kwargs):
        """ 单例模式 """
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod    
    def instance(self):
        return EventLoop()


    def register_handler(self, fileno, events, handler):
        """ 注册文件描述符 """
        self.handlers[fileno] = handler
        self.epoll.register(fileno, events)


    def unregister_handler(self, fileno):
        """ 删除一个已注册的文件描述符 """ 
        self.epoll.unregister(fileno)
        self.handlers.pop(fileno)
        

    def run_coroutine(self, co):
        try:
            print("执行 run_coroutine")
            # 和生成器send一样
            # 进行协程的一次调度
            future = co.send(None)
            print("qqqqqqqqqqqq")
            future.set_coroutine(co)
        except Exception as e:
            print(e)
            print('coroutine {} stoped'.format(co.__name__))


    def run_forever(self):
        """ 循环执行 """
        while True:
            # 先把队列中可执行的执行了：比如开始时执行一下 监听套接字
            while self.runnables:
                print("执行了 run_forever")
                self.run_coroutine(co=self.runnables.popleft())
            print("=====+")
            events = self.epoll.poll(1)
            for fileno, event in events:
                # 回调
                handler = self.handlers.get(fileno)
                handler()
            pass
    
    def create_future(self):
        """ 创建可等待对象 """
        return Future(loop=self)

    def create_listen_socket(self, ip='127.0.0.1', port=7890):
        """ 创建监听套接字 """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
        # print(SocketWrapper(sock=server, loop=self))

        return SocketWrapper(sock=server, loop=self)


    def add_coroutine(self, co):
        """ 任务队列添加协程 """
        print("添加任务到队列")
        self.runnables.append(co)


class TcpServer():
    """ 协程网络服务器 """

    def __init__(self, loop):
        self.loop = loop
        self.listen_sock = self.loop.create_listen_socket()
        self.loop.add_coroutine(self.serve_forever())


    async def handle_client(self, sock):
        while True:
            data = await sock.recv(1024)
            if not data:
                print('client disconnected')
                break
            await sock.send(data.upper())
    

    async def serve_forever(self):
        while True:
            print("等待链接")
            sock, addr = await self.listen_sock.accept()
            print(123)
            print("client connect addr = {}".format(addr))
            self.loop.add_coroutine(self.handle_client(sock))


if __name__ == '__main__':
    loop = EventLoop.instance()
    server = TcpServer(loop)

    loop.run_forever()

