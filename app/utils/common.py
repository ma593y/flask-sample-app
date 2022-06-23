import os, jwt, secrets, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone



def generate_random_password():
    characters = "abcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+-.:;<=>?@[]^_{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_password = (''.join(secrets.choice(characters) for i in range(18)))
    return random_password



def email_password_to_user(user_email, user_password):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"User Account Created"
    message["From"] = os.getenv("EMAIL_ADDRESS")
    message["To"] = user_email
    
    text = f"""Hi, your account has been created.\n\nPlease use the following credentials to login,\n- User Email: {user_email}\n- User Pass: {user_password}"""
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    try:
        with smtplib.SMTP(os.getenv("MAIL_SERVER"), os.getenv("MAIL_PORT")) as server:
            try:
                server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
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



def generate_jwt_token(user_data):
    payload = user_data.copy()
    payload.update(
        {
            'exp': datetime.now(tz=timezone.utc) + timedelta(hours=3),
            'iat': datetime.now(tz=timezone.utc)
        }
    )

    token = jwt.encode(payload, os.getenv("RSA_PRIVATE_KEY"), algorithm="RS512")
    bearer_token = f"Bearer {token}"
    return bearer_token


