import os
import sys
import json
import struct
import socket
import hashlib

def get_md5(salt,text):
    md5 = hashlib.md5(salt.encode('utf-8'))
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def mysend(sk,obj):
    bobj = json.dumps(obj).encode('utf-8')
    blen_bobj = struct.pack('i',len(bobj))
    sk.send(blen_bobj)
    sk.send(bobj)

def myrecv(sk):
    blen_bobj=sk.recv(4)
    len_bobj=struct.unpack('i',blen_bobj)[0]
    bobj=sk.recv(len_bobj)
    obj=json.loads(bobj.decode('utf-8'))
    return obj

def login(sk):
    while True:
        username = input('请输入用户名>>>').strip()
        password = input('请输入密码>>>').strip()
        if username and password:
            password_md5=get_md5(username,password)
            login_form_dic = {'username': username, 'password_md5': password_md5}
            mysend(sk, login_form_dic)
            login_result_dic = myrecv(sk)
            if login_result_dic['operate'] == 'login' and login_result_dic['result']:
                print('登录成功')
                break
            else:
                print('登录失败')
        else:
            print('用户名和密码均不能为空！')

def upload(sk):
    filepath = r'D:\1.mp4'
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    opt_dic = {'operate': 'upload','filename':filename,'filesize':filesize}
    mysend(sk, opt_dic)
    with open(filepath, mode='rb') as f:
        while filesize > 0:
            content = f.read(1024)
            filesize -= len(content)
            sk.send(content)
    print('上传完毕')

def download(sk):
    # 这里可以加入别的信息，比如要下载哪个文件？
    opt_dic = {'operate':'download'}
    mysend(sk,opt_dic)
    fileinfo_dic = myrecv(sk)
    with open(fileinfo_dic['filename'], 'wb') as f:
        while fileinfo_dic['filesize'] > 0:
            content = sk.recv(1024)
            fileinfo_dic['filesize'] -= len(content)
            f.write(content)
    print('下载完毕')

def exit(sk):
    print('Bye!')
    return False

sk = socket.socket()
sk.connect(('127.0.0.1',9001))
opt_tuple_list = [
    ('上传文件','upload'),
    ('下载文件','download'),
    ('退出程序','exit')]
login(sk)
while True:
    for index,opt_tuple in enumerate(opt_tuple_list,1):
        print(index,opt_tuple[0])
    opt_num = input('请选择您要操作的序号>>>').strip()
    if opt_num.isdecimal():
        opt_num = int(opt_num)
        if 1 <= opt_num <= len(opt_tuple_list):
            flag = getattr(sys.modules[__name__], opt_tuple_list[opt_num-1][1])(sk)
            if flag=='exit':
                break
        else:
            print('您输入的序号超出范围，请重新输入！')
    else:
        print('您输入的序号含有非法字符，请重新输入！')
sk.close()


