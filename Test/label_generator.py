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

Dimensiones de la etiqueta:

Convertiremos las dimensiones de milímetros a píxeles. Esto depende de la resolución de la imagen (puntos por pulgada o DPI). Normalmente, 300 DPI es un estándar para impresoras de alta calidad.
12 mm de altura se convierte en aproximadamente 142 píxeles (12 mm * 11.81 px/mm).
27 mm de longitud se convierte en aproximadamente 319 píxeles (27 mm * 11.81 px/mm).
Posicionamiento:

Situaremos el código Data Matrix a la izquierda y el texto a la derecha, asegurando que ambos se ajusten correctamente dentro del espacio disponible.
Fuente:

Utilizaremos una fuente adecuada y ajustaremos su tamaño para que encaje dentro del espacio disponible en la etiqueta.

'''
from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def Impr_label(data):
    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)
    label_width = int(40 * mm_to_px)  # 27 mm de longitud
    label_height = int(12 * mm_to_px)  # 12 mm de altura

    # Generar el código Data Matrix
    encoded = encode(data.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

    # Crear una imagen de etiqueta
    label = Image.new("RGB", (label_width+5, label_height+2), "white")

    # Colocamos el Data Matrix a la izquierda
    dmtx_position = (10, (label_height - dmtx.height) // 2)  # centrado verticalmente
    label.paste(dmtx, dmtx_position)

    # Añadir texto a la derecha del Data Matrix
    draw = ImageDraw.Draw(label)
    '''try:
        # Usa una fuente TTF en lugar de la fuente predeterminada
        font_size = 8  # Ajustar según sea necesario
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()'''
    try:
        # Usa la fuente DejaVu Sans con una altura de 10 píxeles
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Ruta en Linux, ajusta según tu SO
        font_size = 50  # Tamaño de la fuente
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("No se pudo cargar la fuente DejaVu Sans. Asegúrate de que la fuente esté instalada y la ruta sea correcta.")
        return

    # Calculamos la posición del texto
    text_position = (dmtx.width + 5, (label_height - font_size) // 2)
    draw.text(text_position, data, font=font, fill='black')

    etiqueta = 'etiqueta_3_' + data + '.png'
    label.save(etiqueta)

    # Para imprimir la etiqueta, descomenta la siguiente línea
    subprocess.run(["lp","-o","portait","-o","fit-to-page","-d", "Brother_QL_820NWB", etiqueta])
    #subprocess.run(["lp", "-d", "Brother_QL_820NWB", etiqueta])
    # subprocess.run(["/usr/bin/lp", etiqueta])

if __name__ == "__main__":
    Impr_label("37B41")
