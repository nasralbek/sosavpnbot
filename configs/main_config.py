from configs.TOKENS import TELERAM_API_KEY
import os
from configs.xui_creditionals import *


TELERAM_API_KEY = TELERAM_API_KEY

db_filename = "../data/databases/db.sqlite3"
default_inbound = 9


os.environ["XUI_HOST"] = x_ui_host
os.environ["XUI_USERNAME"] = x_ui_username
os.environ["XUI_PASSWORD"] = x_ui_password
os.environ["TLS_CERT_PATH"] = "../data/certificates/fullchain.cer"