from tools.get_os_attr import get_os_attr
from dotenv import load_dotenv
from enum import Enum

load_dotenv(override=False)

TELERAM_API_KEY = get_os_attr("BOT_TELEGRAM_TOKEN")

#deprecated
db_filename = "../data/databases/db.sqlite3"


#3x-ui
XUI_HOST            = get_os_attr("XUI_HOST")
XUI_USERNAME        = get_os_attr("XUI_USERNAME") 
XUI_PASSWORD        = get_os_attr("XUI_PASSWORD") 
XUI_TLS_CERT_PATH   = get_os_attr("XUI_TLS_CERT_PATH") 
DEFAULT_INBOUND     = int(get_os_attr("BOT_DEFAULT_USER_INBOUND"))

#database
PG_DB_NAME          = get_os_attr("BOT_POSTGRES_DBNAME")
PG_USERNAME         = get_os_attr("BOT_POSTGRES_USERNAME")
PG_PASSWORD         = get_os_attr("BOT_POSTGRES_PASSWORD")
PG_HOST             = get_os_attr("BOT_POSTGRES_HOST")
PG_PORT             = get_os_attr("BOT_POSTGRES_PORT")

YOOKASSA_ACCOUNT_ID = get_os_attr('YOOKASSA_ACCOUNT_ID')
YOOKASSA_SECRET_KEY = get_os_attr('YOOKASSA_SECRET_KEY')




class PurshareMethods(str,Enum):
    YOOKASSA = '💳 Банковской картой'
    STARS = 'starts'
    CRYPTO = 'crypto'

enabled_purshare_methods = [
    PurshareMethods.YOOKASSA,
    #PurshareMethods.STARTS,
    #PurshareMethods.CRYPTO
]

#referral programm
BONUS_TO_INVITER = 7
BONUS_TO_INVITED = 15

#plans
day_price = 3.33
default_plans = [30,60,90]


class XUI_CONFIG():
    XUI_HOST            = XUI_HOST
    XUI_USERNAME        = XUI_USERNAME
    XUI_PASSWORD        = XUI_PASSWORD
    XUI_TLS_CERT_PATH   = XUI_TLS_CERT_PATH


class YOOKASSA_CONFIG():
    YOOKASSA_ACCOUNT_ID = YOOKASSA_ACCOUNT_ID
    YOOKASSA_SECRET_KEY = YOOKASSA_SECRET_KEY

class PG_CONFIG:
    PG_DB_NAME = PG_DB_NAME
    PG_USERNAME = PG_USERNAME
    PG_PASSWORD = PG_PASSWORD
    PG_HOST = PG_HOST
    PG_PORT = PG_PORT

class REFERRAL_PROGRAMM_CONFIG():
    BONUS_TO_INVITER = BONUS_TO_INVITER 
    BONUS_TO_INVITED = BONUS_TO_INVITED



# os.environ["XUI_HOST"] = x_ui_host
# os.environ["XUI_USERNAME"] = x_ui_username
# os.environ["XUI_PASSWORD"] = x_ui_password
# os.environ["TLS_CERT_PATH"] = "../data/certificates/fullchain.cer"

# os.environ["PG_DATABASE"] = PG_DB_NAME
# os.environ["PG_USER"] = PG_USERNAME
# os.environ["PG_PASSWORD"] = PG_PASSWORD
# os.environ["PG_HOST"] = PG_HOST
# os.environ["PG_PORT"] = PG_PORT
