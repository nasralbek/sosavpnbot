from enum import Enum



TELEGRAM_WEBHOOK    = "/webhook"
YOOKASSA_WEBHOOK    = "/yookassa"
REMNAWAVE_WEBHOOK   = "/remna"
HELEKET_WEBHOOK     = "/heleket"
PALLY_WEBHOOK       = "/payments"

LOG_ZIP_ARCHIVE_FORMAT = "zip"
LOG_GZ_ARCHIVE_FORMAT = "gz"


class TransactionStatus(Enum):
    PENDING     = "pending"
    COMPLETED   = "completed"
    CANCELED    = "canceled"
    REFUNDED    = "refunded"



MAIN_MESSAGE_ID_KEY     = 'main_message_id'
HELLO_EMOJI_ID_KEY     = 'emoji_message_id'
PREVIOUS_CALLBACK_KEY   = "previous_callback"
PREVIOUS_MESSAGE_ID_KEY = 'previous_message_id' 
SAVED_TEXT_KEY = "saved_text"



SELECTED_DAYS_KEY       = "selected_days"
SELECTED_PRICE_KEY      = "selected_price"
SELECTED_METHOD_KEY     = "selected_method"
SELECTED_PLAN_KEY       = "selected_plan"


DEFAULT_LANGUAGE    = "ru"
I18N_DOMAIN         = "bot"


class REACTS_IDS(Enum):
    fire    =  "5104841245755180586"
    like    =  "5107584321108051014"
    dislike =  "5104858069142078462"
    heart   =  "5044134455711629726"
    gratz   =  "5046509860389126442"
    poop    =  "5046589136895476101"






