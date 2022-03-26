## ---- NETWORK DESIGN: PHASE 4 ---- ##
## --------------------------------- ##
## ----- Ben Kelley -- JJ Hyde ----- ##
## -- David Nguyen-- Liam Sweeney -- ##
## --------------------------------- ##
## ----------- Files: 6  ----------- ##

 FILE DESCRIPTION
-----------------------------
1. | UDPSender.py:
   | Acts as the client that sends over the initial BMP / JPG file. 
   | It converts the image into a number of packets and sends them over to the receiver.
   |
2. | UDPReceiver.py: 
   | Acts as the server that receivers the packets for the BMP / JPG file.
   | Converts the packets' contents back into what is necessary to open the image.
   | 
3. | image.bmp
   | Image that is being sent and received.
   | 
4. | RDT2_protocol.py:
   | This file handles the sending and receiving packets with headers. It uses both checksums and sequence numbers as well.
   |
5. | result.bmp
   | This file is made once the server receives the image and rebuilds it as result.bmp
   |
6. | CheckSumUtility.py
   | This file contains the function necessary to carryout the CheckSum.
   |

   
 STEPS TO EXECUTE
-----------------------------
1. | Open both programs (UDPSender.py & UDPReceiver.py)
   |
2. | Click Run at the top on both programs for the drop down.
   | 
3. | Edit Configurations
   |
4. | Allow for parallel runs on both programs
   | 
5. | Run both programs
   | 
6. | Type image name with the file type and press enter.
   |
7. | ***IF YOU WISH TO CHANGE THE MODE (for the 3 different options with corruption):
   | Look for the 'def __init__(self, hostName, portNum, timeoutVal=0, errorMode=1, debugToggle=0):' line which is on line 10 of RDT3_protocol. 
   | Change the x for the desired mode / option:
   | Type 1: for Option 1 and no corruption
   | Type 2: for Option 2 and ACK corruption
   | Type 3: for Option 3 and Data pack error
   | Type 4: for Option *5* and Data packet loss
   | Type 5: for Option *4* and ACK packet loss
