# import entire socket & rdt library for use
from socket import *
from RDT_protocol import RDT

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420

# create sender primed for reliable data transport and bind to local port
Sender = RDT(serverName, serverPort)

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = open(filePath, 'rb')  # open img
    imgData = img.read() # read data of img
    sendAddr = (serverName, serverPort) # assign receiver
    print('Image sending...')
    Sender.rdt_send(imgData, sendAddr)
    print('Image sent!')
