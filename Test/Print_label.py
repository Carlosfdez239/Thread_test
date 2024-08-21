'''
30/07/2024
C. Fdez

Script para la impresión de las etiquetas tanto la FCT como la del EOL
Para generar la etiqueta se lanza generate_label.sh y se pasan como parámetros
    - El contenido del datamatrix
    - El contenido del texto
    - El formato de etiqueta que queremos crear
        - serial --> Formato de etiqueta del FCT (12mm x 26mm)
        - eol --> Formato de etiqueta del EOL (12mm x 15mm)

Para la impresión usaremos el comando lp -d y le pasamos dos parámetros
    - El primer parámetro indica el hostname de la impresora
    - El segundo parámetro indica el nombre de la etiqueta a imprimir
    Ejemplo: lp -d Brother_QL_820NWB 1223AB1_eol.png

'''
import subprocess
from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageDraw, ImageFont
import os

def Impr_label(data):
    print(os.environ)
    #data = '37C140'
    encoded = encode(data.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx.save(data+'.png')

    # Crear una imagen de etiqueta
    label_width= 150
    #label_height = 100
    label_height = 50
    label = Image.new("RGB",(label_width,label_height),"white")

    # Añadimos texto a la etiqueta
    draw = ImageDraw.Draw (label)
    font = ImageFont.load_default()
    #draw.text((20,150),data, font=font, fill='black')
    draw.text((20,50),data, font=font, fill='black')
    label.paste(dmtx,(50,50))
    label.save('etiqueta_3_'+data+'.png')

    etiqueta = 'etiqueta_3_'+data+'.png'

    #subprocess.run(["lp", "-d", "Brother_QL_820NWB",etiqueta])
    #subprocess.run(["/usr/bin/lp", etiqueta])
if __name__ == "__main__":
    Impr_label("37B41")