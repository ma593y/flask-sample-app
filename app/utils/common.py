import string, secrets, smtplib, ssl, os, jwt, json
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def generate_random_password():
    # characters = string.ascii_lowercase + string.digits + string.punctuation + string.ascii_uppercase
    characters = "abcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+-.:;<=>?@[]^_{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_password = (''.join(secrets.choice(characters) for i in range(18)))

    return random_password



def email_password_to_user(user_email, user_password):
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RECEIVER_EMAIL = user_email

    message = MIMEMultipart("alternative")
    message["Subject"] = f"User Account Created"
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECEIVER_EMAIL
    
    text = f"""Hi, your account has been created.\n\nPlease use the following credentials to login,\n- User Email: {user_email}\n- User Pass: {user_password}"""
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            try:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                try:
                    server.sendmail(message["From"], message["To"], message.as_string())
                except Exception as e:
                    print('- - - - - - - - - - - - - - - - - - - - ')
                    print(f'Exception : {e}')
                    print("[!] Error sending email.")
                    print('- - - - - - - - - - - - - - - - - - - - ')
            except Exception as e:
                print('- - - - - - - - - - - - - - - - - - - - ')
                print(f'Exception : {e}')
                print("[!] Error authenticating SMTP sever.")
                print('- - - - - - - - - - - - - - - - - - - - ')
    except Exception as e:
        print('- - - - - - - - - - - - - - - - - - - - ')
        print(f'Exception : {e}')
        print("[!] Error connecting SMTP sever.")
        print('- - - - - - - - - - - - - - - - - - - - ')



# 