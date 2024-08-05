# para buscar en la red local un Thred
# sudo nmap -sP 192.168.4.1/24 | grep "for\|MAC\|Texas"
# para lanzar desde terminal con el puente
#	Configurar desde putty una conexión serie a 115200
#	abrir el puerto del FTDI
#	Configurar DP1 con --> E0, E2, E6, F0, F1, L9, L4
#	verificar con L8
#	Abrir sesion de Teraterm a la IP
#	una vez logeado --> screen /dev/ttyS0 115200
#	esto nos abre una terminal en la cual al escribir no contestará directamente
#
# importar paramiko --> sudo apt install python3-paramiko
# las reglas para definir FTDI y RS232 están en /etc/udev/rules.d/99-worldsensing.rules

# TO DO:
#   10/07/2024   
#               Implementar en la primera tabla los campos siguientes
#               [ ] --> Article (ERP Code)
#               [ ] --> Product Description
#               [ ] --> Modem Type
#               [ ] --> OS Image flashed
#               [ ] --> Power button color test  ([ PASS ])
#               [ ] --> Ethernet test  ([ PASS ])
#               [ ] --> Firmware  (1.1.9A)
#               [ ] --> Version  (8.8.49)
#               [ ] --> Imei
#               [x] --> Mac address 
#               [x] --> Pressure
#               [x] --> Temperature
#               [ ] --> Battery test date
#               [ ] --> Battery test  ([ PASS ])
#               [ ] --> 
import paramiko
import subprocess
import serial
import time
import Ip_scanner
from colorama import Fore, Style, Back
import Informe
from Pressure_test import leer_presion
from Temp_test import leer_temperatura
from Version import Get_version
from FW_test import Get_FW
from Battery import Get_battery


# Utilizamos Crono para capturar el tiempo del test
Crono = time.time()
# Datos de conexión SSH
#hostname = input('introduce la ip de la placa: ')
hostname = '192.168.5.3'
#rango = input("introduce el rango de la red: ")
#coman = "sudo nmap -sP "+rango+"/24"
#condicion = "Texas"
#hostname = Ip_scanner.listar_lineas(coman,condicion)
#print(hostname)
port = 22
username = 'root'
password = 'imus42'
USB_Serial = '0123456789ABD8C'
good = "[ PASS ]"
bad = "[ FAIL ]"
FTDI = '/dev/ttyUSB0'
RS232='/dev/ttyUSB1'

# Preparar DP1 para USB
DP1_USB = ["G1","e2","e6","f0","f1","J0","J1"]    
# Preparar DP1 para RS232
DP1_232 = ["e2","e6","g1","f0","f1","l9","l4"]
# Preparar DP2 para RS232
DP2_232 = ["e2","e6","g2","f0","f2","m9","m4"]
# Preparar DP3 para RS232
DP3_232 = ["e2","e6","g3","f0","f3","n9","n4"]

# Mensaje en DP1, DP2 y DP3 para RS232
DP1_texto = ["RS","232","_in_","DP1","-->","[PASS]"]
DP2_texto = ["RS232","_in_","DP2-->","[PASS]"]
DP3_texto = ["RS232","_in_","DP3-->","[PASS]"]



def Obtener_mac(ip):
    try:
        res = subprocess.check_output(['arp','-n', ip])
        res_decodificado = res.decode('utf-8')
        lineas = res_decodificado.split('\n')
        for linea in lineas:
            if ip in linea:
                direccion_mac=linea.split()[2]
                return direccion_mac
    except subprocess.CalledProcessError:
        return None
def Configura_USB():
     # Configura la conexión serie
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    print("Conecta el conector del cable para USB al puerto DP1")
    seguimos = input ("presiona una tecla cuando estés lista")
    # Iterar sobre la lista de comandos y ejecutar cada uno
    for comando in DP1_USB:
        #print(f"Ejecutando comando: {comando}")
        ser.write(comando.encode())
        time.sleep(0.7)
    ser.close()
    return print ("El puerto DP1 está configurado para leer dispositivos USB")

def Check_Serial(USB_Serial):   
    Configura_USB()
    time.sleep(12)
    for line in stdout:
        print(line.strip())
        if USB_Serial in line:
            USB_Check_Serial = line.split(":")[2].strip()
            if USB_Serial == USB_Check_Serial:
                print(f"{Fore.GREEN}{"Check USB -->"+ good}{Style.RESET_ALL}")
            else:                
                print(f"{Fore.RED}{"Check USB -->"+bad}{Style.RESET_ALL}")
            break
    else:
        print (f"{Fore.CYAN}{"No se ha detectado dispositivo en el USB"}{Style.RESET_ALL}")
        return False


try:
    # Crea una instancia de SSHClient
    ssh = paramiko.SSHClient()

    # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conecta al servidor
    ssh.connect(hostname, port, username, password)
    contador = 0
    # Ejecuta un comando (por ejemplo, 'ls -l')
    stdin, stdout, stderr = ssh.exec_command('dmesg | grep 0123456789ABD8C')
    Serial_USB = Check_Serial(USB_Serial)
    if Serial_USB == False and contador<1:
        contador = 1
        stdin, stdout, stderr = ssh.exec_command('dmesg | grep 0123456789ABD8C')
        Serial_USB = Check_Serial(USB_Serial)
    

    # Cierra el puerto DP1
    cierre_DP1 ="G1"
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(cierre_DP1.encode())
    time.sleep(0.7)
    ser.close()
    direccion_mac= Obtener_mac(hostname)
    if direccion_mac:
        print(f"la dirección mac del dispositivo con ip {hostname} es --> {direccion_mac}")
        dato_mac = direccion_mac
        resultado = direccion_mac.split(":")
        result_convertido = ''.join([parte[::-1] for parte in resultado])
        #print (result_convertido)
        Serial = result_convertido[6:]
        #print (Serial)
        Serial= Serial[4:]+Serial[2:4]+Serial[:2]
        print (f'El serial del dispositivo es: {Back.LIGHTCYAN_EX}{Fore.BLACK}{Serial.upper()}{Style.RESET_ALL}')
    #else:
        #print(f"No se puedo encontrar el dispositivo con dirección {Fore.RED}{ip_dispositivo}{Style.RESET_ALL}")
        
       
    
    # Mostrar el Serial del dispositivo según su MAC
    



