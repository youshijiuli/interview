#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :mad_client.py
# @Author:Mysticat

import json
import optparse
import os
import shelve
import socket


class FtpClient(object):
    MSG_SIZE = 1024

    def __init__(self):
        self.username = None
        self.terminal_display = None
        self.shelve_obj = shelve.open("Mad_FTP_db")
        self.current_dir = None

        parser = optparse.OptionParser()
        parser.add_option("-H", "--serverHost", dest="serverHost", help="ftp_base server ip_addr")
        parser.add_option("-P", "--port", type="int", dest="port", help="ftp_base server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-p", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()

        print(self.options, self.args, type(self.options))
        self.argvs_verification()

        self.make_connection()

    def argvs_verification(self):
        """
        校验参数的合法性
        :return:
        """
        if not self.options.serverHost or self.options.port:
            exit("Error: must supply servers and port parameters")

    def make_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.options.serverHost, self.options.port))

    def get_response(self):
        data = self.sock.recv(self.MSG_SIZE)
        return json.loads(data.decode('utf-8'))

    def send_msg(self, action_type, *args, **kwargs):
        """
        打包信息并发送
        :param action_type:
        :param args:
        :param kwargs:
        :return:
        """
        msg_send = {
            "action_type": action_type
        }
        # 整合两个字典
        msg_send.update(**kwargs)
        msg_send['fill'] = ""

        bytes_msg = json.dumps(msg_send).encode('utf-8')
        if self.MSG_SIZE > len(bytes_msg):
            msg_send["fill"] = msg_send["fill"].zfill(self.MSG_SIZE - len(bytes_msg))
            bytes_msg = json.dumps(msg_send).encode("utf-8")
        self.sock.send(bytes_msg)

    def auth(self):
        """用户认证"""
        count = 0  # 允许用户尝试登陆三次
        while count < 3:
            username = input("username:").strip()
            if not username:
                continue
            password = input("password:").strip()

            cmd = {
                "action_type": "auth",
                "username": username,
                "password": password
            }
            print(json.dumps(cmd).encode("utf-8"))
            self.sock.send(json.dumps(cmd).encode("utf-8"))

            response = self.get_response()
            # print("response: ", response)

            if response.get("status_code") == 200:  # pass auth
                self.username = username
                self.terminal_display = "[%s]>>: " % self.username
                self.current_dir = "\\"
                return True
            else:
                print(response.get("status_msg"))
            count += 1

    def unfished_file_check(self):
        """检查 shelve db, 把未正常传输完成的文件列表打印，按用户的指令决定是否重传"""
        if list(self.shelve_obj.keys()):
            print("------unfinished file list------")
            for index, abs_file in enumerate(self.shelve_obj.keys()):
                receive_size = os.path.getsize(self.shelve_obj[abs_file][1])
                print("%s.   %s    %s   %s    %s" % (index, abs_file,
                                                     self.shelve_obj[abs_file][0],
                                                     receive_size,
                                                     int(receive_size / self.shelve_obj[abs_file][0] * 100)))
            while True:
                choice = input("[select file index to re-download]: ").strip()
                if not choice: continue
                if choice == "back": break
                if choice.isdigit():
                    choice = int(choice)
                    if choice >= 0 and choice <= index:
                        select_file = list(self.shelve_obj.keys())[choice]
                        already_receive_size = os.path.getsize(self.shelve_obj[select_file][1])
                        print("tell server to resend file", select_file)
                        #
                        self.send_msg("re_get", file_size=self.shelve_obj[select_file][0],
                                      received_size=already_receive_size,
                                      abs_filename=select_file)

                        response = self.get_response()
                        if response.get("status_code") == 401:
                            local_filename = self.shelve_obj[select_file][1]
                            f = open(local_filename, "ab")
                            total_size = self.shelve_obj[select_file][0]
                            recv_size = already_receive_size
                            current_size = int(recv_size / total_size * 100)
                            progress_bar = self.progress_bar(total_size, current_size, current_size)
                            progress_bar.__next__()
                            while recv_size < total_size:
                                if total_size - recv_size < 8196:  # last receive
                                    data = self.sock.recv(8196)
                                else:
                                    data = self.sock.recv(8196)

                                recv_size += len(data)
                                progress_bar.send(recv_size)
                                f.write(data)
                                # progress_bar.send(receive_size)
                                # print(file_size, receive_size)
                            else:
                                print("file re-get done")
                        else:
                            print(response.get("status_msg"))

    def interactive(self):
        """交互指令"""
        if self.auth():
            self.unfished_file_check()

            while True:
                user_input = input(self.terminal_display).strip()
                if not user_input:
                    continue

                cmd_list = user_input.split()
                if hasattr(self, "_%s" % cmd_list[0]):
                    func = getattr(self, "_%s" % cmd_list[0])
                    func(cmd_list[1:])

    def parameter_check(self, args, min_args=None, max_args=None, exact_args=None):
        """参数个数合法性检查"""
        if min_args:
            if len(args) < min_args:
                print("must provide at least %s parameters but %s provide" % (min_args, len(args)))
                return False
        if max_args:
            if len(args) > max_args:
                print("need provide at most %s parameters but %s provide" % (max_args, len(args)))
                return False
        if exact_args:
            if len(args) != exact_args:
                print("need provide exactly %s parameters but %s provide" % (exact_args, len(args)))
                return False

        return True

    def progress_bar(self, total_size, current_percent=0, last_percent=0):

        # current_percent = 0
        # last_percent = 0

        while True:
            recevie_size = yield current_percent
            current_percent = int(recevie_size / total_size * 100)

            if current_percent > last_percent:
                print("#" * int(current_percent / 2) + "{percent}%".format(percent=current_percent), end="\r",
                      flush=True)
                last_percent = current_percent

    def _get(self, cmd_args):
        """
        download file from ftp_base server
        1. 拿到文件名
        2. 发送到远程
        3. 等待服务器响应
            3.1 如果文件存在，拿到文件大小
                3.1.1 循环接收
            3.2 文件不存在
                返回状态码
                print status_msg
        """
        if self.parameter_check(cmd_args, min_args=1):
            filename = cmd_args[0]
            self.send_msg(action_type="get", filename=filename)
            response = self.get_response()
            if response.get("status_code") == 301:  # file exist, ready to receive
                file_size = response.get("file_size")
                receive_size = 0

                progress_bar = self.progress_bar(file_size)
                progress_bar.__next__()

                # save to shalve_db
                file_abs_path = os.path.join(self.current_dir, filename)
                self.shelve_obj[file_abs_path] = (file_size, "%s.dowmload" % filename)

                f = open("%s.dowmload" % filename, "wb")
                while receive_size < file_size:
                    if file_size - receive_size < 8196:  # last receive
                        data = self.sock.recv(8196)
                    else:
                        data = self.sock.recv(8196)

                    receive_size += len(data)
                    f.write(data)
                    progress_bar.send(receive_size)
                    # print(file_size, receive_size)
                else:
                    print("\n")
                    print("------file [%s] recv down, recv size [%s]------" % (filename, file_size))
                    del self.shelve_obj[file_abs_path]
                    f.close()
                    os.rename("%s.dowmload" % filename, filename)
            else:
                print(response.get("status_msg"))

    def _put(self, cmd_args):
        """上传本地文件到服务器
            1. 确保本地文件存在
            2. 拿到文件名+大小，放到信息头里发给远程
            3. 打开文件，发送内容
        """
        if self.parameter_check(cmd_args, exact_args=1):
            local_file = cmd_args[0]
            total_size = os.path.getsize(local_file)
            if os.path.isfile(local_file):  # 如果文件存在
                self.send_msg(action_type="put", file_size=os.path.getsize(local_file), file_name=local_file)
                # response = self.get_response()
                f = open(local_file, "rb")

                receive_size = 0
                progress_bar = self.progress_bar(total_size)
                progress_bar.__next__()
                for line in f:
                    self.sock.send(line)
                    receive_size += len(line)
                    progress_bar.send(receive_size)

                else:
                    print("\n")
                    print("file upload done!".center(50, "-"))
                f.close()

    def _ls(self, cmd_args):
        self.send_msg(action_type="ls")
        response = self.get_response()
        # print(response)
        if response.get("status_code") == 302:
            cmd_result_size = response.get("cmd_result_size")
            recieve_size = 0
            cmd_result = b""
            while recieve_size < cmd_result_size:
                if cmd_result_size - recieve_size < 8192:  # last recieve
                    data = self.sock.recv(cmd_result_size - recieve_size)
                else:
                    data = self.sock.recv(8192)
                recieve_size += len(data)
                cmd_result += data
            else:
                print(cmd_result.decode("gbk"))

    def _cd(self, cmd_args):
        """change to target dir"""
        if self.parameter_check(cmd_args, exact_args=1):
            target_dir = cmd_args[0]
            self.send_msg(action_type="cd", target_dir=target_dir)
            response = self.get_response()
            # print(response)
            if response.get("status_code") == 350:  # change dir
                self.terminal_display = "[\\root%s]" % response.get("current_dir")
                self.current_dir = response.get("current_dir")
            else:
                print(response.get("status_msg"))


if __name__ == '__main__':
    client = FtpClient()
    client.interactive()
