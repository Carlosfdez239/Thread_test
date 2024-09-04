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
from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus import Image as reportlab_Img
from reportlab.lib.styles import getSampleStyleSheet

IMPRESORA = "Brother_12"
DIRECTORIO_LOGO = '/home/carlos/Documentos/Thread/outputs/'


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
    
    #Agregamos los imagotipos y el logo de Ws
    logo_ruta = DIRECTORIO_LOGO+"WS_Logo_3.png"
    imagotipo_ruta = DIRECTORIO_LOGO+"imagotipos_nodos.png"

    #Estilo de los párrafos
    styles = getSampleStyleSheet()
    style_normal= styles["Normal"]

    #Agregamos texto
    Model = Model
    ERP_Code = ERP_Code
    Serial_N = Serial_N

    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)

    # Dimensionamos la etiqueta
    label_width = int(50 * mm_to_px)  # 50 mm de longitud
    label_height = int(36 * mm_to_px)  # 36 mm de altura

    # Creamos el lienzo de la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")

    # Definimos dimensiones del logo
    img = reportlab_Img(logo_ruta)
    img.drawHeight = 13*mm
    img.drawWidth= 30*mm

    # Generar el código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('L', (encoded.width, encoded.height), encoded.pixels)

    # Creamos la tabla del encabezado
    data_encabezado = [[img,dmtx]]
    
    # Declaramos la tabla y su estilo
    tabla_encabezado = Table(data_encabezado)
    style_encabezado = TableStyle([('BACKGROUND',(0,0),(-1,-1), colors.white),
                                   ('TEXTCOLOR',(0,0),(-1,-1), colors.black),
                                   ('ALIGN', (0,0), (-1,-1),'LEFT'),
                                   ('BOTTOMPADDING', (0,0), (-1,0), 10),
                                   ('GRID',(0,0),(-1,-1),1, colors.white),])

    tabla_encabezado.setStyle(style_encabezado)

    # Agregamos una tabla para los contenidos del texto y definimos su estilo
    data = [["Model:",Model],
            ["ERP Code:", ERP_Code],
            ["Serial Nb:", Serial_N]]
    tabla = Table(data)
    style= TableStyle ([
        ('BACKGROUND',(0,0),(-1,-1),colors.white),            #(0 --> columna, 0 --> fila) el -1 indica el final
        ('TEXTCOLOR',(0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1),'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'NotoSansDisplay-Regular'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),  
        ('GRID', (0,0), (-1,-1),1, colors.white)])
    tabla.setStyle(style)

    # Generamos un espacio para separar el texto de la tabla
    espacio = Spacer(1,12) 

    # Insertamos la imagen de los imagotipos
    img2 = reportlab_Img(imagotipo_ruta)
    img2.drawHeight = 10*mm
    img2.drawWidth= 30*mm   

    # Agregamos la tabla para los iconos
    data_ima = [["",img2]]
    tabla_ima = Table(data_ima)
    tabla_ima.setStyle(style)

    # Ancho de la primera columna de las tablas en mm
   
    tabla_encabezado._argW[0]= 35*mm
    tabla._argW[0]= 20*mm
    tabla_ima._argW[0]= 20*mm

    # Ancho de la segunda columna de las tablas en mm
    tabla_encabezado._argW[1]= 15*mm
    tabla._argW[1]= 30*mm
    tabla_ima._argW[1]= 30*mm


    # Lista de elementos que contendrá el documento
    elements = [tabla_encabezado,espacio,tabla, espacio, tabla_ima]

    contenido = datam.split(";")
    ETIQUETA = 'etiqueta_4_' + contenido[-1] + '.png'

    # Grabamos la etiqueta    
    label.save(ETIQUETA)

    # Mostramos en pantalla la etiqueta
    label.show(ETIQUETA)

    # Mandamos a impresión la etiqueta
    subprocess.run(["lp","-o","portait","-d", IMPRESORA, ETIQUETA])



if __name__ == "__main__":
    #Impr_FCT_label("107102-2;102307;307B41")
    #Impr_EOL_label("107102-2;102307;307B41")
    Impr_Node_packaging_label("LSG6TIL90X;2024080200167;150323","LS-G6_TIL90X", "LSG6TIL90X","150323")
