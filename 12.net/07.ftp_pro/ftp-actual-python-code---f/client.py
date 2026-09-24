from socket import socket, AF_INET, SOCK_STREAM
import os, random, json, struct, time, hashlib


# 解出接收的是文本数据时的头部信息
def unpack_recv_info(conn):
    pack = conn.recv(4)
    head_size = struct.unpack("i", pack)[0]
    head = json.loads(conn.recv(head_size).decode('utf-8'))
    message = json.loads(conn.recv(head["data_size"]).decode('utf-8'))
    return message


# 当发送文本数据时使用的头部信息打包函数
def pack_send_info(data, conn):
    data_json = json.dumps(data).encode('utf-8')
    head = {
        "data_size": len(data_json)
    }
    head_json = json.dumps(head).encode('utf-8')
    pack_head_json_size = struct.pack("i", len(head_json))
    conn.send(pack_head_json_size)
    conn.send(head_json)
    conn.send(data_json)


# 解出接收的是文件数据时的头部信息
def unpack_recv_file(file_name, conn):
    pack = conn.recv(4)
    head_size = struct.unpack("i", pack)[0]
    head = json.loads(conn.recv(head_size).decode('utf-8'))
    with open(file_name, 'wb') as file:
        print('\r文件下载中：0%', end='')
        tmp_size = head["data_size"]
        while True:
            if tmp_size >= 1024:
                file.write(conn.recv(1024))
                tmp_size -= 1024
                process = (head["data_size"] - tmp_size) / head["data_size"] * 100
                print('\r文件下载中：%s%%' % str(process.__round__(2)), end='')
            else:
                file.write(conn.recv(tmp_size))
                print('\r文件下载中：100%')
                break
    with open(file_name, 'rb') as download_file:
        file_md5 = hashlib.md5(download_file.read()).hexdigest()
    return file_md5


# 当发送文件数据时使用的头部信息打包函数
def pack_send_file(file_name, conn):
    total_size = os.path.getsize(file_name)
    head = {
        "data_size": total_size,
    }
    head_json = json.dumps(head).encode('utf-8')
    head_json_size = len(head_json)
    pack_head_json_size = struct.pack("i", head_json_size)
    conn.send(pack_head_json_size)
    conn.send(head_json)
    with open(file_name, 'rb') as file:
        print('\r文件传输：0%', end='')
        tmp_size = total_size
        while True:
            if tmp_size >= 1024:
                process = (total_size - tmp_size) / total_size * 100
                conn.send(file.read(1024))
                tmp_size -= 1024
                print('\r文件传输：%s%%' % str(process.__round__(2)), end='')
            else:
                conn.send(file.read(tmp_size))
                print('\r文件传输：100%，已完成！', end='\n')
                break
        file.seek(0)
        file_md5 = hashlib.md5(file.read()).hexdigest()
        pack_send_info(file_md5, conn)


def get_commd_info(args):
    global command_dict, local_command_dict
    if len(args) == 0:
        i = 0
        for key in command_dict.keys():
            i += 1
            print(key, end="\t\t")
            if i != 0 and i % 4 == 0:
                print()
        for key in local_command_dict.keys():
            if key == "quit":
                continue
            i += 1
            print(key, end="\t\t")
            if i != 0 and i % 4 == 0:
                print()
        print()
    elif len(args) == 1:
        with open('help.txt', 'r', encoding='utf-8') as help_file:
            for line in help_file.readlines():
                tmp_list = line.strip().split(":")
                if tmp_list[0] == args[0]:
                    # 这为什莫要指定结束分隔符？才不会与下一行输入多一个空行呢？？？
                    print(tmp_list[0], "\t", tmp_list[1])
                    return
            print("Unknown command '%s' !" % args[0])
    else:
        print("too many argument for command !")


def cd(args, data_conn):
    print(unpack_recv_info(data_conn))
    data_conn.close()


