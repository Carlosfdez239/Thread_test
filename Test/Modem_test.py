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
import paramiko
import subprocess
import serial
import time
from colorama import Fore, Style, Back


HOSTNAME = '192.168.5.3'
PORT = 22
USERNAME = 'root'
PASSWORD = 'imus42'
DEVICE = '/dev/ttyCELL'
BAUDRATE = 115200

def Get_modem():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        contador = 0
        # Ejecuta un comando (por ejemplo, 'ls -l')
        #stdin, stdout, stderr = ssh.exec_command('dmesg | grep cell')
        stdin, stdout, stderr = ssh.exec_command('ls /dev/ttyCELL')

    except paramiko.AuthenticationException:
        print("Fallo de autenticación, verifica el nombre de usuario y la contraseña")
    except paramiko.SSHException as ssh_ex:
        print("Error al intentar conectarse al servidor:", ssh_ex)

    with serial.Serial(DEVICE,BAUDRATE, timeout=1) as ser:

        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f'Recibido: {line}')
        ser.write(b'AT\n')                              # Si no responde con el serial, probar con el ssh
                                                        # usando ECHO AT > /dev/ttyCELL
        line = ser.readline().decode('utf-8').strip()
        print(f'Recibido: {line}')
        if line == 'OK':
            ser.write(b'AT+CGMM\r')
            Cell_model = ser.readline().decode('utf-8').strip()
            print(f'Recibido: {Cell_model}')
            ser.write(b'AT+CIMI\r')
            Sim_serial = ser.readline().decode('utf-8').strip()
            print(f'Recibido: {Sim_serial}')
        else:
            print(f'No se ha recibido el OK, se ha recibido:  {Cell_model}')

if __name__ == '__main__':
    Get_modem()