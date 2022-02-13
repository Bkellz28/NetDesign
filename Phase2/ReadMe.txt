## ---- NETWORK DESIGN: PHASE 2 ---- ##
## --------------------------------- ##
## ----- Ben Kelley -- JJ Hyde ----- ##
## -- David Nguyen-- Liam Sweeney -- ##
## --------------------------------- ##
## ----------- Files: 03 ----------- ##

 FILE DESCRIPTION
-----------------------------
1. | UDPSender.py:
   | Acts as the client that sends over the initial BMP file. 
   | It converts the image into an RGB array and then a bitarray.
   | Sends the desired number of packets to the Recevier
   |
2. | UDPReceiver.py: 
   | Acts as the server that receivers the packets for the BMP file.
   | Converts the packets' contents back into what is necessary to open image.
   | 
3. | image.bmp
   | Image that is being sent and received.
   | 
4. | RDT_protocol.py:
   | This file handles the sending and receiving packets with headers

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
6. | Type image name with the file type
