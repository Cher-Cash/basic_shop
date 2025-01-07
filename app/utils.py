import hashlib
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()


def generate_signature(order_id, company_id, secret_key):
    sigma = f"{order_id}{company_id}{secret_key}"
    hash_object = hashlib.sha256(sigma.encode())
    signature = hash_object.hexdigest()
    return signature


def send_email(order):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = order.email
    subject = f"Номер вашего заказа: {order.id}"
    body = f"Здравствуйте, Благодарим за заказ на нашем сайте \n во вложении находится приобретенный вами товар"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
