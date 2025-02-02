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
    [X] Gestionar los tres voltajes --> 16/08/2024
    [X] Pasar como parámetro el puerto DP y según el puerto lanzar los comandos del MSP --> 16/08/2024
    [X] Returns para cada configuración --> 16/08/2024
    [X] Actualizar informe del Test --> 16/08/2024
    [X] Añadimos los valores analógicos para el informe FCT de calidad --> 23/08/2024
Issue
    [ ] Al arrancar la BK de cero, no podemos parametrizar la corriente. No aparece el texto Sense en el display.
    [ ] Queda mensaje Error en el display
    [ ] 


'''

import subprocess
import serial
import time
from colorama import Fore, Style, Back
from BK_param import Parametriza_BK
from eMail import eMail_to
from Informe_FCT import crearFCT_pdf
import deteccion_USB as USB


#FTDI = '/dev/ttyUSB0'
TOLERANCIA_AMP = 1.48

# Preparar MSP para consulta presion
TDK_DP1 = ["l1", "l2", "l3"]  
TDK_DP2 = ["m1", "m2", "m3"]  
TDK_DP3 = ["n1", "n2", "n3"]  

def leer_tdk(N_serie, FTDI, BK):
    respuesta =""
    # Abrir serial para mandar command leer presión
    ser = serial.Serial(FTDI, 115200)   # Reemplaza '/dev/ttyFTDI' con el puerto correcto
    ser.timeout = 1                     # Tiempo de espera para la lectura en segundos
    print(f'Conecta el cable de la BK en el puerto DP1')
    hola = input('pulsa Enter para iniciar el test')
    for comando in TDK_DP1:
        ser.write(comando.encode())
        #print(f"Ejecutando comando: {comando}")
        puerto = "DP1"
        Resultado = Parametriza_BK(BK)
        time.sleep(0.4)
        # Analizamos el resultado para los 12v
        if comando == "l1":
            limite_inf = 11.0
            Volt=Resultado[0]                   # la posición [0] corresponde al voltaje
            Amp=Resultado[1]                    # la posición [1] corresponde a la corriente
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP1_Volt_12 = "[ PASS ]"
                DP1_Volt_12_Vana = Volt
                DP1_Volt_12_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP1_Volt_12 = "[ FAIL ]"
                DP1_Volt_12_Vana = Volt
                DP1_Volt_12_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP1_Amp_12 = "[ PASS ]"
                DP1_Amp_12_Ana = Amp
                DP1_Amp_12_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP1_Amp_12 = "[ FAIL ]"
                DP1_Amp_12_Ana = Amp
                DP1_Amp_12_lim = TOLERANCIA_AMP

        # Analizamos el resultado para los 13,5v   
        if comando == "l2":
            limite_inf = 12.0
            Volt=Resultado[0]                   # la posición [0] corresponde al voltaje
            Amp=Resultado[1]                    # la posición [1] corresponde a la corriente
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP1_Volt_13_5 = "[ PASS ]"
                DP1_Volt_13_5_Vana = Volt
                DP1_Volt_13_5_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP1_Volt_13_5 = "[ FAIL ]"
                DP1_Volt_13_5_Vana = Volt
                DP1_Volt_13_5_lim = limite_inf
            
            if float(Amp) > 1.48:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP1_Amp_13_5 = "[ PASS ]"
                DP1_Amp_13_5_Ana = Amp
                DP1_Amp_13_5_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP1_Amp_13_5 = "[ FAIL ]"
                DP1_Amp_13_5_Ana = Amp
                DP1_Amp_13_5_lim = TOLERANCIA_AMP

        # Analizamos el resultado para los 15v
        if comando == "l3":
            limite_inf = 13.5
            Volt=Resultado[0]
            Amp=Resultado[1]
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP1_Volt_15 = "[ PASS ]"
                DP1_Volt_15_Vana = Volt
                DP1_Volt_15_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP1_Volt_15 = "[ FAIL ]"
                DP1_Volt_15_Vana = Volt
                DP1_Volt_15_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP1_Amp_15 = "[ PASS ]"
                DP1_Amp_15_Ana = Amp
                DP1_Amp_15_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP1_Amp_13_5 = "[ FAIL ]"
                DP1_Amp_15_Ana = Amp
                DP1_Amp_15_lim = TOLERANCIA_AMP
    
    print(f'Desconecta el cable de la BK del puerto DP1 y conectalo en el puerto DP2')
    hola = input('pulsa Enter para iniciar el test')   
   
    for comando in TDK_DP2:
        ser.write(comando.encode())
        #print(f"Ejecutando comando: {comando}")
        puerto = "DP2"
        Resultado = Parametriza_BK(BK)
        time.sleep(0.4)
        # Analizamos el resultado para los 12v
        if comando == "m1":
            limite_inf = 11.0
            Volt=Resultado[0]                   # la posición [0] corresponde al voltaje
            Amp=Resultado[1]                    # la posición [1] corresponde a la corriente
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP2_Volt_12 = "[ PASS ]"
                DP2_Volt_12_Vana = Volt
                DP2_Volt_12_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP2_Volt_12 = "[ FAIL ]"
                DP2_Volt_12_Vana = Volt
                DP2_Volt_12_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP2_Amp_12 = "[ PASS ]"
                DP2_Amp_12_Ana = Amp
                DP2_Amp_12_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP2_Amp_12 = "[ FAIL ]"
                DP2_Amp_12_Ana = Amp
                DP2_Amp_12_lim = TOLERANCIA_AMP
        
        # Analizamos el resultado para los 13,5v   
        if comando == "m2":
            limite_inf = 12.0
            Volt=Resultado[0]
            Amp=Resultado[1]
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP2_Volt_13_5 = "[ PASS ]"
                DP2_Volt_13_5_Vana = Volt
                DP2_Volt_13_5_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP2_Volt_13_5 = "[ FAIL ]"
                DP2_Volt_13_5_Vana = Volt
                DP2_Volt_13_5_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP2_Amp_13_5 = "[ PASS ]"
                DP2_Amp_13_5_Ana = Amp
                DP2_Amp_13_5_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP2_Amp_13_5 = "[ FAIL ]"
                DP2_Amp_13_5_Ana = Amp
                DP2_Amp_13_5_lim = TOLERANCIA_AMP

        # Analizamos el resultado para los 15v
        if comando == "m3":
            limite_inf = 13.5
            Volt=Resultado[0]
            Amp=Resultado[1]
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP2_Volt_15 = "[ PASS ]"
                DP2_Volt_15_Vana = Volt
                DP2_Volt_15_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP2_Volt_15 = "[ FAIL ]"
                DP2_Volt_15_Vana = Volt
                DP2_Volt_15_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP2_Amp_15 = "[ PASS ]"
                DP2_Amp_15_Ana = Amp
                DP2_Amp_15_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP2_Amp_15 = "[ FAIL ]"
                DP2_Amp_15_Ana = Amp
                DP2_Amp_15_lim = TOLERANCIA_AMP
        
    print(f'Desconecta el cable de la BK del puerto DP2 y conectalo en el puerto DP3')
    hola = input('pulsa Enter para iniciar el test')
   
    for comando in TDK_DP3:
        ser.write(comando.encode())
        #print(f"Ejecutando comando: {comando}")
        puerto = "DP3"
        Resultado = Parametriza_BK(BK)
        time.sleep(0.4)
        # Analizamos el resultado para los 12v
        if comando == "n1":
            limite_inf = 11.0
            Volt=Resultado[0]                   # la posición [0] corresponde al voltaje
            Amp=Resultado[1]                    # la posición [1] corresponde a la corriente
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP3_Volt_12 = "[ PASS ]"
                DP3_Volt_12_Vana = Volt
                DP3_Volt_12_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP3_Volt_12 = "[ FAIL ]"
                DP3_Volt_12_Vana = Volt
                DP3_Volt_12_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP3_Amp_12 = "[ PASS ]"
                DP3_Amp_12_Ana = Amp
                DP3_Amp_12_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP3_Amp_12 = "[ FAIL ]"
                DP3_Amp_12_Ana = Amp
                DP3_Amp_12_lim = TOLERANCIA_AMP
        
        # Analizamos el resultado para los 13,5v   
        if comando == "n2":
            limite_inf = 12.0
            Volt=Resultado[0]
            Amp=Resultado[1]
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP3_Volt_13_5 = "[ PASS ]"
                DP3_Volt_13_5_Vana = Volt
                DP3_Volt_13_5_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP3_Volt_13_5 = "[ FAIL ]"
                DP3_Volt_13_5_Vana = Volt
                DP3_Volt_13_5_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP3_Amp_13_5 = "[ PASS ]"
                DP3_Amp_13_5_Ana = Amp
                DP3_Amp_13_5_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP3_Amp_13_5 = "[ FAIL ]"
                DP3_Amp_13_5_Ana = Amp
                DP3_Amp_13_5_lim = TOLERANCIA_AMP

        # Analizamos el resultado para los 15v
        if comando == "n3":
            limite_inf = 13.5
            Volt=Resultado[0]
            Amp=Resultado[1]
            if float(Volt) > limite_inf:
                print(f'{Fore.YELLOW}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Voltaje --> PASS"}{Style.RESET_ALL}')
                DP3_Volt_15 = "[ PASS ]"
                DP3_Volt_15_Vana = Volt
                DP3_Volt_15_lim = limite_inf
            else:
                print(f'{Fore.RED}{"Voltaje -->  "+Volt+ " V"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Voltaje --> FAIL"}{Style.RESET_ALL}')
                DP3_Volt_15 = "[ FAIL ]"
                DP3_Volt_15_Vana = Volt
                DP3_Volt_15_lim = limite_inf
            
            if float(Amp) > TOLERANCIA_AMP:
                print(f'{Fore.YELLOW}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.GREEN}{"Test de Corriente --> PASS"}{Style.RESET_ALL}')
                DP3_Amp_15 = "[ PASS ]"
                DP3_Amp_15_Ana = Amp
                DP3_Amp_15_lim = TOLERANCIA_AMP
            else:
                print(f'{Fore.RED}{"Corriente -->  "+Amp+ " A"}{Style.RESET_ALL}')
                print(f'{Fore.RED}{"Test de Corriente --> FAIL"}{Style.RESET_ALL}')
                DP3_Amp_15 = "[ FAIL ]"
                DP3_Amp_15_Ana = Amp
                DP3_Amp_15_lim = TOLERANCIA_AMP
        
    print(f'Desconecta el cable de la BK del puerto DP3 el test ha finalizado')
 
    ser.close()


        
   
    # Cierra el puerto DP1
    cierre_DP =["G1", "G2", "G3"]
    ser = serial.Serial(FTDI, 115200)  
    ser.timeout = 1  # Tiempo de espera para la lectura en segundos
    for comando in cierre_DP:
        ser.write(comando.encode())
        time.sleep(0.7)
    ser.close()
    TDKS = [DP1_Volt_12,        # 0
            DP1_Volt_12_Vana,   # 1
            DP1_Volt_12_lim,    # 2
            DP1_Amp_12,         # 3
            DP1_Amp_12_Ana,     # 4
            DP1_Amp_12_lim,     # 5
            DP1_Volt_13_5,      # 6
            DP1_Volt_13_5_Vana, # 7
            DP1_Volt_13_5_lim,  # 8
            DP1_Amp_13_5,       # 9
            DP1_Amp_13_5_Ana,   # 10
            DP1_Amp_13_5_lim,   # 11
            DP1_Volt_15,        # 12
            DP1_Volt_15_Vana,   # 13
            DP1_Volt_15_lim,    # 14
            DP1_Amp_15,         # 15
            DP1_Amp_15_Ana,     # 16
            DP1_Amp_15_lim,     # 17
            DP2_Volt_12,        # 18
            DP2_Volt_12_Vana,   # 19
            DP2_Volt_12_lim,    # 20
            DP2_Amp_12,         # 21
            DP2_Amp_12_Ana,     # 22
            DP2_Amp_12_lim,     # 23
            DP2_Volt_13_5,      # 24
            DP2_Volt_13_5_Vana, # 25
            DP2_Volt_13_5_lim,  # 26
            DP2_Amp_13_5,       # 27
            DP2_Amp_13_5_Ana,   # 28
            DP2_Amp_13_5_lim,   # 29
            DP2_Volt_15,        # 30
            DP2_Volt_15_Vana,   # 31
            DP2_Volt_15_lim,    # 32
            DP2_Amp_15,         # 33
            DP2_Amp_15_Ana,     # 34
            DP2_Amp_15_lim,     # 35
            DP3_Volt_12,        # 36
            DP3_Volt_12_Vana,   # 37
            DP3_Volt_12_lim,    # 38
            DP3_Amp_12,         # 39
            DP3_Amp_12_Ana,     # 40
            DP3_Amp_12_lim,     # 41
            DP3_Volt_13_5,      # 42
            DP3_Volt_13_5_Vana, # 43
            DP3_Volt_13_5_lim,  # 44
            DP3_Amp_13_5,       # 45
            DP3_Amp_13_5_Ana,   # 46
            DP3_Amp_13_5_lim,   # 47
            DP3_Volt_15,        # 48
            DP3_Volt_15_Vana,   # 49
            DP3_Volt_15_lim,    # 50
            DP3_Amp_15,         # 51
            DP3_Amp_15_Ana,     # 52
            DP3_Amp_15_lim,     # 53
            Resultado[2],       # 54
            Resultado[3],       # 55
            ]
    #print(TDKS)
    crearFCT_pdf(N_serie,N_serie, TDKS)
    eMail_to('FCT_'+ N_serie)
    return TDKS

if __name__== "__main__":
    filename = input("Escanea el número de serie de la placa: ")
    leer_tdk(filename)