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

To-Do
    [ ] Gestionar los tres voltajes
    [ ] Pasar como parámetro el puerto DP y según el puerto lanzar los comandos del MSP
    [ ] Returns para cada configuración
Issue
    [ ] Al arrancar la BK de cero, no podemos parametrizar la corriente. No aparece el texto Sense en el display.
    [ ] Queda mensaje Error en el display


'''

import subprocess
import serial
import time
from colorama import Fore, Style, Back

FTDI = '/dev/ttyUSB0'
BK='/dev/ttyUSB1'


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
    #hola = input('pulsa ON en la fuente BK para verificar la corriente')
    try:
        # Mandamos la orden de lectura a la carga electronica BK8600
        ser1.write(b'REM:SENS 1\n')
        time.sleep(0.5)

        # Configuramos a 1.50 Amp la carga
        ser1.write(b'SOUR:CURR 1.50\n')
        time.sleep(0.5)
        
        # Mandamos la orden de control remoto a la carga electronica BK8600
        ser1.write(b'SYST:REM\n')
        time.sleep(0.5)

        # Pedimos la versión del software de la carga electronica
        ser1.write(b':SYST:VERS?\n')
        time.sleep(0.2)
        Ver = ser1.readline().decode().strip()

        # Pedimos la identidad de la carga electronica
        ser1.write(b'*IDN?\n')
        time.sleep(0.2)
        Instrument = ser1.readline().decode().strip()

        # Mandamos la orden de ON de la carga electronica BK8600
        ser1.write(b'SOUR:INP:STAT 1\n')
        time.sleep(2)
        

        #Mandamos la petición de lectura de voltaje y corriente   
        ser1.write(b'REM:SENS 1;:MEAS:VOLT?;CURR?\n')
        time.sleep(0.3)
        
        # Mandamos la orden de OFF de la carga electronica BK8600
        ser1.write(b'SOUR:INP:STAT 0\n')
        time.sleep(0.5)

        #leemos la respuesta
        voltaje = ser1.readline().decode().strip().split(";")
        print(f'{"Test realizado con: "}{Fore.YELLOW}{Instrument}{Style.RESET_ALL}')
        print(f'{"Version de la BK8600: "}{Fore.YELLOW}{Ver}{Style.RESET_ALL}')
        print(f'{"Voltaje leido --> "}{Fore.YELLOW}{voltaje[0]+" Volt"}{Style.RESET_ALL}')
        print(f'{"Corriente leida --> "}{Fore.YELLOW}{voltaje[1]+" Amp"}{Style.RESET_ALL}')
        Volt=voltaje[0]
        Amp=voltaje[1]
        if float(Volt) > 11.0:
            print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
        
        if float(Amp) > 1.48:
            print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
        
   

    except Exception as e:
        print(f'Error al leer en BK: {e}')
    finally:
        ser1.close()
    
    # Cierra el puerto DP1
    cierre_DP1 ="G1"
    ser = serial.Serial(FTDI, 115200)  
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    ser.write(cierre_DP1.encode())
    time.sleep(0.7)
    ser.close()


if __name__== "__main__":
    leer_tdk()