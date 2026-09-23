import hashlib
import json
import os.path
import socket
import configparser
import subprocess
import tarfile
import time

from conf import settings


class FTPSever(object):
    """处理与客户端所有的交互的socket_server"""

    STATUS_CODE = {
        200: "Passed authentication!",
        201: "Wrong username or password!",
        300: "File does not exist !",
        301: "File exist , and this msg include the file size- !",
        302: "This msg include the msg size!",
        350: "Dir changed !",
        351: "Dir doesn't exist !",
        401: "File exist ,ready to re-send !",
        402: "File exist ,but file size doesn't match!",
    }
    MSG_SIZE = 1024  # 消息最长1024

    def __init__(self, managemengt_instance):
        self.managemengt_instance = managemengt_instance
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((settings.HOST, settings.PORT))
        self.sock.listen(settings.MAX_LISTEN)
        self.accounts = self.load_accounts()
        self.user_obj = None
        self.user_current_dir = None

    def run_forever(self):
        """启动 socket server"""
        print('starting FTP server on %s:%s'.center(50, "-") % (settings.HOST, settings.PORT))
        while True:
            self.request, self.addr = self.sock.accept()
            print("got a new connection from %s ....." % (self.addr,))
            try:
                self.handle()
            except Exception as e:
                print('Error happend with client,close connection.', e)

    def handle(self):
        """处理与用户的所有指令交互"""
        while True:
            raw_date = self.request.recv(self.MSG_SIZE)
            print("----->", raw_date)
            if not raw_date:
                print('connection %s is lost..... ' % (self.addr,))  # 链接断开
                del self.request, self.addr
                break
            date = json.loads(raw_date.decode("utf-8"))
            action_type = date.get('action_type')
            if action_type:
                if hasattr(self, '_%s' % action_type):
                    func = getattr(self, '_%s' % action_type)
                    func(date)
            else:
                print('invalid command')

    def load_accounts(self):
        """加载所有用户数据"""
        config_obj = configparser.ConfigParser()
        config_obj.read(settings.ACCOUNT_FILE)
        return config_obj

    def authenticate(self, username, passwoed):
        """用户认证方法"""
        if username in self.accounts:
            _password = self.accounts[username]['password']
            md5_obj = hashlib.md5()
            md5_obj.update(passwoed.encode('utf-8'))
            md5_password = md5_obj.hexdigest()
            # print("passwd:", _password, md5_password)
            if md5_password == _password:
                # print("passed authentication.....")
                # 设置一个用户路径
                self.user_obj = self.accounts[username]
                self.user_obj['home'] = os.path.join(settings.USER_HOME_DIR, username)
                self.user_current_dir = self.user_obj['home']  # 链接后当前目录

                return True
            else:
                # print("wrong username or password")
                return False
        else:
            # print("wrong username or password")
            return False

    def send_response(self, status_code, *args, **kwargs):
        """打包发消息给客户端"""
        date = kwargs
        date["status_code"] = status_code
        date['status_msg'] = self.STATUS_CODE[status_code]
        date['fill'] = ''

        bytes_date = json.dumps(date).encode()
        if len(bytes_date) < self.MSG_SIZE:
            date['fill'] = date['fill'].zfill(self.MSG_SIZE - len(bytes_date))
            bytes_date = json.dumps(date).encode()
        self.request.send(bytes_date)

    def _auth(self, date):
        """处理用户认证请求"""
        # print("auth", date)
        if self.authenticate(date.get('username'), date.get('password')):
            print('pass')
            #  消息内容，状态码 json.dumps .encode
            self.send_response(status_code=200)
        else:
            self.send_response(status_code=201)

    def _get(self, date):
        """get方法"""
        filename = date.get('filename')
        full_path = os.path.join(self.user_obj['home'], filename)
        if os.path.isfile(full_path):
            filesize = os.stat(full_path).st_size
            self.send_response(status_code=301, file_size=filesize)
            print("ready to send")
            f = open(full_path, 'rb')
            for line in f:
                self.request.send(line)
        else:
            self.send_response(status_code=300)
            print('没找着')
        f.close()

    def _ls(self, data):
        """ls方法"""
        cmd_obj = subprocess.Popen('dir %s' % self.user_current_dir, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()
        cmd_res = stderr + stdout
        if not cmd_res:
            cmd_res = b'current dir has no file at all'
        self.send_response(302, cmd_res_size=len(cmd_res))
        self.request.sendall(cmd_res)

    def _cd(self, data):
        """根据用户的target_dir改变self.user_current_dir 的值
        1. 把target_dir 跟user_current_dir 拼接
        2. 检测 要切换的目录是否存在
            2.1 如果存在 ， 改变self.user_current_dir的值到新路径
            2.2 如果不存在，返回错误消息

        """
        target_dir = data.get('target_dir')
        full_path = os.path.abspath(os.path.join(self.user_current_dir, target_dir))  # abspath是为了解决../..的问题
        print("full path:", full_path)
        if os.path.isdir(full_path):
            if full_path.startswith(self.user_obj['home']):  # has permission
                self.user_current_dir = full_path
                relative_current_dir = self.user_current_dir.replace(self.user_obj['home'], '')
                self.send_response(350, current_dir=relative_current_dir)

            else:
                self.send_response(351)

    def _put(self, data):
        """
        put方法
        1.拿到local文件名称和大小
        2。检查本地是否有相应文件。self.user_current_dir/local_file
        3. 接收文件
        """
        local_file = data.get("filename")
        full_path = os.path.join(self.user_current_dir, local_file)
        if os.path.isfile(full_path):  # 如果文件已存在 不能覆盖   创建新文件名+时间戳
            filename = '%s.%s' % (full_path, time.time())
        else:
            filename = full_path

        file_size = data.get('file_size')
        rec_size = 0
        f = open(filename, "wb")
        while rec_size < file_size:
            if file_size - rec_size < 8192:  # 最后一次接收
                date = self.request.recv(file_size - rec_size)
            else:
                date = self.request.recv(8192)
            rec_size += len(date)
            f.write(date)
        else:
            print('file %s recv done' % local_file)
            f.close()
