'''
C. Fdez
11/07/2024

consultamos la Temperatura de la Placa de Thread

usamos conexión SSH y el comando curl -X GET 'http://localhost/api/tempRead'

'''

import subprocess
from colorama import Fore, Style, Back
import paramiko

HOSTNAME = '192.168.5.3'
PORT = 22
USERNAME = 'root'
PASSWORD = 'imus42'
FTDI = '/dev/ttyUSB0'
RS232='/dev/ttyUSB1'
TEMPERATURE ='http://localhost/api/tempRead'

def Get_Temp():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('curl -X GET '+TEMPERATURE)
        for line in stdout:
            #print(line.strip())
            Temperatura = line.split(':')
            Temperatura = Temperatura [1].strip("}")  
            print(f"{"Temperatura : "}{Fore.YELLOW}{Temperatura}{Style.RESET_ALL}")   
                
        return Temperatura
    except subprocess.CalledProcessError:
        return None


if __name__== "__main__":
    Get_Temp()