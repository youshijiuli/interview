import socket
import struct
import hashlib
import json
import os

def mysend(obj):
    obj_bytes = json.dumps(obj).encode('utf-8')
    blen_obj_bytes = struct.pack('i',len(obj_bytes))
    sk.send(blen_obj_bytes)
    sk.send(obj_bytes)

def myrecv():
    blen_obj_bytes=sk.recv(4)
    len_obj_bytes=struct.unpack('i',blen_obj_bytes)[0]
    obj_bytes=sk.recv(len_obj_bytes)
    obj=json.loads(obj_bytes.decode('utf-8'))
    return obj

def encrypt(username,password):
    md5=hashlib.md5(username.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

sk = socket.socket()
sk.connect(('127.0.0.1',9001))
status=False

while status==False:
    username=input('请输入用户名>>>').strip()
    password=input('请输入密码>>>').strip()
    cipertext=encrypt(username,password)
    mysend(username)
    mysend(cipertext)
    status=myrecv()
    if status==False:
        print('用户名或密码错误，请重新登陆！')
print('登陆成功!')
option_list = [('上传', 'upload'), ('下载', 'download'), ('退出','exit')]
while True:
    for index, item in enumerate(option_list,1):
        print(index, item[0])
    choice = input('请输入您的选项>>>').strip()
    mysend(choice)
    if choice=='1':
        filepath = input('请输入要上传文件的绝对路径>>>').strip()
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            fileinfo_dic = {'filename': filename, 'filesize': filesize}
            mysend(fileinfo_dic)
            with open(filepath, mode='rb') as f:
                while filesize > 0:
                    content = f.read(1024)
                    filesize -= len(content)
                    sk.send(content)
            print('文件上传完毕！')
        else:
            print('指定路径的文件不存在！')
    elif choice=='2':
        file_list = myrecv()
        for index, item in enumerate(file_list, 1):
            print(index, item)
        download_num = int(input('请输入要下载的文件序号>>>').strip())
        mysend(download_num)
        fileinfo_dic = myrecv()
        with open(fileinfo_dic['filename'], 'wb') as f:
            while fileinfo_dic['filesize'] > 0:
                content = sk.recv(1024)
                fileinfo_dic['filesize'] -= len(content)
                f.write(content)
        print('文件下载完毕！')
    elif choice=='3':
        print('系统退出')
        # sk.close()
        break
    else:
        print('您的输入有误，请检查后重新输入')