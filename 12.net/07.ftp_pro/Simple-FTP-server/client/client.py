import json
import optparse
import os.path
import socket


class FTPClient(object):
    """ftp_base 客户端"""
    MSG_SIZE = 1024

    def __init__(self):
        self.username = None
        self.terminal_display = None
        parser = optparse.OptionParser()
        parser.add_option("-s", "--server", dest="server", help="ftp_base server ip_addr")
        parser.add_option("-P", "--port", type="int", dest="port", help="ftp_base server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-p", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()
        self.argv_verification()
        self.make_connection()

    def argv_verification(self):
        """检查参数合法性"""
        if not self.options.server or not self.options.port:
            exit("ERR:must supply server and port parameters")

    def make_connection(self):
        """建立socket链接"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.options.server, self.options.port))

    def get_response(self):
        """获取服务器返回值"""
        date = self.sock.recv(self.MSG_SIZE)
        return json.loads(date.decode('utf-8'))

    def auth(self):
        """用户认证"""
        count = 0
        while count < 3:
            username = input("username: ").strip()
            if not username: continue
            password = input("password: ").strip()

            cmd = {
                'action_type': "auth",
                'username': username,
                'password': password,
            }
            self.sock.send(json.dumps(cmd).encode('utf-8'))
            response = self.get_response()
            # print("response：", response)
            if response.get('status_code') == 200:
                self.username = username
                self.terminal_display = "[%s]>>:" % self.username
                return True
            else:
                print(response.get('status_msg'))
            count += 1

    def interactive(self):
        """处理与FTPserver的所有交互"""
        if self.auth():
            while True:
                user_input = input(self.terminal_display).strip()
                if not user_input: continue

                cmd_list = user_input.split()  # 解析指令
                if hasattr(self, "_%s" % cmd_list[0]):
                    func = getattr(self, "_%s" % cmd_list[0])
                    func(cmd_list[1:])

    def paramerter_check(self, args, min_args=None, max_args=None, exact_args=None):
        """检查参数"""
        if min_args:
            if len(args) < min_args:
                print("must provide at least %s parameters but %s received " % (min_args, len(args)))
                return False
        if max_args:
            if len(args) > max_args:
                print("need provide  %s parameters but %s received " % (max_args, len(args)))
                return False
        if exact_args:
            if len(args) != exact_args:
                print("need exactly %s parameters but %s received " % (exact_args, len(args)))
                return False
        return True

    def send_msg(self, action_type, **kwargs):
        """打包消息并发送到远程"""
        msg_date = {
            'action_type': action_type,
            'fill': '',
        }

        msg_date.update(kwargs)  # 两个字典合并成一起
        bytes_msg = json.dumps(msg_date).encode('utf-8')
        if self.MSG_SIZE > len(bytes_msg):
            msg_date['fill'] = msg_date['fill'].zfill(self.MSG_SIZE - len(bytes_msg))
            bytes_msg = json.dumps(msg_date).encode('utf-8')
        self.sock.send(bytes_msg)

    def _get(self, cmd_args):
        """从FTP服务器下载"""
        if self.paramerter_check(cmd_args, min_args=1):
            filename = cmd_args[0]
            self.send_msg(action_type='get', filename=filename)
            response = self.get_response()
            if response.get("status_code") == 301:
                file_size = response.get('file_size')
                rec_size = 0

                progress_generator = self.progress_bar(file_size)
                progress_generator.__next__()
                f = open(filename, "wb")
                while rec_size < file_size:
                    if file_size - rec_size < 8192:  # 最后一次接收
                        date = self.sock.recv(file_size - rec_size)
                    else:
                        date = self.sock.recv(rec_size)
                    rec_size += len(date)
                    f.write(date)
                    progress_generator.send(rec_size)
                else:
                    print("----file[%s] is recv done,recv size [%s]----" % (filename, file_size))
                    f.close()
            else:
                print(response.get('status_msg'))

    def _ls(self, cmd_args):
        """显示当前路径"""
        self.send_msg(action_type='ls')
        response = self.get_response()  # 定长的消息头 1024
        if response.get('status_code') == 302:  # 准备接收长消息
            cmd_res_size = response.get('cmd_res_size')
            received_size = 0
            cmd_res = b''
            while received_size < cmd_res_size:
                if cmd_res_size - received_size < 8192:
                    data = self.sock.recv(cmd_res_size - received_size)
                else:
                    data = self.sock.recv(8192)
                cmd_res += data
                received_size += len(data)
            else:
                print(cmd_res.decode('gbk'))

    def _cd(self, cmd_args):
        """change to target dir"""
        if self.paramerter_check(cmd_args, exact_args=1):
            target_dir = cmd_args[0]
            self.send_msg('cd', target_dir=target_dir)
            response = self.get_response()
            if response.get("status_code") == 350:  # dir changed
                self.terminal_display = "[%s]>>:" % response.get('current_dir')
                self.current_dir = response.get('current_dir')

    def _put(self, cmd_args):
        """上传本地文件到服务器"""

        if self.paramerter_check(cmd_args, exact_args=1):
            local_file = cmd_args[0]
            if os.path.isfile(local_file):
                total_size = os.path.getsize(local_file)
                self.send_msg('put', filename=local_file, file_size=total_size)
                f = open(local_file, 'rb')
                uploaded_size = 0
                last_percent = 0

                for line in f:
                    self.sock.send(line)
                    uploaded_size += len(line)
                    current_percent = int(uploaded_size / total_size * 100)
                    if current_percent > last_percent:
                        print('#' * int(current_percent / 2) + "{percent}%".format(percent=current_percent), end='\r',
                              flush=True)
                        last_percent = current_percent  # 更新进度条
            else:
                print('\n')
                print('file upload done'.center(50, "-"))
            f.close()

    def progress_bar(self, total_size):
        current_percent = 0
        lsat_percent = 0
        rec_size = 0
        while True:
            rec_size = yield current_percent
            current_percent = int(rec_size / total_size * 100)
            if current_percent > lsat_percent:
                print('#' * int(current_percent / 2) + "{percent}%".format(percent=current_percent), end='\r',
                      flush=True)
                last_percent = current_percent  # 更新进度条


if __name__ == "__main__":
    client = FTPClient()
    client.interactive()  # 交互
