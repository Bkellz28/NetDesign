# import entire socket & rdt library for use
from socket import *
from RDT_protocol import RDT
import numpy as np
import cv2 as cv

# initialize server info
serverName = '127.0.0.1'
serverPort = 10421
# create receiver primed for reliable data transfer and bind to local port
Receiver = RDT(serverName, serverPort)
# leaving first param blank allows for svr to rcv from other hosts
Receiver.UDPsocket.bind(('', serverPort))
# alert user that server is ready
print("The receiver is ready")

# server reads and modifies message
# loop receive action for server
while True:
    # receive data from client
    receivedData = Receiver.rdt_recv()
    # arrange data back into img and save result
    img = np.asarray(bytearray(receivedData), dtype=np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    cv.imwrite("result.bmp", img)
    # open result image!
    print("Opening image: ")
    cv.imshow('result.bmp', img)
    cv.waitKey()
