## NETWORK DESIGN: PHASE 1 ##
## ----- Ben Kelley ------ ##
## ------ Files: 2 ------- ##

 FILE DESCRIPTION
-----------------------------
1. | UDPServer.py
   | -- creates server on host IP and generates and binds a
   |  socket to a specified port, prints status to user
   | -- awaits message from UDPClient and upon reception,
   |  converts message to uppercase and appends an introduction
   |  to message and then sends message back to UDPClient
   |
2. | UDPClient.py
   | -- creates client on host IP and generates a socket to the
   |  same port as UDPServer
   | -- prompts user for message and sends message to UDPServer 
   |  through the generated socket
   | -- receives modified message from UDPServer through same
   |  socket and prints message to user
   
 STEPS TO EXECUTE
-----------------------------
1. | Ensure UDPServer.py & UDPClient.py are in same directory
   |
2. | Open one terminal in directory of source files and enter
   | server command: $ python3 UDPServer.py
   | -- python cmd will vary from system to system
   |
3. | Open another terminal in same directory and enter 
   | client command: $ python3 UDPClient.py
   |
4. | In same terminal (step 3) respond to prompt with desired
   | lowercase sentence and await response from server
   |
5. | RECEIVE RESPONSE
