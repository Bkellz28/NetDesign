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
    
    
