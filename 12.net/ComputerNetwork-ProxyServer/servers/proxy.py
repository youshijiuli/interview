import os
import os.path as op
import pickle as pkl
import requests

from servers.base import BaseServer
from utils.loggers import Logger


class ProxyServer(BaseServer):
    def __init__(self, port: int = 8888, comm_num: int = 5):
        super(ProxyServer, self).__init__(port, comm_num)
        self.logger = Logger("proxy-server", add_console=True)
        self.cache_save_path = op.join(op.abspath(op.dirname(__file__)), "proxy_cache.pkl")
        if op.exists(self.cache_save_path):
            self.cache = pkl.load(open(self.cache_save_path, "rb"))  # dict type
        else:
            self.cache = {}

    def process(self, message):
        try:
            url = message.split()[1]
            self.logger.info("url:{}".format(url))
            if url in self.cache.keys():
                self.logger.info("cache HIT:{}".format(url))
                context = self.cache[url]  # NOTES value is str type
            else:
                self.logger.info("cache MISS:{}".format(url))
                proxies = {"http": "127.0.0.1:80"}
                self.logger.info("get web-server")
                res = requests.get(url, proxies=proxies)
                context = res.text
                self.cache[url] = context
            self.logger.info("rev context:{}".format(context))

            header = "HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: {}\n\n".format(
                len(context))
            send_msg = header.encode("utf-8")
            for i in range(0, len(context)):  # Send the content of the requested file to the client
                send_msg += context[i].encode()
            return send_msg
        except Exception:
            self.logger.error("process ERROR")
            header = "HTTP/1.1 404 Not Found"
            return header.encode("utf-8")

    def __del__(self):
        pkl.dump(self.cache, open(self.cache_save_path, "wb"))
        self.serverSocket.close()


if __name__ == '__main__':
    proxy_server = ProxyServer()
    proxy_server.run()
