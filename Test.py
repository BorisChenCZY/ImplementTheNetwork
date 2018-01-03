from LinkLayer import LinkLayer, util
from socket import *
def callback(frame):
    src_mac = frame.src_mac
    dst_mac = frame.dst_mac
    data = frame.payload
    print(util.mac_ntoa(dst_mac), data.decode())

linkLayer = LinkLayer(callback)
linkLayer.sendto()
print(util.mac_ntoa(linkLayer.MAC))
that_mac = '02:00:0A:14:6A:48'
