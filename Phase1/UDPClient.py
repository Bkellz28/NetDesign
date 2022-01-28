#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket library for use
from socket import *

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# prompt input and send message to socket
msg = input('Input lowercase sentence: ')
clientSocket.sendto(msg.encode(), (serverName, serverPort))
# receive msg and print
modMsg, serverAddress = clientSocket.recvfrom(2048)
print(modMsg.decode())

