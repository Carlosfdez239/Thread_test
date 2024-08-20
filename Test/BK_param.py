'''
C. Fdez
16/08/2024

Parametrizamos el uso de la BK 8600 configurando una corriente de 1,5A

por el puerto ttyUSB4 consultaremos la lectura de los valores para voltaje y corriente

To-Do
    [x] Pasar como parámetro el puerto DP --> 16/08/2024
    [x] Returns para cada configuración --> 16/08/2024
Issue
    [ ] Al arrancar la BK de cero, no podemos parametrizar la corriente. No aparece el texto Sense en el display.
    [ ] Queda mensaje Error en el display
    [ ] 

'''


import subprocess
import serial
import time
from colorama import Fore, Style, Back

BK='/dev/ttyUSB0'

def Parametriza_BK():
    # Abrir serial1 para mandar command a la carga electronica BK8600
    ser1 = serial.Serial(BK, 9600,bytesize=serial.EIGHTBITS, 
                        parity=serial.PARITY_NONE, 
                        stopbits=serial.STOPBITS_ONE, 
                        timeout=1)  # Parametrizamos la comunicación serie BK
    
    try:
        # Mandamos la orden de lectura a la carga electronica BK8600
        ser1.write(b':REM:SENS 1\n')
        time.sleep(0.5)

        # Configuramos a 1.50 Amp la carga
        ser1.write(b'SOUR:CURR 1.50\n')
        time.sleep(0.5)
        
        # Mandamos la orden de control remoto a la carga electronica BK8600
        ser1.write(b':SYST:REM\n')
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

    except Exception as e:
        print(f'Error al leer en BK: {e}')
    finally:
        ser1.close()
        time.sleep(0.4)
        return Volt, Amp, Instrument, Ver
    
if __name__== "__main__":
    Parametriza_BK()
