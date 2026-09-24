# 客户端
import socket
import struct
import json

phone = socket.socket()

phone.connect(('192.168.14.230', 8849))

while 1:
    to_server_data = input('>>>').strip().encode('utf-8')
    if not to_server_data:  # 服务端如果收到了空的内容,服务端就会一直阻塞中.无论是那一端发送,都不能为空
        print('发送内容不能为空')
        continue

    phone.send(to_server_data)
    if to_server_data.upper() == b'Q':  # 判断如果是Q的话就退出,正常退出
        break

    head_bytes = phone.recv(4)  # 1. 接收报头

    len_head_dic_json_bytes = struct.unpack('i', head_bytes)[0]  # 2 获得bytes类型字典的总字节数

    head_dic_json_bytes = phone.recv(len_head_dic_json_bytes)  # 3 接收bytes类型的dic数据

    head_dic_json = head_dic_json_bytes.decode('utf-8')  # 4 转化成json类型dic

    head_dic = json.loads(head_dic_json)  # 5 转化成字典形式的报头

    '''
    head_dic = {
            head_dic = {  # 1 自定义报头
                'file_name': 'test1',  # 需要操作的文件名.使用变量
                'md5': 987654321,  # 文件字节的md5加密,校验使用.变量
                'total_size': total_size,  # 字节总长度
            }
    '''

    total_data = b''  # 接收内容,依次相加bytes类型,如果只是英文可以不加ASCII码

    while len(total_data) < head_dic['total_size']:  # 接收的内容长度不会超过反解包头的长度,所以用判断
        total_data += phone.recv(1024)  # 本来就是反解报头,然后直接全部接收,然后每1024处理一次,直到结束

    print(len(total_data))
    print(total_data.decode('gbk'))

phone.close()