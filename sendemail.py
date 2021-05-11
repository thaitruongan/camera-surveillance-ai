import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

def send_email(subject, body,filename,to):
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['to'] = to

    user = "camera.surveillance.ai@gmail.com"
    msg['from'] = user
    password = "wsknesnxguxmnbnd"

    msg.attach(MIMEText(body,'plain'))

    attachment = open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    msg.attach(part)
 
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)    
    server.quit()
