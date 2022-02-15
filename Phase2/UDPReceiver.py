#!/usr/bin/env python3
# above line is necessary in Linux VM, but not for PyCharm in Win10

# import entire socket & rdt library for use
from RDT_protocol import RDT
from socket import *
from PIL import Image
import numpy as np
import cv2 as cv

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420
# create socket and bind to local port
Receiver = RDT(serverName, serverPort)
# leaving first param blank allows for svr to rcv from other hosts
Receiver.UDPsocket.bind(('', serverPort)) 
# alert user that server is ready
print("The receiver is ready")

# server reads and modifies message
# loop receive action for server
while True:
    # receive message from client
    msgData, msgHeader = Receiver.rdt_recv(1024)
    if msgHeader == 0:
        ## GRAB HEIGHT AND WIDTH FROM MESSAGE
        print('Initial image send message received: ' + msgData)
        indx1 = msgData.find(',')  # index of comma between header and height
        indx2 = msgData.rfind(',') # index of comma between height and width
        endIn = len(msgData)
        height = msgData[indx1+1:indx2] # grab height number
        height = int(height)
        width = msgData[indx2+1:endIn]  # grab width number
        width = int(width)
        numPack = width
        print(str(numPack))
        numReceived = 0
        recvList = []
        while True:
            msgData, msgHead = Receiver.UDPsocket.recvfrom(1024)
            numReceived += 1
            recvList.append(msgData)
            # print(str(msgData))
            # print(str(msgHead))
            if numReceived%50 == 0:
                print(str(numReceived))
            if numReceived == numPack:
                break
            
        
        print('Finished Receiving.')
        newImg = recvList[0]
        print("Final packet number: " )
        print(len(recvList))  # Final packet number
        for i in range(1, len(recvList)):
            newImg = newImg + recvList[i]

        img = np.asarray(bytearray(newImg), dtype=np.uint8)
        img = cv.imdecode(img, cv.IMREAD_COLOR)
        cv.imwrite("result.bmp", img)  # Creating a name for the copied over file
        cv.imshow('result.bmp', img)  # Opening the picture in a new pop-up window
        cv.waitKey()  # Necessary for cv.imshow
        
        '''
        
        # create empty array for image
        a = np.empty((height, width), dtype = object)
        for z in range(height):
            for y in range(width):
                a[z,y] = (0, 0, 0)
        print(str(height) + 'x' + str(width) + ' array initialized')
        
        numPacketsComing = height * 2
        progressTicker = 0
        while True:
            # this is here  for debugging purposes, prints header and full message data
            msgData, msgHeader = Receiver.rdt_recv(1024)
            # row to insert to is headerNum/2
            rowNum = (msgHeader // int(2)) - 1
            # odd header is first half of row, even is last half
            if msgHeader%2 == 0:
                colNum = width / 2 #last half will start at halfway through row
            else:
                colNum = 0 # otherwise start at beginning of row
            
            numPixels = int(width/2) # number of pixels in packet is half a row
            arrInd = 0 # array index starting at 0
            for i in range(numPixels):
                # grab RGB values
                R = msgData[arrInd]
                G = msgData[arrInd+1]
                B = msgData[arrInd+2]
                # insert values into array a
                a[int(rowNum), int(colNum+i)] = (R, G, B)
                # increment arrInd
                arrInd += 3
                
            progressTicker += 1 # increment progress ticker for console updates
            # update user around every hundred packets
            if progressTicker >= 100: # update user that packets are being received
                print(str(msgHeader) + ' packets received...')
                progressTicker = 0
            elif msgHeader == numPacketsComing: 
                break # leave while loop once all packets received
                
        print('All packets received!')
        receivedImg = Image.fromarray(a, mode='RGB')
        receivedImg.show() # show our received image!
        '''
        
    

