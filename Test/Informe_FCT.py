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
#def crearFCT_pdf(nombre, titulo,data_USB,data_232_DP1, data_232_DP2,data_232_DP3,
#              mac,presion,temperatura,Fw,Version, Bateria,TDKS):
def crearFCT_pdf(nombre, titulo,TDKS):
    nombre = 'FCT_'+ nombre
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
    principal = "         Serial: " + titulo + "\n"+"         fecha: "+fecha_Informe
    #tiempo = "El test ha durado "+ str(tiempo_test)+" segundos"
    Quality = "FCT Quality Inspection Report"
    Instrumento = TDKS[54]
    Vers_instrumento = TDKS[55]
    Quality = Quality + "\n" + "Test realizado con : "+ Instrumento + " version:  " + Vers_instrumento

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
    data = [["Check","Espec","Min","Result"],
            #["Mac", "","",mac],
            #["Firmware version", "","",Fw],
            #["Version", "","",Version],
            #["Battery Voltage", Bateria[0]],
            #["Battery Health", Bateria[1]],
            #["Pressure", presion],
            #["Temperature", temperatura],
            #["Check USB", data_USB],
            #["RS232_DP1", data_232_DP1],
            #["RS232_DP2", data_232_DP2],
            #["RS232_DP3", data_232_DP3],
            ["Voltaje TDK_DP1","12v",TDKS[2], TDKS[1]],
            ["Corriente TDK_DP1","1.50 A", TDKS[5], TDKS[4]],
            ["Voltaje TDK_DP1","13.5v", TDKS[8], TDKS[7]],
            ["Corriente TDK_DP1","1.50 A", TDKS[11], TDKS[10]],
            ["Voltaje TDK_DP1", "15v",TDKS[14],TDKS[13]],
            ["Corriente TDK_DP1","1.50 A", TDKS[17], TDKS[16]],
            ["Voltaje TDK_DP2", "12v", TDKS[20], TDKS[19]],
            ["Corriente TDK_DP2", "1.50 A", TDKS[23], TDKS[22]],
            ["Voltaje TDK_DP2", "13.5v", TDKS[26], TDKS[25]],
            ["Corriente TDK_DP2", "1.50 A", TDKS[29], TDKS[28]],
            ["Voltaje TDK_DP2", "15v", TDKS[32], TDKS[31]],
            ["Corriente TDK_DP2", "1.50A", TDKS[35], TDKS[34]],
            ["Voltaje TDK_DP3", "12v", TDKS[38], TDKS[37]],
            ["Corriente TDK_DP3", "1.50A", TDKS[41], TDKS[40]],
            ["Voltaje TDK_DP3", "13.5v", TDKS[44], TDKS[43]],
            ["Corriente TDK_DP3", "1.50A", TDKS[47], TDKS[46]],
            ["Voltaje TDK_DP3", "15v", TDKS[50], TDKS[49]],
            ["Corriente TDK_DP3", "1.50A", TDKS[53], TDKS[52]],
            ]
    tabla = Table(data)

    #Estilo para la tabla
    style= TableStyle ([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),            #(0 --> columna, 0 --> fila) el -1 indica el final
        ('TEXTCOLOR',(0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (1,-1),'CENTER'),
        ('ALIGN', (0,1), (-1,-1),'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        #('TEXTCOLOR',(1,1), (1,-1), colors.green),
        #('BACKGROUND', (0,1), (0,-1), colors.beige),
        ('GRID', (0,0), (-1,-1),1, colors.black),
    ])
    
    

    #Aplicar el estilo a la tabla
    tabla.setStyle(style)
    

    #Ajustar el tamaño de la tabla a mm
    tabla._argW[0]= 80*mm
   
    tabla_encabezado._argW[0]= 180*mm

    #Ancho de la primera columna
    tabla._argW[1]= 30*mm
    tabla._argW[2]= 30*mm
    tabla._argW[3]= 30*mm 
    #Lista de elementos que contendrá el documento
    elements = [tabla_encabezado,
                espacio,
                tabla, 
                espacio, 
                parrafo_2, 
                espacio ]
    
    #Construimos el pdf
    pdf.build(elements)

    #Abrir el pdf
    webbrowser.open_new(directorio_pdf+nombre+'.pdf')

if __name__== "__main__":
    crearFCT_pdf("Report_TEMPLATE",
                 "Report_Template",
                 ["DP1_Volt_12",        # 0
                 "11.32",   # 1
                "11.0",    # 2
                "DP1_Amp_12",         # 3
                "1.498",     # 4
                "1.48",     # 5
                "DP1_Volt_13_5",      # 6
                "12.5", # 7
                "12",  # 8
                "DP1_Amp_13_5",       # 9
                "1.4987",   # 10
                "1.48",   # 11
                "DP1_Volt_15",        # 12
                "14.5",   # 13
                "14",    # 14
                "DP1_Amp_15",         # 15
                "1.4988",     # 16
                "1.48",     # 17
                "DP2_Volt_12",        # 18
                "11.5",   # 19
                "11",    # 20
                "DP2_Amp_12",         # 21
                "1.4976",     # 22
                "1.48",     # 23
                "DP2_Volt_13_5",      # 24
                "12.87", # 25
                "12.0",  # 26
                "DP2_Amp_13_5",       # 27
                "1.4976",   # 28
                "1.48",   # 29
                "DP2_Volt_15",        # 30
                "14.78",   # 31
                "14.5",    # 32
                "DP2_Amp_15",         # 33
                "1.4954",     # 34
                "1.48",     # 35
                "DP3_Volt_12",        # 36
                "11.5",   # 37
                "11.0",    # 38
                "DP3_Amp_12",         # 39
                "1.4976",     # 40
                "1.48",     # 41
                "DP3_Volt_13_5",      # 42
                "12.587", # 43
                "12.5",  # 44
                "DP3_Amp_13_5",       # 45
                "1.4987",   # 46
                "1.48",   # 47
                "DP3_Volt_15",        # 48
                "14.78",   # 49
                "14.0",    # 50
                "DP3_Amp_15",         # 51
                "1.4987",     # 52
                "1.48",     # 53
                "BK Precision 8600",       # 54
                "ver 3.87",       # 55
                 ]
                 
                 
                 )