import os

os.system("rm -rf keys/")
os.system("mkdir -p keys")
os.system("ssh-keygen -t rsa -b 4096 -E SHA512 -m PEM -P '' -f ./keys/RS512.key")
os.system("openssl rsa -in ./keys/RS512.key -pubout -outform PEM -out ./keys/RS512.key.pub")

RSA_PRIVATE_KEY = str(open("./keys/RS512.key", "rb").read())[1:]
RSA_PUBLIC_KEY = str(open("./keys/RS512.key.pub", "rb").read())[1:]

ENV_FILE = open("../.env", "w")
ENV_FILE.write(f"""HOST = '0.0.0.0'
PORT = 5000

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'app_db'
DB_USERNAME = 'db_user'
DB_PASSWORD = 'db_pass'
DB_ROOT_PASSWORD = 'root_pass'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB_SESSION = 0
REDIS_PASSWORD = 'redis_pass'

MAIL_SERVER = 'smtp-relay.domain.com'
MAIL_PORT = 587
EMAIL_ADDRESS = 'email@domain.com'
EMAIL_PASSWORD = 'password'

RSA_PRIVATE_KEY = {RSA_PRIVATE_KEY}
RSA_PUBLIC_KEY = {RSA_PUBLIC_KEY}
""")

os.system("rm -rf keys/")