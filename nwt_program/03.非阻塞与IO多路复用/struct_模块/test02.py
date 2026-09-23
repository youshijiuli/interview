import struct

"""
-  pack(fmt, v1, v2, ...) ------ 根据所给的fmt描述的格式将值v1，v2，...转换为一个字符串。
-  unpack(fmt, bytes)  ------ 根据所给的fmt描述的格式将bytes反向解析出来，返回一个元组。
-  calcsize(fmt)       ------ 根据所给的fmt描述的格式返回该结构的大小。
"""

pack_num = struct.pack('i', 126)
print('pack_string', pack_num, len(pack_num))
unpack_num = struct.unpack('i', pack_num)
print('unpack_string', unpack_num)

# pack_string b'~\x00\x00\x00' 4
# unpack_string (126,)

print("len: ", struct.calcsize('i'))  # len:  4
print("len: ", struct.calcsize('ii'))  # len:  8
print("len: ", struct.calcsize('f'))  # len:  4
print("len: ", struct.calcsize('ff'))  # len:  8
print("len: ", struct.calcsize('s'))  # len:  1
print("len: ", struct.calcsize('ss'))  # len:  2
print("len: ", struct.calcsize('d'))  # len:  8
print("len: ", struct.calcsize('dd'))  # len:  16
print("len: ", struct.calcsize('B'))  # len:  1
print("len: ", struct.calcsize('!BH'))  # len:  3
print("len: ", struct.calcsize('!BQ'))  # len:  9