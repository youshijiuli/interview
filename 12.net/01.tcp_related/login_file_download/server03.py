import struct
import json
import os
import socketserver

path=r'D:\My Documents\Pycharm\data'

class Myserver(socketserver.BaseRequestHandler):

    @staticmethod
    def mysend(conn,obj):
        bobj = json.dumps(obj).encode('utf-8')
        blen_bobj = struct.pack('i', len(bobj))
        conn.send(blen_bobj)
        conn.send(bobj)

    @staticmethod
    def myrecv(conn):
        blen_bobj = conn.recv(4)
        len_bobj = struct.unpack('i', blen_bobj)[0]
        bobj = conn.recv(len_bobj)
        obj = json.loads(bobj.decode('utf-8'))
        return obj

    def handle(self):

        conn = self.request

        flag=True

        while flag:

            status=False

            while status==False:
                input_username=self.myrecv(conn)
                input_cipertext=self.myrecv(conn)
                with open(path,encoding='utf-8') as f1:
                    for line in f1:
                        username, cipertext = line.strip().split('|')
                        if input_username == username and input_cipertext == cipertext:
                            status=True
                            break
                    else:
                        status=False
                self.mysend(conn,status)

            while True:
                choice = self.myrecv(conn)
                if choice == '1':
                    fileinfo_dic = self.myrecv(conn)
                    with open(fileinfo_dic['filename'], 'wb') as f2:
                        while fileinfo_dic['filesize'] > 0:
                            content = conn.recv(1024)
                            fileinfo_dic['filesize'] -= len(content)
                            f2.write(content)
                    print('用户%s成功上传了文件%s'%(username,fileinfo_dic['filename']))
                if choice == '2':
                    dirpath = r'D:\软件'
                    file_list = os.listdir(dirpath)
                    for i in range(len(file_list)):
                        file_list[int(i)] = os.path.join(dirpath, file_list[i])
                    self.mysend(conn,file_list)
                    download_num = self.myrecv(conn)
                    filepath = file_list[download_num - 1]
                    filename = os.path.basename(filepath)
                    filesize = os.path.getsize(filepath)
                    fileinfo_dic = {'filename': filename, 'filesize': filesize}
                    self.mysend(conn,fileinfo_dic)
                    with open(filepath, mode='rb') as f:
                        while filesize > 0:
                            content = f.read(1024)
                            filesize -= len(content)
                            conn.send(content)
                    print(f'用户{username}成功下载了文件{filename}')
                if choice == '3':
                    print(f'用户{username}退出')
                    conn.close()
                    flag=False
                    break

server = socketserver.ThreadingTCPServer(('127.0.0.1',9001),Myserver)
server.serve_forever()