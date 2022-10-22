import struct

data = b'\x7e\x00'
nor = list(data)
test = [210, 4, 41, 9, 128, 13]

# value = int.from_bytes(test[2:4], "little", signed=False)
# print(nor)
print(struct.unpack('<HHH',bytes(test)))  # 126

# print(struct.pack('<hhl',210,2,41))
