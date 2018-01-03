import queue
import random
import IP
import UDP
from LinkLayer import util


class UDPsocket(object):
    def __init__ (self):
        self.bind((get_ip(), get_port()))
    
    def bind (self, address):
        self.src_ip = address[0]
        self.src_port = address[1]
        self.IP = IP.IP(IP.PROTOCOL_UDP, self.src_ip)
        UDP.buffer[self.src_port] = queue.Queue()
    
    def recvfrom (self, buffersize = 2048):
        segment, address = UDP.buffer[self.src_port].get()
        return segment, address
    
    def sendto (self, datagrem, address):
        dst_ip = address[0]
        dst_port = address[1]
        self.IP.sendto(dst_ip, UDP.pack(self.src_port, dst_port, datagrem))
        
    def close(self):
        del UDP.buffer[self.src_port]
        
def get_ip():
    return util.get_local_ipv4_address()

def get_port():
    port = random.randint(0, 65535)
    while port in UDP.buffer:
        port = random.randint(0, 65535)
    return port