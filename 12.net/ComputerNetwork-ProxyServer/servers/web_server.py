import os
import os.path as op

from servers.base import BaseServer
from utils.loggers import Logger


class WebServer(BaseServer):
    def __init__(self, port: int = 80, comm_num: int = 5):
        super(WebServer, self).__init__(port, comm_num)
        self.logger = Logger("web-server", add_console=True)

    def process(self, message):
        try:
            url = message.split()[1]
            self.logger.info("url:{}".format(url))
            if 'http' in url:
                filename = url.split('//')[1].partition('/')[2]
            else:
                filename = url
            self.logger.info("filename:{}".format(filename))
            with open(op.join(op.abspath(op.dirname(__file__)), filename), "r") as f:
                data = f.read()
                header = "HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: {}\n\n".format(
                    len(data))
                send_msg = header.encode("utf-8")
                # Send the content of the requested file to the client
                for i in range(0, len(data)):
                    send_msg += data[i].encode()
                return send_msg
        except Exception:
            self.logger.error("process ERROR")
            header = "HTTP/1.1 404 Not Found"
            return header.encode("utf-8")


if __name__ == '__main__':
    web_sever = WebServer()
    web_sever.run()
