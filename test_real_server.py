from socket import *
ip = "10.20.13.19"
port = 5000
address = (ip, port)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(address)
while 1:
    raw_message, clientAddress = serverSocket.recvfrom(2048)
    print(raw_message.decode('utf-8'))
    serverSocket.sendto("Hello too!".encode(), clientAddress)