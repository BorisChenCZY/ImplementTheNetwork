def _unpack_flags(byte):
    byte = bin(int.from_bytes(byte, 'little'))[2:]
    array = [0 for i in range(8)]
    for i in range(len(byte)):
        if byte[i] == '1':
            array[8 - (len(byte) - i)] = 1
    return array

a = int.to_bytes(3, 1, 'little')
print(_unpack_flags(a))