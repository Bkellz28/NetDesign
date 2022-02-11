#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from socket import *
from PIL import Image

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = Image.open(filePath)
    
    clientSocket.sendto(msg.encode(), (serverName, serverPort))
    # receive msg and print
    modMsg, serverAddress = clientSocket.recvfrom(2048)
    print(modMsg.decode())
    
