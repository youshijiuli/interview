import struct


"""
以下是一些常见的功能和用法：
struct.pack(format, v1, v2,...): 按照指定的格式将数据打包成二进制字符串。
struct.unpack(format, buffer): 按照指定的格式从二进制字符串中解包数据。
常见的格式字符包括：
'i' : 整数（4 字节）
'f' : 浮点数（4 字节）
's' : 字符串

"""

# 打包数据
data = struct.pack('if', 10, 3.14)
print("打包后的二进制数据:", data)

# 解包数据
unpacked_data = struct.unpack('if', data)
print("解包后的整数和浮点数:", unpacked_data)

# 处理字符串
name = "Python"
packed_name = struct.pack('10s', name.encode())
print("打包后的字符串:", packed_name)
unpacked_name = struct.unpack('10s', packed_name)[0].decode().rstrip('\x00')
print("解包后的字符串:", unpacked_name)

"""
打包后的二进制数据: b'\n\x00\x00\x00\xc3\xf5H@'
解包后的整数和浮点数: (10, 3.140000104904175)
打包后的字符串: b'Python\x00\x00\x00\x00'
解包后的字符串: Python
"""