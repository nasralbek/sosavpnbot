from enum import Enum



TELEGRAM_WEBHOOK = "/webhook"
YOOKASSA_WEBHOOK = "/yookassa"

LOG_ZIP_ARCHIVE_FORMAT = "zip"
LOG_GZ_ARCHIVE_FORMAT = "gz"


class TransactionStatus(Enum):
    PENDING     = "pending"
    COMPLETED   = "completed"
    CANCELED    = "canceled"
    REFUNDED    = "refunded"



MAIN_MESSAGE_ID_KEY     = 'main_message_id'
PREVIOUS_CALLBACK_KEY   = "previous_callback"
PREVIOUS_MESSAGE_ID_KEY = 'previous_message_id' 

SELECTED_DAYS_KEY       = "selected_days"
SELECTED_PRICE_KEY      = "selected_price"
SELECTED_METHOD_KEY     = "selected_method"
SELECTED_PLAN_KEY       = "selected_plan"


DEFAULT_LANGUAGE    = "ru"
I18N_DOMAIN         = "bot"
