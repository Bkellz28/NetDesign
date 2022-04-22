# import entire socket & rdt library for use
from socket import *
from RDT3_protocol import RDT3
import time

# initialize server info
sndrName = '127.0.0.1'
sndrPort = 10420

# create sender primed for reliable data transport and bind to local port

# 1ST & 2ND INPUTS: receiver name and port
# 3RD INPUT: optional, message receive timeout number in seconds (mostly used for sender)
# 4TH INPUT: optional, error simulation mode (1 is no errors and the default, 2-5 remaining options)
# 5TH INPUT: optional, debug mode (0 is very few feedback print messages and the default, 1 prints much more info to terminal)
Sender = RDT3(sndrName, sndrPort, 0.03, 2, 1)
Sender.UDPsocket.bind(('', sndrPort))

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = open(filePath, 'rb')  # open img
    imgData = img.read() # read data of img
    sendAddr = (sndrName, 10421) # assign receiver
    print('Image sending...')
    before = time.time()
    Sender.rdt_send(imgData, sendAddr)
    after = time.time()
    totalTime = round(after-before, 3)
    print('Image sent in ' + str(totalTime) + ' seconds!')
