'''
C. Fdez
10/07/2024

consultamos Presión de la Placa de Thread

desde FTDI el comando es A5 para leer la presión

'''

import subprocess
import serial
import time
from colorama import Fore, Style, Back

FTDI = '/dev/ttyUSB0'
RS232='/dev/ttyUSB1'


# Preparar MSP para consulta presion
Q_Press = "A5"  

def leer_presion():
    respuesta =""
    presion ="A5"
    # Abrir serial para mandar command leer presión
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(presion.encode())
    time.sleep(0.7)
    respuesta += ser.readline().decode().strip()
    time.sleep(0.4)
    ser.close()
    respuesta = respuesta.split(": ")
    respuesta = respuesta [2]
    print ("la presión es de : "+respuesta)
    
    # Cierra el puerto DP1
    cierre_DP1 ="G1"
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(cierre_DP1.encode())
    time.sleep(0.7)
    ser.close()
    respuesta = respuesta.split("(")
    respuesta = respuesta[0]
    print (respuesta)
    return respuesta

if __name__== "__main__":
    leer_presion()