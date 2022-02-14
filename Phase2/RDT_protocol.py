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
        else: # need to append header to bytes
            # header is packet number expressed using two bytes
            # the first byte is packetNum/255 and the second is the remainder of packetNum/255
            firstByte = headerData // 255
            secondByte = headerData % 255
            # append bytes to data and send
            header = bytearray()  # create header
            header.append(firstByte)  # add the first
            header.append(secondByte) # and second byte to the header
            fullPacket = header + msgData # append data to end of header for full packet
            self.UDPsocket.sendto(fullPacket, receiver) # send full packet
            
    def rdt_recv(self, bufSize):
        recvPacket, serverAddress = self.UDPsocket.recvfrom(1024) # receive packet
        try: # try to decode it to ascii WILL NOT WORK for typical byte data
            recvData = recvPacket.decode('ascii') # will work for initial string message
            recvHeader = 0
        except: # otherwise we're dealing with bytes
            # convert bytes to number array
            packetData = np.frombuffer(recvPacket, dtype = np.uint8)
            packLen = len(packetData)
            # calculate header from first two bytes
            recvHeader = packetData[0]*255 + packetData[1]
            # all but first two bytes are data
            recvData = packetData[2:packLen]
            # recvData = recvPacket[2:packLen]
        # return header and data
        return recvData, recvHeader
