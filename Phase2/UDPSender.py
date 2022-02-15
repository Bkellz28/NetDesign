# import entire socket & rdt library for use
from RDT_protocol import RDT

# initialize server info
serverName = '127.0.0.1'
serverPort = 10420

# create socket
Sender = RDT(serverName, serverPort)

# loop client to allow for multiple file sends
while True:
    # prompt input and send message to socket
    filePath = input('Input path of image file: ')
    img = open(filePath, 'rb')  # open img
    imgData = img.read()
    length = len(imgData)  # get length of byte array
    print("String length: ")
    print(str(length // int(1024)))

    ## CREATE INITIAL MESSAGE WHICH CONTAINS IMG SIZE
    numPack = length // int(1024)
    sendAddr = (serverName, serverPort)

    if (length % 1024 != 0):
        numPack += 1
    imgSizeMsg = str(numPack) + ',' + str(numPack)
    Sender.rdt_send(imgSizeMsg, 0, sendAddr)  # header of 0 represents initial message
    print("Number of packets being sent: ")
    # print(str(length))

    sendList = []  # Packets being sent in a list
    for i in range(numPack):
        msg = imgData[i * 1024:(i + 1) * 1024]
        sendList.append(msg)

    print(len(sendList))

    for i in range(len(sendList)):
        sendMsg = sendList[i]
        Sender.UDPsocket.sendto(sendMsg, sendAddr)  # Repeatedly sending packets over

    print('All packets sent.')  # Close.
