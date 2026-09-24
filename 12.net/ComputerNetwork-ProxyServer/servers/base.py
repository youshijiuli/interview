from socket import *


class BaseServer(object):
    def __init__(self, port: int = 80, comm_num: int = 5):
        # Prepare a sever socket
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', port))  # bind port
        self.serverSocket.listen(comm_num)  # max comm num 5

        self.logger = None

    def receive(self, connectionSocket, addr):  # -> Tuple[socket, str]
        """接收"""
        try:
            message = connectionSocket.recv(1024).decode()  # 获取客户发送的报文
            self.logger.info("RECEIVE:SUCCESS\n{}".format(message.replace("\n", "")))
            return connectionSocket, str(message)
        except IOError:
            self.logger.error("RECEIVE:ERROR")
            return connectionSocket, "__RECEIVE_ERROR__"

    def process(self, message):  # -> bytes
        """处理"""
        pass

    def send(self, connectionSocket, message):  # -> None
        """发送"""
        try:
            connectionSocket.send(message)
            self.logger.info("SEND:SUCCESS\n{}".format(message.decode("utf-8")))
            connectionSocket.close()
        except IOError:
            self.logger.error("SEND:ERROR\n{}".format(message.decode("utf-8")))
            connectionSocket.close()

    def response(self):  # -> None
        """回复"""
        connectionSocket, addr = self.serverSocket.accept()
        self.logger.info("CONNECTED")
        connectionSocket, message = self.receive(connectionSocket, addr)
        send_msg = self.process(message)
        self.send(connectionSocket, send_msg)
        self.logger.info("FINISHED")

    def run(self):  # -> None
        """运行"""
        while True:
            self.response()

    def __del__(self):
        self.serverSocket.close()
