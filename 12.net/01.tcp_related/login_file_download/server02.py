import os
import sys
import json
import struct
import socket
import hashlib

userinfo_path=r'userinfo'

def get_md5(salt,text):
    md5 = hashlib.md5(salt.encode('utf-8'))
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def get_sha1(salt,text):
    sha1 = hashlib.sha1(salt.encode('utf-8'))
    sha1.update(text.encode('utf-8'))
    return sha1.hexdigest()

def mysend(conn,obj):
    bobj = json.dumps(obj).encode('utf-8')
    blen_bobj = struct.pack('i',len(bobj))
    conn.send(blen_bobj)
    conn.send(bobj)

def myrecv(conn):
    blen_bobj=conn.recv(4)
    len_bobj=struct.unpack('i',blen_bobj)[0]
    bobj=conn.recv(len_bobj)
    obj=json.loads(bobj.decode('utf-8'))
    return obj

def login(conn):
    flag = True
    while flag:
        login_form_dic = myrecv(conn)
        with open(userinfo_path, encoding='utf-8') as f:
            for line in f:
                username, cipertext = line.strip().split('|')
                if username == login_form_dic['username'] and cipertext == get_sha1(username, login_form_dic['password_md5']):
                    login_result = True
                    flag = False
                    break
            else:
                login_result = False
            login_result_dic = {'operate': 'login', 'result': login_result}
            mysend(conn, login_result_dic)

def upload(conn,opt_dic):
    with open(opt_dic['filename'], 'wb') as f:
        while opt_dic['filesize'] > 0:
            content = conn.recv(1024)
            opt_dic['filesize'] -= len(content)
            f.write(content)

def download(conn,opt_dic):
    filepath = r'D:\1.mp4'
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    fileinfo_dic = {'filename': filename, 'filesize': filesize}
    mysend(conn,fileinfo_dic)
    with open(filepath, mode='rb') as f:
        while filesize > 0:
            content = f.read(1024)
            filesize -= len(content)
            conn.send(content)

sk = socket.socket()
sk.bind(('127.0.0.1',9001))
sk.listen()
conn,_ =sk.accept()
login(conn)
opt_dic = myrecv(conn)
if hasattr(sys.modules[__name__],opt_dic['operate']):
    getattr(sys.modules[__name__],opt_dic['operate'])(conn,opt_dic)
conn.close()
sk.close()