def pwd(args, data_conn):
    path = unpack_recv_info(data_conn)
    if len(path) == 0:
        print("\\")
    else:print(path)
    data_conn.close()


def lcd(args):
    if len(args) == 1:
        try:
            os.chdir(args[0])
        except FileNotFoundError:
            print("system can not find such as file. : '%s' !" % args[0])
            return
    elif len(args) > 1:
        print("too many argument for command !")
        return
    print("present local work path is %s" % os.getcwd())


def put(args, data_conn):
    if len(args) == 0:
        local_file_name = input("local file : ").strip()
        if local_file_name == "":
            pack_send_info("", data_conn)
            data_conn.close()
            return
        args.append(local_file_name)
        server_file_name = input("remote file : ").strip()
        args.append(server_file_name)
        print(args)
        pack_send_info(args, data_conn)
        put(args, data_conn)
        return
    if not os.path.isfile(args[0]):
        print("can't not find file %s !" % args[0])
        pack_send_info(0,data_conn)
        data_conn.close()
        return
    pack_send_info(1,data_conn)
    server_info = unpack_recv_info(data_conn)
    if server_info == "file exists, do you want to recover it ? (y/n) :":
        print(server_info, end="")
        choose = input("").strip()
        pack_send_info(choose, data_conn)
        if choose.lower() == 'n':
            data_conn.close()
            return
    else:
        print(server_info)
    pack_send_file(args[0], data_conn)
    data_conn.close()


def get(args, data_conn):
    global local_md5
    if len(args) == 0:
        server_file_name = input("remote file : ").strip()
        if server_file_name == "":
            pack_send_info("", data_conn)
            data_conn.close()
            return
        args.append(server_file_name)
        local_file_name = input("local file : ").strip()
        args.append(local_file_name)
        pack_send_info(args, data_conn)
        get(args, data_conn)
        return
    server_info = unpack_recv_info(data_conn)
    if server_info == "Successfully to open file.":
        if len(args) == 1 and os.path.isfile(args[0]) or len(args) == 2 and os.path.isfile(args[1]):
            pack_send_info("file exist",data_conn)
            choose = input("file exists, do you want to recover it ? (y/n) :").strip()
            pack_send_info(choose,data_conn)
            if choose.lower() == 'n':
                data_conn.close()
                return
        else: pack_send_info("file not exist", data_conn)
        print(server_info)
        if len(args) == 1 or args[1] == "":
            local_md5 = unpack_recv_file(args[0], data_conn)
        elif len(args) == 2:
            local_md5 = unpack_recv_file(args[1], data_conn)
        remote_md5 = unpack_recv_info(data_conn)
        if remote_md5 != local_md5:
            print("file was incomplete during transmission. The system reclaims the incomplete file !")
            if len(args) == 1 or args[1] == "":
                os.remove(args[0])
            elif len(args) == 2:
                os.remove(args[1])
        else:
            print("file transfer successful !")
    data_conn.close()


def print_file_info(files):
    mode = {
        0: "---",
        1: "--x",
        2: "-w-",
        4: "r--",
        5: "r-x",
        6: "rw-",
        7: "rwx"
    }
    for file_name, file_status in files.items():
        user_mode = int(oct(file_status[0])[-3])
        group_mode = int(oct(file_status[0])[-2])
        other_mode = int(oct(file_status[0])[-1])
        if file_status[3] == 1:
            print("-", end="")
        else:
            print("d", end="")
        print(mode[user_mode], mode[group_mode], mode[other_mode], ".", end='\t\t', sep="")
        print(file_status[3], "\t", file_status[4], "\t", file_status[5], "\t", str(file_status[6]).rjust(8),
              end="\t\t", sep="")
        # 时间戳换成结构化元组时间，结构化元组时间再转换成格式化时间
        print(time.strftime("%m月 %d %M:%S", time.localtime(file_status[8])), end='\t')
        print(file_name)


