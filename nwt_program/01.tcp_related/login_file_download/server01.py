import socket
import struct
import json
import os

path=r'D:\My Documents\Pycharm\data'

# 无反射

def mysend(obj):
    obj_bytes = json.dumps(obj).encode('utf-8')
    blen_obj_bytes = struct.pack('i',len(obj_bytes))
    conn.send(blen_obj_bytes)
    conn.send(obj_bytes)

def myrecv():
    blen_obj_bytes=conn.recv(4)
    len_obj_bytes=struct.unpack('i',blen_obj_bytes)[0]
    obj_bytes=conn.recv(len_obj_bytes)
    obj=json.loads(obj_bytes.decode('utf-8'))
    return obj

sk = socket.socket()
sk.bind(('127.0.0.1',9001))
sk.listen()

while True:
    conn,_ = sk.accept()
    status=False

    while status==False:
        input_username=myrecv()
        input_cipertext=myrecv()
        with open(path,encoding='utf-8') as f1:
            for line in f1:
                username, cipertext = line.strip().split('|')
                if input_username == username and input_cipertext == cipertext:
                    status=True
                    break
            else:
                status=False
        mysend(status)

    while True:
        choice = myrecv()
        if choice == '1':
            fileinfo_dic = myrecv()
            with open(fileinfo_dic['filename'], 'wb') as f2:
                while fileinfo_dic['filesize'] > 0:
                    content = conn.recv(1024)
                    fileinfo_dic['filesize'] -= len(content)
                    f2.write(content)
            print('用户成功上传了文件%s'%(fileinfo_dic['filename']))
        if choice == '2':
            dirpath = r'D:\软件'
            file_list = os.listdir(dirpath)
            for i in range(len(file_list)):
                file_list[int(i)] = os.path.join(dirpath, file_list[i])
            mysend(file_list)
            download_num = myrecv()
            filepath = file_list[download_num - 1]
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            fileinfo_dic = {'filename': filename, 'filesize': filesize}
            mysend(fileinfo_dic)
            with open(filepath, mode='rb') as f:
                while filesize > 0:
                    content = f.read(1024)
                    filesize -= len(content)
                    conn.send(content)
            print('用户成功下载了文件%s' % (filename))
        if choice == '3':
            conn.close()
            break