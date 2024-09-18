import subprocess
from requests import Response
import serial
import time
import paramiko

Com_485= "/dev/ttyUSB3"
comando = "FF050000FF0099E4"
#comando = "FF050011FF00E1C9"
hostname = '192.168.5.3'
port = 22
username = 'root'
password = 'imus42'

def enciede_rele():
    ser = serial.Serial(Com_485,9600,8,"N",1,1)
    command = bytes.fromhex(comando)
    ser.write(command)

    response = ser.read(8)  # Ajusta el número de bytes a leer según la respuesta esperada
    print(f"Respuesta: {response.hex().upper()}")
    respuesta = response
    ser.close()
def lee_estado():    
    lee = 'FF01000008302E'
    #lee = "000000030185DB"
    lee_est = bytes.fromhex(lee)
    ser = serial.Serial("/dev/ttyUSB0",9600,8,"N",1,1)
    ser.write(lee_est)
    #time.sleep(.7)
    estado = ser.read()
    print(f"El estado de los relés es : {estado.hex()}")
    ser.close()

def apaga_rele():
    apagado = "FF0500000000D814"
    apaga = bytes.fromhex(apagado)
    ser = serial.Serial("/dev/ttyUSB0",9600,8,"N",1,1)
    ser.write(apaga)
    time.sleep(.7)
    response = ser.read(8)
    print(f"la respuesta del módulo es {response.hex().upper()} el relé número 1 está apagado")
    ser.close()

def dispositivo():
    dir = "000000030185DB"
    #dir = '0000000301E530'
    dir_disp = bytes.fromhex(dir)
    ser = serial.Serial("/dev/ttyUSB0",9600,8,"N",1,1)
    ser.write(dir_disp)
    #time.sleep(.7)
    response = ser.read()
    print(f"la respuesta del módulo es {response.hex()} ")
    ser.close()

def calculate_crc(data):
    crc = 0xFFFF  # Valor inicial
    for byte in data:
        crc ^= byte  # XOR entre el CRC actual y el byte de datos
        for _ in range(8):  # Procesar 8 bits
            if crc & 0x0001:  # Si el bit menos significativo es 1
                crc = (crc >> 1) ^ 0xA001  # Desplazar y hacer XOR con el polinomio
            else:
                crc >>= 1  # Solo desplazar a la derecha
    # El CRC es un valor de 16 bits, devolvemos LSB primero, luego MSB
    return crc.to_bytes(2, byteorder='little')

ssh = paramiko.SSHClient()

# Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conecta al servidor
ssh.connect(hostname, port, username, password)
contador = 0
# Ejecuta un comando (por ejemplo, 'ls -l')
stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS2 > /dev/ttyS2')




if __name__ == "__main__":
    #dispositivo()
    enciede_rele()
    #lee_estado()
    apaga_rele()
   
    #data = bytes.fromhex('FF01000008')  # Comando sin el CRC
    #crc = calculate_crc(data)
    #print(f"CRC calculado: {crc.hex().upper()}")  # Imprime el CRC en hexadecimal
    '''
    # Preparar DP2 para RS232
    DP2_485 = ["e2","e6","g2","f0","f2","m9","m5"]
    ssh = paramiko.SSHClient()
    # Permite que se añadan automáticamente hosts desconocidos (no es seguro en producción)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Conecta al servidor
    ssh.connect(hostname, port, username, password)
    contador = 0
    # Ejecuta un comando (por ejemplo, 'ls -l')
    stdin, stdout, stderr = ssh.exec_command('cat /dev/ttyS2 > /dev/ttyS2')
    comando = "FF050000FF0099E4"
    dir_disp = bytes.fromhex(comando)
    ser4= serial.Serial('/dev/ttyUSB0', 19200)  
    ser4.timeout = 1  
    for mensaje in DP2_485:
        ser4.write(mensaje.encode())
        FTDI_res = ser4.read()
        print (f'respuesta snoopy : {FTDI_res}')

    ser = serial.Serial("/dev/ttyS2",9600,8,"N",1,1)
    ser.write(dir_disp)
    #time.sleep(.7)
    resp= ""
    resp += ser.read()
    print(f"la respuesta del módulo es {resp.hex()} ")
    
    ser.close()'''