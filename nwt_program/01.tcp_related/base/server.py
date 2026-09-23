import socket

phone = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)

phone.bind(('127.0.0.1', 8001))

phone.listen(5)

conn, addr = phone.accept()

data = conn.recv(1024)

print('客户端发数据是：', data) # 客户端发数据是： b'hello world'

conn.send(data.upper())

conn.close()
phone.close()