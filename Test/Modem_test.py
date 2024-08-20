'''
C. Fdez
16/08/2024

Desde Atlasian How to Verify USB to Cellular Modem:

For a more thorough test, connect to the cell modem over USB and verify its part number:

Power on the cell modem (should be automatic; controlled by the Octavo)

Connect to the cell modem with screen:

screen /dev/ttyCELL 115200

See if it is responding:

Type AT <enter>

Receive: OK<enter>

Get model number:

Type AT+CGMM

Receive: LE910-SVG (depends on model)




'''

pass