# import socket library and checksum function
from CheckSumUtility import *
from socket import *
import time
import random
from threading import Timer


# updated RDT protocol to rdt2.3
class RDT3:
    def __init__(self, hostName, portNum, frameSize, timeoutVal, errorMode=1, debugToggle=0):
        self.host = hostName
        self.port = portNum
        # open socket for use
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
        # keep track of debugToggle (1 for debug messages, 0 for none)
        self.debug = debugToggle
        self.timeout = timeoutVal
        self.erMode = errorMode
        self.frame = frameSize

    # data file send
    def rdt_send(self, sendData, receiver):
        # TIMEOUT ERROR SIMULATION (ERROR MODE 4)
        # ASSIGN PERCENT ERROR HERE (10% is huge, results in >5min send time)
        errorPcnt = 10
        
        ## CUT UP DATA AND SEND INITIAL MESSAGE TO RECEIVER
        ########
        db = self.debug  # grab debug val
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
            packStart = i * 1024  # packet start index
            packEnd = (i + 1) * 1024  # packet end index
            packet = sendData[packStart:packEnd]  # parse packet
            sendList.append(packet)  # add packet to list
        # check that sendList is same size as numPack
        if (len(sendList) != numPack):
            print('ERROR: packet list does not match estimated packet size')
            print('Ending send call...')
            return
        elif (len(sendList) == numPack and db == 1):  
            print('Data successfully parsed into packets...')
            
        ## GO-BACK-N SENDING ALGORITHM
        #############
        # set socket to non-blocking
        self.UDPsocket.setblocking(0)
        # grab frame number
        N = self.frame
        # start sending packets with go-back-N algorithm
        sn = 0  # init identifier as 0, will count up to numPack-1
        base = 0 # init go-back-n frame base as first packet
        sendTime = -1 # init sendTime for timeout handling
        while True:
            # check if next packet to send is within frame
            if sn < (base + N):
                # send packet and iterate sn
                try: msg = sendList[sn] 
                except: nothing = 0
                packet = self.packetize(msg, sn)
                self.UDPsocket.sendto(packet, receiver)
                sn = sn + 1
                # start timer if base of frame
                if sn == base: sendTime = time.time()
                
            # try to receive ack, do nothing if none available
            ackRcvd = 0
            recvSn = -1 # init for use outside of try
            recvCS = -1 # init for use outside of try
            try:
                # receive ack msg
                recvPacket, recvAddr = self.UDPsocket.recvfrom(14)
                recvSn, recvCS, recvAck = self.depacketize(recvPacket)
                # IMPLEMENT ACK LOSS SIMULATION
                randy = random.randrange(1, 100, 1)
                if (self.erMode == 4 and randy < errorPcnt):
                    ackRcvd = 0 # do nothing with ack to simulate a loss
                    print("ACK packet lost...")
                else:
                    ackRcvd = 1
            except:
                ackRcvd = 0 # do nothing if no ack available
            
            # handle ack if one was received
            if ackRcvd == 1:
                # check for corruption
                if int(recvCS, 2) != 0:
                    # ack is corrupted, simply discard
                    if (db == 1): print('ERROR: ACK msg corrupted, discarding...')
                elif recvSn < base:
                    # ack is not for current base, simply discard
                    if (db == 1): print('ERROR: Expected ACK' + str(base) + ' but received ACK' + str(recvSn)) 
                else:
                    # otherwise ACK is for current base, can now iterate and reset timer
                    base = recvSn + 1
                    sendTime = time.time()
                    # IF LAST ACK, EXIT WHILE LOOP
                    if base == numPack: break
                
            # check for and handle timeout 
            if (time.time() - sendTime) >= self.timeout:
                # resend already sent packets in the frame and restart timer
                for i in range(base, sn-1):
                    try: msg = sendList[i]
                    except: nothing = 0
                    packet = self.packetize(msg, i)
                    self.UDPsocket.sendto(packet, receiver)
                # restart timer
                sendTime = time.time()
        
        # end of algorithm 
        if (db == 1): print('All packets sent!')

    # data file receive
    def rdt_recv(self):
        # TIMEOUT ERROR SIMULATION (ERROR MODE 4)
        # ASSIGN PERCENT ERROR HERE (10% is huge, results in >5min send time)
        errorPcnt = 10

        db = self.debug  # grab debug val
        # create ACK data message
        ackBi = binarySize('111', 64)  # 64 bit uint 7
        ack = int(ackBi, 2).to_bytes(8, byteorder='big', signed=False)
        # recv initial message that gives number of packets
        recvStart, serverAddress = self.UDPsocket.recvfrom(1024)
        numPack = int(recvStart.decode())
        if (db == 1): print(str(numPack) + ' packets incoming...')
        numRecv = 0
        # receive data packets and ACKnowledge reception from sender
        snLast = -1  # start iDlast as 1, since first packet iD will be 0
        packetsReceived = []  ### list of packets that pass checks and are received successfully
        recvNum = 0
        while (True):
            packet, svrAddr = self.UDPsocket.recvfrom(1030)
            # parse packet down into message, checksum, and identifier
            seqNum, recvCS, msgData = self.depacketize(packet)
            ackPacket = []  # initialize ackPacket outside of if-else handling
            # check sequence numbers, discard if anything besides expected seqNum
            if seqNum != (snLast+1):
                if (db == 1): print('ERROR: pkt' + str(seqNum) + ' received, expected pkt' + str(snLast+1))
                if (db == 1): print('Sending ACK' + str(snLast) + ' to sender...')
                # sending prev ack
                ackPacket = self.packetize(ack, snLast)
                self.UDPsocket.sendto(ackPacket, svrAddr)
                # if this if was correct, the rest is skipped and the flag above is sent to resend the same packet

            # check checksums:
            elif int(recvCS, 2) != 0:
                if (db == 1): print('ERROR on pkt' + str(recvNum) + ' Corruption detected in packet.')
                if (db == 1): print('Sending ACK' + str(snLast) + ' to sender...')
                # send snLast ack
                ackPacket = self.packetize(ack, snLast)
                self.UDPsocket.sendto(ackPacket, svrAddr)
                # if this elif was correct, the rest is skipped and the flag above is sent to resend the same packet

            # both checks pass, packet will be added to list
            else:
                # HANDLE TIMEOUT ERROR SIMULATION
                randy = random.randrange(1, 100, 1)
                if (self.erMode == 5 and randy < errorPcnt):
                    # DO NOTHING HERE TO SIMULATE LOSING THIS PACKET
                    nothing = 1
                else:  # otherwise continue with good packet handling
                    # print('GOOD PACKET RECEIVED')
                    # iterate recvNum and add packet to list of received packets
                    recvNum += 1
                    packetsReceived.append(msgData)  # add packet to list of packets
                    if recvNum % 25 == 0 and db == 1:  # update user on packets for every 5, (or whatever number you want)
                        print(str(recvNum) + ' packets received...')
                    # send correct ACK to sender
                    ackPacket = self.packetize(ack, seqNum)
                    self.UDPsocket.sendto(ackPacket, svrAddr)
                    # iterate snLast
                    snLast = seqNum
                    if recvNum == numPack:  # break loop if all packets received
                        print('All packets received!')
                        break

        # combine list of data-pieces back into one single piece of data
        dataReceived = packetsReceived[0]
        for i in range(1, len(packetsReceived)):
            dataReceived += packetsReceived[i]  # construct packets back into data array
        return dataReceived  # return data

    # CREATE PACKET FUNCTION
    # "packetizes" data, checksum, and seq num into a single packet
    # first calculates the checksum of the data
    def packetize(self, data, sn):
        # convert seq num to 2bytes
        snBy = sn.to_bytes(2, byteorder='big', signed=False)
        # convert data to bits for checksum calculation
        dataBi = bin(int(data.hex(), 16))
        # calculate and convert checksum to bytes
        cs = checksum(dataBi)  # calc checksum
        csBy = int(cs, 2).to_bytes(4, byteorder='big', signed=False)
        # DATA IS CORRUPTED AFTER CHECKSUM TO PROPERLY SIMULATE BIT ERROR
        # FIRST INPUT AFTER DATA IS ERMODE INPUT FROM CONSTRUCTOR
        # SECOND INPUT IS % ERROR

        data = self.corrupt(data, self.erMode, 10)

        # create and return full packet
        packet = snBy + csBy + data
        # print(len(packet))
        return packet

    # DECONSTRUCT PACKET FUNCTION
    # "depacketizes" data, checksum, and seq num
    def depacketize(self, packet):
        # grab raw pieces
        snRaw = packet[0:2]
        csRaw = packet[2:6]
        msg = packet[6:]
        # convert seq num back to integer
        sn = int(snRaw.hex(), 16)
        # convert received checksum to binary (cut off 0b binary string header)
        recvCs = bin(int(csRaw.hex(), 16))[2:]  # [2:] skips '0b'
        recvCs = binarySize(recvCs, 32)  # add leading 0s if needed
        # calculate checksum of the data and compare to received checksum
        msgBi = bin(int(msg.hex(), 16))
        cs = checksum(msgBi, recvCs)
        # return formatted seq num and header
        # no need to format the msg data any further
        return sn, cs, msg

    # CORRUPTION FUNCTION
    # 3 mode: 1, 2, and 3
    # Mode 1: no corruption
    # Mode 2: ACK packet corruption, these packets are small, < 100 byte
    # Mode 3: data packet corruption, these packets are big, > 100 byte
    def corrupt(self, data, mode, thresh):
        # gen random num
        randy = random.randrange(1, 100, 1)
        if (mode == 2 and len(data) < 100):
            if randy < thresh:
                # CONVERT DATA TO BINARY AND FLIP SOME BITS
                # print(len(data))
                data = bin(int(data.hex(), 16))[2:]
                data = binarySize(data, 64)
                crpt = ''
                for i in range(64):  # invert first 64bit=8byte
                    if (data[i] == '1'):
                        crpt += '0'
                    else:
                        crpt += '1'
                corruptData = crpt + data[64:]
                # THEN CONVERT BACK TO BYTES
                corruptData = int(corruptData, 2).to_bytes(8, byteorder='big', signed=False)
                # print(len(corruptData))
            else:
                corruptData = data
        elif (mode == 3 and len(data) > 100):
            if randy < thresh:
                # CONVERT DATA TO BINARY AND FLIP SOME BITS
                # print(len(data))
                data = bin(int(data.hex(), 16))[2:]
                crpt = ''
                for i in range(64):  # invert first 64bit=8byte
                    if (data[i] == '1'):
                        crpt += '0'
                    else:
                        crpt += '1'
                corruptData = crpt + data[64:]
                # THEN CONVERT BACK TO BYTES
                corruptData = int(corruptData, 2).to_bytes(1024, byteorder='big', signed=False)
                # print(len(corruptData))
            else:
                corruptData = data
        else:  # mode 1, 4, 5, or data that doesn't match current mode
            # no need to corrupt this data
            corruptData = data
        return corruptData


