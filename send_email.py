from email.mime.text import MIMEText
import smtplib
from config import *


def send_email(content, subject, receiver_email, cc_email=None, sender_email = 'sabahraporu@skoda.com.tr'):
    sender_email = sender_email
    password = mailPassword

    message = MIMEText(content, "html")

    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    if cc_email:
        message["Cc"] = cc_email

    recipients = [receiver_email]
    if cc_email:
        recipients.append(cc_email)

    server = smtplib.SMTP("mail.yuceauto.com.tr",)
    server.starttls()
    #server.login(sender_email, password)
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()
