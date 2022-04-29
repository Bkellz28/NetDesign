## ---- NETWORK DESIGN: PHASE 6 ---- ##
## --------------------------------- ##
## ----- Ben Kelley -- JJ Hyde ----- ##
## --------- David Nguyen ---------- ##
## --------------------------------- ##
## ----------- Files: _  ----------- ##

(Liam did not participate in any of the extra credit for Phase 6)

We choose to do the GUI extra credit that would depict the file transfer.

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
3. | sample.bmp
   | Image that is being sent and received.
   | 
4. | result.bmp
   | This file is made once the server receives the image and rebuilds it as result.bmp
   |
5. | CheckSumUtility.py
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
7. | There are a number of things to change for this program in the line that can be found on line 17 on UDP.Sender that says
     'Sender = RDT3(sndrName, sndrPort, 10, 0.03, 1, 1)'
     # 1ST & 2ND INPUTS: receiver name and port
     # 3RD INPUT: go-back-n frame size
     # 4TH INPUT: message receive timeout number in seconds (mostly used for sender)
     # 5TH INPUT: optional, error simulation mode (1 is no errors and the default, 2-5 remaining options)
     # 6TH INPUT: optional, debug mode (0 is very few feedback print messages and the default, 1 prints much more info to terminal)