def dir(args, data_conn):
    files = unpack_recv_info(data_conn)
    if files != "":
        print_file_info(files)
    data_conn.close()


def ls(args, data_conn):
    file_list = unpack_recv_info(data_conn)
    if file_list != " ":
        for file in file_list:
            print(file)
    data_conn.close()


def mls(args, data_conn):
    if len(args) == 0:
        args = input("远程文件名：").strip().split(" ")
        if args == "":
            pack_send_info("", data_conn)
            data_conn.close()
            return
        pack_send_info(args, data_conn)
        mls(args, data_conn)
        return
    for dir0 in args:
        file_list = unpack_recv_info(data_conn)
        if file_list == " ":
            continue
        for file in file_list:
            print("%s/%s" % (dir0,file))
    data_conn.close()


def mdir(args, data_conn):
    if len(args) == 0:
        args = input("remote file : ").strip().split(" ")
        if args == "":
            pack_send_info("", data_conn)
            data_conn.close()
            return
        pack_send_info(args, data_conn)
        mdir(args, data_conn)
        return
    for dir0 in args:
        file_list = unpack_recv_info(data_conn)
        if file_list == "":
            continue
        print(dir0)
        print_file_info(file_list)
    data_conn.close()


def delete(args, data_conn):
    if len(args) == 0:
        file_name = input("file : ")
        args.append(file_name)
        delete(args, data_conn)
    pack_send_info(args, data_conn)
    print(unpack_recv_info(data_conn))
    data_conn.close()


def close_connected(conn):
    pack_send_info("close", conn)
    print("Goodbye.")
    conn.close()


def try_to_connect(client_config, args, client_port):
    if len(args) == 0:
        print("usage: open hostname [port]")
        return 1
        # 控制连接
    server_IP = args[0]
    if len(args) == 1:
        server_port = 21
    else:
        if not args[1].isalnum():
            print("please enter the correct port.")
            return 1
        server_port = args[1]
    ctrl_socket = socket(AF_INET, SOCK_STREAM)
    ctrl_socket.bind((client_config["listen_ip"], client_port))
    try:
        ctrl_socket.connect((server_IP, server_port))
        return ctrl_socket
    except Exception:
        print("unknown hostname %s." % server_IP)
        return 1


def menu():
    print('=' * 35)
    print('*' * 5, '成功进入FTP功能'.center(18, ' '), '*' * 5)
    print('*' * 5, "输入'help'查看帮助信息".center(16, ' '), '*' * 5)
    print('*' * 5, '退出：quit'.center(20, ' '), '*' * 5)
    print('tips：连接认证失败需要先close再重新连接'.center(5, ' '))
    print('=' * 35)


def exit_ftp(args):
    quit()


# 控制连接通道：
def connected(server_IP, ctrl_conn, ctrl_port, available_commd, local_available_commd):
    client_config = {}
    data_port = ctrl_port  # 先定义好数据连接端口从控制连接端口开始，每一次建立都会在此基础上+1
    while True:
        user_input = input('ftp_base > ').strip()
        command = user_input.split(" ")[0]
        args = user_input.split(" ")[1:]
        if command != 'close' and command != 'quit' and command in local_available_commd.keys():
            local_available_commd[command](args)
            continue
        # 未知命令
        elif command not in available_commd.keys() and command not in local_available_commd.keys():
            print("invalid command '%s' !!!" % command)
            continue
        # ，除了监听端口不可改，其余跟服务端交换的信息，通过配置文件确定，程序运行时，修改配置文件保存后也可使用最新的配置
        with open('client_ftp_conf.txt', 'r', encoding='utf-8') as config_file:
            for line in config_file.readlines():
                client_config[line.split('=')[0]] = line.split('=')[1].split('\n')[0]
        pack_send_info(client_config, ctrl_conn)
        server_info = unpack_recv_info(ctrl_conn)
        print(server_info)
        # 如果服务端交换信息成功（主动或被动模式与服务端不冲突）
        if server_info.split(" ")[0] == "200":
            pack_send_info(user_input, ctrl_conn)
            # quit命令直接断联
            if command == 'quit':
                ctrl_conn.close()
                print('连接断开......')
                quit()
            elif command == 'close':
                print("Goodbye.")
                ctrl_conn.close()
                return 1
            # 命令输入有效
            else:
                data_port += 1  # 数据连接端口
                # 被动模式
                if client_config["PASV"] == "yes":
                    data_conn = PASV_conn(server_IP, client_config["listen_ip"], data_port, ctrl_conn)
                # 主动模式
                else:
                    data_socket = no_PASV_conn(client_config["listen_ip"], data_port, ctrl_conn)
                    data_conn, client_add = data_socket.accept()
            available_commd[command](args, data_conn)
        # 交换信息失败，直接断联
        else:
            ctrl_conn.close()
            break


