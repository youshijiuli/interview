import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 8001))

while True:
    username = input('请输入用户名：').strip()
    password = input('请输入密码：').strip()

    client.send((username + '|' + password).encode('utf-8'))

    if username == 'Q':
        break
    recv_msg = client.recv(1024)

    print(recv_msg.decode('utf-8'))

client.close()