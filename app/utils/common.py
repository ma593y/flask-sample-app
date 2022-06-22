import string, secrets, smtplib, ssl, os, jwt, json
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def generate_random_password():
    # characters = string.ascii_lowercase + string.digits + string.punctuation + string.ascii_uppercase
    characters = "abcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+-.:;<=>?@[]^_{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_password = (''.join(secrets.choice(characters) for i in range(18)))

    return random_password


# 