## ---- NETWORK DESIGN: PHASE 3 ---- ##
## --------------------------------- ##
## ----- Ben Kelley -- JJ Hyde ----- ##
## -- David Nguyen-- Liam Sweeney -- ##
## --------------------------------- ##
## ----------- Files: 7  ----------- ##

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
7. | Test.py
   | An optional file uses to test both CheckSum and packet sending.
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
