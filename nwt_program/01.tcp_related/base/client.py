import socket

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)

client.connect(('127.0.0.1', 8001))

client.send('hello world'.encode('utf-8'))

data = client.recv(1024)

print(data) # b'HELLO WORLD'

client.close()