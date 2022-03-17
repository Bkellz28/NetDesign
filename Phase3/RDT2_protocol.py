# import socket library and checksum function
from Phase3.CheckSumUtility import *
from socket import *
import time


# updated RDT protocol to rdt2.3
class RDT2:
    def __init__(self, hostName, portNum, debugToggle = 0):
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
        elif (len(sendList) != numPack and db == 1):   ## '&&' should be 'and'
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
            packet, svrAddr = self.UDPsocket.recvfrom(1029)
            # parse packet down into message, checksum, and identifier
            # first byte is identifier, next four is checksum, remainder is message
            # grab and convert iD to int
            iDraw = packet[0:1]
            iD = int(iDraw.hex(), 16)
            # grab and convert checksum to binary string
            csRaw = packet[1:5] 
            cs = bin(int(csRaw.hex(), 16))[2:]
            cs = binarySize(cs, 32) # add leading zeros if needed
            # grab message data and calculate comparison checksum
            msg = packet[5:]
            msgBi = bin(int(msg.hex(),16))[2:]
            recvChecksum = checksum(msgBi, cs)
    
    # CREATE PACKET FUNCTION
    # "packetizes" data and checksum into a single packet
    # if a sequence number (sn) is input as well, it is also added to the packet
    def packetize(self, data, cs, sn = -1):
        # convert seq num to 1byte if one is present
        if (sn != -1): snBy = sn.to_bytes(1, byteorder = 'big', signed = False)
        # convert checksum to bytes
        csBy = int(cs, 2).to_bytes(4, byteorder = 'big', signed = False)
        # create and return full packet
        packet = snBy + csBy + data
        return packet

    