except paramiko.AuthenticationException:
    print("Fallo de autenticación, verifica el nombre de usuario y la contraseña")
except paramiko.SSHException as ssh_ex:
    print("Error al intentar conectarse al servidor:", ssh_ex)


# Configura la conexión serie
ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
ser.timeout = 1  # Tiempo de espera para la lectura en segundos
print("Conecta el conector del cable RS232 al puerto DP1")
seguimos = input ("presiona una tecla cuando estés lista")
# Iterar sobre la lista de comandos y ejecutar cada uno
for comando in DP1_232:
    #print(f"Ejecutando comando: {comando}")
    ser.write(comando.encode())
    time.sleep(0.5)


ser2= serial.Serial(RS232, 115200)  # Reemplaza '/dev/ttyRS232' con el puerto correcto
ser2.timeout = 1  # Tiempo de espera para la lectura en segundos
stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS0 > /dev/ttyS0')
respuesta = ""
for comando in DP1_texto:
    ser2.write(comando.encode())
    #print(f"Ejecutando comando: {comando}")
    time.sleep(0.4)
    # Lee la respuesta
    respuesta += ser2.readline().decode().strip()
    time.sleep(0.4)
    if "PASS" in respuesta:
        DP1_formateado = f"{Fore.GREEN}{"RS232_in_DP1 --> "+good}{Style.RESET_ALL}"
        break
print("Respuesta DP1:", DP1_formateado)
ser2.close()

# Cierra la conexión serie
cierre_DP1 ="G1"
ser.write(cierre_DP1.encode())
time.sleep(0.3)
#print(f"cerrando DP1: {cierre_DP1}")
print("Cambia el conector del cable RS232 al puerto DP2")
seguimos = input("presiona una tecla cuando estés lista")

for comando in DP2_232:
    #print(f"Ejecutando comando: {comando}")
    ser.write(comando.encode())
    time.sleep(0.3)

ser3= serial.Serial(RS232, 9600)  # Reemplaza '/dev/ttyRS232' con el puerto correcto
ser3.timeout = 1  # Tiempo de espera para la lectura en segundos
stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS2 > /dev/ttyS2')

respuesta = ""
#for comando in DP2_texto:
#while True:
for comando in DP2_texto:
    ser3.write(comando.encode())
    #print(f"Ejecutando comando: {comando}")
    time.sleep(0.3)
    # Lee la respuesta
    respuesta += ser3.readline().decode().strip()
    time.sleep(0.4)
    if "PASS" in respuesta:
        DP2_formateado = f"{Fore.GREEN}{"RS232_in_DP2 --> "+good}{Style.RESET_ALL}"
        break

#print("Respuesta DP2:", respuesta)
print("Respuesta DP2:", DP2_formateado)
ser3.close()
# Cierra la conexión serie
cierre_DP2 ="G2"
ser.write(cierre_DP2.encode())
#print(f"cerrando DP2: {cierre_DP2}")
time.sleep(0.4)
print("Cambia el conector del cable RS232 al puerto DP3")
seguimos = input("presiona una tecla cuando estés lista")
for comando in DP3_232:
    #print(f"Ejecutando comando: {comando}")
    ser.write(comando.encode())
    time.sleep(0.3)

ser4= serial.Serial(RS232, 9600)  # Reemplaza '/dev/ttyRS232' con el puerto correcto
ser4.timeout = 1  # Tiempo de espera para la lectura en segundos
stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS1 > /dev/ttyS1')
#seguimos = input("presiona una tecla cuando estés lista")
respuesta = ""
for comando in DP3_texto:
    ser4.write(comando.encode())
    #print(f"Ejecutando comando: {comando}")
    time.sleep(0.4)
    # Lee la respuesta
    respuesta += ser4.readline().decode().strip()
    time.sleep(0.4)
    if "PASS" in respuesta:
        DP3_formateado = f"{Fore.GREEN}{"RS232_in_DP3 --> "+good}{Style.RESET_ALL}"
        break
    
print("Respuesta DP3:", DP3_formateado)
ser4.close()
# Cierra la conexión serie
cierre_DP3 ="G3"
ser.write(cierre_DP3.encode())
#print(f"cerrando DP3: {cierre_DP3}")
time.sleep(0.5)

print("Desconecta el cable del Thread, el test ha finalizado")


ser.close()
#ssh.close()
Fin_test = time.time()
Total_test = Fin_test-Crono
dato_presion = leer_presion()
dato_temperatura = leer_temperatura()
fw = Get_FW()
version = Get_version()
bateria = Get_battery()
print (f"El tiempo del test ha sido: {Total_test}")
Info = Informe.crear_pdf(Serial,
                         Serial,
                         good,
                         good,
                         good,
                         good,
                         dato_mac,
                         dato_presion,
                         dato_temperatura,
                         fw,
                         version,
                         bateria,
                         )




