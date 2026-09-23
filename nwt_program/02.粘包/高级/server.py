# 服务端
import socket
import subprocess
import struct
import json

phone = socket.socket()

phone.bind(('192.168.14.230', 8849))

phone.listen(2)  # listen 允许2个人链接,剩下的链接等待

while 1:
    conn, addr = phone.accept()  # 等待客户端连接我,阻塞的状态中
    # print(f'链接来了{conn,addr}')

    while 1:
        try:
            from_client_data = conn.recv(1024)

            if from_client_data.upper() == b'Q':  # 正常退出 服务端跟着关闭
                print('客户正常退出聊天了')
                break

            result = from_client_data.decode('utf-8'),

            total_size = len(result)  # 字节
            print(f'总字节数:{total_size}')  # 查看字节

            head_dic = {  # 1 自定义报头
                'file_name': 'test1',  # 需要操作的文件名.使用变量
                'md5': 987654321,  # 文件字节的md5加密,校验使用.变量
                'total_size': total_size,  # 字节总长度
            }

            head_dic_json = json.dumps(head_dic)  # 2 json形式的报头

            head_dic_json_bytes = head_dic_json.encode('utf-8')  # 3 bytes形式报头

            len_head_dic_json_bytes = len(head_dic_json_bytes)  # 4 获取bytes形式的报头的总字节数

            four_head_bytes = struct.pack('i', len_head_dic_json_bytes)  # 5 将不固定的int总字节数编程固定长度的4个字节

            conn.send(four_head_bytes)  # 6 发送固定的4个字节

            conn.send(head_dic_json_bytes)  # 7 发送报头数据

            conn.send(result)  # 8 发送总数据

        except ConnectionResetError:  # 异常退出 会报错 写提示内容
            print('客户端链接中断了')
            break
    conn.close()
phone.close()