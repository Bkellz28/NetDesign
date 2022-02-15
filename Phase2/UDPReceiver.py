# import entire socket & rdt library for use
from RDT_protocol import RDT
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
        ## GRAB length FROM MESSAGE
        print('Initial image; message received: ' + msgData)
        indx = msgData.rfind(',')  # index of comma between height and width
        endIn = len(msgData)
        length = msgData[indx + 1:endIn]  # grab length number
        length = int(length)
        numPack = length
        numReceived = 0
        recvList = []
        while True:
            msgData, msgHead = Receiver.UDPsocket.recvfrom(1024)
            numReceived += 1
            recvList.append(msgData)
            if numReceived % 50 == 0:
                print("Number of packets received: " + str(numReceived))
            if numReceived == numPack:
                break

        print('Finished Receiving.')
        newImg = recvList[0]
        print("Final packet number: " )
        print(len(recvList))
        for i in range(1, len(recvList)):
            newImg = newImg + recvList[i]

        img = np.asarray(bytearray(newImg), dtype=np.uint8)
        img = cv.imdecode(img, cv.IMREAD_COLOR)
        cv.imwrite("result.bmp", img)
        cv.imshow('result.bmp', img)
        cv.waitKey()

        print("Opening image: ")
