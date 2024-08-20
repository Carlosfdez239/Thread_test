
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

import paramiko
import subprocess
import serial
import time
from colorama import Fore, Style, Back

hostname = '192.168.5.3'
port = 22
username = 'root'
password = 'imus42'


FTDI = '/dev/ttyUSB1'
RS232='/dev/ttyUSB0'

# Preparar comandos para activar XBEE
XBEE_USB = ["D8","D7","E8","E7"]  

# Comandos AT para XBEE
XBEE_AT = ["+++","AT\n"]

def Get_XBEE():

    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    
    for comando in XBEE_USB:
        ser.write(comando.encode())
        linea = ser.readline().decode().strip()
        print(linea+'\n')
        time.sleep(1)
    
    


    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(hostname, port, username, password)
        
        #for text in XBEE_AT:

        # Ejecuta un comando (por ejemplo, 'ls -l')
        inicializar = """(echo -e "+++"; cat< /dev/ttyO4) | head -n 10 """
        stdin, stdout, stderr = ssh.exec_command(inicializar)
        #stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS0 > /dev/ttyS0')
        time.sleep (10)
        respuesta = stdout.read().decode()
        
        print (respuesta)
    
    except paramiko.AuthenticationException:
        print("Fallo de autenticación, verifica el nombre de usuario y la contraseña")
    except paramiko.SSHException as ssh_ex:
        print("Error al intentar conectarse al servidor:", ssh_ex)
    time.sleep(10)
    ser.write("d8".encode())
    linea = ser.readline().decode().strip()
    print(linea+'\n')
    ser.write("d7".encode())
    linea = ser.readline().decode().strip()
    print(linea+'\n')
    ser.close()
if __name__ == "__main__":
    Get_XBEE()