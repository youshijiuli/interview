import os,sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import server

class FTP():
    def __init__(self):
        pass
    def run(self):
        print('-------请先开启服务器--------')
        operate_list = [('开启服务端','start_server'),
                        ('退出','exit')]
        for id, item in enumerate(operate_list, 1):
            print(id, item[0])
        while True:
            func_str = operate_list[int(input('>>>')) - 1][1]
            if hasattr(self, func_str):
                getattr(self, func_str)()
            else:
                print('\033[1;31m请重新选择\033[0m')
    def start_server(self):
        """启动服务端"""
        print('-----start----')
        server_obj = server.TCPServer()
        server_obj.run()

    def exit(self):
        print('exit')
        exit()