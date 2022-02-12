#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from RDT_protocol import RDT
from socket import *
from PIL import Image
import numpy as np

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket
Sender = RDT(serverName, serverPort)

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = Image.open(filePath) # open img
    arrayImg = np.asarray(img) # convert img to array of 3-tuples (RGB  vals)
    bArray = bytearray(arrayImg) # convert RGB array to byte array
    imgW, imgH = img.size # get size of img
    length = len(bArray) # get length of byte array (should be w*h*3)
    
    ## CREATE INITIAL MESSAGE WHICH CONTAINS IMG SIZE
    imgSizeMsg = str(imgH) + ',' + str(imgW)
    sendAddr = (serverName, serverPort)
    Sender.rdt_send(imgSizeMsg, 0, sendAddr) # header of 0 represents initial message
    
    numPackets = imgH * 2  # one packet is a half of a row, for smaller imgs thats 600-800 bytes
    packetLength = (imgW / 2) * 3 # packet length is half the width of a row
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
        

    ## DEBUGGING AND INITIAL TRIAL STUFF
    ## DELETE BEFORE SUBMISSION
    """
    someArray = arrayImg[426,639]
    somebArray = bArray[0:6]
    
    somebArrayConv = np.frombuffer(somebArray, dtype = np.uint8)
    print('orig w: ' + str(w) + ', h: ' + str(h))
    print('byt array len: ' + str(length))
    print('1 int in array example: ' + str(someArray))
    print('1 in byt array example: ' + str(somebArrayConv))
    # newData = "w: " + str(w) + ", h: " + str(h)
    sendAddr = (serverName, serverPort)
    newData = somebArray
    Sender.rdt_send(newData, 420, sendAddr)
    """
    
    
