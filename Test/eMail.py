'''
C. Fdez
23/08/2024

Construimos un correo electrónico con los datos resultados

# TO DO:
#   23/08/2024   
#               Implementar 
#               [x] --> Parámetros de entrada para email sender
#               [x] --> Parámetros para destinatario
#               [x] --> Respuesta principal
#               [x] --> Datos adjuntos
#              

'''
from json import encoder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Configuración del servidor y credenciales
smtp_server = "smtp.mail.yahoo.com"
smtp_port = 465
sender_email = "carlosfdez239@yahoo.es"
password = 'iehmyzhxueesgmij'

# Destinatario
reciver_email = ["cfernandez@worldsensing.com","carlos.fernandez239@gmail.com"]

def eMail_to(filename):
    filename = filename + ".pdf"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ",".join (reciver_email)
    msg['Subject'] = "Resultados test Thread"

    # Cuerpo del correo
    body = "Adjunto los resultados del test"
    msg.attach(MIMEText(body,'plain'))

    # Adjuntar archivo
    
    with open (filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename={filename}',)
        msg.attach(part)
    
    # Conexión al servidor y envío del correo
    try:
        print('Conectando con Yahoo ...')
        #server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        server = smtplib.SMTP(smtp_server, 587)
        #server.set_debuglevel(1)
        server.starttls()
        server.login(sender_email, password)
        print('Enviando el correo ...')
        text = msg.as_string()
        server.sendmail(sender_email, reciver_email,text)
        print ('Correo enviado correctamente')
    except Exception as e:
        print (f'Error al enviar el correo: {e}')
    finally:
        server.quit()

if __name__ == "__main__":
    eMail_to(filename = 'ECC0B3.pdf')




