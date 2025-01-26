'''
C. Fdez
20/01/2025

Script para localizar los dispositivos conectados a los puertos ttyUSB usando dmesg y conociendo los datos de sus
attributos

REV

0 --> 20/01/2025
<<<<<<< HEAD
1 --> 26/01/2025 Fine tunning del metodo asignar_tty(serial)
=======
>>>>>>> 4e55d811583e274961d92f8c4dfe639002053c01
'''

import subprocess
import re
import os
import time

<<<<<<< HEAD

def Buscardispositivo_ttyUSB(SERIAL):
=======
primero = "SerialNumber"

def Buscardispositivo_ttyUSB():
>>>>>>> 4e55d811583e274961d92f8c4dfe639002053c01
    try:
        print('Iniciando try')
        resultado = subprocess.run(['sudo','dmesg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida_dmesg= resultado.stdout
        salida_stdErr= resultado.stderr
        print (f'Salida stdout: {salida_dmesg}')
        print (f'Salida stdErr: {salida_stdErr}')
<<<<<<< HEAD
        dispositivos=[]
        for linea in salida_dmesg.splitlines():
            if SERIAL in linea :           
                dispositivos.append(linea)
        if dispositivos:
            print(f'Dispositivos conectados a puertos ttyUSB:')
            for dispositivo in dispositivos:
=======

        #Filtrado de la linea que contiene la información buscada
        #dispositivos = re.findall(r"(ttyUSB[0-9]+).*?Manufacturer=([0-9a-Fa-f]+).*?Product=([0-9a-fA-F]+)", salida_dmesg,re.DOTALL)
        #dispositivos = re.findall(r"^(FTDCRGN5)"),salida_dmesg
        dispositivos=[]
        for linea in salida_dmesg.splitlines():
            if "SerialNumber: FTDCRGN5" in linea :
            
                dispositivos.append(linea)

        if dispositivos:
            print(f'Dispositivos conectados a puertos ttyUSB:')
            for dispositivo in dispositivos:
                #puerto, id_vendor,id_product = dispositivo
                #print (f'Puerto : {puerto}, idVendor : {id_vendor}, id_Product : {id_product}')
>>>>>>> 4e55d811583e274961d92f8c4dfe639002053c01
                print(f'Dispositivo --> {dispositivo}')
        else:
            print (f'No se han encontrado dispositivos que cumplan con los datos buscados')
    except Exception as e:
        print(f'Error al ejecutar el script: {e}')

<<<<<<< HEAD
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
=======
def asignar_tty(id_product, serial):
    try:
        #dispositivos = subprocess.run(["ls", "-l", "/dev/serial/by-id/"], stdout=subprocess.PIPE, text=True)
        dispositivos = subprocess.run(['sudo','dmesg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida = dispositivos.stdout.splitlines()
        print(f'dispositivos encontrados: {salida}')

        for linea in salida:
            if serial in linea:
                #parts = linea.split ("->")
                print (f'Contenido de la linea: {linea}')
                parts = linea.split(":")
                usb = parts[0]
                usb_buscado = usb[-8:]
                print(f'usb buscado --> {usb_buscado}')
                for linea in salida:
                    if usb_buscado in linea:
                        print (f'Datos del usb_buscado --> {linea}')
                        if "ttyUSB" in linea:
                            tty_original = linea.split(":")
                            disp_original= tty_original[1]
                            print(f'dispositivo original --> {disp_original}')
                            valor_tty_original = disp_original[-7:]
                            print(f'valor tty original --> {valor_tty_original}')
                #dispositivo_original = os.path.basename(parts[0].strip())
                ruta_original = f"/dev/{valor_tty_original}"
                print(f'Ruta original del dispositivo --> {ruta_original}')
                time.sleep(2)
                enlace_simbolico = "/dev/ttyUSB0"
                if os.path.exists(enlace_simbolico):
                    os.remove(enlace_simbolico)
                os.symlink(ruta_original, enlace_simbolico)
                print (f'Enlace simbolico creado: {enlace_simbolico} --> {ruta_original}')
                return
            print(f'No se ha encontrado ningún dispositivo que coincida')
>>>>>>> 4e55d811583e274961d92f8c4dfe639002053c01
    except Exception as e:
        print(f'Error al ejecutar el scrip --> {e}')

if __name__== "__main__":
<<<<<<< HEAD
    SERIAL = "AU05IC2W"
    asignar_tty(SERIAL)
=======
    #Buscardispositivo_ttyUSB()
    #ID_VENDOR = ""
    ID_PRODUCT = "TTL232R-3V3"
    SERIAL = "FTDCRGN5"
    asignar_tty(ID_PRODUCT, SERIAL)
>>>>>>> 4e55d811583e274961d92f8c4dfe639002053c01
