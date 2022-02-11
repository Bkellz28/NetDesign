#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import socket library
from socket import *


class packet:
    def __init__(self, data, header)
        self.data = data
        self.header = header

class RDT:
    def __init__(self, hostName, portNum)
        self.host = hostName
        self.port = portNum
        # open socket  for device
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
        
    # msg is data to be sent
    # header is header to be appended to packet
    # receiver is a tuple containing (receiverName, receiverPort)
    def rdt_send(self, msgData, headerData, receiver)
        msg = packet(msgData, headerData)
        self.UDPsocket.sendto(msg.encode(), receiver)
        
    def rdt_recv(self, bufSize)
        recvPacket, serverAddress = self.UDPsocket.recvfrom(1024)
        return recvPacket
