# 客户端
import socket
import struct

phone = socket.socket()

phone.connect(('127.0.0.1', 8849))

while 1:
    to_server_data = input('>>>').strip().encode('utf-8')
    if not to_server_data:  # 服务端如果收到了空的内容,服务端就会一直阻塞中.无论是那一端发送,都不能为空
        print('发送内容不能为空')
        continue

    phone.send(to_server_data)
    if to_server_data.upper() == b'Q':  # 判断如果是Q的话就退出,正常退出
        break

    head_bytes = phone.recv(4)  # 1. 接收报头

    total_size = struct.unpack('i', head_bytes)[0]  # 2. 反解报头 'i'固定四个报头

    total_data = b''  # 接收内容,依次相加bytes类型,如果只是英文可以不加ASCII码

    while len(total_data) < total_size:
        total_data += phone.recv(1024)

    print(len(total_data))
    print(total_data.decode('gbk'))

phone.close()