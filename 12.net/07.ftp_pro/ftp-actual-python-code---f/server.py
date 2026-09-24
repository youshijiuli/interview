from socket import socket, AF_INET, SOCK_STREAM
import os, random, json, struct, hashlib


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
                print('\r文件下载中：100%，已完成！', end='\n')
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
                print('\r文件传输：100%')
                break
        file.seek(0)
        file_md5 = hashlib.md5(file.read()).hexdigest()
        pack_send_info(file_md5, conn)


def cd(args, data_conn):
    global config
    if len(args) == 0:
        os.chdir(config["local_dir"])
        pack_send_info("Directory successfully changed.", data_conn)
        data_conn.close()
        return
    dir_path = os.path.join(config["local_dir"], args[0])
    print(dir_path)
    if os.path.isdir(dir_path):
        os.chdir(dir_path)
        pack_send_info("Directory successfully changed.", data_conn)
    else:
        pack_send_info("Failed to change directory.", data_conn)
    data_conn.close()


def pwd(args, data_conn):
    global config
    data = os.getcwd()
    pack_send_info(data[len(config["local_dir"]):], data_conn)
    data_conn.close()


def put(args, data_conn):
    global local_md5
    if len(args) == 0:
        args = unpack_recv_info(data_conn)
        if type(args) is not list:
            data_conn.close()
            return
    is_file = unpack_recv_info(data_conn)
    if is_file == 0:
        data_conn.close()
        return
    if len(args) == 1 and os.path.isfile(args[0]) or len(args) == 2 and os.path.isfile(args[1]):
        pack_send_info("file exists, do you want to recover it ? (y/n) :", data_conn)
        choose = unpack_recv_info(data_conn)
        if choose.lower() == 'n':
            data_conn.close()
            return
    else:
        pack_send_info("Successfully to open file.", data_conn)
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


def get(args, data_conn):
    if len(args) == 0:
        args = unpack_recv_info(data_conn)
        if type(args) is not list:
            data_conn.close()
            return
    if os.path.isfile(args[0]):
        pack_send_info("Successfully to open file.", data_conn)
    else:
        pack_send_info("Failed to open file.", data_conn)
        data_conn.close()
        return
    is_file = unpack_recv_info(data_conn)
    if is_file == "file exist":
        choose = unpack_recv_info(data_conn)
        if choose.lower() == 'n':
            data_conn.close()
            return
    pack_send_file(args[0], data_conn)
    data_conn.close()


def ls(args, data_conn):
    # 命令后面没有参数
    if len(args) == 0:
        file_list = os.listdir(os.getcwd())
        pack_send_info(file_list, data_conn)
    # 当命令后面有参数时，只看第一个参数，后面多余的参数不理
    else:
        dir_path = os.path.join(os.getcwd(), args[0])
        # 三元表达式写法：当拼接的目录不存在时，取” “值，当存在时，取该目录下的所有文件及子目录列表
        pack_send_info(os.listdir(dir_path) if os.path.isdir(dir_path) else " ", data_conn)
        # 另外两种三元表达式写法
        # pack_send_info((" ", os.listdir(dir_path))[os.path.isdir(dir_path)], data_conn)
        # pack_send_info({os.listdir(dir_path), " "}[os.path.isdir(dir_path)], data_conn)
    data_conn.close()


def dir(args, data_conn):
    # 命令后面没有参数
    files_status = {}
    if len(args) == 0:
        for file in os.listdir(os.getcwd()):
            files_status[file] = os.stat(file)
        pack_send_info(files_status, data_conn)
    # 当命令后面有参数时，只看第一个参数，后面多余的参数不理
    else:
        dir_path = os.path.join(os.getcwd(), args[0])
        if os.path.isdir(dir_path):
            print(dir_path)
            print(os.listdir(dir_path))
            for file in os.listdir(dir_path):
                files_status[file] = os.stat(os.path.join(dir_path, file))
            pack_send_info(files_status, data_conn)
        else:
            pack_send_info("", data_conn)
    data_conn.close()


def mls(args, data_conn):
    if len(args) == 0:
        args = unpack_recv_info(data_conn)
        if type(args) is not list:
            data_conn.close()
            return
    for dir0 in args:
        dir_path = os.path.join(os.getcwd(), dir0)
        pack_send_info(os.listdir(dir_path) if os.path.isdir(dir_path) else " ", data_conn)
    data_conn.close()


