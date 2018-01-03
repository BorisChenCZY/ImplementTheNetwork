from mysocket import *
from LinkLayer import util
ip = util.get_local_ipv4_address()
ip_dict = {"10.20.7.144":"10.20.13.19","10.20.13.19":"10.20.7.144"}
port = 5000
local_address = (ip, port)
remote_address = ('192.168.43.132', 5000)
ClientSocket = socket(AF_INET, SOCK_STREAM)
ClientSocket.bind(local_address)
ClientSocket.connect(remote_address)
for i in range(10):
    ClientSocket.send("{}".format(i).encode())
    raw_message = ClientSocket.recv(2048)
    print("\n---------------\n", raw_message.decode(), "\n----------------\n")