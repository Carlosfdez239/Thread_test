# necesario importar nmap --> sudo apt install python3-nmap
# si queremos que no nos pida la contraseña de sudo -->
#   editar el archivo etc/sudoers
#   sudo visudo --> incluir esta linea miusuario ALL=(ALL) NOPASSWD: /usr/bin/nmap
#   atención cambiar miusuario por el usuario del equipo que se está usando

import subprocess

def listar_lineas(comando, condicion):
    lineas_anteriores=[]
    proceso = subprocess.Popen(comando,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    for linea in proceso.stdout:
        if condicion in linea:
            print("Se ha encontrado el Thread en: ")
            for linea_anterior in lineas_anteriores:
                direccion = linea_anterior[-14:].split(')')
                #print (direccion[0])
                return direccion[0]
                #return direccion
                #break
        lineas_anteriores.append(linea)
        if len(lineas_anteriores)>2:
            lineas_anteriores.pop(0)
