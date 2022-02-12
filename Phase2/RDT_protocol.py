#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import socket library
from socket import *
import numpy as np


class RDT:
    def __init__(self, hostName, portNum):
        self.host = hostName
        self.port = portNum
        # open socket  for device
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
        
    # msg is data to be sent
    # header is header to be appended to packet
    # receiver is a tuple containing (receiverName, receiverPort)
    def rdt_send(self, msgData, headerData, receiver):
        if headerData == 0: # initial messge with imgSize
            msgData = '000,' + msgData
            self.UDPsocket.sendto(msgData.encode(), receiver)
        
    def rdt_recv(self, bufSize):
        recvPacket, serverAddress = self.UDPsocket.recvfrom(1024)
        if '000' in recvPacket.decode():
            return recvPacket.decode()
        recvData = np.frombuffer(recvPacket, dtype = np.uint8)
        return recvData
