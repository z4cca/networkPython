## Import necessary libraries

import smtplib

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Configure smtp server (I'm using outlook mailing server, it uses port 587)
server = smtplib.SMTP('smtp-mail.outlook.com', 587)

# Start service
server.ehlo()

## Note to future: implement input variables to automate Server, Sender and Receiver

# Account login
# Read encrypted file with mail password (located inside scripts directory)
with open('password.txt', 'r') as p:
    password = p.read()
# Login
server.login('mail@outlook.com', password)


## Create mail message
# Set mail Sender and Receiver config
msg = MIMEMultipart()
msg['From'] = 'Name <mail@outlook.com>'
msg['To'] = 'Name <mail@mail.com>'
msg['Subject'] = 'Subject'

# Read text file with message (located inside scripts directory)
with open('message.txt', 'r') as m:
    message = m.read()
# Attach plain text message into mails body 
msg.attach(MIMEText(message, 'plain'))


## Attachments
# Creates attachment object and read image file in 'Read Bytes' mode (located inside scripts directory)
imgfile = 'image.jpg'
attachment = open(imgfile, 'rb') 
# Creates attachment payload object
p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())
# Encode image data into payload and finally attach into the message
encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={imgfile}')
msg.attach(p)

# Set sendmail configurations
body = msg.as_string()
server.sendmail('mail@outlook.com', 'mail@mail.com', body)