# -*- encoding=utf-8 -*-


class BaseRequestHandler:
    def __init__(self, server, request, client_address):
        self.server = server
        self.request = request
        self.client_address = client_address

    def handle(self): #不需要做任何工作，主要由后面继承它的类去做相关工作
        pass

#功能：编码、解码、读写消息
class StreamRequestHandler(BaseRequestHandler):

    def __init__(self, server, request, client_address):
        BaseRequestHandler.__init__(self, server, request, client_address)

        self.rfile = self.request.makefile('rb')
        self.wfile = self.request.makefile('wb')
        self.wbuf = []

    # 编码
    # 字符串—>字节码
    def encode(self, msg):
        if not isinstance(msg, bytes):  #如果不是字节码就编码成字节码
            msg = bytes(msg, encoding='utf-8')
        return msg

    # 解码
    # 字节码—>字符串
    def decode(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode()
        return msg

    # 读消息
    def read(self, length):
        msg = self.rfile.read(length)
        return self.decode(msg)

    # 读取一行消息
    def readline(self, length=65536):  #65536是http请求报文的最大长度
        msg = self.rfile.readline(length).strip()
        return self.decode(msg)

    # 写消息
    #接受内容，然后写到缓存里面
    def write_content(self, msg):
        msg = self.encode(msg)  #把字符串转成字节码
        self.wbuf.append(msg)

    # 发送消息
    def send(self):
        for line in self.wbuf:
            self.wfile.write(line)
        self.wfile.flush()
        self.wbuf = []  #发送完之后清空缓冲区

    def close(self):
        self.wfile.close()
        self.rfile.close()
