import json
import socket

path = 'users.json'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('127.0.0.1', 8001))
server.listen(5)

with open(path, 'r', encoding='utf-8') as f:
    users = json.load(f)

while True:
    print('等待客户端连接...')
    client, addr = server.accept()
    print('客户端已连接:', addr)
    recv_msg = client.recv(1024)
    username, password = recv_msg.decode('utf-8').split('|')
    print(username, password, '----')
    if username == "Q":
        break

    if username in users:
        if users[username]['password'] == password:
            send_msg = 'login successfully!!!'
        else:
            send_msg = '用户名或者密码错误，登录失败！！'
    else:
        send_msg = '用户名不存在，请先注册'

    client.send(send_msg.encode('utf-8'))
client.close()