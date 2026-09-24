# 粘包第一种： send的数据过大，大于对方recv的上限时，对方第二次recv时，会接收上一次没有recv完的剩余的数据。


# 服务端
import socket
import subprocess
import struct

phone = socket.socket()

phone.bind(('127.0.0.1', 8849))

phone.listen(2)  # listen 允许2个人链接,剩下的链接等待

while 1:
    conn, addr = phone.accept()  # 等待客户端连接我,阻塞的状态中
    # print(f'链接来了{conn,addr}')

    while 1:
        try:
            from_client_data = conn.recv(1024)

            if from_client_data.upper() == b'Q':  # 正常退出 服务端跟着关闭
                print('客户正常退出聊天了')
                break

            result = from_client_data.decode('utf-8')
            total_size = len(result)  # 查看字节
            print(f'总字节数:{total_size}')

            head_bytes = struct.pack('i', total_size)  # 1. 制作固定长度的报头  'i'固定四个报头

            conn.send(head_bytes)  # 2. 发送固定长度的报头

            conn.send(result)  # 3. 发送总数据

        except ConnectionResetError:  # 异常退出 会报错 写提示内容
            print('客户端链接中断了')
            break
    conn.close()
phone.close()