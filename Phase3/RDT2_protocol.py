# import socket library and checksum function
from CheckSumUtility import *
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
        sn = 0 # init identifier as 0, will flip b/t 0 and 1
        for i in range(len(sendList)):
            # grab packet and append checksum and identifier
            msg = sendList[i] # grab packet
            # Corruption needs to be implemented after this line
            if (sn == 0): sn = 1
            elif (sn == 1): sn = 0
            # create and send packet
            packet = self.packetize(msg, sn)
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
        snLast = 1 # start iDlast as 1, since first packet iD will be 0
        while (recvNum != numPack):
            packet, svrAddr = self.UDPsocket.recvfrom(1029)
            # parse packet down into message, checksum, and identifier
            seqNum, recvCS, msgData = self.depacketize(packet)
    
    # CREATE PACKET FUNCTION
    # "packetizes" data, checksum, and seq num into a single packet
    # first calculates the checksum of the data
    def packetize(self, data, sn):
        # convert seq num to 1byte
        snBy = sn.to_bytes(1, byteorder = 'big', signed = False)
        # convert data to bits for checksum calculation
        dataBi = bin(int(data.hex(), 16))
        # calculate and convert checksum to bytes
        cs = checksum(dataBi) #calc checksum
        csBy = int(cs, 2).to_bytes(4, byteorder = 'big', signed = False)
        # create and return full packet
        packet = snBy + csBy + data
        return packet
    
    # DECONSTRUCT PACKET FUNCTION
    # "depacketizes" data, checksum, and seq num
    def depacketize(self, packet):
        # grab raw pieces
        snRaw = packet[0:1]
        csRaw = packet[1:5]
        msg = packet[5:]
        # convert seq num back to integer
        sn = int(snRaw.hex(), 16)
        # convert received checksum to binary (cut off 0b binary string header)
        recvCs = bin(int(csRaw.hex(), 16))[2:] # [2:] skips '0b'
        recvCs = binarySize(recvCs, 32) # add leading 0s if needed
        # calculate checksum of the data and compare to received checksum
        msgBi = bin(int(msg.hex(), 16))
        cs = checksum(msgBi, recvCs)
        # return formatted seq num and header
        # no need to format the msg data any further
        return sn, cs, msg
    
