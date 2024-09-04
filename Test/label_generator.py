'''
29/08/2024
C. Fdez
v1.0

Script para la impresión de las etiquetas Para generar la etiqueta
se pasa un único parámetro que tiene los tres campos necesarios separados por ";"
los campos son referencia del artículo, Número de lote, Número de serie del artículo

El formato de la etiqueta se define en el método llamado:
    Impr_FCT_label(data) --> Etiqueta necesaria tras el test FCT de la placa.
        La etiqueta tiene unas dimensiones de 12 mm de altura y 32 mm de longitud
        Situa un datamatrix centrado en el ancho de la etiqueta
        separa un texto a 10 px del datamatrix

            - El contenido del datamatrix --> 
             [ref del articulo;Número de lote;Número de serie]
            - El contenido del texto imprimible se extrae del último parámetro -->
                Número de Serie
    
    Impr_EOL_label(data) --> Formato de etiqueta del EOL 
        La etiqueta tiene unas dimensiones de 12 mm de altura y 15 mm de longitud
        Situa un datamatrix centrado en el ancho de la etiqueta
        ubica un texto bajo el datamatrix

            - El contenido del datamatrix --> 
             [ref del articulo;Número de lote;Número de serie]
            - El contenido del texto imprimible se extrae del último parámetro -->
                Número de Serie

Para la impresión usaremos el comando lp -d lanzado desde subprocess.run y le pasamos como parámetros
    -o portait para asegurarnos que la impresión se realiza en el sentido de alimentación de la cinta
    -d "nombre de la impresora "
    archivo que queremos imprimir (tener en cuenta que debe indicar la ruta completa y la extensión del archivo)

    Ejemplo: subprocess.run(["lp","-o","portait","-d", "Brother_12", etiqueta])

Importante
Dimensiones de la etiqueta:

Convertiremos las dimensiones de milímetros a píxeles. Esto depende de la resolución de la imagen (puntos por pulgada o DPI). Normalmente, 300 DPI es un estándar para impresoras de alta calidad.
12 mm de altura se convierte en aproximadamente 142 píxeles (12 mm * 11.81 px/mm).
27 mm de longitud se convierte en aproximadamente 319 píxeles (27 mm * 11.81 px/mm).


To Do:
    [] pasar como parámetro la impresora --> 
    [] Crear métodos para resto de etiquetas
        [] Producto nodos
        [] Packaging nodos
            [] Customizaciones
        [] Producto Thread
            [] Customizaciones
        [] Packaging Thread
            [] Accesorios
            [] Cables


'''
from ast import Mod
from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

IMPRESORA = "Brother_12"
DIRECTORIO_LOGO = '/home/carlos/Documentos/Thread/outputs/'
font_size = 30  # Reduce o aumenta el tamaño según sea necesario
font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
font = ImageFont.truetype(font_path, font_size)


