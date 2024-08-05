from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

# Mostramos el informe al finalizar el test
import webbrowser
import os
import datetime

directorio_pdf ='/home/carlos/Documentos/Thread/outputs/pdf/'
directorio_logo = '/home/carlos/Documentos/Thread/outputs/'

fecha_Informe = datetime.date.today()
fecha_Informe = fecha_Informe.strftime("%d/%m/%Y")

#Creamos el documento pdf
def crear_pdf(nombre, titulo,data_USB,data_232_DP1, data_232_DP2,data_232_DP3,
              mac,presion,temperatura,Fw,Version, Bateria):
    pdf = SimpleDocTemplate(directorio_pdf+nombre+".pdf", pagesize=A4)

    #Estilo de los párrafos
    styles = getSampleStyleSheet()
    style_normal= styles["Normal"]

    #Definimos propiedades de la pagina
    width, height = A4

    #Agregamos el logo de Ws
    logo_ruta= directorio_logo+"WS_Logo_3.png"
    logo_firma= directorio_logo+"Firma_1.png"

    img = Image(logo_ruta)
    img.drawHeight = 13*mm
    img.drawWidth= 50*mm

    #Agregamos la firma del informe
    img_firma= Image(logo_firma)
    img_firma.drawHeight = 15*mm
    img_firma.drawWidth = 60*mm

    #Agregamos texto
    titulo = titulo.upper()
    principal = "         Serial: " + titulo
    #tiempo = "El test ha durado "+ str(tiempo_test)+" segundos"
    Quality = "Quality Inspection"

    #Creamos la tabla del encabezado
    data_encabezado = [[img],
                       [principal]]
    tabla_encabezado = Table(data_encabezado)
    # Creamos el estilo de esta tabla de encabezado
    style_encabezado = TableStyle([('BACKGROUND',(0,0),(-1,-1), colors.white),
                                   ('TEXTCOLOR',(0,0),(-1,-1), colors.black),
                                   ('ALIGN', (0,0), (-1,-1),'LEFT'),
                                   ('BOTTOMPADDING', (0,0), (-1,0), 20),
                                   ('GRID',(0,0),(-1,-1),1, colors.white),])

    tabla_encabezado.setStyle(style_encabezado)

    #Creamos el párrafo con el texto
    #parrafo = Paragraph(principal, style_normal)
    parrafo_2 = Paragraph(Quality, style_normal)
    #parrafo_3 = Paragraph(tiempo, style_normal)

    #Generamos un espacio para separar el texto de la tabla
    espacio = Spacer(1,12)

    #Agregamos una tabla
    data = [["Check","Result"],
            ["Mac", mac],
            ["Firmware version", Fw],
            ["Version", Version],
            ["Battery Voltage", Bateria[0]],
            ["Battery Health", Bateria[1]],
            ["Pressure", presion],
            ["Temperature", temperatura],
            ["Check USB", data_USB],
            ["RS232_DP1", data_232_DP1],
            ["RS232_DP2", data_232_DP2],
            ["RS232_DP3", data_232_DP3]]
    tabla = Table(data)

    #Agregamos la tabla de controles visuales
    sd = "[ CHECK ]"
    interior = "[ CHECK ]"
    Torque_1 = "[ CHECK ]"
    etiqueta = "[ CHECK ]"
    exterior = "[ CHECK ]"
    power = "[ CHECK ]"
    power_label = "[ CHECK ]"
    plug_label = "[ CHECK ]"
    pack_label = "[ CHECK ]"
    pack_ext_label = "[ CHECK ]"
    power_cord = "[ CHECK ]"
    quick_label = "[ CHECK ]"

    visuales = [["SD correct placed",sd],
                ["Thread General Interior Visual Inspection",interior],
                ["Screw Torque Enclosure Check (14 x 1Nm)",Torque_1],
                ["Product Label", etiqueta],
                ["Thread General Exterior Visual Inspection", exterior],
                ["Power Supply finished", power],
                ["Power Supply Label", power_label],
                ["Plug Label", plug_label], 
                ["Packaging Labels", pack_label],
                ["Packaging General Exterior Visual Inspection", pack_ext_label],
                ["Power Cord", power_cord],
                ["Quickstart Guide", quick_label]]
    tabla_2= Table(visuales)

    #Estilo para la tabla
    style= TableStyle ([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),            #(0 --> columna, 0 --> fila) el -1 indica el final
        ('TEXTCOLOR',(0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (1,-1),'CENTER'),
        ('ALIGN', (0,1), (0,-1),'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('TEXTCOLOR',(1,1), (1,-1), colors.green),
        #('BACKGROUND', (0,1), (0,-1), colors.beige),
        ('GRID', (0,0), (-1,-1),1, colors.black),
    ])
    
    #Estilo para la tabla de inspecciones visuales
    style_2 = TableStyle ([   
        ('ALIGN', (1,0), (1,-1),'CENTER'),              #(0 --> columna, 0 --> fila) el -1 indica el final
        ('ALIGN', (0,0), (0,-1),'LEFT'),
        ('TEXTCOLOR',(1,0), (1,-1), colors.green),
        ('GRID', (0,0), (-1,-1),1, colors.black),
    ])

    #Aplicar el estilo a la tabla
    tabla.setStyle(style)
    tabla_2.setStyle(style_2)

    #Ajustar el tamaño de la tabla a mm
    tabla._argW[0]= 100*mm
    tabla_2._argW[0]= 100*mm
    tabla_encabezado._argW[0]= 180*mm

    #Ancho de la primera columna
    tabla._argW[1]= 30*mm
    tabla_2._argW[1]= 30*mm
    
    #Creamos la tabla de Global Results
    data_Result = [["Global Result:","PASS"],
                    ]
    
    tabla_Result = Table(data_Result)

    # Creamos el estilo de esta tabla de encabezado
    style_Result = TableStyle([('BACKGROUND',(0,0),(-1,-1), colors.white),
                                   ('TEXTCOLOR',(0,0),(0,0), colors.black),
                                   ('ALIGN', (0,0), (0,-1),'LEFT'),
                                   ('ALIGN', (0,0), (1,-1),'CENTER'),
                                   ('BOTTOMPADDING', (0,0), (-1,0), 20),
                                   ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                   ('TEXTCOLOR',(1,0), (1,-1), colors.green),
                                   ('GRID',(0,0),(-1,-1),1, colors.white),])
    tabla_Result.setStyle(style_Result)
    tabla_Result._argW[0] = 100*mm
    tabla_Result._argW[1] = 30*mm

    #Creamos la tabla de la firma
    data_firma = [[img_firma],
                       ["Operations director: Gustavo Closa"],
                       ["Quality Approved to Standard", fecha_Informe]]
    
    tabla_firma = Table(data_firma)

    # Creamos el estilo de esta tabla de encabezado
    style_firma = TableStyle([('BACKGROUND',(0,0),(-1,-1), colors.white),
                                   ('TEXTCOLOR',(0,0),(-1,-1), colors.black),
                                   ('ALIGN', (0,0), (-1,-1),'CENTER'),
                                   #('ALIGN', (0,1), (0,-1),'RIGHT'),
                                   ('ALIGN', (0,2), (0,-1),'LEFT'),
                                   ('FONTNAME', (0,2), (0,2), 'Helvetica-Bold'),
                                   ('ALIGN', (1,2), (1,-1),'RIGHT'),
                                   ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                                   ('GRID',(0,0),(-1,-1),1, colors.white),])
    tabla_firma.setStyle(style_firma)
    tabla_firma._argW[0] = 100*mm
    tabla_firma._argW[1] = 30*mm

    #Lista de elementos que contendrá el documento
    elements = [tabla_encabezado,espacio,tabla, espacio, parrafo_2, espacio, tabla_2, espacio,tabla_Result,espacio,tabla_firma,espacio]

    #Construimos el pdf
    pdf.build(elements)

    #Abrir el pdf
    webbrowser.open_new(directorio_pdf+nombre+'.pdf')

if __name__== "__main__":
    crear_pdf("Report_TEMPLATE")