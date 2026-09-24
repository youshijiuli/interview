import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 8080))

while True:
    send_msg = input('请输入...').strip()
    client.send(send_msg.encode('utf-8'))
    data = client.recv(1024)
    print(data)
    if send_msg == 'Q':
        break

client.close()
