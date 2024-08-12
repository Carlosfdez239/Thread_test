'''
C. Fdez
10/07/2024

consultamos la version del FW de la Placa de Thread

usamos conexión SSH y el comando curl -X GET 'http://localhost/api/batteryVoltage' para el voltaje
y 'http://localhost/api/stateOfCharge' para el porcentaje de carga

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
BATTERY_VOLT ='http://localhost/api/batteryVoltage'
BATTERY_STATE ='http://localhost/api/stateOfCharge'
def Get_battery():
    try:
        # Crea una instancia de SSHClient
        ssh = paramiko.SSHClient()

        # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta al servidor
        ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('curl -X GET '+ BATTERY_VOLT)
        for line in stdout:
            #print(line.strip())
            Battery = line.split(':')
            Battery = Battery [1].strip('}')
            print(f'{"Battery Voltage : "}{Fore.YELLOW}{Battery}{Style.RESET_ALL}')   
        stdin, stdout, stderr = ssh.exec_command('curl -X GET '+ BATTERY_STATE)
        for line in stdout:
            #print(line.strip())
            St_Battery = line.split(':')
            #print(St_Battery[1])
            St_Battery = St_Battery [1].strip('}')
            if float(St_Battery) > 97.0 :
                print(f'{Fore.GREEN}{"Battery Health status --> [ PASS ]"}{Style.RESET_ALL}')
                St_Battery_check = "[ PASS ]"
            else:
                print(f'{Fore.RED}{"Battery Health status --> [ FAIL ] ( "}{St_Battery}{" V )"}{Style.RESET_ALL}')
                St_Battery_check = "[ FAIL ]"
            return Battery, St_Battery_check
    except subprocess.CalledProcessError:
        return None


if __name__== "__main__":
    Get_battery()
