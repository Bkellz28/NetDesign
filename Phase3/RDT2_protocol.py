# import socket library
from socket import *
import time


# updated RDT protocol to rdt2.3
class RDT2:
    def __init__(self, hostName, portNum, debugToggle):
        self.host = hostName
        self.port = portNum
        # open socket for use
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
        # keep track of debugToggle (1 for debug messages, 0 for none)
        self.debug = debugToggle
    
    # data file send
    def rdt_send(self, sendData, receiver):
        db = self.debug # grab debug val
        # calc num packets, data length / 1024 bytes
        length = len(sendData)
        numPack = length // int(1024)
        # add extra packet for any leftover bytes
        if (length % 1024 != 0): numPack += 1
        # send numPack to receiver to start the data transfer
        self.UDPsocket.sendto(str(numPack).encode(), receiver)
        if (db == 1): print(str(numPack) + ' packets to send...')
        # create list of packets to send
        sendList = []
        for i in range(numPack):
            packStart = i * 1024 # packet start index
            packEnd = (i+1) * 1024 # packet end index
            packet = sendData[packStart:packEnd] # parse packet
            sendList.append(packet) # add packet to list
        # check that sendList is same size as numPack
        if (len(sendList) != numPack):
            print('ERROR: packet list does not match estimated packet size')
            print('Ending send call...')
            return
        elif (len(sendList) != numPack && db == 1): 
            print('All packets successfully parsed...')
        # send packet one at a time and wait for ACK response from server
        iD = 0 # init identifier as 0, will flip b/t 0 and 1
        for i in range(len(sendList)):
            # grab packet and append checksum and identifier
            msg = sendList[i] # grab packet
            cs = checksum(msg) # calculate checksum
            # Corruption needs to be implemented after this line
            if (iD == 0): iD = 1
            elif (iD == 1): iD = 0
            # MORE TO ADD
        
    # data file receive
    def rdt_recv(self):
        db = self.debug # grab debug val
        # recv initial message that gives number of packets
        recvStart, serverAddress = self.UDPsocket.recvfrom(1024)
        numPack = int(recvStart.decode())
        if (db == 1): print(str(numPack) + ' packets incoming...')
        numRecv = 0
        # receive data packets and ACKnowledge reception from sender
        iDlast = 1 # start iDlast as 1, since first packet iD will be 0
        while (recvNum != numPack):
            packet, svrAddr = self.UDPsocket.recvfrom(1028)
            # parse packet down into message, checksum, and identifier
            # first byte is identifier, next three is checksum, remainder is message
            # iD = packet[0]   PSEUDO-CODE NEED ACTUAL IMPLEMENTATION
            # cs = packet[1:3] PSEUDO-CODE NEED ACTUAL IMPLEMENTATION
            # msg = packet[4:] PSEUDO-CODE NEED ACTUAL IMPLEMENTATION
            iD = int.from_bytes(iD) # convert iD back to an integer
            cs = bin(int(msg.hex(), 16)) # convert cs back to binary
            recvCS = checksum(msg, cs)

    
# checksum for use in send and recv
# function passed WITHOUT second param will return binary checksum of data
# function passed WITH second param will compare calculated checksum with input compCS checksum
def checksum(data, compCS = 0):
    # convert byte data to bits
    dataBits = bin(int(data.hex(), 16))
    # initialize checkSum and iterate through bits
    checkSum = 0
    for i in range(2, len(dataBits)): # start at 2 since string will start with 0b
        if dataBits[i] == '1': checkSum += 1
    # return calculated checksum if no comparison specified
    if (compCS == 0): return checkSum
    else:
        # ADD checkSum with compCS
        # IF 0, data is good, return 1
        # ELSE, data is corrupted, return 0
