from socket import *
ip = "10.20.13.19"
port = 5000
address = (ip, port)
ClientSocket = socket(AF_INET, SOCK_DGRAM)
while 1:
    ClientSocket.sendto("Hello".encode(), address)
    raw_message, clientAddress = ClientSocket.recvfrom(2048)
    print("\n---------------\n", raw_message.decode(), "\n----------------\n")