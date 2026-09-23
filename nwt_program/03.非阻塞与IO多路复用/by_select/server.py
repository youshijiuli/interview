import socket
import select

# 创建socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8888))
server_socket.listen(5)

# 用于存储所有需要监控的socket
sockets_list = [server_socket]
# 存储客户端连接的信息
clients = {}

while True:
    # 调用select函数，等待文件描述符就绪
    read_sockets, write_sockets, error_sockets = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == server_socket:
            # 有新的客户端连接
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted new connection from {client_address}")
        else:
            try:
                # 接收客户端数据
                data = sock.recv(1024)
                if data:
                    print(f"Received message from {clients[sock]}: {data.decode('utf-8')}")
                    # 简单回显
                    sock.send(data)
                else:
                    # 客户端断开连接
                    sockets_list.remove(sock)
                    del clients[sock]
                    print(f"Connection closed from {clients[sock]}")
            except:
                # 处理异常，比如连接异常断开
                sockets_list.remove(sock)
                del clients[sock]
                print(f"Connection closed from {clients[sock]}")