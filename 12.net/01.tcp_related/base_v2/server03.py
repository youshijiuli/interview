import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('127.0.0.1', 9000))
    server.listen(5)
    print('服务器启动，监听端口9000...')

    try:
        while True:
            with server.accept()[0] as conn:
                print(f'客户端 {conn.getpeername()} 已连接')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f'收到: {data.decode("utf-8")}')
                    conn.send(data.upper())

    except KeyboardInterrupt:
        print('\n服务器被用户中断')