# import socket library and checksum function
from CheckSumUtility import *
from socket import *
import time
import random
from threading import Timer

# updated RDT protocol to rdt2.3
class RDT3:
    def __init__(self, hostName, portNum, debugToggle=0):
        self.host = hostName
        self.port = portNum
        # open socket for use
        self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
        # keep track of debugToggle (1 for debug messages, 0 for none)
        self.debug = debugToggle

    # data file send
    def rdt_send(self, sendData, receiver):
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
        elif (len(sendList) == numPack and db == 1):  ## '&&' should be 'and'
            print('Data successfully parsed into packets...')
        # send packet one at a time and wait for ACK response from server
        sn = 0  # init identifier as 0, will flip b/t 0 and 1
        for i in range(len(sendList)):
            # grab packet and append checksum and identifier
            msg = sendList[i]  # grab packet
            # Corruption needs to be implemented after this line
            # create and send packet
            t = Timer(20, self)
            t.start()
            packet = self.packetize(msg, sn)
            ### everything in this chunk here is jj's addition
            goodAck = 0
            while goodAck == 0:
                self.UDPsocket.sendto(packet, receiver)
                # receive ACK from receiver
                recvPacket, recvAddr = self.UDPsocket.recvfrom(1024)
                recvSn, recvCS, recvAck = self.depacketize(recvPacket)
                ackNum = int(recvAck.hex(), 16)
                # print('ACK' + str(recvSn) + ' RECEIVED!!')
                # first verify integrity of msg with checksum
                if int(recvCS, 2) != 0:
                    if (db == 1): print('ERROR: ACK msg corrupted.')
                    if (db == 1): print('Resending current packet...')
                    # repacketize data and allow resend to occur
                    packet = self.packetize(msg, sn)
                # otherwise check the ACK msg
                elif recvSn != sn:
                    if (db == 1): print('ERROR: Previous ACK received.')
                    if (db == 1): print('Resending current packet...')
                    packet = self.packetize(msg, sn)
                    # do nothing to allow packet resend to occur
                else:
                    # change goodAck to 1 to leave the send loop
                    goodAck = 1
                # time.sleep(1)
            # print('Good ACK')
            # Data is acknowledged by sender, can move on to next packet
            # flip seq num
            if (sn == 0):
                sn = 1
            elif (sn == 1):
                sn = 0
            # print('DATA VERIFIED BY RECEIVER')
            # time.sleep(5)
        if (db == 1): print('All packets sent!')

    # data file receive
    def rdt_recv(self):
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
        snLast = 1  # start iDlast as 1, since first packet iD will be 0
        packetsReceived = []  ### list of packets that pass checks and are received successfully
        recvNum = 0
        while (recvNum != numPack):
            packet, svrAddr = self.UDPsocket.recvfrom(1029)
            # parse packet down into message, checksum, and identifier
            seqNum, recvCS, msgData = self.depacketize(packet)

            # check sequence numbers:
            if seqNum == snLast:
                if (db == 1): print('ERROR on pkt' + str(recvNum) + ': Sequence numbers are the same.')
                if (db == 1): print('Sending ACK' + str(seqNum) + ' to sender...')
                # sending prev ack
                ackPacket = self.packetize(ack, seqNum)
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
                # print('GOOD PACKET RECEIVED')
                # iterate recvNum and add packet to list of received packets
                recvNum += 1
                packetsReceived.append(msgData)  # add packet to list of packets
                if recvNum % 5 == 0 and db == 1:  # update user on packets for every 5, (or whatever number you want)
                    print(str(recvNum) + ' packets received...')
                # send correct ACK to sender
                if seqNum == 0:
                    ackPacket = self.packetize(ack, 0)
                elif seqNum == 1:
                    ackPacket = self.packetize(ack, 1)
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
        # convert seq num to 1byte
        snBy = sn.to_bytes(1, byteorder='big', signed=False)
        # convert data to bits for checksum calculation
        dataBi = bin(int(data.hex(), 16))
        # calculate and convert checksum to bytes
        cs = checksum(dataBi)  # calc checksum
        csBy = int(cs, 2).to_bytes(4, byteorder='big', signed=False)
        # DATA IS CORRUPTED AFTER CHECKSUM TO PROPERLY SIMULATE BIT ERROR
        # FIRST INPUT AFTER DATA IS MODE (1, 2, or 3)
        # SECOND INPUT IS % ERROR

        data = self.corrupt(data, 3, 80)

        # create and return full packet
        packet = snBy + csBy + data
        # print(len(packet))
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
    # Mode 4: ACK packet loss, these packets are small, < 100 byte
    # Mode 5: data packet loss, these packets are big, > 100 byte
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
        if (mode == 4 and len(data) < 100):
            if randy < thresh:
                # CONVERT DATA TO BINARY and CREATE PACKET LOSS
                # print(len(data))
                data = bin(int(data.hex(), 16))[2:]
                data = binarySize(data, 64)
                crpt = ''
                for i in range(64):  # make all bits 0
                    if (data[i] == '1'):
                        crpt += '0'
                corruptData = crpt + data[64:]
                # THEN CONVERT BACK TO BYTES
                corruptData = int(corruptData, 2).to_bytes(8, byteorder='big', signed=False)
                # print(len(corruptData))
            else:
                corruptData = data
        elif (mode == 5 and len(data) > 100):
            if randy < thresh:
                # CONVERT DATA TO BINARY AND FLIP SOME BITS
                # print(len(data))
                data = bin(int(data.hex(), 16))[2:]
                crpt = ''
                for i in range(64):  # make all bits 0
                    if (data[i] == '1'):
                        crpt += '0'
                corruptData = crpt + data[64:]
                # THEN CONVERT BACK TO BYTES
                corruptData = int(corruptData, 2).to_bytes(1024, byteorder='big', signed=False)
                # print(len(corruptData))
            else:
                corruptData = data
        else:  # mode 1 or data that doesn't match current mode
            # no need to corrupt this data
            corruptData = data
        return corruptData



