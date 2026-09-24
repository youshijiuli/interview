import threading
import socket
import time

from server.socket_server import TCPServer
from handler.base_handler import StreamRequestHandler


class TestBaseRequestHandler(StreamRequestHandler):

    #实现一些具体的处理逻辑
    #实现Echo
    def handle(self):
        msg = self.readline()
        print('Server recv msg: ' + msg)
        time.sleep(1) #模拟每个客户端的处理都需要花费1s的时间
        self.write_content(msg)
        self.send()

#测试SocketServer(TCPServer)
class SocketServerTest:

    def run_server(self):
        tcp_server = TCPServer(('127.0.0.1',8888),TestBaseRequestHandler)
        tcp_server.serve_forever()

    #客户端的具体连接逻辑
    def client_connect(self):
        client = socket.socket()
        client.connect(('127.0.0.1',8888))
        client.send(b'Hello TCPServer\r\n')
        msg = client.recv(1024)
        print('Client recv msg: ' + msg.decode())

    #生成num个客户端
    def gen_clients(self,num):
        clients = []
        for i in range(num):
            client_thread = threading.Thread(target=self.client_connect) #新建不同的线程去连接客户端
            clients.append(client_thread)
        return clients
    
    def run(self):
        #先把服务端跑起来
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        #生成10个客户端
        clients = self.gen_clients(10)
        for client in clients:
            client.start()
        
        server_thread.join()
        for client in clients:
            client.join()


if __name__ == '__main__':
    SocketServerTest().run()