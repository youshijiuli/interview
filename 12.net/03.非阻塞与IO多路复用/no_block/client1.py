import socket

client = socket.socket()
client.connect(('127.0.0.1', 9999))

while True:
    msg = input(">>>")
    if msg != 'q':
        client.send(msg.encode())
        data = client.recv(1024)
        print('收到的数据{}'.format(data.decode()))
    else:
        client.close()
        print('close client socket')
        break