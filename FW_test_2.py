'''
C. Fdez
10/07/2024

consultamos la Temperatura de la Placa de Thread

desde FTDI el comando es A6 para leer la temperatura

'''

import subprocess
import serial
import time
from colorama import Fore, Style, Back

FTDI = '/dev/ttyUSB0'
RS232='/dev/ttyUSB1'


# Preparar MSP para consulta presion

def leer_FW():
    respuesta =""
    command ="I5"
    # Abrir serial para mandar command leer presión
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(command.encode())
    time.sleep(0.9)
    respuesta += ser.readline().decode().strip()
    time.sleep(0.5)
    ser.close()
    #respuesta = respuesta.split()
    #respuesta = respuesta [0]
    print ("el FW instalado es : "+respuesta)
    ser.close()
    return respuesta

if __name__== "__main__":
    leer_FW()