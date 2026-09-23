import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)
print('服务器启动，监听端口9000...')

# 用于控制服务器运行的标志
running = True


def handle_client(conn, addr):
    print(f'客户端 {addr} 已连接')
    try:
        while running:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f'来自 {addr}: {message}')
            conn.send(data.upper())
    except Exception as e:
        print(f'处理客户端 {addr} 时出错: {e}')
    finally:
        conn.close()
        print(f'客户端 {addr} 已断开')


try:
    while running:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

except KeyboardInterrupt:
    print('\n服务器被用户中断')
finally:
    running = False  # 通知所有线程停止
    server.close()
    print('服务器已关闭')