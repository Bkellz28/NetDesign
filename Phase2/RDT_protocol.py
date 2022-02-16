# import socket library
from socket import *
import time

class RDT:
    def __init__(self, hostName, portNum):
        self.host = hostName
        self.port = portNum
        # open socket  for device
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)

    # data file to be sent 
    def rdt_send(self, sendData, receiver):
        # calc num packets, length of data / 1024 bytes
        length = len(sendData);
        numPack = length // int(1024)
        if (length % 1024 != 0): # add extra packet for leftover
            numPack += 1
        # send initial message to receiver alerting how many packets to expect
        numPackMsg = 'packets:' + str(numPack)
        self.UDPsocket.sendto(numPackMsg.encode(), receiver)
        print(str(numPack) + ' packets to send...')
        sendList = [] # initialize list of packets to send
        for i in range(numPack):
            packStart = i*1024   # starting index for packet
            packEnd = (i+1)*1024 # ending index for packet
            msg = sendData[packStart:packEnd] # parse packet
            sendList.append(msg) # add packet to list
        for i in range(len(sendList)):
            sendMsg = sendList[i] # grab packet
            self.UDPsocket.sendto(sendMsg, receiver) # send packet

    def rdt_recv(self):
        recvHead, serverAddress = self.UDPsocket.recvfrom(1024)  # receive initial msg
        header = recvHead.decode()
        indx = header.rfind(':') # index of colon between "packet" and numPack
        endIn = len(header)
        numPack = int(header[indx+1:endIn]) # grab numPack
        print(str(numPack) + ' packets incoming...')
        recvNum = 0 # initialize number of packets received
        packetsReceived = [] # initialize list of received packets
        while True:
            msgData, serverAddress = self.UDPsocket.recvfrom(1024)
            recvNum += 1
            packetsReceived.append(msgData) # add packet to list of packets
            if recvNum % 100 == 0: # update user on packets
                print(str(recvNum) + ' packets received...')
            if recvNum == numPack: # break loop if all packets received
                break
        print('All packets received!')
        dataReceived = packetsReceived[0] # initialize reconstructed data
        for i in range(1, len(packetsReceived)):
            dataReceived += packetsReceived[i] # construct packets back into data array
        return dataReceived # return data
