import socket
import os


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9000))

    file_path = input('请输入文件路径:').strip()
    file_name = file_path.split('/')[-1]
    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 第一步：发送文件名
    client.send(file_name.encode('utf-8'))
    # 第二步：发送文件大小
    client.send(str(file_size).encode('utf-8'))

    # 第三步：发送文件内容
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            client.send(chunk)
    recv_msg = client.recv(1024)
    print(recv_msg.decode('utf-8'))
    client.close()


if __name__ == '__main__':
    main()