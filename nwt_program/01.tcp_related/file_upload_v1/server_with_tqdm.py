import socket
from tqdm import tqdm
import os


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9000))
    server.listen(5)
    print('等待客户端连接....')
    while True:
        conn, addr = server.accept()
        print(f'客户端{addr}连接成功，准备接收文件')

        # 第一步：接收文件名
        file_name = conn.recv(1024).decode('utf-8')
        # 第二步：接收文件大小（这里需要客户端配合发送文件大小信息）
        file_size_bytes = conn.recv(1024)
        file_size = int(file_size_bytes.decode('utf-8'))

        received_data = b''
        # 使用 tqdm 创建进度条，total 参数为文件总大小，单位是字节
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Receiving {file_name}', ncols=80) as pbar:
            while len(received_data) < file_size:
                data = conn.recv(1024)
                if not data:
                    break
                received_data += data
                # 更新进度条，每次接收的数据长度就是进度增加量
                pbar.update(len(data))

        # 保存文件
        with open(f'upload_{file_name}', 'wb') as f:
            f.write(received_data)

        conn.send('文件接受成功！'.encode('utf-8'))
        conn.close()
        print(f'文件 {file_name} 接收完成，已保存为 upload_{file_name}')

    server.close()


if __name__ == '__main__':
    main()