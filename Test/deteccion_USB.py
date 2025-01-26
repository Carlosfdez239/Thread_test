'''
C. Fdez
20/01/2025

Script para localizar los dispositivos conectados a los puertos ttyUSB usando dmesg y conociendo los datos de sus
attributos

REV

0 --> 20/01/2025
1 --> 26/01/2025 Fine tunning del metodo asignar_tty(serial)
'''

import subprocess
import re
import os
import time


def Buscardispositivo_ttyUSB(SERIAL):
    try:
        print('Iniciando try')
        resultado = subprocess.run(['sudo','dmesg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida_dmesg= resultado.stdout
        salida_stdErr= resultado.stderr
        print (f'Salida stdout: {salida_dmesg}')
        print (f'Salida stdErr: {salida_stdErr}')
        dispositivos=[]
        for linea in salida_dmesg.splitlines():
            if SERIAL in linea :           
                dispositivos.append(linea)
        if dispositivos:
            print(f'Dispositivos conectados a puertos ttyUSB:')
            for dispositivo in dispositivos:
                print(f'Dispositivo --> {dispositivo}')
        else:
            print (f'No se han encontrado dispositivos que cumplan con los datos buscados')
    except Exception as e:
        print(f'Error al ejecutar el script: {e}')

def asignar_tty(serial):
    try:
        
        dispositivos = subprocess.run(['sudo','dmesg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida = dispositivos.stdout.splitlines()
        #print(f'dispositivos encontrados: {salida}')

        for linea in salida:
            if serial in linea:
                #print (f'Contenido de la linea: {linea}')
                parts = linea.split(":")
                usb = parts[0]
                usb_buscado = usb[-8:]
                #print(f'usb buscado --> {usb_buscado}')
                for linea in salida:
                    if usb_buscado in linea:
                        #print (f'Datos del usb_buscado --> {linea}')
                        if "ttyUSB" in linea:
                            tty_original = linea.split(":")
                            disp_original= tty_original[1]
                            #print(f'dispositivo encontrado --> {disp_original}')
                            valor_tty_encontrado = disp_original[-7:]
                            #print(f'valor tty encontrado --> {valor_tty_encontrado}')
                ruta_completa_dispositivo = f'/dev/{valor_tty_encontrado}'
                #print(f'Ruta dispositivo encontrado --> {ruta_completa_dispositivo}')
                #print (f'Enlace simbolico creado: {enlace_simbolico} --> {ruta_original}')
                return ruta_completa_dispositivo
            #print(f'No se ha encontrado ningún dispositivo que coincida')
    except Exception as e:
        print(f'Error al ejecutar el scrip --> {e}')

if __name__== "__main__":
    SERIAL = "AU05IC2W"
    asignar_tty(SERIAL)