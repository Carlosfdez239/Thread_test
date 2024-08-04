'''
C. Fdez
30/07/2024

podemos manipular la tensión de los DP de la Placa de Thread

usamos conexión SSH y el comando curl -X POST 

'''

import subprocess
from colorama import Fore, Style, Back
import paramiko

HOSTNAME = '192.168.5.3'
PORT = 22
USERNAME = 'root'
PASSWORD = 'imus42'

RS232='/dev/ttyUSB0'
VOLTAGE ='curl -X POST http://localhost/api/deviceVoltage -d'
PUERTO = '{"portNumber":1, "value":0}'

def Put_Voltage():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        stdin, stdout, stderr = ssh.exec_command(VOLTAGE + "'"+PUERTO+"'")
           
        
        return 
    except subprocess.CalledProcessError:
        return None


if __name__== "__main__":
    Put_Voltage()
