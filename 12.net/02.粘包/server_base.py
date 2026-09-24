import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8001))
sock.listen(5)
conn, addr = sock.accept()

# 固定读取4字节
header1 = conn.recv(4)
print(header1)
data_length1 = struct.unpack('i', header1)[0]  # 数据字节长度
data1 = conn.recv(data_length1)

print(data1.decode('utf-8'))

# 固定读取4字节
header2 = conn.recv(4)
print(header2)
data_length2 = struct.unpack('i', header2)[0]  # 数据字节长度
data2 = conn.recv(data_length2)  # 长度
print(data2.decode('utf-8'))

conn.close()
sock.close()

# b'\r\x00\x00\x00'
# alex正在吃
# b'\x03\x00\x00\x00'
# 翔