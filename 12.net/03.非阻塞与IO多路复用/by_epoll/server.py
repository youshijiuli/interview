import socket
import select

# 创建socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8888))
server_socket.listen(5)
server_socket.setblocking(False)  # 设置为非阻塞模式

# 创建epoll对象
epoll = select.epoll()
# 注册server_socket，关注读事件
epoll.register(server_socket.fileno(), select.EPOLLIN)

# 用于存储客户端连接的信息
clients = {}

while True:
    # 等待事件发生，返回就绪的文件描述符列表
    events = epoll.poll(1)
    for fileno, event in events:
        if fileno == server_socket.fileno():
            # 有新的客户端连接
            client_socket, client_address = server_socket.accept()
            client_socket.setblocking(False)
            # 注册新客户端socket，关注读事件