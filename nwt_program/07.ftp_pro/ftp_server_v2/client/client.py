import os,sys,pickle,struct,time
import socket,hashlib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


class FTPClient():
    ip_port = ('127.0.0.1', 8080)
    recv_size = 1024
    listen_size = 5
    DOWNLOAD_PATH = os.path.join(BASE_DIR,'client','download')
    UPLOAD_PATH = os.path.join(BASE_DIR,'client','upload')

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        """服务器没打开时"""
        try:
            self.client.connect(self.ip_port)
        except Exception as e:
            print(e)
            exit('----服务器异常----')

    def handle(self):
        """client交互"""
        # 首先进行用户认证，再输入相应的操作指令
        if self.auth():
            while True:
                try:
                    user_cmd = input('(q:退出)>>>').strip()
                    if not user_cmd:continue
                    if user_cmd == 'q':
                        exit()
                    self.client.send(user_cmd.encode('utf-8'))
                    self.cmds = user_cmd.split()
                    if hasattr(self,self.cmds[0]):
                        getattr(self,self.cmds[0])()
                    else:
                        print('----wrong input, try again-----')
                except Exception as e:
                    print(e)
                    break

    def auth(self):
        """用户认证
               1.输入用户名,密码有三次机会
               2.用户名,密码发送到server
               3.打印服务端传过来的用户信息：{'username': 'alex', 'homedir': 'home/alex', 'quota': '50'}
               """
        count = 0
        while count < 3:
            user_name = input('username>>>:').strip()
            if not user_name: continue
            pass_word = input('password>>>:').strip()
            user_dic = {
                'username': user_name,
                'password': pass_word
            }
            self.client.send(pickle.dumps(user_dic))
            # res = struct.unpack('i',self.socket.recv(4))[0]
            res = self.client.recv(self.recv_size).decode('utf-8')
            if res == '登录成功':
                print('welcome'.center(20, '-'))
                # 接收account_info.ini存的用户信息
                user_info_dic = self.get_recv()
                # self.username = user_info_dic.get('username')
                # 显示服务端传来的用户信息
                print(user_info_dic)
                return True
            else:
                print(res)
            count += 1

    def get_recv(self):
        return pickle.loads(self.client.recv(self.recv_size))

    def readfile(self):
        """读取文件,得到文件内容的bytes型"""
        with open(self.filepath, 'rb') as f:
            filedata = f.read()
        return filedata

    def getfile_md5(self):
        """对文件内容md5"""
        return hashlib.md5(self.readfile()).hexdigest()

    def progress_bar(self, num, get_size, file_size):
        """进度条显示"""
        float_rate = get_size / file_size
        rate = round(float_rate * 100, 2)
        str ='>'
        # 1 表示下载
        if num == 1:
            sys.stdout.write('\r'+str*int(round(float_rate * 10))+'[{0}%]'.format(rate))
            time.sleep(0.01)
        # 2 表示上传
        elif num == 2:
            sys.stdout.write('\r' + str * int(round(float_rate * 10)) + '[{0}%]'.format(rate))
            time.sleep(0.01)
        sys.stdout.flush()

    def recv_file_header(self, header_size):
        """接收文件的header, filename file_size file_md5"""
        header_dic = pickle.loads(self.client.recv(header_size))
        print(header_dic)
        filename = header_dic.get('filename')
        file_size = header_dic.get('file_size')
        file_md5 = header_dic.get('file_md5')
        return (filename, file_size, file_md5)

    def verification_filemd5(self, file_md5):
        """验证文件内容的MD5是否相等"""
        # 判断下载下来的文件MD5值和server传过来的MD5值是否一致
        if self.getfile_md5() == file_md5:
            print('\n恭喜您,下载成功')
        else:
            print('\n下载失败，再次下载支持断点续传')

    def write_file(self, f, get_size, file_size):
        """下载文件，将内容写入文件中"""
        while get_size < file_size:
            file_bytes = self.client.recv(self.recv_size)
            f.write(file_bytes)
            get_size += len(file_bytes)
            self.progress_bar(1, get_size, file_size)
            # 1表示下载

    def get(self):
        """       主逻辑
        从server下载文件到client
    1.判断用户是否输入文件名
    2.判断要下载的文件是否之前已经下载过
    3.下载过：
        3.1.发送已下载文件的大小
        3.2.判断现有文件在服务端是否还存在
            3.2.1.返回header_size 表示存在，
            3.2.2.返回0 表示该文件在服务器不存在了
        3.3.接收文件header，得到filename 、file_size、 file_md5
            3.3.1.现有文件大小 == file_size 提示 完整的文件 已存在
            3.3.2.现有文件大小 != file_size 执行 断点续传 功能
                3.3.2.1.文件以ab模式打开， f.seek(现有文件大小)，再接着f.write()，显示进度条
                3.3.2.2.判断文件内容的md5和 header里面的file_md5值是否相等 相等显示下载成功
    4.没有下载过：
        4.1.发送 0 给服务器 告诉server该文件没有被下载过
        4.2.判断文件在服务端是否存在：
            4.2.1.存在，服务器 返回  header 、filename、 file_size 、file_md5
            4.2.2.不存在，返回0，提示该目录下，文件不存在
        4.3.文件以wb模式打开，f.write(),显示进度条
        4.4.判断文件内容的md5和header里面的file_md5值是否相等，相等显示下载成功
                """
        # cmds是列表
        if len(self.cmds) > 1:
            filename = self.cmds[1]
            self.filepath = os.path.join(self.DOWNLOAD_PATH, filename)
            if os.path.isfile(self.filepath):
                # 如果文件存在 支持断点续传
                temp_file_size = os.path.getsize(self.filepath)
                self.client.send(struct.pack('i', temp_file_size))
                header_size = struct.unpack('i', self.client.recv(4))[0]
                if header_size:
                    filename, file_size, file_md5 = self.recv_file_header(header_size)
                    if temp_file_size == file_size:
                        print('------文件已存在----')
                    else:
                        print('----正在进行断点续传...')
                        download_filepath = os.path.join(self.DOWNLOAD_PATH, filename)
                        with open(download_filepath, 'ab') as f:
                            f.seek(temp_file_size)
                            get_size = temp_file_size
                            self.write_file(f, get_size, file_size)
                        # 判断文件是否下载完全
                        self.verification_filemd5(file_md5)
                else:
                    print('------当前目录下,文件不存在------')
            else:
                # 文件第一次下载  # 0 表示之前没有下载过
                self.client.send(struct.pack('i', 0))
                header_size = struct.unpack('i', self.client.recv(4))[0]
                if header_size:
                    filename, file_size, file_md5 = self.recv_file_header(header_size)
                    download_filepath = os.path.join(self.DOWNLOAD_PATH, filename)
                    with open(download_filepath, 'wb') as f:
                        get_size = 0
                        self.write_file(f, get_size, file_size)
                    self.verification_filemd5(file_md5)
                else:
                    print('当前目录下,文件不存在')
        else:
            print('用户没有输入文件名')

    def openfile_tosend(self, filesize, has_size=0):
        """上传时，打开文件读取文件内容send(data)"""
        with open(self.filepath, 'rb') as f:
            f.seek(has_size)
            while True:
                data = f.read(1024)
                if data:
                    self.client.send(data)
                    recv_size = struct.unpack('i', self.client.recv(4))[0]
                    self.progress_bar(2, recv_size, filesize)
                else:
                    break
        print('\n' + self.client.recv(self.recv_size).decode('utf-8'))  # 显示上传成功或失败

    def put_situation(self, filesize, situa=0):
        """上传的文件有两种情况，"""
        quota_state = struct.unpack('i', self.client.recv(4))[0]
        if quota_state:
            # 文件已经存在
            if situa:
                has_size = struct.unpack('i', self.client.recv(4))[0]
                self.openfile_tosend(filesize, has_size)
            else:
                # 第一次上传
                self.openfile_tosend(filesize)
        else:
            print('超出了用户的配额')

    def put(self):
        """往server自己的home/alice目录下,当前工作的目录下上传文件
       1.判断用户是否输入文件名
       2.判断要上传的文件是否存在
       3.发送header 包括 filename file_md5 file_size
       4.根据服务端的返回state，知道该文件之前是否上传过一部分
           4.1.server端已经存在了，断点续传
               4.1.1.存在的文件has_size和该文件大小不等
                   4.1.1.1.传送该文件的剩余部分，没有超出用户的配额
                       4.1.1.1.1.文件以rb模式打开，f.seek(has_size),send(line),
                           从server端接收recv_size,同步，显示进度条，server端对接收文件内容md5
                           返回是否上传成功！
                   4.1.1.2.传送该文件的剩余部分，超出了用户的配额，就提示超出了用户的配额
               4.1.2.存在的文件和该文件大小相等，提示当前目录下，文件已经存在
           4.2.server端不存在，第一次上传
               4.2.1.传送该文件，没有超出用户的配额
                   文件以rb模式打开，send(line),从server端接收recv_size，同步，显示进度条，
                    server端对接收文件内容md5,返回是否上传成功！
               4.2.2.传送该文件，超出了用户的配额，就提示超出了用户的额度
               """
        # 判断用户输入了文件名
        if len(self.cmds) > 1:
            filename = self.cmds[1]
            filepath = os.path.join(self.UPLOAD_PATH, filename)
            if os.path.isfile(filepath):
                self.client.send(struct.pack('i', 1))
                self.filepath = filepath
                filesize = os.path.getsize(self.filepath)
                header_dic = {
                    'filename': filename,
                    'file_md5': self.getfile_md5(),
                    'file_size': filesize
                }
                header_bytes = pickle.dumps(header_dic)
                self.client.send(struct.pack('i', len(header_bytes)))
                self.client.send(header_bytes)

                state = struct.unpack('i', self.client.recv(4))[0]
                # 已经存在了
                if state:
                    has_state = struct.unpack('i', self.client.recv(4))[0]
                    if has_state:
                        # 上次没有传完 接着继续传
                        self.put_situation(filesize, 1)
                    else:
                        # 存在的大小 和文件大小一致 不必再传
                        print('当前目录下，文件已经存在')
                else:
                    # 第一次传
                    self.put_situation(filesize)
            else:
                # 文件不存在
                print('文件不存在')
                self.client.send(struct.pack('i', 0))
        else:
            print('用户没有输入文件名')

    def ls(self):
        """查询当前工作目录下,文件列表"""
        dir_size = struct.unpack('i', self.client.recv(4))[0]
        recv_size = 0
        recv_bytes = b''
        while recv_size < dir_size:
            temp_bytes = self.client.recv(self.recv_size)
            recv_bytes += temp_bytes
            recv_size += len(temp_bytes)
            # gbk 适合windows utf-8 适合linux
        print(recv_bytes.decode('gbk'))

    def cd(self):
        """切换目录"""
        if len(self.cmds) > 1:
            print(self.client.recv(self.recv_size).decode('utf-8'))
        else:
            print('没有输入要切换的目录名')

    def mkdir(self):
        """"新建目录"""
        if len(self.cmds) > 1:
            print(self.client.recv(self.recv_size).decode('utf-8'))
        else:
            print('没有输入要增加的目录名')

    def rmdir(self):
        """删除指定的文件夹，或者文件"""
        if len(self.cmds)>1:
            print(self.client.recv(self.recv_size).decode('utf-8'))
        else:
            print('没有输入要删除的文件名')

    def close(self):
        self.client.close()


if __name__ == '__main__':
    obj = FTPClient()
    obj.handle()
    obj.close()