def Impr_FCT_label(data):
    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)
    label_width = int(32 * mm_to_px)  # 27 mm de longitud
    label_height = int(12 * mm_to_px)  # 12 mm de altura
    

    # Generar el código Data Matrix
    encoded = encode(data.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

    # Crear una imagen de etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")

    # Colocamos el Data Matrix a la izquierda
    dmtx_position = (0, (label_height - dmtx.height) // 2)  # centrado verticalmente
    label.paste(dmtx, dmtx_position)

    # Añadir texto a la derecha del Data Matrix
    draw = ImageDraw.Draw(label)

    try:
        # Usa la fuente DejaVu Sans con una altura de 10 píxeles
        font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"  # Ruta en Linux, ajusta según tu SO
        font_size = 70  # Tamaño de la fuente
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("No se pudo cargar la fuente DejaVu Sans. Asegúrate de que la fuente esté instalada y la ruta sea correcta.")
        return

    # Calculamos la posición del texto
    text_position = (dmtx.width + 10, (label_height - font_size) // 2)
    draw.text(text_position, data.split(";")[-1], font=font, fill='black')

    etiqueta = 'etiqueta_3_' + data + '.png'
    label.save(etiqueta)

    subprocess.run(["lp","-o","portait","-d", "Brother_12", etiqueta])


def Impr_EOL_label(data):
    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)
    label_width = int(15 * mm_to_px)  # 27 mm de longitud
    label_height = int(12 * mm_to_px)  # 12 mm de altura
    

    # Generar el código Data Matrix
    encoded = encode(data.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

    # Crear una imagen de etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")

    # Colocamos el Data Matrix a la izquierda
    #dmtx_position = (0, (label_height - dmtx.height) // 2)  # centrado verticalmente
    dmtx_position = ((label_width - dmtx.width) // 2, 0)
    label.paste(dmtx, dmtx_position)

    # extracción de la última posición para imprimir el texto
    text_to_print = data.split(";")[-1]

    # Añadir texto a la derecha del Data Matrix
    draw = ImageDraw.Draw(label)

    try:
        # Usa la fuente DejaVu Sans con una altura de 10 píxeles
        font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"  # Ruta en Linux, ajusta según tu SO
        font_size = 25  # Tamaño de la fuente
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("No se pudo cargar la fuente DejaVu Sans. Asegúrate de que la fuente esté instalada y la ruta sea correcta.")
        return

    # Calculamos la posición del texto centrado horizontalmente
    bbox = draw.textbbox((0, 0), text_to_print, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position_x = (label_width - text_width) // 2
    text_position_y = dmtx.height + 2  # Ajustamos 5 píxeles de espacio entre el Data Matrix y el texto

    draw.text((text_position_x, text_position_y), text_to_print, font=font, fill='black')

    etiqueta = 'etiqueta_3_'+ text_to_print + '.png'
    label.save(etiqueta)

    subprocess.run(["lp","-o","portait","-d", "Brother_12", etiqueta])


def Impr_Node_packaging_label(datam,Model,ERP_Code,Serial_N):

    font_size = 25  # Reduce o aumenta el tamaño según sea necesario
    font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    #Agregamos los imagotipos y el logo de Ws
    logo_ruta = DIRECTORIO_LOGO+"logo.png"
    #imagotipo_ruta = DIRECTORIO_LOGO+"imagotipos_nodos.png"


    #Agregamos texto
    Model = Model
    ERP_Code = ERP_Code
    Serial_N = Serial_N

    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)

    # Dimensionamos la etiqueta
    label_width = int(36 * mm_to_px)  # 50 mm de longitud
    label_height = int(50 * mm_to_px)  # 36 mm de altura

    # Creamos el lienzo de la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    # Cargar e insertar la imagen .png en la etiqueta
    image_path = DIRECTORIO_LOGO+"iconos.png"
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(18 * mm_to_px), int(13 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (label_width - insert_image.width, int(16* mm_to_px)))  # Posición en la esquina superior derecha

    # Cargar e insertar el logo de Worldsensing
    image_path = logo_ruta
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(29 * mm_to_px), int(9 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (0, 0))  # Posición en la esquina superior izda

    draw = ImageDraw.Draw(label)
    draw.text((2* mm_to_px, 9* mm_to_px), "Model: " + Model, font=font, fill='black')
    draw.text((2* mm_to_px, 12* mm_to_px), "ERP_Code: " + ERP_Code, font=font, fill='black')
    draw.text((2* mm_to_px, 15* mm_to_px), "Serial_Nb: " + Serial_N, font=font, fill='black')

    # Generar el código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx.save("dmtx_debug.png")
    label.paste(dmtx,(label_width-encoded.width,int(8*mm_to_px)))
    #dmtx.show()

    label.save("output_test.png")
    #label.show()

    contenido = datam.split(";")
    ETIQUETA = 'etiqueta_4_' + contenido[-1] + '.png'

    # Grabamos la etiqueta    
    label.save(ETIQUETA)

    # Mostramos en pantalla la etiqueta
    #label.show()

    # Mandamos a impresión la etiqueta
    subprocess.run(["lp","-o","portait","-d", IMPRESORA, ETIQUETA])


def Impr_Israel_label(PartName):

    font_size = 35 # Reduce o aumenta el tamaño según sea necesario
    font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    #Agregamos los imagotipos y el logo de Ws
    logo_ruta = DIRECTORIO_LOGO+"logo.png"
    #imagotipo_ruta = DIRECTORIO_LOGO+"imagotipos_nodos.png"


    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)

    # Dimensionamos la etiqueta
    label_width = int(30 * mm_to_px)  # 30 mm de longitud
    label_height = int(50 * mm_to_px)  # 50 mm de altura

    # Creamos el lienzo de la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    draw = ImageDraw.Draw(label)
    # Dibujar un marco alrededor de la etiqueta
    marco_color = "grey"  # Color del marco
    marco_grosor = 1  # Grosor del marco en píxeles
    draw.rectangle([(marco_grosor+5)//2, 
                    (marco_grosor+5)//2, 
                    label_height-(marco_grosor+35)//2, 
                    label_width-(marco_grosor+15)//2], 
                   outline=marco_color, 
                   width=marco_grosor)


    #draw.rectangle(0,0,label_width,label_height, fill='white', outline=None ,width=1)
    draw.text((2* mm_to_px, 9* mm_to_px), "For ISRAEL market", font=font, fill='black')
    draw.text((2* mm_to_px, 12* mm_to_px), PartName.upper(), font=font, fill='black')


    ETIQUETA = 'Israel' + '.png'

    # Grabamos la etiqueta    
    label.save(ETIQUETA)

    # Mostramos en pantalla la etiqueta
    #label.show()

    # Mandamos a impresión la etiqueta
    subprocess.run(["lp","-o","portait","-d", IMPRESORA, ETIQUETA])



if __name__ == "__main__":
    #Impr_FCT_label("107102-2;102307;307B41")
    #Impr_EOL_label("107102-2;102307;307B41")
    #Impr_Node_packaging_label("LSG6TIL90X;2024080200167;150323","LS-G6_TIL90X", "LSG6TIL90X","150323")
    Impr_Israel_label("LS-G6-TIL90-X-IL")