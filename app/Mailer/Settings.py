from fastapi import FastAPI
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, html):
    # Configuration de l'expéditeur, du destinataire et du contenu du message
    sender_email = "nguemazengmp@gmail.com"
    sender_password = "rrwbidotkxojnytn"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    # message.attach(MIMEText(body, "plain"))

    text_part = MIMEText(body, "plain")
    html_part = MIMEText(html, "html")
    message.attach(text_part)
    message.attach(html_part)

    # Connexion au serveur SMTP et envoi de l'e-mail
    with SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.send_message(message)
        