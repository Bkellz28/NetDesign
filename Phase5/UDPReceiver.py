# import entire socket & rdt library for use
from RDT3_protocol import RDT3
import numpy as np
import cv2 as cv

# initialize server info
rcvrName = '127.0.0.1'
rcvrPort = 10421
# create receiver primed for reliable data transfer and bind to local port

# 1ST & 2ND INPUTS: receiver name and port
# 3RD INPUT: optional, message receive timeout number in seconds (mostly used for sender)
# 4TH INPUT: optional, error simulation mode (1 is no errors and the default, 2-5 remaining options)
# 5TH INPUT: optional, debug mode (0 is very few feedback print messages and the default, 1 prints much more info to terminal)
Receiver = RDT3(rcvrName, rcvrPort, 1, 2, 1)
# leaving first param blank allows for svr to rcv from other hosts
Receiver.UDPsocket.bind(('', rcvrPort))

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
