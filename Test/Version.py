'''
C. Fdez
10/07/2024

consultamos la version del FW de la Placa de Thread

usamos conexión SSH y el comando curl -X GET 'http://localhost/api/version'

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
VERSION ='http://localhost/api/version'

def Get_version():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('curl -X GET '+VERSION)
        for line in stdout:
            #print(line.strip())
            Version = line.split('"')
            Version = Version [3]  
            print(f'Snoopy version : {Fore.YELLOW}{Version}{Style.RESET_ALL}')   
        
        return Version
    except subprocess.CalledProcessError:
        return None


if __name__== "__main__":
    Get_version()
