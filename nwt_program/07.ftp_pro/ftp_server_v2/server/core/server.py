import socket
import struct
import hashlib
import subprocess
import os,sys,pickle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from core import user_handle
from core.file_handle import FileHandle
import queue
from threading import Thread,currentThread


class TCPServer:
    STATE_FLAG = {'200': '增加目录成功',
                  '201': '目录名已存在',
                  '202': '切换目录成功',
                  '203': '切换目录失败',
                  '204': '切换的目录不在该目录下',
                  '205': '删除成功',
                  '206': '文件夹非空，不能删除',
                  '207': '不是文件,也不是文件夹',
                  '208': '登录成功',
                  '209': '密码不对',
                  '210': '用户不存在',
                  '211': '上传成功',
                  '212': '上传失败'
                  }

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind(settings.ip_port)
        self.socket.listen(settings.listen_size)
        self.homedir_conn = {}
        self.message = self.state_bytes()
        self.file_handle = FileHandle(settings.recv_size, self.message)
        self.q = queue.Queue(2)

    def state_bytes(self):
        # 将STATE_FLAG的value值转化成 bytes 型
        return {k: bytes(v, 'utf-8') for k, v in self.STATE_FLAG.items()}

    def run(self):
        self.server_accept()

    def server_accept(self):
        """等到客户端连接"""
        # ----链接循环-------
        while True:
            conn,client_addr = self.socket.accept()
            print('----客户端地址:---', client_addr)
            t = Thread(target=self.server_handle,args=(conn,))
            #self.server_handle(conn)
            self.q.put(t)
            t.start()
            # except Exception as e:
            #     print(e)
            #     conn.close()
            #     # 把超过 队列数的删除
            #     self.q.get()
            #     break

    def server_handle(self,conn):
        """处理与用户的交互指令
               """
        # 首先进行用户认证
        if self.auth(conn):
            print('用户登录成功')
            while True:
                """
                1、用于处理 当客户端，单方面异常断开连接的占用服务端内存的情况
                   1.1 1if not user_input:适用于linux操作系统
                   1.2 except ConnectionResetError:适用于windows操作系统
                2、此时的 except Exception as e:还可以处理其他操作异常断开的处理，比如上传文件
                conn,双向链接，客户端一端断开，conn报错  
                """
                try:
                    user_input = conn.recv(settings.recv_size).decode('utf-8')
                    # 正常退出，异常退出出路
                    if not user_input:
                        conn.close()
                        print('-----链接异常----')
                        self.q.get()
                        self.server_accept()
                    self.cmds = user_input.split()
                    if hasattr(self, self.cmds[0]):
                        getattr(self, self.cmds[0])(conn)
                    else:
                        print('请用户重复输入')
                except Exception as e:
                    print(e)
                    conn.close()
                    self.q.get()
                    self.server_accept()

    def auth(self,conn):
        """处理用户的认证请求
               1.根据username读取conf/account_info.ini文件,password相比,判断用户是否存在
               2.将用户的home,current_dir存在homedir_conn[conn],供后续conn使用
               3.给client返回用户的详细信息
               """
        print('----处理用户的认证请求----')
        while True:
            """
            用于处理 当客户端在进行用户认证时，单方面异常断开连接的占用服务端内存的情况
                if not user_input:适用于linux操作系统
                :except ConnectionResetError:适用于windows操作系统
            conn套接字对象 ,双向链接，客户端一端断开，conn无意义 报错    
            """
            try:
                user_dic = pickle.loads(conn.recv(settings.recv_size))
                if not user_dic:
                    print('链接异常')
                    conn.close()
                    self.q.get()
                    self.server_accept()
                name = user_dic.get('username')
                User_Handle = user_handle.UserHandle(name)
                # 判断用户是否存在 返回列表eg:[('password', '202cb962ac59075b964b07152d234b70'), ('homedir', 'home/alex'), ('quota', '100')]
                user_data = User_Handle.judge()
                if user_data:
                    if user_data[0][1] == hashlib.md5(user_dic.get('password').encode('utf-8')).hexdigest():
                        conn.send(self.message['208'])  # 登录成功
                        username = name
                        homedir_path =os.path.join(settings.BASE_DIR, 'home', username)
                        self.homedir_conn[conn] = {'username': username, 'home': homedir_path,
                                                   'current_dir': homedir_path}
                        # 将用户配额的大小从M 改到字节
                        self.homedir_conn[conn]['quota_bytes'] = int(user_data[2][1]) * 1024 * 1024
                        user_info_dic = {
                            'username': username,
                            'homedir': user_data[1][1],
                            'quota': user_data[2][1]
                        }
                        # 用户的详细信息发送到客户端
                        conn.send(pickle.dumps(user_info_dic))

                        return True
                    else:
                        # 密码不对
                        conn.send(self.message['209'])
                else:
                    # 用户不存在
                    conn.send(self.message['210'])
            except Exception as e:
                print(e)
                conn.close()
                self.q.get()
                self.server_accept()

    def get(self,conn):
        """从server下载文件到client
               1.判断用户是否输入文件名
               2.判断文件是否存在
               3.接收client发来的文件大小
                   3.1.exist_file_size != 0 表示之前已被下载过一部分
                       3.1.1.发送文件的header_size header_bytes
                       3.1.2.判断exist_file_size是否等于文件的真实大小
                           3.1.2.1.不等，文件以rb模式打开，f.seek(exist_file_size),接着再send(line)
                           3.1.2.2.相等，提示文件大小相等
                   3.2.exist_file_size == 0 表示第一次下载
                       3.2.1.发送文件的header_size, header_bytes
                       3.2.2.文件以rb模式打开，send(line)
               """
        if len(self.cmds) > 1:
            filename = self.cmds[1]
            filepath = os.path.join(self.homedir_conn[conn]['current_dir'], filename)
            if os.path.isfile(filepath):
                exist_file_size = struct.unpack('i', conn.recv(4))[0]
                self.homedir_conn[conn]['filepath'] = filepath
                header_dic = {
                    'filename': filename,
                    'file_md5': self.file_handle.getfile_md5(filepath),
                    'file_size': os.path.getsize(filepath)
                }
                header_bytes = pickle.dumps(header_dic)
                # 发送报头的长度
                conn.send(struct.pack('i', len(header_bytes)))
                # 再发报头
                conn.send(header_bytes)
                if exist_file_size:
                    # if表示之前被下载过 一部分
                    if exist_file_size != os.path.getsize(filepath):
                        self.file_handle.openfile_tosend(self.homedir_conn[conn]['filepath'], conn, exist_file_size)
                    else:
                        print('------断点和文件本身大小一样-----')
                # 文件第一次下载
                else:
                    self.file_handle.openfile_tosend(self.homedir_conn[conn]['filepath'], conn)

            else:
                # 这里无论收到文件大小或者0 都不做处理，因为server根本不存在该文件了返回0
                print('-----当前目录下文件不存在------')
                conn.send(struct.pack('i', 0))
        else:
            print('用户没有输入文件名')

    def put(self,conn):
        """从client上传文件到server当前工作目录下
        1.判断用户是否输入文件名
        2.从client得知，待传的文件是否存在
            2.1.current_home_size(),得知用户home/alex大小，self.home_bytes_size
            2.2.接收文件header filename file_size file_md5
            2.3.上传文件在当前目录下,已经存在，断点续传：
                2.3.1.算出文件已经有的大小，has_size
                    2.3.1.1.发现 has_size == file_size,发送0，告诉client,文件已经存在
                       2.3.1.2.has_size != file_size,接着继续传，
                       2.3.1.2.1.self.home_bytes_size + int(file_size - has_size) > self.quota_bytes
                               算出接着要上传的大小是否超出了配额，超出配额就提示。
                        2.3.1.2.2.没有超出配额，就send(has_size),文件以ab模式打开，f.seek(has_size),f.write()
                               发送每次的has_size,同步，为了client显示进度条
                        2.3.1.2.3.验证文件内容的md5,是否上传成功！
            2.4.上传文件在当前目录下，不存在，第一次上传：
                2.4.1.self.home_bytes_size + int(file_size) > self.quota_bytes:
                       验证上传的文件是否超出了用户配额，超出就提示
                2.4.2.文件以wb模式打开，f.write(),发送每次得recv_size,同步，为了client显示进度条
                2.4.3.验证文件内容的md5,是否上传成功！
                       """

        if len(self.cmds) > 1:
            state_size = struct.unpack('i', conn.recv(4))[0]
            # 客户端文件存在
            if state_size:
                self.homedir_conn[conn]['home_bytes_size'] = self.file_handle.current_home_size(
                    self.homedir_conn[conn]['home'])
                # 算出了home下已被占用的大小self.home_bytes_size
                header_bytes = conn.recv(struct.unpack('i', conn.recv(4))[0])
                header_dic = pickle.loads(header_bytes)
                print(header_dic)
                filename = header_dic.get('filename')
                file_size = header_dic.get('file_size')
                file_md5 = header_dic.get('file_md5')

                upload_filepath = os.path.join(self.homedir_conn[conn]['current_dir'], filename)
                self.homedir_conn[conn]['filepath'] = upload_filepath
                # 文件已经存在
                if os.path.exists(upload_filepath):
                    conn.send(struct.pack('i', 1))
                    has_size = os.path.getsize(upload_filepath)
                    if has_size == file_size:
                        print('-----文件已经存在------')
                        conn.send(struct.pack('i', 0))
                    else:  # 上次没有传完 接着继续传
                        conn.send(struct.pack('i', 1))
                        self.file_handle.put_situation(self.homedir_conn[conn], conn, file_md5, file_size, has_size)
                else:  # 第一次 上传
                    conn.send(struct.pack('i', 0))
                    self.file_handle.put_situation(self.homedir_conn[conn], conn, file_md5, file_size)
            else:
                print('-----待传的文件不存在------')
        else:
            print('------用户没有输入文件名-----')

    def ls(self, conn):
        """查询当前工作目录下,先返回文件列表的大小,在返回查询的结果"""
        # 切换到conn 当前目录
        os.chdir(self.homedir_conn[conn]['current_dir'])
        if len(self.cmds) > 1:
            file_name = self.cmds[1]
            file_path =os.path.join(self.homedir_conn[conn]['current_dir'], file_name)
            if os.path.isdir(file_path):
                subpro_obj = subprocess.Popen('dir ' + file_name, shell=True,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
            else:
                subpro_obj = subprocess.Popen('dir', shell=True,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        else:
            subpro_obj = subprocess.Popen('dir', shell=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        stdout = subpro_obj.stdout.read()
        stderr = subpro_obj.stderr.read()
        conn.send(struct.pack('i', len(stdout + stderr)))
        conn.send(stdout)
        conn.send(stderr)

    def cd(self,conn):
        """切换目录
               1.查看是否是目录名
               2.拿到当前目录,拿到目标目录,
               3.判断conn的home是否在目标目录内
               4.send(切换的状态)
               """
        if len(self.cmds) > 1:

            # 例如dir_path   alex/2.jpg
            dir_path = os.path.join(self.homedir_conn[conn]['current_dir'], self.cmds[1])
            if os.path.isdir(dir_path):
                previous_path = self.homedir_conn[conn]['current_dir']
                # 改变工作目录到
                os.chdir(dir_path)
                # 得到当前工作目录路径
                target_dir = os.getcwd()
                if self.homedir_conn[conn]['home'] in target_dir:
                    self.homedir_conn[conn]['current_dir'] = target_dir
                    # 切换目录成功
                    conn.send(self.message['202'])
                else:
                    os.chdir(previous_path)
                    # 切换目录失败
                    conn.send(self.message['203'])
            else:
                # 切换的目录不在该目录下
                conn.send(self.message['204'])

        else:
            print('没有传入切换的目录名')

    def mkdir(self,conn):
        """"新建目录"""
        if len(self.cmds) > 1:
            mkdir_path = os.path.join(self.homedir_conn[conn]['current_dir'], self.cmds[1])
            if not os.path.exists(mkdir_path):
                os.mkdir(mkdir_path)
                # 增加目录成功
                conn.send(self.message['200'] + (' 目录名为: %s' % self.cmds[1]).encode('utf-8'))
            else:
                # 目录名已存在
                conn.send(self.message['201'])
        else:
            print('----用户没有输入目录名----')

    def rmdir(self,conn):
        """删除指定的文件夹"""
        if len(self.cmds)>1:
            file_name = self.cmds[1]
            file_path = os.path.join(self.homedir_conn[conn]['current_dir'],file_name)
            # 检测给出的路径是否是一个文件
            if os.path.isfile(file_path):
                os.remove(file_path)
                conn.send(self.message['205'])
            # 检测所给的路径是否是一个目录
            elif os.path.isdir(file_path):
                # os.listdir()返回指定目录下所有文件和目录名
                if not len(os.listdir(file_path)):
                    # 删除多个目录
                    os.removedirs(file_path)
                    conn.send(self.message['205'])
                else:
                    conn.send(self.message['206'])
            else:
                conn.send(self.message['207'])
        else:
            print('没有输入要删除的文件名')

    def close(self):
        self.socket.close()