# 被动模式（是针对数据连接的）连接建立：
def PASV_conn(server_ip, client_ip, port, ctrl_conn):
    P = int(unpack_recv_info(ctrl_conn))
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind((client_ip, port))
    data_socket.connect((server_ip, P))
    return data_socket


# 主动模式连接建立：
def no_PASV_conn(ip, port, ctrl_conn):
    pack_send_info(str(port), ctrl_conn)
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind((ip, port))
    data_socket.listen(5)
    return data_socket


def auth(conn):
    username = input("user: ").strip()
    pack_send_info(username,conn)
    server_info = unpack_recv_info(conn)
    print(server_info)
    if server_info.split(" ")[0] == "331":
        password = input("password: ").strip()
        pack_send_info(password, conn)
        server_info = unpack_recv_info(conn)
        print(server_info)
        if server_info.split(" ")[0] == "230":
            return 0
        elif server_info.split(" ")[0] == "530":
            return 2
    elif server_info.split(" ")[0] == "530":
        return 2


if __name__ == '__main__':
    config = {}
    # 读取ftp配置文件
    with open('client_ftp_conf.txt', 'r', encoding='utf-8') as config_file:
        for line in config_file.readlines():
            config[line.split('=')[0]] = line.split('=')[1].split('\n')[0]
    # 定义功能，分为两部分：本地命令、远程命令
    local_command_dict = {
        "open": try_to_connect,
        "lcd": lcd,
        "close": close_connected,
        "help": get_commd_info,
        "quit": exit_ftp
    }
    command_dict = {
        "cd": cd,
        "pwd": pwd,
        "put": put,
        "get": get,
        "ls": ls,
        "dir": dir,
        "mls": mls,
        "mdir": mdir,
        "delete": delete,
        "quit": None
    }
    exit_code = 1
    menu()
    while True:
        user_input = input("ftp_base > ").strip()
        command = user_input.split(" ")[0]
        args = user_input.split(" ")[1:]
        if command != 'quit' and command in command_dict.keys():
            if exit_code == 1:
                print("percent server is unconnected.")
            elif exit_code == 2:
                print("please login first.")
            continue
        elif command == "open":
            if exit_code == 2:
                print("already connecting to %s , please close the connection first." % args[0])
                continue
            # 取出配置文件中定义的监听端口
            ctrl_port = random.randint(int(config["listen_min_port"]),
                                       int(config["listen_max_port"]))
            ctrl_conn = try_to_connect(config,args, ctrl_port)
            if ctrl_conn == 1:
                continue
            exit_code = auth(ctrl_conn)
            if exit_code == 0:
                exit_code = connected(args[0], ctrl_conn, ctrl_port, command_dict, local_command_dict)
            continue
        elif command == "close":
            try:
                close_connected(ctrl_conn)
                exit_code = 1
            except Exception:
                print("present session unconnected.")
        elif command not in local_command_dict.keys():
            print("invalid command '%s' !!!" % command)
        else:
            local_command_dict[command](args)





