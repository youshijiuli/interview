from socket import *

server = socket(AF_INET, SOCK_STREAM)

server.bind(('127.0.0.1', 8001))
server.listen(5)
print('waiting for connect...')
while True:
    conn, addr = server.accept()
    print('connect from', addr)

    while True:
        try:
            data = conn.recv(1024)
            if len(data) == 0: break
            if data.decode('utf-8') == 'Q': break
            print(data,type(data)) # 字节

            conn.send(data.decode('utf-8').upper().encode('utf-8'))
        except Exception as error:
            break
    conn.close()
    break