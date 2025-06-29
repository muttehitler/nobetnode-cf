from decouple import config
from dotenv import load_dotenv

load_dotenv()

SERVICE_ADDRESS = config("SERVICE_ADDRESS", default="0.0.0.0")
SERVICE_PORT = config("SERVICE_PORT", cast=int, default=51032)
INSECURE = config("INSECURE", cast=bool, default=False)

CF_TOKEN = config("CF_TOKEN")

UNBAN_ALL_IN_STARTUP = config("UNBAN_ALL_IN_STARTUP", cast=bool, default=False)

SSL_CERT_FILE = config("SSL_CERT_FILE", default="./ssl_cert.pem")
SSL_KEY_FILE = config("SSL_KEY_FILE", default="./ssl_key.pem")
SSL_CLIENT_CERT_FILE = config("SSL_CLIENT_CERT_FILE", default="")

DEBUG = config("DEBUG", cast=bool, default=False)
