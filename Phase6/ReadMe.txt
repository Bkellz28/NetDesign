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
   | GUI pops up when this is run.
   |
2. | UDPReceiver.py: 
   | Acts as the server that receivers the packets for the BMP / JPG file.
   | Opens the image when all packets are sent.
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
5. | Run both programs (do receiver first, then sender)
   | 
6. | Type image name with the file type in the entry box and press submit.
   |
7. | Watch the file transfer depiction with the GUI.
   |
8. | The same error modes can be made as done in previous phases. Refer to lines 60 and 335 in sender, and 196 in receiver.
