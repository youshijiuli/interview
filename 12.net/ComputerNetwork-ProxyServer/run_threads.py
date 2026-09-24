import time

import requests

from utils.thread import BaseThread
from servers.web_server import WebServer
from servers.proxy import ProxyServer


class WebServerThread(BaseThread):
    def __init__(self):
        BaseThread.__init__(self)
        self.web_server = WebServer()

    def func(self):
        self.web_server.response()


class ProxyServerThread(BaseThread):
    def __init__(self):
        BaseThread.__init__(self)
        self.proxy_server = ProxyServer()

    def func(self):
        self.proxy_server.response()


class ClientThread(BaseThread):
    def __init__(self):
        BaseThread.__init__(self)

    def func(self):
        proxies = {
            "http": "127.0.0.1:8888"
            # "http":"127.0.0.1:80"
        }
        r = requests.get("http://127.0.0.1/HelloWorld.html", proxies=proxies)
        time.sleep(0.1)
        print("Client Receive: ", r.text)
        time.sleep(1)


if __name__ == '__main__':
    ws = WebServerThread()
    ps = ProxyServerThread()
    cs = ClientThread()

    ws.start()
    ps.start()
    time.sleep(1)
    cs.start()
