
'''

C. Fdez
16/08/2024

Desde Atlasian How to Test the XBEE

********************************
To test the XBee:
********************************

Remove power from board
Insert module
Enable XBee power (command ‘E8’) & Enable module (command ‘E7’)
Turn on Octavo (command ‘E2’)
In Octavo, screen to tty04 at 9600 baud (the XBee)
Press +++ to enter command mode (no enter key)
The module should reply ‘OK’
Enter AT <enter>
The module should reply ‘OK’
If you do not get a response from module, probe the Reset pin (pin 5 on J6 left side of XBee). It should be high. If it is low then enter the command to enable Xbee reset. Then probe both UART lines. Both should be high. If they were being pulled low then something may be not functional. 

To rule out the module:
Power off the board 
Remove the module
Place a jumper between Tx & Rx
Power on the board, and enable the Octavo (command ‘E2’)
Open screen and connect to TTY04:
screen /dev/ttyO4 9600
Enter text into the screen window. It should be echoed back.
If this is not working then there may be an issue with the Octavo OR the UART multiplexer on UART4 may be set to a different destination, e.g. Expansion Port.

**********************************
Testing
**********************************

This was tested on the following Xbee versions:

S3B
SX868
SX
Pro SX

'''


pass