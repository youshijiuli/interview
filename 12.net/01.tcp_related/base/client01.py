import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',8001))


while True:
    message = input('请输入消息:').strip()
    if message == 'Q':
        break
    client.send(message.encode('utf-8'))
    data = client.recv(1024)
    print(data)