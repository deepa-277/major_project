
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email.header import decode_header
import email
import re
from imaplib import IMAP4_SSL



class EmailClient:
    
    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.port = 465
        self.receiver_email = 'kan074bex010@kec.edu.np'
        self.client_email = 'kan074bex007@kec.edu.np'
        self.client_password = '9845617091'
        self.context = ssl.create_default_context()
        self.html = """
                        <html>
                            <body>
                                <b> Hello, mam </b>
                                <span>Some human detected outside!!</span>
                                <img src="data:detected_image/png;base64,{encoded_image}">
                            </body>
                        </html>
                    """
        self.address_pattern = re.compile('<(.*?)>')
    
    def sendemail(self, image):
        try:
            part = MIMEText(self.html, "html")
            message = MIMEMultipart()
            message["subject"] = Header("Human Detection", 'utf-8').encode()
            message["From"] = self.client_email
            message["To"] = self.receiver_email
            message.attach(part)
            with open('./detected_image.png', 'rb') as image:
                mime_image = MIMEBase('image', 'png', filename='detected_image.png')
                mime_image.add_header('Content-Decomposition', 'attatchment', filename='detected_image.png')
                mime_image.add_header('X-Attachment-Id', '0')
                mime_image.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
                mime_image.set_payload(image.read())
                # encode with base64
                encoders.encode_base64(mime_image)
                # add MIMEBase object to MIMEMultipart object
                message.attach(mime_image)
            print('Sending email...')
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.client_email, self.client_password)
                print("logged into the email")
                server.sendmail(self.client_email, self.receiver_email, message.as_string())
                return True
        except smtplib.SMTPException as se:
            return False

    def retriveemail(self):
        with IMAP4_SSL(self.smtp_server) as imap:
            print('Authenticating...!')
            imap.login(self.client_email, self.client_password)
            print('Authentication grated!')
            status, number_of_emails = imap.select('INBOX')
            res, msg = imap.fetch(str(int(number_of_emails[0])), 'RFC822')
            for response in msg:
                if isinstance(response, tuple):
                    message = email.message_from_bytes(response[1])
                    frm, encoding = decode_header(message['From'])[0]
                    if isinstance(frm, bytes):
                        frm = frm.decode(encoding=encoding)
                    from_address = self.address_pattern.findall(frm)[0]
                    subject, encoding = decode_header(message['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding=encoding)
                    print("Subject: ", subject)
                    print('\n')
                    if from_address == self.receiver_email and subject == 'Open the door':
                        print('From=>', from_address)
                        print('\n')
                        print('Subject=> ', subject)
                        return True
                    else:
                        print('From=> ', from_address)
                        print('\n')
                        print('Subject=> ', subject)
                        print('Unauthorized email.')
                        return False
    


