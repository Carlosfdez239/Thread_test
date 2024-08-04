'''
C. Fdez
30/07/2024

consultamos voltaje y corriente leidos por la BK 8600 para cada canal DP1, DP2 y DP3 del Thread

desde FTDI configuraremos los voltajes en cada canal
    - 12v
    - 13,5v
    - 15v
en la Bk8600 programaremos una corriente de 1.5A

por el puerto ttyUSB4 consultaremos la lectura de los valores para voltaje y corriente

'''

import subprocess
import serial
import time
from colorama import Fore, Style, Back

FTDI = '/dev/ttyUSB0'
BK='/dev/ttyUSB0'


# Preparar MSP para consulta presion
TDK_DP1 = ["l1"]  

def leer_tdk():
    respuesta =""
    # Abrir serial para mandar command leer presión
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos

    for comando in TDK_DP1:
        ser.write(comando.encode())
        #print(f"Ejecutando comando: {comando}")
        time.sleep(0.4)
    ser.close()

    # Abrir serial1 para mandar command a la carga electronica BK8600
    ser1 = serial.Serial(BK, 9600,bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser1.timeout = 1  # Tiempo de espera para la lectura en segundos
    hola = input('pulsa ON en la fuente BK para verificar la corriente')
    try:
        # Mandamos la orden de control remoto a la carga electronica BK8600
        #ser1.write(b'SYST:REM')

        # Mandamos la orden de apagado de la carga electronica BK8600
        #ser1.write(b'REM:SENS 1')
        
        # Mandamos la orden de encendido de la carga electronica BK8600
        #ser1.write(b'REM:SENS 1')
        #print(f'Activamos la carga electronica')

        #Mandamos la petición de lectura de voltaje
        #ser1.write(b'MEAS:VOLT?\n')
        ser1.write(b'REM:SENS 1;:MEAS:VOLT?;CURR?\n')
        #ser1.write(b'*IDN?\n')
        #leemos la respuesta
        voltaje = ser1.readline().decode().strip()
        print(f'Voltaje leido --> {voltaje} Volt')
        
        # Mandamos la petición de lectura de la corriente
        #ser1.write(b'MEAS:CURR?\n')
        #time.sleep(0.1)
        # Leemos la respuesta
        #corriente = ser1.readline().decode().strip()
        #print(f'Corriente leida --> {corriente} Amp')

        # Mandamos la orden de apagado de la carga electronica BK8600
        #ser1.write(b'REM:SENS 0')

            
        # Mandamos la orden de anular el control remoto a la carga electronica BK8600
        #ser1.write(b'SYST:LOC')

    except Exception as e:
        print(f'Error al leer el voltaje: {e}')
    finally:
        ser1.close()
    
    # Cierra el puerto DP1
    valida = input('presiona una tecla cuando estés lista para finalizar el test')
    cierre_DP1 ="G1"
    ser = serial.Serial(FTDI, 115200)  # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(cierre_DP1.encode())
    time.sleep(0.7)
    ser.close()


if __name__== "__main__":
    leer_tdk()