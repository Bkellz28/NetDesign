#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from RDT_protocol import RDT
from socket import *
from PIL import Image
import numpy as np
import time

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket
Sender = RDT(serverName, serverPort)

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = open(filePath, 'rb') # open img
    imgData = img.read()
    # arrayImg = np.asarray(img) # convert img to array of 3-tuples (RGB  vals)
    # bArray = bytearray(arrayImg) # convert RGB array to byte array
    # imgW, imgH = img.size # get size of img
    length = len(imgData) # get length of byte array (should be w*h*3)
    print(str(length//int(1024)))
    ## CREATE INITIAL MESSAGE WHICH CONTAINS IMG SIZE
    numPack = length//int(1024)
    # imgSizeMsg = str(imgH) + ',' + str(imgW)
    # print(imgSizeMsg)
    sendAddr = (serverName, serverPort)
    
    
    if (length%1024 != 0):
        numPack += 1
    imgSizeMsg = str(numPack) + ',' + str(numPack) 
    Sender.rdt_send(imgSizeMsg, 0, sendAddr) # header of 0 represents initial message
    print(str(length))
    
    sendList = []
    for i in range(numPack):
        msg = imgData[i*1024:(i+1)*1024]
        sendList.append(msg)
        # Sender.rdt_send(msg, i+1, sendAddr)
        #if i%100 == 0:
        #    time.sleep(0.5)
    
    
    print(len(sendList))
    for i in range(len(sendList)):
        sendMsg = sendList[i]
        Sender.UDPsocket.sendto(sendMsg, sendAddr)
    
    print('all sent')
    """
    numPackets = imgH * 2  # one packet is a half of a row, for smaller imgs thats 600-800 bytes
    print(str(numPackets) + ' packets to create')
    packetLength = (imgW / 2) * 3 # packet length is half the width of a row (*3 for bytes)
    # packetLength = 4 # debugging purposes
    arrIndex = 0  # index for where in the array to grab bytes
    testtest = [254, 255, 256, 257] # if you want to test a specific range of header numbers
    for i in range(numPackets):
        # start parsing and sending packets
        # we dont have to worry about 2D for the byte array, so we can keep iterating again and again
        packetEnd = arrIndex + (packetLength)  # calculate end point for packet
        newPacket = bArray[int(arrIndex):int(packetEnd)] # parse and create packet
        # send the packet , header is the number of the packet
        # which is i + 1 (we do this to avoid packet number 0, which is reserved for
        # the initial message and now lost packets)
        Sender.rdt_send(newPacket, i+1, sendAddr)
        # increment arrIndex by the size of a packet
        arrIndex += (packetLength)
        # send packets in bursts to ensure all packets are sent
        if (i%100) == 0: 
            print(str(i) + ' packets sent...') # update user
            time.sleep(0.5)
        
    print('All packets sent!')
    """
    
