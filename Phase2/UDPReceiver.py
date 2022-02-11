#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from socket import *
from rdt import *

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket and bind to local port
serverSocket = socket(AF_INET, SOCK_DGRAM)
# leaving first param blank allows for svr to rcv from other hosts
serverSocket.bind(('', serverPort)) 
# alert user that server is ready
print("The server is ready to receive")

# server reads and modifies message
# loop receive action for server
while True:
    # receive message from client
    msg, clientAddress = serverSocket.recvfrom(2048)
    # convert message to uppercase and append intro to message
    modMsg = msg.decode().upper()
    modMsg = "Message received from server: " + modMsg
    # send modified message back to client
    serverSocket.sendto(modMsg.encode(), clientAddress)
    
