'''
C. Fdez
10/07/2024

consultamos la version del FW de la Placa de Thread

usamos conexión SSH y el comando curl -X GET 'http://localhost/api/firmware'

'''

import subprocess
from colorama import Fore, Style, Back
import paramiko

HOSTNAME = '192.168.5.3'
PORT = 22
USERNAME = 'root'
PASSWORD = 'imus42'
#FTDI = '/dev/ttyUSB0'
#RS232='/dev/ttyUSB1'
FIRMWARE ='http://localhost/api/firmware'

def Get_FW():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('curl -X GET '+FIRMWARE)
        for line in stdout:
            #print(line.strip())
            FW_version = line.split('"')
            FW_version = FW_version [3]  
            print(f"{"Fw version : "}{Fore.YELLOW}{FW_version}{Style.RESET_ALL}")   
                
        return FW_version
    except subprocess.CalledProcessError:
        return None


if __name__== "__main__":
    Get_FW()
