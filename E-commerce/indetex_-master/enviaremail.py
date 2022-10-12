from email.message import EmailMessage
import smtplib
import x

def enviar_email(email_destino,codigo):
    remitente = "correo@uninorte.edu.co"
    destinatario = email_destino
    mensaje = "Codigo de Activacion: "+codigo
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Codigo de Activacion"
    email.set_content(mensaje, subtype="html")
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, 'password')
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()



