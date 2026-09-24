import os
import pickle
import subprocess
import hashlib
import struct
import socket
# 客户端类

class MyClient:
    userstate = {"userstate":False}
    clietn_path = os.path.dirname(__file__)

    def __init__(self,ip_port):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.func_dic = {
            '1': ['注册功能', '_register']
            ,'2':['登录功能','_login']
            ,'3':['下载功能','_get']
            ,'4':['上传功能','_put']
            ,'5':['查看空间','_size']
            ,'6':['查看文件夹信息','_dir']
            ,'7':['创建文件夹','_mkdir']
            ,'8':['创建文件','_found']
            ,'9':['删除文件','_del']
            ,'10':['切换目录','_cd']
            ,'11':['退出','_quit']
            ,'12':['关闭服务器','_closeserver']
        }

        try:
            self.client.connect(ip_port)
        except Exception:
            self.client.close()

    def run(self):

        while True:
            try:
                print('欢迎使用FTP系统')
                for k, v in self.func_dic.items():
                    print(k, "", v[0])
                cmd = input('请输入指令：').strip()
                if not cmd.isdigit():continue
                if cmd in self.func_dic:
                    cmd = self.func_dic[cmd][1]
                    getattr(self,cmd)(cmd)

                else:
                    print('输入错误！')
            except Exception:
                continue


    def userdic(self,cmd,username,password):
        '''待发送用户信息字典'''
        user_dic = {
            'cmd':cmd
            ,'username':username
            ,'password':password
            ,'userstate':False
            ,'cdpath':None
        }
        return user_dic

    def filedic(self,cmd,inp):
        '''待发送文件信息字典'''
        dic = {
            'cmd':cmd
            ,'filesname':inp
            ,'username':self.userstate['username']
        }
        return dic

    def mk_found_file(self,cmd,inp):
        '''创建文件信息功能'''
        filedic = self.filedic(cmd, inp)
        self.client_send_data(filedic)
        server_data = self.client_recv_data()

        if server_data['mkdirstate']:
            username = server_data['username']
            mkdirname = server_data['mkdirname']
            mkdirpath = server_data['mkdirpath']
            print('用户创建[%s]，[%s]文件信息成功,服务端路径:%s' % (username, mkdirname, mkdirpath))
        else:
            print('文件已存在，创建失败！')

    def login_register(self,cmd,username,psd,state):
        '''登录注册功能字典'''
        psd = self.getmd5(psd)
        user_dic = self.userdic(cmd, username, psd)
        self.client_send_data(user_dic)
        server_data = self.client_recv_data()
        if server_data['userstate']:
            print('用户 [%s] %s成功' % (username,state))
            if state == '登录':
                self.userstate = server_data
                print(self.userstate,'客户端登录状态信息')
        else:
            print('%s失败,账号已存在'%state)


    def _register(self,cmd):
        '''注册功能'''
        print('注册功能')
        username = input('请输入注册账号：').strip()
        password = input('请输入注册密码：').strip()
        if password != None:
            self.login_register(cmd,username,password,'注册')
        else:
            print('账号密码不能为空')

    def getmd5(self,password):
        '''密码转换MD5值'''
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()
    def _login(self,cmd):
        '''登录功能'''
        username = input('请输入登录账号：').strip()
        password = input('请输入登录密码：').strip()
        if username != None and password != None:
            self.login_register(cmd, username, password, '登录')
        else:
            print('账号密码不能为空')

    def _get(self):
        '''下载发送数据'''
        if not self.userstate['userstate']:return

    def _put(self):
        '''上传接收数据'''
        if not self.userstate['userstate']: return

    def _mkdir(self,cmd):
        '''创建文件夹'''
        if not self.userstate['userstate']: return
        mkdirname = input('请输入创建文件夹名称：').strip()
        if not mkdirname:return
        self.mk_found_file(cmd,mkdirname)

    def _found(self):
        '''创建文件'''
        if not self.userstate['userstate']: return

    def _size(self):
        '''查看空间大小'''
        if not self.userstate['userstate']: return

    def _dir(self):
        '''查看用户文件夹信息'''
        if not self.userstate['userstate']: return

    def _del(self,cmd):
        '''删除文件'''
        if not self.userstate['userstate']: return
        inp = input('请输入切换目录名：').strip()
        if not inp: return
        filedic = self.filedic(cmd,inp)
        self.client_send_data(filedic)
        server_data = self.client_recv_data()
        if server_data['filestate']:
            print('[%s]文件已删除'%server_data['filesname'])
        else:
            print('删除失败')

    def _cd(self,cmd):
        '''切换目录'''
        if not self.userstate['userstate']: return
        inp = input('请输入切换目录名：').strip()
        if not inp:return
        filedic = self.filedic(cmd,None)
        filedic['cd'] = inp
        self.client_send_data(filedic)
        server_data = self.client_recv_data()
        if server_data['cdpath']:
            print('当前进入的目录为：',server_data['cdpath'])
        else:
            print('未找到目录')

    def _quit(self,cmd):
        '''用户退出登录'''
        exit('退出程序')

    def _closeserver(self):
        '''关闭服务器'''
        if not self.userstate['userstate']: return

    def client_send_data(self,dic):
        '''服务端发送报头数据'''

        head_data = pickle.dumps(dic)
        head_struct = struct.pack('i', len(head_data))
        self.client.send(head_struct)
        self.client.send(head_data)
    def client_recv_data(self):
        '''服务端发送报头数据'''
        head_struct = self.client.recv(4)
        head_data = struct.unpack('i', head_struct)[0]
        return pickle.loads(self.client.recv(head_data))

if __name__ == '__main__':
    client = MyClient(('127.0.0.1',9999))
    client.run()