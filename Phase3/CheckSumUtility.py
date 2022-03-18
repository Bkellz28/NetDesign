# Contains a checksum function which calculates a 32-bit (4 byte) checksum for a 1024 byte packet
import time

# adds leading zeroes to a binary string if it is not already the input bitSize
# if data is LARGER than input bitSize, returns -1
def binarySize(data, bitSize):
    # assess how many leading zeros needed
    zeroNeed = bitSize - len(data)
    if (zeroNeed < 0): #data is bigger than bitSize
        return (-1)
    elif (zeroNeed == 0): # none needed, return data untouched
        return data
    else: # add leading zeros and then return data
        for i in range(zeroNeed): data = '0' + data
        return data

# computes and returns a 32-bit checksum for an input 1024 byte packet
# if an addition cmpSum checksum value is input as well, will return the sum of the 
# calculated checksum and input checksum
def checksum(data, cmpSum = 0):
    # PART ONE: CALCULATE INITIAL CHECKSUM
    # check length and add leading zeros if necessary
    data = binarySize(data[2:], 8192)
    print(len(data))
    # chop data into 32 bit sections
    bitList = []
    for i in range(256):
        bitStart = i*32
        bitEnd = (i+1)*32
        bitSec = data[bitStart:bitEnd]
        # print(bitSec)
        bitList.append(bitSec)

    # add each bit section together
    checkSum = '000'
    for i in range(256):
        bs = bitList[i]
        addSum = bin(int(checkSum, 2) + int(bs, 2))
        zeroCheck = binarySize(addSum[2:], 32)
        if (zeroCheck == -1):
            addSum = addSum[2:]
            # cut off the leading one and grab carry
            cLen = len(addSum) - 32 # length of carry on addSum
            newCarry = addSum[0:cLen] # the carry
            addSum = addSum[cLen:] # addSum w/o the carry
            # wrap the carry around, i.e. add the carry to addSum
            newSum = bin(int(addSum, 2) + int(newCarry, 2))
            addSum = newSum[2:]
        else: # no carry, so zeroCheck returned 32-bit addSum
            addSum = zeroCheck
        # addSum has been properly checked
        # addSum is now our checkSum
        checkSum = addSum
        # time.sleep(1)
    print('Pre-flip checksum:   ' + checkSum)
    
    # PART TWO: ADD COMPARE CHECKSUM IF INPUT AND INVERT
    # check if a comparison checksum was input
    if (cmpSum != 0):
        print('Previous checksum:   ' + cmpSum)
        # calculate comparison b/t calc and input checksums
        compSum = bin(int(checkSum, 2) + int(cmpSum, 2))
        # check for carry bit
        if (len(compSum) == 34): 
            # no carry bit, index at beginning of binary string
            checkSum = compSum[2:]
        else: 
            # carry bit present, ignore it by indexing beyond it
            checkSum = compSum[3:]
    # INVERT BITS 
    inv = ''
    for i in range(32):
        if (checkSum[i] == '1'): inv += '0'
        else: inv += '1'
    checkSum = inv
    print('Calculated checksum: ' + checkSum)
    
    return checkSum
      
