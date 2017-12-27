import array
import struct
import os
HEADER = 8

class UDP_Socket(object):
    def __init__(self):
        self.IP = None
        self.src_ip = None
        self.src_port = None
    
    def bind(self, src_ip, src_port):
        self.src_ip = src_ip
        self.src_port = src_port
        self.IP = Network(src_ip, dst_ip)
        
    def recvfrom(self):
        datagrem, dst_ip = IP.recv()
        
    
    def sendto(self, datagrem, address):
        dst_ip = address[0]
        dst_port = address[1]
        src_ip = self.src_ip if self.src_ip is not None else get_ip()
        src_port = self.src_port if self.src_port is not None else get_port()
        if self.IP is None:
        
        self.IP.send(UDP(src_port, dst_port, datagrem).pack())

class UDP(object):
    def __init__(self, src_port, dst_port, payload):
        self.src_port = src_port
        self.dst_port = dst_port
        self.payload = payload
        
    def pack(self):
        return UDP.udp_pack(self.src_port, self.dst_port, self.payload)
    
    @staticmethod
    def udp_unpack(datagram):
        src_port, dst_port, length, checksum_ = struct.unpack('!HHH2s', datagram[:HEADER])
        payload = datagram[HEADER:]
        return UDP(src_port, dst_port, payload)

    @staticmethod
    def udp_pack(src_port, dst_port, payload):
        length = len(payload) + HEADER
        uncheck_datagram = struct.pack('!HHH2s%ds' % len(payload), src_port, dst_port, length, b'\x00', payload)
        checksum_ = checksum(uncheck_datagram)
        datagram = struct.pack('!HHH2s%ds' % len(payload), src_port, dst_port, length, checksum_, payload)
        return datagram
    
    def __str__(self):
        return 'src: %(src_port)s\n' \
               'dst: %(dst_port)s\n' \
               'payload: %(payload)s}\n' % self.__dict__

def fake_header(des_ip, des_port):
    pass

def get_ip():
    pass

def get_port():
    pass

def checksum (data):
    data_array = array.array('H', data)
    s = 0
    for d in data_array:
        s += d
    s = (s & 0xFFFF) + (s >> 16)
    s += (s >> 16)
    return int.to_bytes(~s & 0xFFFF,2,'little')

# u = UDP()
# header = struct.pack('>H', 65502)+struct.pack('>H', 4040)+struct.pack('>H', 72)+b'\x2f\x7f'
# print(u.decode(b'\xff\xde\x0f\xc8\x00\x48\x2f\x7f'))