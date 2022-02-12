#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from RDT_protocol import RDT
from socket import *
from PIL import Image
import numpy as np

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket and bind to local port
Receiver = RDT(serverName, serverPort)
# leaving first param blank allows for svr to rcv from other hosts
Receiver.UDPsocket.bind(('', serverPort)) 
# alert user that server is ready
print("The receiver is ready")

# server reads and modifies message
# loop receive action for server
while True:
    # receive message from client
    msgData= Receiver.rdt_recv(1024)
    if '000' in msgData:
        ## GRAB HEIGHT AND WIDTH FROM MESSAGE
        print(msgData)
        indx1 = msgData.find(',')  # index of comma between header and height
        indx2 = msgData.rfind(',') # index of comma between height and width
        endIn = len(msgData)
        height = msgData[indx1+1:indx2]
        print("height: " + height)
        height = int(height)
        width = msgData[indx2+1:endIn]
        print("width: " + width)
        width = int(width)
        
# THIS IS WHERE WE CREATE EMPTY ARRAY
# AND START RECEIVING PACKETS

# empty array with 3 tuple?
# a=np.empty((426,640), dtype=object)
#for z in range(426):
#    for y in range(640):
#       a[z,y] = (0,0,0)
# ABOVE is INITIALIZATION of EMPTY array

# BELOW is populating it ---- need to loop it
# packet = Receiver.rdt_recv(1024)
# i = packet (first pixel number)
# j = packet (second pixel number)
# k = packet (third pixel number)
# for z in range(426):
#    for y in range(640):
#       a[z,y] = (i,j,k) where i, j, k are numbers for the pixels
