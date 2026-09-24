import struct
#把一个数字打包成固定长度的4字节，得到字节格式数据
obj=struct.pack('i',1024) # 'i'是格式
print(obj)
print(len(obj))

# 解包，得到元祖类型数据
l=struct.unpack('i',obj)
print(l)

# b'\x00\x04\x00\x00'
# 4
# (1024,)