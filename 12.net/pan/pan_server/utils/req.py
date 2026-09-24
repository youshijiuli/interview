#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :req.py
# @Author:Mysticat


import struct


def send_data(conn, content: str):
    """
    发送数据
    :return:
    """
    data = content.encode('utf-8')
    header = struct.pack('i', len(data))
    conn.sendall(header)
    conn.sendall(data)


def recv_data(conn, chunk_size=1024):
    """
    接收数据
    :return:
    """
    # 获取头部信息：数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        has_read_size += len(chunk)
        bytes_list.append(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    # 获取数据
    data_list = []
    has_data_size = 0
    while has_data_size < data_length:
        size = chunk_size if (data_length - has_data_size) > chunk_size else data_length - has_data_size
        chunk = conn.recv(size)
        data_list.append(chunk)
        has_data_size += len(chunk)

    data = b"".join(data_list)

    return data


def recv_save_file(conn, save_file_path, chunk_size=1024):
    """
    接受并且保存文件
    :param conn:
    :param save_file_path:
    :param chunk_size:
    :return:
    """
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        bytes_list.append(chunk)
        has_read_size += len(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    file_obj = open(save_file_path, 'wb')
    has_read_data_size = 0

    while True:
        size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
        chunk = conn.recv(size)
        file_obj.write(chunk)
        file_obj.flush()
        has_read_data_size += len(chunk)

    file_obj.close()


def send_file_by_seek(conn, file_size, file_path, seek=0):
    """
    读取并且发送文件
    :param conn:
    :param file_size:
    :param file_path:
    :param seek:
    :return:
    """
    header = struct.pack('i', file_size)
    conn.sendall(header)

    has_send_size = 0
    file_object = open(file_path, mode='rb')
    if seek:
        file_object.seek(seek)
    while has_send_size < file_size:
        chunk = file_object.read(2048)
        conn.sendall(chunk)
        has_send_size += len(chunk)
    file_object.close()
