from server.conf.settings import SERVER_DB_PATH as db_path
from server.conf.settings import SERVER_HOME_PATH as home_path
from server.conf.settings import SERVER_HOME_PATH as home_path
from server.bin.common import progress as pgs
import socketserver
import os
import pickle
import subprocess
import hashlib
import struct
# 服务器类
class MyServer(socketserver.BaseRequestHandler):
    userinfopath = os.path.join(db_path,'user_info')
    user_info_dict = {}
    user_state = {}
    def handle(self):
        '''运行函数'''
        print('server runing ...')
        while True:
            try:
                client_data = self.server_recv_data()
                cmd = client_data['cmd']
                print('用户[%s]信息请求信息 [%s]...'%(client_data['username'],cmd))
                if hasattr(self,cmd):
                    func = getattr(self,cmd)
                    func(client_data)
            except ConnectionError:
                pass

    def _register(self,dic):
        '''注册功能'''
        username = dic['username']
        if not username in self.user_info_dict:
            self.user_info_dict[username] = {
                'username':username
                ,'password':dic['password']
                ,'dirtotalsiez':100*1024
                ,'dirusablesize':100*1024
                ,'userhome':'home\\%s'%username
                , 'cdpath': None
            }
            self.user_state = self.user_info_dict[username]
            self.user_state['userstate'] = True
            self.server_send_data(self.user_state)
            # 注册成功后创建加目录文件夹
            if not os.path.isdir(os.path.join(home_path,username)):
                os.mkdir(os.path.join(home_path,username))
            print('用户[%s] 注册成功！'%username)
        else:
            self.server_send_data({'usehome':None,'userstate':False})

        print('用户字典数据',self.user_info_dict)

    def _login(self,dic):
        '''登录功能'''
        if dic['username'] in self.user_info_dict and dic['password'] == self.user_info_dict[dic['username']]['password']:
            print('用户[%s] 登录成功！'%dic['username'])
            self.user_state = self.user_info_dict[dic['username']]
            self.user_state['userstate'] = True
            self.server_send_data(self.user_state)
        else:
            self.server_send_data({'usehome':None,'userstate':False})


    def _get(self):
        '''下载发送数据'''

    def _put(self):
        '''上传接收数据'''

    def _mkdir(self,dic):
        '''创建文件夹'''
        # 2021年5月1日22:29:39 创建文件夹 和创建文件可优化代码
        userpath = os.path.join(home_path,self.user_state['username'])
        filepath = os.path.join(userpath,dic['filesname'])
        if self.user_state['cdpath'] != None:
            cdpath = os.path.join(home_path, self.user_state['cdpath'])
            filepath = os.path.join(cdpath, dic['filesname'])
            if not os.path.isdir(filepath):
                os.mkdir(filepath)
                dic['mkdirname'] = dic['filesname']
                dic['mkdirstate'] = True
                dic['mkdirpath'] = filepath
            return self.server_send_data(dic)
        if not os.path.isdir(filepath) :
            # 判断文件路径是否存在，不存在创建文件夹
            os.mkdir(filepath)
            dic['mkdirname'] = dic['filesname']
            dic['mkdirstate'] = True
            dic['mkdirpath'] = filepath
            self.server_send_data(dic)
        else:
            dic['mkdirstate'] = False
            self.server_send_data(dic)
    def _found(self):
        '''创建文件'''

    def _size(self):
        '''查看空间大小'''

    def _dir(self):
        '''查看用户文件夹信息'''

    def _del(self,dic):
        '''删除文件'''
        try:
            filepath = os.path.join(home_path,dic['filesname'])
            if os.path.isfile(filepath):
                print('用户[%s],删除文件[%s]'%(self.user_state['username'],dic['filesname']))
                dic['filestate'] = True
                os.remove(filepath)
                self.server_send_data(dic)
            else:
                dic['filestate'] = False
            self.server_send_data(dic)
        except FileNotFoundError:
                dic['filestate'] = False
                self.server_send_data(dic)
    def dirsize(self,*args):
        '''遍历用户家目录所有文件大小'''
        name_list = os.listdir(args[0])
        size = 0
        for i in name_list:
            j = '%s\%s'%(args[0],i)
            if os.path.isdir(j):
                size += self.dirsize(j)
            else:
                size += os.path.getsize(j)
        return size

    def _cd(self,dic):
        '''切换目录'''
        cdpath = os.path.join(home_path, dic['cd'])
        if os.path.dirname(cdpath):
            dic['cdpath'] = 'home\\%s'%dic['cd']
            self.user_state['cdpath'] = '%s'%dic['cd']
        else:
            dic['cdpath'] = False
        self.server_send_data(dic)


    def send_cuteftp(self,dic):
        '''断点续传发送数据'''


    def recv_cuteftp(self):
        '''断点续传接收数据'''


    def getmd5(self):
        '''获取MD5值'''

    def filemd5(self):
        '''获取文件MD5值'''

    def filedict(self):
        '''文件信息字典'''

    def getdirsize(self):
        '''获取用户目录空间大小'''

    def filestate(self):
        '''文件状态信息'''

    def sendfiledata(self):
        '''发送文件数据'''

    def recvfiledata(self):
        '''接收文件数据'''

    def server_send_data(self,dic):
        '''服务端发送报头数据'''

        head_data = pickle.dumps(dic)
        head_struct = struct.pack('i', len(head_data))
        self.request.send(head_struct)
        self.request.send(head_data)
    def server_recv_data(self):
        '''服务端发送报头数据'''
        head_struct = self.request.recv(4)
        head_data = struct.unpack('i', head_struct)[0]
        return pickle.loads(self.request.recv(head_data))

    def userverify(self):
        '''校验用户登录状态'''

    def userdict(self,dic):
        '''抽取单独用户信息'''

    def save_data(self,dic):
        '''保存用户信息字典'''

    def import_data(self):
        '''导入用户信息字典'''

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',9999),MyServer)
    server.serve_forever()