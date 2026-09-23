#继承TCPServer

from server.socket_server import TCPServer

class BaseHTTPServer(TCPServer):

    def __init__(self,server_address,handler_class):
        TCPServer.__init__(self,server_address,handler_class)

