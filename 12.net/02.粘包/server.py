import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8001))
sock.listen(5)
conn, addr = sock.accept()

# 固定读取4字节
header1 = conn.recv(4)
data_length1 = struct.unpack('i', header1)[0]  # 数据字节长度 2,1
has_recv_len = 0
data1 = b""
while True:
    # 判断数据长度，对比1024，大于1024那么就接受1024，多次接收
    length = data_length1 - has_recv_len
    if length > 1024:
        lth = 1024
    else:
        lth = length
    chunk = conn.recv(lth)  # 可能一次收不完，自己可以计算长度再次使用recv收取，指导收完为止。 1024*8 = 8196
    data1 += chunk
    has_recv_len += len(chunk)
    if has_recv_len == data_length1:  # 【已经达到目标数据长度就跳出循环】
        break
print(data1.decode('utf-8'))

# 固定读取4字节
header2 = conn.recv(4)
data_length2 = struct.unpack('i', header2)[0]  # 数据字节长度
data2 = conn.recv(data_length2)  # 长度
print(data2.decode('utf-8'))

conn.close()
sock.close()