def mdir(args, data_conn):
    if len(args) == 0:
        args = unpack_recv_info(data_conn)
        if type(args) is not list:
            data_conn.close()
            return
        print(args)
    for dir0 in args:
        files_status = {}
        dir_path = os.path.join(os.getcwd(), dir0)
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                files_status[file] = os.stat(os.path.join(dir_path, file))
            pack_send_info(files_status, data_conn)
        else:
            pack_send_info("", data_conn)
    data_conn.close()


def delete(args, data_conn):
    if len(args) == 0:
        args = unpack_recv_info(data_conn)
    try:
        os.remove(args[0])
        pack_send_info("Successfully to delete file.", data_conn)
    except FileNotFoundError:
        pack_send_info("Failed to delete file.", data_conn)
        return
    data_conn.close()


# 控制连接通道：
def connected(client_ip, server_config, ctrl_conn, available_commd):
    while True:
        client_config = unpack_recv_info(ctrl_conn)
        print(client_config)
        print(config)
        # 排除服务端没开启被动模式，但客户端想要被动模式连接的情况
        if client_config["PASV"] == "yes":
            if server_config["used_PASV"] == "no":
                pack_send_info("Error[10048]: doesn't open PASV !", ctrl_conn)
                # 交换信息失败直接断联
                ctrl_conn.close()
                return
        pack_send_info('200 STOR correctly', ctrl_conn)
        user_input = unpack_recv_info(ctrl_conn)
        command = user_input.split(" ")[0]
        args = user_input.split(" ")[1:]
        # 如果是quit命令直接断联
        if command == 'quit' or command == 'close':
            ctrl_conn.close()
            return
        # 未知命令
        elif command not in available_commd.keys():
            print("Unknown command %s !!!" % command)
            continue
        # 被动模式
        if client_config["PASV"] == "yes":
            # 生成服务端随机端口P
            server_data_port = random.randint(int(server_config["pasv_min_port"]), int(server_config["pasv_max_port"]))
            data_socket = PASV_conn(config["listen_IP"], str(server_data_port), ctrl_conn)
            data_conn, client_add = data_socket.accept()
        # 主动模式
        else:
            data_conn = no_PASV_conn(client_ip, config["listen_IP"], int(config["connect_from_port"]), ctrl_conn)
        available_commd[command](args, data_conn)


# 被动模式（是针对数据连接的）连接建立：
def PASV_conn(server_ip, server_port, ctrl_conn):
    pack_send_info(server_port, ctrl_conn)
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind((server_ip, int(server_port)))
    data_socket.listen(5)
    return data_socket


# 主动模式连接建立：
def no_PASV_conn(client_ip, server_ip, server_port, ctrl_conn):
    client_port = int(unpack_recv_info(ctrl_conn))
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind((server_ip, server_port))
    data_socket.connect((client_ip, client_port))
    return data_socket


def auth(server_config, conn):
    login_username = unpack_recv_info(conn)
    with open(server_config["user_db"], 'r', encoding='utf-8') as file:
        while True:
            try:
                username = file.readline().strip()
                password = file.__next__().strip()
                if login_username == username:
                    pack_send_info("331 Please specify the password.", conn)
                    break
            except StopIteration:
                pack_send_info("530 login incorrect.", conn)
                return 1
    login_password = unpack_recv_info(conn)
    if login_password == password:
        pack_send_info("230 Login successful.", conn)
        return 0
    else:
        pack_send_info("530 Login incorrect.", conn)
        return 1


if __name__ == '__main__':
    config = {}
    # 读取配置文件
    with open('server_ftp_conf.txt', 'r', encoding='utf-8') as config_file:
        for line in config_file.readlines():
            config[line.split('=')[0]] = line.split('=')[1].split("\n")[0]
    os.chdir(config["local_dir"])
    # 定义功能
    command_dict = {
        "pwd": pwd,
        "put": put,
        "get": get,
        "ls": ls,
        "dir": dir,
        "mls": mls,
        "mdir": mdir,
        "delete": delete,
        "cd": cd
    }
    # 控制连接
    ctrl_socket = socket(AF_INET, SOCK_STREAM)
    ctrl_socket.bind((config["listen_IP"], int(config["listen_port"])))
    ctrl_socket.listen(5)

    while True:
        try:
            ctrl_conn, add = ctrl_socket.accept()
            exit_code = auth(config, ctrl_conn)
            if exit_code == 0:
                os.chdir(config["local_dir"])
                connected(add[0], config, ctrl_conn, command_dict)
            else:
                command = unpack_recv_info(ctrl_conn)
                if command == "close":
                    ctrl_conn.close()
        except ConnectionResetError:
            print("客户端异常断开！")
            continue

