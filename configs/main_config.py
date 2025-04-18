from configs.TOKENS import TELERAM_API_KEY
import os
from configs.xui_creditionals import *
from configs.pgconfig import *


TELERAM_API_KEY = TELERAM_API_KEY

db_filename = "../data/databases/db.sqlite3"
default_inbound = 9


os.environ["XUI_HOST"] = x_ui_host
os.environ["XUI_USERNAME"] = x_ui_username
os.environ["XUI_PASSWORD"] = x_ui_password
os.environ["TLS_CERT_PATH"] = "../data/certificates/fullchain.cer"

os.environ["PG_DATABASE"] = PG_DB_NAME
os.environ["PG_USER"] = PG_USERNAME
os.environ["PG_PASSWORD"] = PG_PASSWORD
os.environ["PG_HOST"] = PG_HOST
os.environ["PG_PORT"] = PG_PORT


class PG_CONFIG:
    PG_DB_NAME = PG_DB_NAME
    PG_USERNAME = PG_USERNAME
    PG_PASSWORD = PG_PASSWORD
    PG_HOST = PG_HOST
    PG_PORT = PG_PORT
